# from langchain_community.embeddings import XinferenceEmbeddings
import copy
import importlib
import json
import random
import time
import json
from pathlib import Path
from azure.storage.blob import BlobServiceClient, ContentSettings

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.prompts.chat import SystemMessagePromptTemplate
from libs.Logger import logger

from libs.LLMs import *


class JLPTProcessor:
    SECTION_CONFIGS = {
        "語彙": {"max_score": 60, "target_score": 42, "target_percentage": 70},
        "文法": {"max_score": 30, "target_score": 22.5, "target_percentage": 75},
        "読解": {"max_score": 30, "target_score": 22.5, "target_percentage": 75},
        "聴解": {"max_score": 60, "target_score": 42, "target_percentage": 70},
    }

    def __init__(self, level="n1"):
        self.level = level
        self.prompt_data = self._import_prompts(level)

    @staticmethod
    def _import_prompts(level: str):
        """Dynamically import prompt set for the given level (n5–n1)."""
        return importlib.import_module(f"graphs.{level}.prompts")

    @staticmethod
    def _add_fields_to_question(question):
        """Add user_answer and is_correct fields to a single question dict."""
        if not isinstance(question, dict):
            return question

        choices = question.get("choices", [])
        num_choices = len(choices)

        if num_choices > 0:
            user_answer = random.randint(1, num_choices)
            question["user_answer"] = user_answer
            correct_answer = question.get("correct_answer")
            question["is_correct"] = user_answer == correct_answer if correct_answer else False
        else:
            question["user_answer"] = None
            question["is_correct"] = False

        return question

    def add_user_answers_and_correctness(self, data):
        """Traverse JSON structure and add user answers + correctness."""
        for section in data.get("sections", []):
            for subsection in section.get("subsections", []):
                for topic in subsection.get("question_topics", []):
                    result = topic.get("result", {})

                    if "questions" in result:
                        for q in result["questions"]:
                            self._add_fields_to_question(q)
                    elif "choices" in result and "correct_answer" in result:
                        self._add_fields_to_question(result)
                    elif "listen_questions" in result:
                        for q in result["listen_questions"]:
                            self._add_fields_to_question(q)
                    elif "choices" in topic and "correct_answer" in topic:
                        self._add_fields_to_question(topic)

        return data

    def add_teacher_prompts_to_json(self, data):
        """Attach teacher prompts to all question_topics."""
        for section in data.get("sections", []):
            for subsection in section.get("subsections", []):
                var_name = f"{subsection.get('subsection_title')}_teacher_prompt"
                if not hasattr(self.prompt_data, var_name):
                    print(f"警告: 未找到变量 {var_name}")
                    continue
                teacher_prompt = getattr(self.prompt_data, var_name)
                for topic in subsection.get("question_topics", []):
                    topic["teacher_prompt"] = teacher_prompt
        return data

    def remove_teacher_prompts_from_json(self, data):
        """Remove teacher_prompt from all question_topics."""
        for section in data.get("sections", []):
            for subsection in section.get("subsections", []):
                for topic in subsection.get("question_topics", []):
                    topic.pop("teacher_prompt", None)
        return data

    def add_jlpt_analysis_to_json(self, data):
        """Compute per-section and overall JLPT analysis."""
        section_stats = {}

        # collect stats
        for section in data.get("sections", []):
            name = section.get("section_title")
            if name not in self.SECTION_CONFIGS:
                continue
            correct_count, total_count = 0, 0
            for subsection in section.get("subsections", []):
                for topic in subsection.get("question_topics", []):
                    result = topic.get("result", {})
                    if "questions" in result:
                        questions = result["questions"]
                        total_count += len(questions)
                        correct_count += sum(1 for q in questions if q.get("is_correct") is True)
                    else:
                        total_count += 1
                        is_correct = result.get("is_correct") or result.get("is_correct:", False)
                        if is_correct is True:
                            correct_count += 1
            section_stats[name] = {"correct_count": correct_count, "total_count": total_count}

        # calculate scores
        sections_result, total_score, total_correct, total_questions = {}, 0, 0, 0
        for section_name, config in self.SECTION_CONFIGS.items():
            if section_name not in section_stats:
                continue
            stats = section_stats[section_name]
            correct, total = stats["correct_count"], stats["total_count"]
            estimated_score = round(correct / total * config["max_score"], 1) if total else 0
            accuracy_rate = round(correct / total * 100, 1) if total else 0
            pass_status = estimated_score >= config["target_score"]
            sections_result[section_name] = {
                "correct_count": correct,
                "total_count": total,
                "estimated_score": estimated_score,
                "max_score": config["max_score"],
                "accuracy_rate": accuracy_rate,
                "target_score": config["target_score"],
                "target_percentage": config["target_percentage"],
                "pass": pass_status,
                "result": "达标" if pass_status else "不达标"
            }
            total_score += estimated_score
            total_correct += correct
            total_questions += total

        overall_pass = all(sec["pass"] for sec in sections_result.values())
        total_max_score = sum(c["max_score"] for c in self.SECTION_CONFIGS.values())
        total_target_score = sum(c["target_score"] for c in self.SECTION_CONFIGS.values())

        data['analysis'] = {
            "sections": sections_result,
            "overall": {
                "total_correct": total_correct,
                "total_questions": total_questions,
                "total_accuracy": round(total_correct / total_questions * 100, 1) if total_questions else 0,
                "total_score": round(total_score, 1),
                "total_max_score": total_max_score,
                "total_target_score": total_target_score,
                "target_percentage": round(total_target_score / total_max_score * 100, 1),
                "overall_pass": overall_pass,
                "result": "达标" if overall_pass else "不达标"
            }
        }
        return data

    @staticmethod
    def _gen_explain(data):
        if not isinstance(data, dict):
            return None
        result = data.get("result", {})
        is_correct = result.get("is_correct", result.get("is_correct:", None))
        if is_correct is False:
            resolver = QuestionResolver(system_prompt=individual_prompt)
            system_message = json.dumps(data, ensure_ascii=False)
            messages = [HumanMessage(content=system_message)]
            res = resolver.invoke(messages)
            logger.info(res.get("explanation"))
            return res.get("explanation")
        return None

    def generate_explained_data(self, data):
        if not data or "sections" not in data:
            return data
        for section in data["sections"]:
            for subsection in section["subsections"]:
                for topic in subsection["question_topics"]:
                    result = topic.get("result", {})
                    questions_list = result.get("questions") or result.get("listen_questions")
                    if questions_list:
                        new_questions = []
                        for q in questions_list:
                            temp_topic = copy.deepcopy(topic)
                            temp_topic["result"] = q
                            q['explained'] = self._gen_explain(temp_topic)
                            new_questions.append(q)
                        topic['result']['questions'] = new_questions
                    else:
                        topic['result']['explained'] = self._gen_explain(topic)
        return data

    def add_summary_data(self, data):
        if not data or "sections" not in data:
            return data

        summaries = []
        for section in data["sections"]:
            resolver = QuestionResolver(system_prompt=summary_prompt, section=section["section_title"])
            user_message = json.dumps(section, ensure_ascii=False)
            messages = [HumanMessage(content=user_message)]
            res = resolver.invoke(messages)
            summaries.append(res['explanation'])
            data["analysis"]["sections"][section["section_title"]]["comments"] = res['explanation']

        resolver = QuestionResolver(system_prompt=training_prompt)
        user_message = json.dumps("\n\n".join(summaries), ensure_ascii=False)
        messages = [HumanMessage(content=user_message)]
        res = resolver.invoke(messages)
        data["analysis"]["overall"]["improves"] = res['explanation']

        return data

