from graphs.common.node_builder import *
from graphs.common.utils import *
from graphs.common.state import *
from libs.LLMs import azure_llm
import random
from langgraph.graph import StateGraph

load_dotenv()

teacher_prompt = """
Role: You are a Japanese teacher.

Task: Your job is to write a synonym question for candidates to identify the most appropriate word with a similar meaning in a JLPT N3 level exam paper. 
Each question presents a word in kanji or katakana within a sentence.
The options should include one correct synonym and three distractors that are plausible.

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
さん、避難してください。
	1.	ならんで
	2.	入って
	3.	にげて
	4.	急いで

来週、ここで企業の説明会があります。
	1.	旅行
	2.	会社
	3.	大学
	4.	建物

ちょっとバックしてください。
	1.	前に進んで
	2.	後ろに下がって
	3.	横に動いて
	4.	そこで止まって

このやり方がベストだ。
	1.	最もよい
	2.	最もよくない
	3.	最も難しい
	4.	最も難しくない

田中さんがようやく来てくれました。
	1.	笑に
	2.	すぐに
	3.	やっと
	4.	初めて
"""

def synonym_substitution(word, vocab):

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
    print(synonym_substitution(vocab=n3_vocab,
          word=random_word))


