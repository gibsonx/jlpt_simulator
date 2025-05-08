from graphs.common.node_builder import *
from graphs.common.utils import *
from graphs.common.state import *
from libs.LLMs import azure_llm
import random
from IPython import display
from langgraph.graph import StateGraph

load_dotenv()

teacher_prompt = """
Role: You are a Japanese teacher. 

Task: Your job is to write a listening question for candidates to prepare the original text and options for the listening dialogue based on the reference format. 
Students need to listen to monologues or dialogues, summarize their understanding, and choose options that match the meaning of the question based on the listening content. 
There will be 3-5 back and forth dialogues, containing about 150-250 words and 4 options. 
After listening to a conversation, I often ask someone in the conversation what they are going to do next.
 
Instructions:
Format: Follow the format of formal exam papers.
Content: Ensure the vocabulary is restricted to N3 level. Use the vocabulary in the `Dictionary` as much as possible.
Reference: Get inspiration from the Search result. Only use the format as a reference; do not use any specific content from existing exams.
Explanation: Append the correct answer and an explanation of the main challenges in simplified Chinese at each question.
Additional Requirement: Don't show question requirement and revised submission in the generated content.

Dictionary: {vocab_dict}
Search result: {search_result}
Formal exam paper: {example}
"""

example = """
問題3  
  
1番 正解: 2  
会話内容:
日本語学校で女の留学生と男の留学生が話しています。  
- 女: 来月で佐藤先生、学校を辞めちゃうんだよね。  
- 男: 寂しくなるね。  
- 女: うん。ねえ、クラスのみんなで先生に何か記念になるものをあげたいね。  
- 男: あ、いいね。何か身に付けるものとか?  
- 女: 先生おしゃれだし、そういうの選ぶの難しくない? それより私たちで何か作ろうよ。  
- 男: あ、メッセージカードは? クラスのみんなにも書いてもらおうよ。  
- 女: じゃ、スポーツ大会の時に撮ったクラスの集合写真を真ん中に貼って、周りにメッセージを書いてもらう?  
- 男: いいね。皆にももらえるといいね。明日、休み時間にクラスのみんなに話してみよう。  
  
2人は何について話していますか?  
1. 先生が学校を辞める理由    
2. 先生に贈る物    
3. クラスからのメッセージ    
4. 先生との思い出    
  
---  
  
2番 正解: 1  
会話内容:
ラジオでアナウンサーが女の人にインタビューしています。  
- 男: 高橋さんのグループは20年前から緑山に関わっていらっしゃるそうですね。  
- 女: はい、私たちは緑山の自然を未来に残したいと考えています。緑山の木は、ほとんどは自然のものなんですが、商業目的で木が切られて、その後、新しく植えられたところもあるんです。  
- 男: そうなんですか。  
- 女: 人の手で植えられた木は世話をしないと細く、弱くなります。根も強くないので大雨や強い風で倒れたり、流されたりしてしまうこともあって、山全体にも影響が出てきます。そうならないように細い枝を落としたり、周りの草を取ったりして1本1本世話をし、木を育てています。  
  
女の人は何について話していますか?  
1. 緑山の自然を守る活動    
2. 緑山の木が減っている原因    
3. 自然に育った木の特徴    
4. 山に木を植える方法   
  
---  
  
3番 正解: 2  
会話内容:
ラジオで男の人が話しています。  
- 男: 僕、わさびが好きでお寿司や刺身にたくさん付けて食べるのが好きなんですよ。わさびって食べると鼻が痛くなったり、涙が出たりして苦手な人もいるかもしれませんけど、魚の匂いを消してくれたり、食べ物が悪くなるのを防いでくれたりするんですよね。最近、雑誌で読んだんですが、わさびを食べると食欲が出たり、風邪を引きにくくなったりするなど健康にもいいということが研究によってわかってきたそうです。  
   
男の人は何について話していますか?  
1. わさびを好きになったわけ    
2. わさびの効果    
3. わさびが苦手な人が多い理由    
4. わさびのおいしさの研究    
"""

def summary_understanding(word, vocab):

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
    summary_understanding(vocab=n3_vocab,
          word=random_word)