class QuestionResolver:
    def __init__(self, system_prompt: str, **system_vars):
        """
        system_prompt: a template string, e.g.
          "You are a {role}. Explain the answer in {language}."
        system_vars: variables used in system_prompt, e.g.
          role="Japanese teacher", language="Chinese"
        """
        self.system_prompt = system_prompt
        self.system_vars = system_vars

        # Use prompt templates, not raw SystemMessage
        self.prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(system_prompt),
            MessagesPlaceholder(variable_name="messages")
        ])

    def invoke(self, messages: list) -> dict:
        """
        messages: list of HumanMessage / AIMessage objects
        Returns: dict with explanation and messages
        """
        # Build input variables for the prompt
        input_vars = {
            **self.system_vars,
            "messages": messages
        }

        # Resolve prompt into a list of messages
        resolved_prompt = self.prompt.invoke(input_vars)

        # Call the LLM (LangChain 1.x style)
        msg = gen_llm.invoke(resolved_prompt)

        return {
            "explanation": msg.content,
            "messages": messages + [AIMessage(content=msg.content)]
        }


def report_writer(data):
    sections = data["analysis"]["sections"]
    overall = data["analysis"]["overall"]

    # ===== 雷达图数据 =====
    labels = list(sections.keys()) + ["综合"]
    values = [s["accuracy_rate"] for s in sections.values()] + [overall["total_accuracy"]]

    labels_json = json.dumps(labels, ensure_ascii=False)
    values_json = json.dumps(values)

    # ===== 分项表格（不含 comments）=====
    rows = ""
    for name, s in sections.items():
        rows += f"""
        <tr>
            <td>{name}</td>
            <td>{s['correct_count']}</td>
            <td>{s['total_count']}</td>
            <td>{s['accuracy_rate']}%</td>
            <td>{s['estimated_score']}</td>
            <td>{s['max_score']}</td>
            <td>{s['target_score']}</td>
            <td class="{'pass' if s['pass'] else 'fail'}">{s['result']}</td>
        </tr>
        """

    # ===== 分项点评（原 comments，独立章节）=====
    comments_html = ""
    for name, s in sections.items():
        comment = s.get("comments", "")
        if comment:
            comments_html += f"""
            <div style="margin-bottom: 18px;">
                <strong style="color:#2c3e50; font-size:15px;">{name}</strong>
                <div style="
                    margin-top: 6px;
                    padding: 14px 18px;
                    background: #f8f9fa;
                    border-left: 4px solid #667eea;
                    border-radius: 6px;
                    line-height: 1.7;
                    color: #555;
                    font-size: 14.5px;
                ">
                    {comment}
                </div>
            </div>
            """

    # ===== HTML 模板 =====
    html = f"""
<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<title>JLPT成绩分析报告</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
body {{
    font-family: 'Microsoft YaHei', Arial, sans-serif;
    background: #f7f9fc;
    margin: 40px;
    color: #333;
}}
h1 {{ 
    margin-bottom: 25px; 
    text-align: center;
    color: #2c3e50;
    font-size: 28px;
    padding-bottom: 15px;
    border-bottom: 2px solid #eaeaea;
}}

.dashboard-row {{
    display: flex;
    flex-wrap: wrap;
    gap: 30px;
    margin-bottom: 30px;
}}

.dashboard-card {{
    flex: 1;
    min-width: 300px;
    background: #fff;
    padding: 25px;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}}

.radar-card {{ flex: 1.2; }}
.summary-card {{ flex: 0.8; }}

.card {{
    background: #fff;
    padding: 25px;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    margin-bottom: 30px;
}}

.card h2 {{
    color: #2c3e50;
    margin-top: 0;
    font-size: 20px;
    padding-bottom: 12px;
    border-bottom: 2px solid #f0f0f0;
}}

table {{
    width: 100%;
    border-collapse: collapse;
    margin-top: 15px;
}}

th {{
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: #fff;
    padding: 12px;
}}

td {{
    padding: 12px;
    text-align: center;
    border-bottom: 1px solid #eee;
}}

.pass {{
    color: #28a745;
    font-weight: bold;
    background: #d4edda;
    padding: 4px 10px;
    border-radius: 20px;
}}

.fail {{
    color: #dc3545;
    font-weight: bold;
    background: #f8d7da;
    padding: 4px 10px;
    border-radius: 20px;
}}
</style>
</head>

<body>

<h1>📈 JLPT 成绩分析报告</h1>

<div class="dashboard-row">
    <div class="dashboard-card radar-card">
        <h2>📊 分项正确率雷达图</h2>
        <canvas id="radar" style="height:320px;"></canvas>
    </div>

    <div class="dashboard-card summary-card">
        <h2>✅ 综合评价</h2>
        <p><strong>综合正答数：</strong>{overall['total_correct']} / {overall['total_questions']}</p>
        <p><strong>综合正答率：</strong>{overall['total_accuracy']}%</p>
        <p><strong>综合得点：</strong>{overall['total_score']} / {overall['total_max_score']}</p>
        <p><strong>目标得点：</strong>{overall['total_target_score']}</p>
        <p>
            <strong>最终结果：</strong>
            <span class="{'pass' if overall['overall_pass'] else 'fail'}">
                {overall['result']}
            </span>
        </p>
       <h2>📋 分项详细分析</h2>
        <table>
            <thead>
                <tr>
                    <th>项目</th>
                    <th>正确数</th>
                    <th>题目数</th>
                    <th>正确率</th>
                    <th>预估得分</th>
                    <th>满分</th>
                    <th>目标分</th>
                    <th>结果</th>
                </tr>
            </thead>
            <tbody>
                {rows}
            </tbody>
        </table>
    </div>
</div>


<div class="card">
    <h2>📝 分项点评</h2>
    {comments_html}
</div>

<div class="card">
    <h2>💡 提升建议</h2>
    <div style="
        line-height: 1.7;
        padding: 20px;
        background: #f8f9ff;
        border-left: 5px solid #3498db;
        border-radius: 8px;
    ">
        {overall.get('improves', '暂无具体建议')}
    </div>
</div>

<script>
new Chart(document.getElementById('radar'), {{
    type: "radar",
    data: {{
        labels: {labels_json},
        datasets: [{{
            label: "正确率 (%)",
            data: {values_json},
            fill: true
        }}]
    }},
    options: {{
        responsive: true,
        scales: {{
            r: {{
                min: 0,
                max: 100
            }}
        }}
    }}
}});
</script>

</body>
</html>
"""
    base_path = os.environ["PROJECT_PATH"]
    report_output = os.path.join(base_path, f"output")

    file_name = f"jlpt_report_{data['_id']}.html"

    file_path = os.path.join(report_output, file_name)

    Path(file_path).write_text(html, encoding="utf-8")

    print("✅ 已生成 jlpt_report.html（comments 已独立为分项点评章节）")

    blob_service_client = BlobServiceClient.from_connection_string(os.getenv("AZURE_STORAGE_CONNECTION_STRING"))
    container_client = blob_service_client.get_container_client(os.getenv("AZURE_REPORT_CONTAINER", "report"))

    try:
        with open(file_path, "rb") as data:
            container_client.upload_blob(
                name=file_name,
                data=data,
                overwrite=True,
                timeout=300,
                content_settings=ContentSettings(content_type="text/html")
            )
        logger.info(f"✅ Uploaded {file_path} as blob {file_name}")
    except Exception as e:
        logger.info(f"Upload failed: {e}")

    # UID-specific subfolders
    report_output = os.path.join(base_path, "output")

    return report_output

