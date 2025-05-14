from graphs.common.node_builder import *
from graphs.common.utils import *
from graphs.common.state import *
from libs.LLMs import azure_llm
import random
from langgraph.graph import StateGraph

load_dotenv()

teacher_prompt = """
Role: You are a Japanese teacher. 

Task: Your job is to write a paper for JLPT N3 level. 
At this section, please write an Japanese article about 300-400 words with 4-5 lines written with markdown. 
After that, you should give 4 related questions from the content of the article. 
The purpose is to also test candidate the ability to identify Japanese sentence structure. 
Candidate should fill in the gaps in the article by choosing the grammar structure that best fits the context from the following 4 options, 

Instructions:
Format: Follow the format of formal exam papers. Each question has 4 options in Japanese
Content: Ensure the vocabulary is restricted to N3 level. Use the vocabulary in the `Dictionary` as much as possible.
Reference: Get inspiration from the Search result. Only use the format as a reference; do not use any specific content from existing exams.
Explanation: give the correct answer and an explanation of the main challenges  at each question.
Additional Requirement: Don't show question requirement and revised submission in the generated content.

Dictionary: {vocab_dict}
Search result: {search_result}
Formal exam paper: {example}
"""

example = """
夏休みの思い出  
  
お母さん、中学生の妹さんと住んでいます。[19] 日本人の家に泊まるのは初めてだったので、行く前は少し不安な気持ちもありました。[20] 行ってみたらとても楽しかったです。  
  
印象に残っているのは、巡りの畑で育てた野菜を使って、みんなで料理を作ったことです。友達のお母さんは、畑でいろいろな野菜を育てていました。私たちは、その野菜を使ってみんなで料理をしました。私は、お店に売られている野菜 [21] 食べたことがありませんでした。家で育てた野菜を食べたのは初めてでしたが、とてもおいしかったです。特に「私も野菜を育ててみたい」と、胸がいっぱ言う行ってらない。」と言ったら、それを聞いていたお母さんが、家の中でも育てることができる野菜について教えてくれました。  
  
お母さんに教えてもらったやり方で、私も野菜を [22]。今、２種類の野菜を育てています。  
  
野菜の世話をしながら、楽しかった夏休みのことをいつも思い出しています。  
  
--- 

1. 招待してくれたのです    
2. 招待してくれたはずです    
3. 招待してくれたばかりです    
4. 招待してくれたそうです    
  
1. それで    
2. でも    
3. 実は    
4. また    
  
1. は    
2. などを    
3. しか    
4. だけ    
  
1. 育ててみてほしいです    
2. 育ててみてもいいです    
3. 育ててみようとしました    
4. 育ててみることにしました     
"""

def structure_selection(word, vocab):

    online_search = online_search_node_builder()

    generator = generation_node_builder(vocab_dict=vocab,
                                        llm=azure_llm,
                                        prompt_text=teacher_prompt,
                                        example=example)

    reflector = reflection_node_builder(llm=azure_llm)

    formatter = formatter_node_builder(llm=azure_llm, OutType=MultipleQuestionOutput)

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
    print(structure_selection(vocab=n3_vocab,
          word=random_word))


