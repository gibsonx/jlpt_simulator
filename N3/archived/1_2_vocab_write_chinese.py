from graphs.common.node_builder import *
from graphs.common.utils import *
from libs.LLMs import azure_llm

load_dotenv()

teacher_prompt = """
Role: Japanese Teacher

Task: Write a kanji question for the JLPT N3 exam. Your job is to provide a kanji vocabulary word and ask the candidate to choose the correct kana reading.

Instructions:
Format: Follow the format of formal exam papers.
Content: Ensure the vocabulary is restricted to N3 level. Use the vocabulary in the `Dictionary` as much as possible.
Reference: Get inspiration from the Search result. Only use the format as a reference; do not use any specific content from existing exams.
Explanation: Append the correct answer and an explanation of the main challenges in simplified Chinese at each question.

Dictionary: {vocab_dict}
Search result: {search_result}
Formal exam paper: {example}
"""

example = """
9. ここから じゅんばん に見てください。
	1.	順番
	2.	項番
	3.	順落
	4.	項落

10. 父は銀行に つとめて います。
	1.	勧めて
	2.	勤めて
	3.	仕めて
	4.	労めて

11. ポケットが さゆう にあるんですね。
	1.	裏表
	2.	右左
	3.	表裏
	4.	左右

12. 昨日の試合は まけて しまいました。
	1.	退けて
	2.	負けて
	3.	失けて
	4.	欠けて

13. かこの 例も調べてみましょう。
	1.	適去
	2.	過古
	3.	過去
	4.	適古

14. この資料はページが ぎゃく になっていますよ。
	1.	達
	2.	変
	3.	逆
	4.	別
"""

def kanji(word, vocab):

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

    kanji_graph = build_graph(builder, nodes)

    kanji = kanji_graph.invoke(
        {"messages": [HumanMessage(content=word)]},
        config={"configurable": {"thread_id": "1"}}
    )

    display(kanji["question"])
    print(json.dumps(kanji['formatted_output'], indent=4, ensure_ascii=False))


if __name__ == "__main__":
    n3_vocab = collect_vocabulary("../../Vocab/n3.csv")
    random_word = random.choice(list(json.loads(n3_vocab).values()))
    kanji(vocab=n3_vocab,
          word=random_word)