individual_prompt =  """
你是一个资深的日语教师, 专门辅导中国学生 JLPT 考试, 请根据题目内容和学生答题结果, 指导学生，要求简洁明了。
  输出html格式， html内容包含在一个<div></div>内, 由于内容会被插入Json中html必须在一行中避免换行。
    题目内容和学生答题情况包含在Json格式对象里,相关字段做用如下：
    - teacher_prompt: 这道题是如何出的, 这里会给出详细过程。
    - html_article：整篇文章内容，使用单行 HTML 字符串表示。
    - questions：题目列表，每一项是一个选择题对象
    - gender：说话者或角色标识，单人对话时为 male / female，多人物对话时为 male1、male2、female1、female2，用于区分不同人物。
    - context：具体的日语对话内容文本，不包含性别或角色信息。
    - background：对话或场景的背景说明，用于帮助理解情境；在图片听力题中还作为生成图片的详细背景描述提示词。
    - follow_up：在听完对话或结合场景后提出的问题。
    - conversation：对话内容主体，是一个列表，元素为单人对话结构或多人物对话结构。
    - choices：答案选项列表，每个元素是一个字符串形式的选项内容。
    - correct_answer：正确答案的选项
    - user_answer: 学生答题的选项
    - listen_questions：基于同一段多人物对话生成的多道题目列表，每一项包含该题的问题、选项以及正确答案编号。
    给出的解释和指导必须包含下面几个点, 每个点之间必须空行隔开：
    - 【问题翻译】仅包含问题的question的中文翻译，不再显示日语原文。不包含原文html_article
    - 【考点分析】
    - 【选项难点解析】
    - 【错误原因分析】
    - 【改正/加强练习建议】
    如果有html_article或者有男女对话conversation,background的, 提供文章的中文翻译作为一个补充点【文章翻译】放在【问题翻译】之后, 要求中文自然流畅, 不再显示日语原文。尽量保留格式、如果是表格必须保留table样式, 但是里面的内容需要中文翻译          
    格式参考:
    <div style="background:#eef6ff;padding:12px;border-radius:6px;margin-bottom:12px;">
      <h4>【问题翻译】</h4>
      <p>从地中喷出的气体会对环境产生影响</p>
      <h4>【考点分析】</h4>
      <p>本题考查N1级别常见汉字词汇“噴出”的正确读音。要求考生能够准确区分和记忆“噴”与“出”组合时的标准发音，属于常见但易混淆的音读词汇考查。</p>
      <h4>【选项难点解析】</h4>
      <p>选项1“ふんしゅう”与选项4“ふんしゅち”均为不存在或错误的组合，迷惑性较强。选项2“ふんしつ”容易与“紛失（ふんしつ）”混淆，正确答案3“ふんしゅつ”是“噴出”的标准音读。</p>
      <h4>【错误原因分析】</h4>
      <p>你选择了2“ふんしつ”，这可能是因为你将“噴出”误认为“紛失”或其他类似词汇，未能准确识别“噴”字的音读“ふん”与“出”字的音读“しゅつ”的组合。</p>
      <h4>【改正 / 加强练习建议】</h4>
      <p>建议重点复习常见N1汉字词汇的音读组合，尤其是“噴（ふん）”和“出（しゅつ）”等常考字的发音。可通过制作错题本、反复朗读和书写来加深记忆，并多做类似的汉字读音题，提升区分能力。</p>
    </div>
"""

