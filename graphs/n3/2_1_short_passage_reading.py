from graphs.common.node_builder import *
from graphs.common.utils import *
from graphs.common.state import *
from libs.LLMs import azure_llm
import random
from langgraph.graph import StateGraph

load_dotenv()

teacher_prompt = """
Role: You are a Japanese teacher. 

Task: Your job is to write a question for candidate to read a short article around 200 words.
The article is composed as 5-6 lines, you must split lines. Then, you give a question from the related content of the article.
The content is specific for emails Notification and letter articles.

Instructions:
Format: Follow the format of formal exam papers. Don't show sequence number of the questions.
Content: Ensure the vocabulary is restricted to N3 level. Use the vocabulary in the `Dictionary` as much as possible.
Reference: Get inspiration from the Search result. Only use the format as a reference; do not use any specific content from existing exams.
Explanation: Append the correct answer and an explanation of the main challenges in simplified Chinese at each question.
Additional Requirement: Don't show question requirement and revised submission in the generated content.

Dictionary: {vocab_dict}
Search result: {search_result}
Formal exam paper: {example}
"""

example = """
(1)

これは、今川さんが後のミゲルさんに書いたメールである。


ミゲルさん

メールをありがとう。

同じ会社で働くことになって、うれしいです。

住む所についてアドバイスをくださいと書いてあったので、お答えします。

会社まで歩いて行きたいと書いてありましたが、会社の周りはオフィスばかりで、アパートはほとんどありません。電車通勤になりますが、私が以前住んでいた緑野という町はいいですよ。

緑野駅から会社のある北駅まで電車で15分だし、いろいろなお店があって便利です。

いい所が見つかるといいですね。会えるのを楽しみにしています。

今川


23. まで電車で15分で行けるし、店も多いので、緑野にしたらどうか。
	1.	(選択肢なし)
	2.	いろいろな店があって便利なので、北園駅の近くにしたらどうか
	3.	北駅まで電車で15分で行けるし、店も多いので、緑野にしたらどうか
	4.	いろいろな店があって便利なので、北園駅の近くにしたらどうか
    
(2)

友達のマキは、いいことがあったという話をよくする。だから私は、マキは運がいいのだと思っていた。しかし、最近、そうではないと気づいた。

先日二人で出かけたとき、事故で電車が止まっていて、何キロも歩いて帰ることになった。嫌だなと思っている私に、マキは「知らない町を歩けるね。」と嬉しそうに言った。とても不思議だった。でも、マキは楽しめてしまうのだ。今まで私が聞いた話も、マキだから「いいこと」だと感じたのだろうと思う。


24. 最近、「私」はマキのことをどのような人だと思うようになったか。
	1.	「いいこと」ばかりが起きる。運がいい人
	2.	「私」と一緒に経験したことは、何でも「いいこと」だと思える人
	3.	ほかの人に起こった「いいこと」を一緒に喜んであげられる人
	4.	ほかの人が「いいこと」だと思わないことも「いいこと」だと思える人

 (3)

(会社で)

ミンさんが席に戻ると、机の上に、原口課長からのメモが置いてあった。

ミンさん

子どもが熱を出したので、早退します。午後、明日の会議の進行について確認する約束だったのに、すみません。午後の話し合いのために予約していた小会議室はキャンセルしてくれますか。席に戻ったら、すぐにお願いします。会議の進行については、明日の朝、最初に確認して、そのあとに会議室の準備をしましょう。

それから、ミンさんの作った資料ですが、問題ないので、今日中に8人分印刷しておいてください。

よろしくお願いします。

9月8日 12:10
原口

25. このメモを読んで、ミンさんはまず何をしなければならないか。
	1.	会議の進行について口課長と確認する
	2.	小会議室をキャンセルする
	3.	会議室の準備をする
	4.	会議の資料を8人分印刷する

    (4)

日本のファミリーレストランは、店の壁やソファーなどに、赤やオレンジ色のような暖かさを感じさせる色、つまり、暖色を使うことが多い。

暖色には食欲を感じさせる効果があるので、暖色に囲まれていると、料理がおいしそうに見える。また、暖色は、時間を実際より長く感じさせる効果もある。客は、店にいた時間が短くても、ゆっくりできたように感じるのだ。


26.

日本のファミリーレストランで暖色が使われる理由は何か。
	1.	店の暖房にあまりお金がかからないようにするため
	2.	客に、店の料理と店で過ごす時間にいい印象を持ってもらうため
	3.	店をおしゃれに見せて、客に店に入りたいと思ってもらうため
	4.	客に長く店にいてもらって、料理をたくさん注文してもらうため       
"""

def short_passage_read(word, vocab):

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
    with open("../../Vocab/topics.txt", "r",encoding="utf-8") as file:
        lines = file.readlines()
    random_topic = random.choice(lines).strip()
    print(random_topic)
    print(short_passage_read(vocab=n3_vocab,
          word=random_topic))


