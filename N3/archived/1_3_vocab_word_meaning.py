import random

from langgraph.graph import StateGraph

from graphs.common.node_builder import *
from graphs.common.state import *
from graphs.common.utils import *
from libs.LLMs import azure_llm

load_dotenv()

teacher_prompt = """
Role: You are a Japanese teacher. 

Task: Your job is to write a vocabulary question for candidates to identify the correct kanji writing of a given word in hiragana for a JLPT N3 level exam paper.
Each question presents a word in hiragana within a sentence, and candidates must choose the correct kanji representation from four options. 
The options should include one correct kanji form and three distractors that are plausible but incorrect.

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
大雪で朝から電車が（　）している。
	1.	縮小
	2.	滞在
	3.	延期
	4.	運休

今日は暑かったので、シャツが（　）でぬれてしまった。
	1.	いびき
	2.	あくび
	3.	あせ
	4.	いき

答えさんに声がよく聞こえるように、（　）を使って話してください。
	1.	サイレン
	2.	エンジン
	3.	ノック
	4.	マイク

昨日は早く寝たが、夜中に大きな音がして目が（　）しまった。
	1.	嫌がって
	2.	覚めて
	3.	驚いて
	4.	怖がって

林さんはいつも冗談ばかり言うので、その話も本当かどうか（　）。
	1.	あやしい
	2.	おそろしい
	3.	にくらしい
	4.	まずしい

本日の面接の結果は、1 週間以内にメールで（　）します。
	1.	広告
	2.	合図
	3.	通知
	4.	伝言

兄はいつも（　）シャツを着ているので、遠くにいてもすぐに見つかる。
	1.	派手な
	2.	盛んな
	3.	わがままな
	4.	身近な

ここに車を止めることは規則で（　）されていますから、すぐに移動してください。
	1.	支配
	2.	英殺
	3.	禁止
	4.	批判

このコートは古いがまだ着られるので、捨ててしまうのは（　）。
	1.	もったいない
	2.	しかたない
	3.	かわいらしい
	4.	こいかない

弟への誕生日プレゼントは、誕生日まで弟に見つからないように、たんすの奥に（　）。
	1.	包んだ
	2.	隠した
	3.	囲んだ
	4.	閉じた

山口さんは今度のパーティーには来られないかもしれないが、（　）誘うつもりだ。
	1.	十分
	2.	一応
	3.	けっこう
	4.	たいてい
"""

def word_meaning(word, vocab):

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
    print(word_meaning(vocab=n3_vocab,
          word=random_word))