summary_prompt = """
你是一位资深日语教师，专门辅导中国学生准备 JLPT 考试。你在辅导学生的 {section}
你的任务是：根据给定的试题内容和学生答题结果，生成一份针对性的学习指导。  

要求如下：  
1. 输出格式为 HTML，内容包含在一个 <div></div> 内, 由于内容会被插入Json中html必须在一行中避免换行。。  
2. 学生指导必须包含以下2个部分，每个部分之间空一行：  
   - 【优势分析】：指出学生答对的题目、已经掌握较好的题型与知识点给与肯定
   - 【弱项分析】：指出学生答错的题目、知识点薄弱的需要加强的地方。
3. 分析过程中要结合以下信息（JSON 对象中的字段）：  
                - teacher_prompt: 这道题是如何出的, 这里会给出详细过程。
                - html_article：整篇文章内容，使用单行 HTML 字符串表示。
                - questions：题目列表，每一项是一个选择题对象
                - gender：说话者或角色标识，单人对话时为 male / female，多人物对话时为 male1、male2、female1、female2，用于区分不同人物。
                - context：具体的日语对话内容文本，不包含性别或角色信息。
                - background：对话或场景的背景说明，用于帮助理解情境；在图片听力题中还作为生成图片的详细背景描述提示词。
                - follow_up：在听完对话或结合场景后提出的问题。
                - conversation：对话内容主体，是一个列表，元素为单人对话结构或多人物对话结构。
                - choices：答案选项列表，每个元素是一个字符串形式的选项内容。
                - correct_answer：正确答案的选项
                - user_answer: 学生答题的选项
                - listen_questions：基于同一段多人物对话生成的多道题目列表，每一项包含该题的问题、选项以及正确答案编号。 
4. 分析要简洁明了，条理清晰，每条指导应具体可操作，讲解知识点，不需要提出具体哪道题目。

参考格式：
<div style="background:#eef6ff;padding:12px;border-radius:6px;margin-bottom:12px;">
  <p>【优势分析】...</p>
  <p>【弱项分析】...</p>
 </div>  
"""

