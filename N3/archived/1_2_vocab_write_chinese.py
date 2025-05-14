import random

from langgraph.graph import StateGraph

from graphs.common.node_builder import *
from graphs.common.state import *
from graphs.common.utils import *
from libs.LLMs import azure_llm

load_dotenv()

teacher_prompt = """
Role: You are a Japanese teacher. 

Task: Your job is to write a word meaning question for a JLPT N3 level exam paper, asking candidate to identify the correct kanji writing of a given word in hiragana.
Each question contains a word in hiragana in a sentence, and candidates must choose the correct option from 4 options. 
The options should include one correct kanji form and three distractors that are plausible. 

Instructions:
Format: Follow the format of formal exam papers.
Content: Ensure the vocabulary is restricted to N3 level. Use the vocabulary in the `Dictionary` as much as possible.
Reference: Get inspiration from the Search result. Only use the format as a reference; do not use any specific content from existing exams.
Explanation: Append the correct answer and an explanation of the main challenges  at each question.
Additional Requirement: Don't show question requirement in the generated content.

Dictionary: {vocab_dict}
Search result: {search_result}
Formal exam paper: {example}
"""

example = """
ここから じゅんばん に見てください。
	1.	順番
	2.	項番
	3.	順落
	4.	項落

父は銀行に つとめて います。
	1.	勧めて
	2.	勤めて
	3.	仕めて
	4.	労めて

ポケットが さゆう にあるんですね。
	1.	裏表
	2.	右左
	3.	表裏
	4.	左右

昨日の試合は まけて しまいました。
	1.	退けて
	2.	負けて
	3.	失けて
	4.	欠けて

かこの 例も調べてみましょう。
	1.	適去
	2.	過古
	3.	過去
	4.	適古

この資料はページが ぎゃく になっていますよ。
	1.	達
	2.	変
	3.	逆
	4.	別
"""


def write_chinese(word, vocab):

    online_search = online_search_node_builder()

    generator = generation_node_builder(vocab_dict=vocab,
                                        llm=azure_llm,
                                        prompt_text=teacher_prompt,
                                        example=example)

    reflector = reflection_node_builder(llm=azure_llm)

    formatter = formatter_node_builder(llm=azure_llm, OutType=SimpleChoiceQuestionOutput)

    nodes = {
        "online_search": online_search,
        "generator": generator,
        "reflector": reflector,
        "formatter": formatter
    }

    builder = StateGraph(SimpleQuestionState)

    graph = build_graph(builder, nodes)

    instance = graph.invoke(
        {"messages": [HumanMessage(content=word)]},
        config={"configurable": {"thread_id": "1"}}
    )

    return json.dumps(instance['formatted_output'], indent=4, ensure_ascii=False)


if __name__ == "__main__":
    n3_vocab = collect_vocabulary("../../Vocab/n3.csv")
    random_word = random.choice(list(json.loads(n3_vocab).values()))
    print(write_chinese(vocab=n3_vocab,
                  word=random_word))
