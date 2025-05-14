from graphs.common.node_builder import *
from graphs.common.utils import *
from graphs.common.state import *
from libs.LLMs import azure_llm
import random
from langgraph.graph import StateGraph

load_dotenv()

teacher_prompt = """
Role: You are a Japanese teacher. 

Task: Your job is to write a word usage question for candidates, examining the usage of words in actual contexts.
request candidates to select the most appropriate context, includes Japanese idiomatic expressions and fixed collocations.)

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
31. 内容
	1.	修理のため、エアコンの内容を一度取り出します
	2.	鍋の中にカレーの内容を入れて、1時間くらい煮てください
	3.	古い財布から新しい財布へ内容を移しました
	4.	この手紙の内容は、ほかの人には秘密にしてください

32. 活動
	1.	彼は有名なロック歌手だったが、今は活動していない
	2.	山に登ると、新鮮な空気が活動していて気持ちがいい
	3.	さっきまで活動していたパソコンが、急に動かなくなった
	4.	駅前のコンビニは24時間活動しているので便利だ

33. 落ち着く
	1.	この辺りは、冬になると雪が落ち着いて、春になるまで溶けません
	2.	シャツにしみが落ち着いてしまって、洗ってもきれいになりません
	3.	あそこの木の上に美しい鳥が落ち着いています
	4.	大好きなこの曲を聞くと、いつも気持ちが落ち着きます

34. ぐっすり
	1.	遠慮しないで、ぐっすり食べてください
	2.	優勝できたのは、毎日ぐっすり練習したからだと思う
	3.	今日は疲れているので、朝までぐっすり眠れそうだ
	4.	古い友人と久しぶりに会って、ぐっすりおしゃべりした

35. 性格
	1.	日本の古い性格に興味があるので、神社やお寺によく行きます
	2.	森さんはおとなしい性格で、自分の意見はあまり言いません
	3.	値段が高くても、塗装で性格のいい車を買うつもりです
	4.	音楽の性格を伸ばすために、5歳から専門家の指導を受けました
"""

def word_usage(word, vocab):

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
    print(word_usage(vocab=n3_vocab,
          word=random_word))


