from graphs.common.node_builder import *
from graphs.common.utils import *
from graphs.common.state import *
from libs.LLMs import azure_llm
import random
from langgraph.graph import StateGraph

load_dotenv()

teacher_prompt = """
Role: You are a Japanese teacher. 

Task: Your job is to write a listening question for candidates to prepare the original text and options for the listening dialogue based on the reference format. 
Looking at the picture and listening to the recording, students need to listen to the dialogue. 
Based on the listening content, choose the option that matches the question meaning. 
Choose what the person pointed by the arrow in the picture, will say next in the background given in the picture and recording, 
and provide three options. After listening to a conversation, you often ask someone in the conversation what they are going to do next. 
must include a background context that describes the picture in English.

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
1番
  
朝、家の玄関で妻と夫が話しています。夫はどうしても家に戻ってきましたか。  
  
女:あれ？どうしたの？忘れ物？書類？    
男:いや、バス停で待ってたんだけど、なぜかバスがなかなか来なくて。今日は車で会社に行くよ。車の鍵、取ってくれる？    
女:えー、私、今日車使いたいんだけど・・・会社まで送ってったあげるよ。    
男:本当？悪いね。走って戻ってきたら、喉渇いちゃった。ちょっと水飲んでくるから待ってて。    
女:あ、机の上に切手が貼ってあるハガキがあったけど、出さなくていいの？    
男:あぁ、忘れてた。取ってくるよ。    
  
夫はどうしても家に戻ってきましたか。  

1. しょるいをわすれたから    
2. 車で会社に行くことにしたから    
3. のどがかわいたから    
4. はがきをわすれたから   
 
---  
  
2番
  
女の人と男の人が話しています。男の人は犬を飼って何が最もよかったと言っていますか。  
  
女:木村くん、犬を飼い始めたんだって？    
男:うん、すごくかわいくて・・・すっかり家族のアイドルだよ。    
女:毎日散歩に連れて行くの？    
男:うん、朝は僕、夕方は母の係なんだけど、いい運動になってるよ。母は他の犬の飼い主とも仲良くなったみたい。男の人は犬を飼って何が最もよかったと言っていますか。   
女:そうなんだ。    
男:最初は朝早く起きるのが辛かったんだけどね、おかげで寝る時間も早くなって規則正しい生活になったよ。それに散歩では普段会話が少ない母と、それが増えたなって思ってる。散歩中に他の犬の飼い主さんとか、交流が深まって何かわかったみたいで、楽しいよ。    
女:そっか、今度会いに行きたいな。    
男:うん、いいよ。    

1. 犬のさんぽがいい運動になること    
2. 知り合いがふえたこと    
3. きそく正しい生活になったこと    
4. かぞくの会話がふえたこと


3番

雑誌を作る会社で男の人と女の人が話しています。女の人は何のためにもう一度パン屋に行きますか。女の人です。  
  
男:青木さん、あまり、来月、雑誌で取り上げる特集の人気のパン屋、いろいろ話聞けた？    
女:はい。でも今日の夕方、もう一度行かなきゃならないんです。    
男:何か聞くの忘れた？    
女:いえ、楽しくお店が雰囲気作りをされているかという点をしゃべらなかったんです。店長さんが雑誌に写真を載せるか悩まれているそうで、いつも写真がないっておしゃってるので。    
男:なるほど、あの店主にとって2年以上一緒に過ごしてきた店だからね。写真を載せるかどうか、新面目な意見を聞いてもらったほうが良いよね。奥さんが考えたことも聞いてよかったよ。    
女:僕も提案にビジョン、一緒に行くよ。新聞のパンも買いたいし。    
男:わかりました。    
  
女の人は何のためにもう一度パン屋に行きますか。

1. おんせんに行きたい    
2. 着物の着方を習いたい    
3. 日本料理の作り方を習いたい    
4. しんかんせんに乗りたい  

"""


def active_expression(word, vocab):

    online_search = online_search_node_builder()

    generator = generation_node_builder(vocab_dict=vocab,
                                        llm=azure_llm,
                                        prompt_text=teacher_prompt,
                                        example=example)

    reflector = reflection_node_builder(llm=azure_llm)

    formatter = formatter_node_builder(llm=azure_llm, OutType=ImageListenQuestionOutput)

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
    print(active_expression(vocab=n3_vocab,
                                 word=random_word))


