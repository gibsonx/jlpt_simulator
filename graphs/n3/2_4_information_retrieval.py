from graphs.common.node_builder import *
from graphs.common.utils import *
from graphs.common.state import *
from libs.LLMs import azure_llm
import random
from langgraph.graph import StateGraph
load_dotenv()

teacher_prompt = """
Role: You are a Japanese teacher. 

Task: You are a japanese teacher. Your job is to write a paper for candidate to read a Japanese information retrieval article. 
you must provide a markdown format table and clues related to the table. The content cannot be same as the Formal exam paper
The content includes searching for advertisements, notifications, schedules, and other information, 
Then, ask candidate to answer 2 questions from the related content of the article. 

Instructions:
Format: Follow the format of formal exam papers. Each question has 4 options in Japanese
Content: Ensure the vocabulary is restricted to N3 level. Use the vocabulary in the `Dictionary` as much as possible.
Reference: Get inspiration from the Search result. Only use the format as a reference; do not use any specific content from existing exams.
Explanation: Append the correct answer and an explanation of the main challenges in simplified Chinese at each question.
Additional Requirement: Don't show question requirement and revised submission in the generated content.

Dictionary: {vocab_dict}
Search result: {search_result}
Formal exam paper: {example}
"""

example = """
スキー教室の案内（抜粋）
| 通勤の種類 | 通勤日、時間 | 通勤場所/内容 |
|---|---|---|
| 0    | 定々木の世話   | 毎週火曜日9:00-11:00 | 無料で、定々木の世話をします。初心者も歓迎。 |
| 0    | ホームページ付け   | 毎週火曜日9:00-11:00 | 事務所でホームページの記事を書きます。PCスキルが必要。 |
| 3    | 公園の清掃   | 毎週水曜日14:00-16:00 | 無料で公園の清掃を行います。多くの協力が必要。 |
| 6    | 公園の案内   | 毎月第2日曜日9:00-11:00 | 無料で公園を案内します。 |

応募条件
奥山市在住・在勤者が対象。他地域の方は要確認。  

説明
参加希望日の前日までに事務所へ電話連絡が必要（A・Bは同じ内容）。  

応募方法
応募用紙に必要事項を記入し、事務所へ持参または郵送。◎印の活動は直接事務所へ来場（連絡不要）。  

---

37. 次のうち、正しい活動の選択肢はどれか。
（※問題文の具体的な選択肢が不足しているため、活動内容から推測）  
1. **①**（定々木の世話）  
2. ②（ホームページ付け）  
3. ③（公園の清掃）  
4. ④（公園の案内）  

38. 瞬時活動の魅力者になりたい人が気をつけるべきことはどれか。
1. 機能の活躍に応募できない  
2. 透明点（A・B）の両方に参加必須  
3. 参加希望日の前日までに電話連絡が必要
4. 応募用紙を事務所へ持参必須  

"""


def info_retrieval(word, vocab):

    online_search = online_search_node_builder()

    generator = generation_node_builder(vocab_dict=vocab,
                                        llm=azure_llm,
                                        prompt_text=teacher_prompt,
                                        example=example)

    reflector = reflection_node_builder(llm=azure_llm)

    formatter = formatter_node_builder(llm=azure_llm, OutType=MultipleQuestionOutput)

    nodes = {
        "online_search": online_search,
        "generator": generator,
        "reflector": reflector,
        "formatter": formatter
    }

    builder = StateGraph(SimpleQuestionState)

    graph = build_kanji_graph(builder, nodes)

    instance = graph.invoke(
        {"messages": [HumanMessage(content=word)]},
        config={"configurable": {"thread_id": "1"}}
    )

    return json.dumps(instance['formatted_output'], indent=4, ensure_ascii=False)


if __name__ == "__main__":
    n3_vocab = collect_vocabulary("../../Vocab/n3.csv")
    with open("../../Vocab/topics.txt", "r",encoding="utf-8") as file:
        lines = file.readlines()
    random_topic = random.choice(lines).strip()
    print(random_topic)
    print(info_retrieval(vocab=n3_vocab,
          word=random_topic))