training_prompt = """
你是一位资深日语教师，专门辅导中国学生准备 JLPT 考试。
你的任务是：根据给定的试题内容和学生答题结果，生成一份针对性的学习计划。
输出格式为 HTML，内容包含在一个 <div></div> 内, 由于内容会被插入Json中html必须在一行中避免换行。。
- 【复习 / 训练方法建议】：针对弱项给出具体的复习或训练方法，练习或记忆技巧。
- 【下一阶段目标和计划】：给出可执行的下一步学习目标和建议计划，帮助学生持续提升。

参考格式：
<div style="background:#eef6ff;padding:12px;border-radius:6px;margin-bottom:12px;">
  <p>【复习 / 训练方法建议】...</p>
  <p>【下一阶段目标和计划】...</p>
 </div>  
"""

if __name__ == "__main__":
    start_time = time.time()  # 记录开始时间

    # 1️⃣ Load JSON data
    file_path = "../output/temp.json"
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 2️⃣ Initialize processor for the desired JLPT level
    processor = JLPTProcessor(level="n1")
    # 3️⃣ Run the full processing pipeline
    # data = processor.add_user_answers_and_correctness(data)
    # data = processor.add_teacher_prompts_to_json(data)
    # data = processor.generate_explained_data(data)
    # data = processor.remove_teacher_prompts_from_json(data)
    data = processor.add_jlpt_analysis_to_json(data)
    data = processor.add_summary_data(data)

    print(json.dumps(data, ensure_ascii=False, separators=(',', ':')))
    report_writer(data)

    end_time = time.time()  # 记录结束时间
    total_time = end_time - start_time
    print(f"总执行时间: {total_time:.2f} 秒")

        # print(incorrect_answers)