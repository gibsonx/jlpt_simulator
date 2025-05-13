import pandas as pd
import json
import os
import random
import pickle
import re
import uuid
from typing import *
from langchain_openai import AzureOpenAI,AzureChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv
from langchain_aws import ChatBedrock
from langchain.embeddings.base import Embeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain_community.embeddings import XinferenceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from typing import Annotated, Literal, Sequence
from typing_extensions import TypedDict
from IPython.display import display, Markdown, Latex
from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from typing import Annotated, Sequence
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage,RemoveMessage,HumanMessage,AIMessage,ToolMessage
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field
from langgraph.graph import END, StateGraph, START
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field, validator
from typing import List, Optional
from langchain_tavily import TavilySearch
from langchain.schema import Document
from langgraph.prebuilt import create_react_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from graphs.common.state import QuestionState
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from IPython.display import Image, display
from graphs.common.node_builder import *
from graphs.common.utils import *
from libs.LLMs import aws_llm, azure_llm

load_dotenv()

teacher_prompt = """
Role: You are a Japanese teacher. 

Task: Your job is to write a listening question for candidates to prepare the original text and options for the listening dialogue based on the reference format. 
Students need to listen to dialogues, choose options that match the meaning of the question based on the listening content, 
listen to dialogues or monologues, choose the correct answer, listening dialogue needs 150-350 words. 
The roll only displays options. Only refer to the format, not the content. 

Instructions:
Format: Follow the format of formal exam papers.
Content: Ensure the vocabulary is restricted to N3 level. Use the vocabulary in the `Dictionary` as much as possible.
Reference: Get inspiration from the Search result. Only use the format as a reference; do not use any specific content from existing exams.
Explanation: Append the correct answer and an explanation of the main challenges  at each question.

Dictionary: {vocab_dict}
Search result: {search_result}
Formal exam paper: {example}
"""

reviser_prompt = """you are a Japanese language educator reviewing a JLPT exam paper. Generate critique and recommendations for the user's submission.
            the review focuses on content accuracy and question quality. 
            - For content accuracy, you must verify that the grammar and vocabulary questions accurately reflect the appropriate JLPT N3 level, ensuring the reading passages are clear, relevant, and appropriately challenging. 
            - For question quality, you must ensure all questions are clearly worded and free from ambiguity to comprehensively assess different language skills, and confirm that the difficulty level of the questions matches the intended JLPT N3 level.
            - During detailed refinement, you check the format and presentation of the paper, ensuring it is well-organized and the instructions are clear and concise. you also ensure the content is culturally appropriate and relevant to Japanese language and culture.
            - Finally, you make give feedback, providing detailed recommendations, including requests.If you think the exam paper is good enough, you just say "GOOD ENOUGH"
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
  
---  

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

n3_vocab = collect_vocabulary("../../Vocab/n3.csv")

generator = generation_node_builder(vocab_dict=n3_vocab,
                                    llm=azure_llm,
                                    prompt_text=teacher_prompt,
                                    example=example)

reflector = reflection_node_builder(llm=azure_llm,
                                    prompt_text=reviser_prompt
                                    )

# Build workflow
builder = StateGraph(QuestionState)

builder.add_node("online_search", online_search)
builder.add_node("generator", generator)
builder.add_node("reflector", reflector)
# Add nodes

# Add edges to connect nodes
builder.add_edge(START, "online_search")
builder.add_edge("online_search", "generator")
builder.add_edge("generator","reflector")
#
builder.add_conditional_edges("reflector", should_continue)

# Compile
sentence_sort_graph = builder.compile()

if __name__ == "__main__":
    random_word = random.choice(list(json.loads(n3_vocab).values()))

    print(f"Randomly chosen definition: {random_word}")

    sentence_sort_question = sentence_sort_graph.invoke(
        {
            "messages": [
                HumanMessage(
                    content="レストランで食べ物を注文する"
                )
            ],
        },
        config={"configurable": {"thread_id": "1"}}
    )
    display(sentence_sort_question["question"])


