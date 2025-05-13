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

Task:  Your job is to write a listening question for candidates to prepare the original text and options for the listening dialogue based on the reference format. Instant response. 
students need to listen to the conversation, choose the option that matches the meaning of the question based on the listening content, select the appropriate answer for this sentence in the current context, and provide three options. 
After listening to a conversation, you often ask someone in the conversation what they are going to do next.

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


