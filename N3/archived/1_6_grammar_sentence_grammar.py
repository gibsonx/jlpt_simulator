from graphs.common.node_builder import *
from graphs.common.utils import *
from graphs.common.state import *
from libs.LLMs import azure_llm
import random
from langgraph.graph import StateGraph

load_dotenv()

teacher_prompt = """
Role: You are a Japanese teacher. 

Task: Your job is to provide a sentence with a blank space and ask the candidate to fill in the most appropriate grammatical structure.

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
1.

私は、自分の作ったパンを多くたくさんの人（　）食べてほしいと思って、パン屋を始めた。
	1.	は
	2.	に
	3.	まで
	4.	なら

2.（学校にて）

学生：「先生、今、よろしいですか。英語の発表（　）、ちょっと相談したいのですが。」
先生：「ええ、いいですよ。」
	1.	にとって
	2.	によると
	3.	のことで
	4.	のは

3.

いつもは勉強を2時間以上かかるが、今日は1時間（　）終わりそうだ。
	1.	くらい
	2.	ころで
	3.	ぐらい
	4.	ぐらいで

4.

母：「えっ、（　）ご飯食べたばかりなのに、もうおなかすいたの？」
	1.	そろそろ
	2.	だんだん
	3.	さっき
	4.	ずっと

5.

大事なレシートをズボンのポケットに（　）洗濯してしまった。
	1.	入れたまま
	2.	入ったまま
	3.	入れている間
	4.	入っている間

6.（駅のホームにて）

「急げ、9時の特急に間に合うかもしれないし、走ろうか。」
「いや、（　）もう間に合わないと思う。次の電車にしよう。」
	1.	走ってて
	2.	走ってるよ
	3.	走らさきゃ
	4.	走っちゃって

7.

私はよくインターネットで物を買い替えるが、掃除機は壊れたら、実際に（　）買いたいものだ。
	1.	見てないと
	2.	見ておきたくなった
	3.	見てから
	4.	見ておいて

8.（料亭にて）

（体を丸めてお辞儀をして）「おいしそうな料理ですね。」
店員：「どうぞたくさん（　）ください。」
	1.	召し上がって
	2.	おっしゃって
	3.	なおって
	4.	いらっし

9.

A：「最近、寒くなって（　）ね。」
B：「ええ、今日は特に冷えますね。」
	1.	いました
	2.	ありました
	3.	いきました
	4.	きました

10.（大学にて）

A：「日曜日の留学生交流会、どうだった？」
B：「楽しかったよ。初めてだったからちょっと緊張したけど、新しい友達もできたし。」
	1.	行ってよかったよ
	2.	行こうかと思うよ
	3.	行きたかったなあ
	4.	行けたらいいなあ

11.（大学の事務所で）

学生：「すみません、ペンを（　）。」
事務所の人：「あ、はい、これを使ってください。」
	1.	お貸しできますか
	2.	お貸しいたしますか
	3.	貸したらいかがですか
	4.	貸していただけませんか

12.（家にて）

娘：「ちょっと駅前の本屋に行ってくるね。」
父：「雨が降っているし、車で（　）？」
娘：「いいの？ありがとう。」
	1.	送っててない
	2.	送ってこようか
	3.	送ってあげない
	4.	送ってあげようか

13.（会社にて）

「中山さん、今、ちょっといいですか。」
中山：「あ、ごめんなさい、これからABC銀行に（　）、戻ってきてからでもいいですか。」
	1.	行くところだからです
	2.	行くとこなんです
	3.	行っているところだからです
	4.	行っているところなんです
"""

def sentence_grammar(word, vocab):

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
    print(sentence_grammar(vocab=n3_vocab,
          word=random_word))


