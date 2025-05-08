from graphs.common.node_builder import *
from graphs.common.utils import *
from graphs.common.state import *
from libs.LLMs import azure_llm
import random
from langgraph.graph import StateGraph

load_dotenv()

teacher_prompt = """
Role: You are a Japanese teacher. 

Task: Your job is to provide a sentence sorting question that requires selecting the correct arrangement order.
Ask candidate to choose the correct option from the following 4 options.

Instructions:
Format: Follow the format of formal exam papers.
Content: Ensure the vocabulary is restricted to N3 level. Use the vocabulary in the `Dictionary` as much as possible.
Reference: Get inspiration from the Search result. Only use the format as a reference; do not use any specific content from existing exams.
Explanation: Append the correct answer and an explanation of the main challenges in simplified Chinese at each question.
Additional Requirement: Don't show question requirement in the generated content.

Dictionary: {vocab_dict}
Search result: {search_result}
Formal exam paper: {example}
"""

example = """
山川大学では、__★_ 新入生がにアンケート調査を行っている。
	1.	大学生活
	2.	持っている
	3.	に対して
	4.	イメージ

来週の夫の誕生日には、__★_ つもりだ。
	1.	最近
	2.	プレゼントする
	3.	かばんを
	4.	欲しがっている

私は、健康の__★_。
	1.	している
	2.	ために
	3.	毎日8時間以上寝る
	4.	ように

部長が__★_ クッキーがとてもおいしいので、私も東京に行くことがあったら、買おうと思う。
	1.	たびに
	2.	ために
	3.	お土産の
	4.	ように

私はこの図書館が好きだ。広くて本の数が多い __★_ いい。
	1.	景色を楽しみながら
	2.	大きな窓から街が見えて
	3.	だけでなく
	4.	読書ができるのも
"""

def sentence_sort(word, vocab):

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
    print(sentence_sort(vocab=n3_vocab,
          word=random_word))


