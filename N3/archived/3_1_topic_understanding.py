from graphs.common.node_builder import *
from graphs.common.utils import *
from graphs.common.state import *
from libs.LLMs import azure_llm
import random
from langgraph.graph import StateGraph
load_dotenv()

teacher_prompt = """
Role: You are a Japanese teacher. 

Task: Your job is to write a listening question for candidates to prepare original text and options for the listening dialogue. 
Students need to listen to dialogues and choose options that match the meaning of the question based on the listening content.
Some questions have picture options, while others are mostly text options. 
There will be 3-5 back and forth dialogues with around 200-300 words. The roll only displays options. Listen often
After the conversation, ask one person in the conversation what they want to do next. Only refer to the format, not the content.The JLPT exam paper includes a mix of easy, moderate, and difficult questions to accurately assess the test-taker’s proficiency across different aspects of the language.

Instructions:
Format: Follow the format of formal exam papers. Each question has 4 options in Japanese
Content: Ensure the vocabulary is restricted to N3 level. Use the vocabulary in the `Dictionary` as much as possible.
Reference: Get inspiration from the Search result. Only use the format as a reference; do not use any specific content from existing exams.
Explanation: Append the correct answer and an explanation of the main challenges  at each question.
Additional Requirement: Don't show question requirement and revised submission in the generated content.

Dictionary: {vocab_dict}
Search result: {search_result}
Formal exam paper: {example}
"""

example = """
1 番 

> 会社で課長と男の人が話しています。男の人は出張レポートのことを国きなればなみませんか。
>
> 女：田中さん。初めての出張、お疲れ様でした、この出張のレポート詳みました。
> 男：はい。
> 女：出張の目的と訪問した会社で誰に会ったのかはこれています。ただ、話し合いについては最終的にどうなったのかがわかりくいています。そこを直してください。
> 男：はい、わかりました。
> 女：次の訪問日は3ヶ月後になつたんですね。
> 男：はい。
>
> 男の人は出張レポートのことを直きなければなりませんか。

1ばん

1. しゅっちょうの　もくてき  
2. 会った人のじょうほう  
3. 話し合いのけっか  
4. つぎのほうもん日

正解：3  

2 番

> 図書館で男の学生と受付の人が話しています。男の学生は本の子をずるためにこの後、何をしますか。
>
> 男：すみません。昔れたし本があるんですが、図書館のパソコンで調べたら貸し出し中になっていて、子でっていう件があきけと押せんいんです。
> 女：すみません。その本の名前は今、問題があって使えないてなっています。あの、図書館の利用カードは持っていますか。
> 男：はい。
> 女：それではうちの図書館に貸して出してしたければ予约できますよ。
> 男：あ、そうですか。わかりました。
> 女：あ、ただ、借りているつしゃの本の中に貸し出し期限を過ぎた本があると予約できるって子的できるが…。
> 男：それは大丈夫です。ありがとうごさいます。

男の学生は本の予約をするためにこの後、何をしますか。
1. パソコンでもうしこむ  
2. 利用カードを作る  
3. もうしこみ用紙に書いて出す  
4. かりている本をかえす

3番

> 大学の音楽クラブの部室で女の学生と男の学生が話しています。女の学生は之後、何をしますか。
>
> 女：遅くなってごめん。明日のコンサートの準備、もう始まってると聞いた？みんなもう会場の準備してる？
> 男：あ、伊藤さん。みんな体育館に椅子を並べに行ったよ。伊藤さんも行ってくれる？
> 女：今、ちょっとプログラム印刷し終わったから持って、体育館の入口で受け用的テーブルがあるからその上に置いて。
> 男：わかりました。
> 女：わかって。
> 男：その後、みんなと一緒に椅子、並べくれる？
> 女：OK。楽器を運ぶのはその後？大家い内的に今日のうちに運びだせな。
> 男：ああ、さっき体育館に行った時に最初に運んでもらった。僕は先生に明日のこと相談して行ったから体育館に向かうね。
> 女：わかって。

女の学生はこの後、何をしますか。
1. アイ  
2. アイウ  
3. アエ  
4. イウエ

4番

> 会社で女の人と男の人が話しています。女の人は之後まず何しますか。
>
> 女：村上さん。今年の新入社員のセミナー、来月ですが、1日目的予定表はこれでよろしいですか？
> 男：ああ、はい。えっと、9時スタートで社長の話。その後、昼までビジネスマナーの先生の講義、去年と同じだね。あー、毎年9時スタートで朝から準備で忙しいという意見が多くて。
> 女：そうでしたか。
> 男：それで今年は30分遅くして9時半開始にしようという話になったんだ。終わるのは１２時じゃなくて１２時半になるけど。  
> 女：はい。  
> 男：会場は一応、午後１時まで使ってるから問題ないよ。社員に去年より３０分遅くなってもいいか、言合せ聞いてなくて、いちいちのは最初のところだけだから大丈夫だと思うけど。  
> 女：わかりました。  
> 男：先生には今日会うことになってるから確認しておくよ。全部確認取れてから予定表、直してくれる？  
> 女：はい。

女の人はこの後まず何をしますか。

1. 会場のよやく時間をかえる  
2. しゃちょうに予定を聞く  
3. 先生に会いに行く  
4. よていひょうをなおす  
"""

def topic_understanding(word, vocab):

    online_search = online_search_node_builder()

    generator = generation_node_builder(vocab_dict=vocab,
                                        llm=azure_llm,
                                        prompt_text=teacher_prompt,
                                        example=example)

    reflector = reflection_node_builder(llm=azure_llm)

    formatter = formatter_node_builder(llm=azure_llm, OutType=ListenSingleChoiceOutput)

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
    print(topic_understanding(vocab=n3_vocab,
          word=random_word))


