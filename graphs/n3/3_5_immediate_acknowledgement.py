from graphs.common.node_builder import *
from graphs.common.utils import *
from graphs.common.state import *
from libs.LLMs import azure_llm
import random
from langgraph.graph import StateGraph
load_dotenv()

load_dotenv()

teacher_prompt = """
Role: You are a Japanese teacher. 

Task:  Your job is to write a listening question for candidates to prepare the original text and options for the listening dialogue based on the reference format. Instant response. 
students need to listen to the conversation, choose the option that matches the meaning of the question based on the listening content, select the appropriate answer for this sentence in the current context, and provide three options. 
After listening to a conversation, you often ask someone in the conversation what they are going to do next. 

Instructions:
Format: Follow the format of formal exam papers.
Content: Ensure the vocabulary is restricted to N3 level. Use the vocabulary in the `Dictionary` as much as possible.
Reference: Get inspiration from the Search result. Only use the format as a reference; do not use any specific content from existing exams.
Explanation: Append the suggesting answer and an explanation of the main challenges in simplified Chinese at each question.
Additional Requirement: Don't show question requirement and revised submission in the generated content.

Dictionary: {vocab_dict}
Search result: {search_result}
Formal exam paper: {example}
"""

example = """
問題5  
  
1番 正解: 1  
会話内容:
- 女: 足、痛そうだね。午後のテニスの練習、休んだら？  
- 男: そうする。今日は帰るね。  
- 女: 今日は練習、ないんだね。  
- 男: テニス、今日は休むの?  
  
---  
  
2番 正解: 2  
会話内容: 
- 男: 町の花火大会、今年はやらないことになったそうだよ。  
- 女: やらないかもしれないんだね。  
- 男: え? なんで? 楽しみにしてたのに・・・  
- 女: じゃ、見に行かなくきゃね。  
  
---  `
  
3番 正解: 1  
会話内容:
- 男: 吉田さん、今回の旅行、楽しかったよ。吉田さんが案内してくれたおかげだよ。  
  1. 喜んでもらえてよかった  
  2. 一緒に行けなくてごめんね  
  3. 案内してくれてありがとう  

---  
   
#### 4番 正解: 1  
**会話内容:**  
- 男: 来週の食事会、参加できるかまだわからなくて、いつまでにお返事すればいいですか?  
  1. 今週中なら大丈夫ですよ  
  2. 参加できそうでよかったです  
  3. はい、返事お待ちしていますね  
  
---  
  
5番 正解: 3  
会話内容:
- 女: 曇ってきたね。雨が降らないうちに帰ろうか。  
  1. え? もう降ってきた?  
  2. 雨が止んでから帰るの?  
  3. 降る前に帰ったほうがいいね  
  
---  
  
6番 正解: 3  
会話内容:  
- 女: 森さん、悪いけど、ドアの近くにあるダンボール箱、倉庫に運んでくれる?  
  1. 倉庫にあるんですね。取ってきます  
  2. ありがとうございます。お願いします  
  3. あとでいいですか?  
  
---  
  
7番 正解: 1  
会話内容:
- 女: あの、こちらのお店、店の中の写真を撮っても構いませんか? すごく素敵なので。  
  1. あ、写真はご遠慮ください  
  2. 素敵な写真、ありがとうございます  
  3. 写真は撮ってなんないですよ  
  
---  
   
8番 正解: 2  
会話内容:
- 男: 今、課長から電話があったんですが、訪問先から会社に戻らずに帰宅されるそうです。  
  1. 一度会社に戻って来られるんですね  
  2. あ、そのまま家に帰られるんですね  
  3. え? 家に寄って来られるんですか?  
  
---  
  
9番 正解: 3  
会話内容:
- 男: 工事、遅れてるんだって? 課長に報告したほうがいいんじゃない?  
  1. 遅れてるって課長が言ってたんですか?  
  2. じゃ、報告はしないことにします  
  3. そうですね。伝えておきます  
"""


def immediate_ack(word, vocab):

    online_search = online_search_node_builder()

    generator = generation_node_builder(vocab_dict=vocab,
                                        llm=azure_llm,
                                        prompt_text=teacher_prompt,
                                        example=example)

    reflector = reflection_node_builder(llm=azure_llm)

    formatter = formatter_node_builder(llm=azure_llm, OutType=ListenOpenQuestionOutput)

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
    print(immediate_ack(vocab=n3_vocab,
          word=random_word))

