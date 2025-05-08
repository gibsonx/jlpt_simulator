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

Task: You are a japanese teacher. Your job is to write a paper for candidate to read an information retrieval article. 
you provide a markdown format table. The content cannot be same as the Formal exam paper
The content includes searching for advertisements, notifications, schedules, and other information, 
Then, ask candidate to answer 2 specific questions.

Instructions:
Format: Follow the format of formal exam papers.
Content: Ensure the vocabulary is restricted to N3 level. Use the vocabulary in the `Dictionary` as much as possible.
Reference: Get inspiration from the Search result. Only use the format as a reference; do not use any specific content from existing exams.
Explanation: Append the correct answer and an explanation of the main challenges in simplified Chinese at each question.

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
スキー教室の案内（抜粋）
| 通勤の種類 | 通勤日、時間 | 通勤場所/内容 |
|---|---|---|
| 0    | 定々木の世話   | 毎週火曜日9:00-11:00 | 無料で、定々木の世話をします。初心者も歓迎。 |
| 0    | ホームページ付け   | 毎週火曜日9:00-11:00 | 事務所でホームページの記事を書きます。PCスキルが必要。 |
| 3    | 公園の清掃   | 毎週水曜日14:00-16:00 | 無料で公園の清掃を行います。多くの協力が必要。 |
| 6    | 公園の案内   | 毎月第2日曜日9:00-11:00 | 無料で公園を案内します。 |

応募条件
奥山市在住・在勤者が対象。他地域の方は要確認。  

説明
参加希望日の前日までに事務所へ電話連絡が必要（A・Bは同じ内容）。  

応募方法
応募用紙に必要事項を記入し、事務所へ持参または郵送。◎印の活動は直接事務所へ来場（連絡不要）。  

---

37. 次のうち、正しい活動の選択肢はどれか。
（※問題文の具体的な選択肢が不足しているため、活動内容から推測）  
1. **①**（定々木の世話）  
2. ②（ホームページ付け）  
3. ③（公園の清掃）  
4. ④（公園の案内）  

38. 瞬時活動の魅力者になりたい人が気をつけるべきことはどれか。
1. 機能の活躍に応募できない  
2. 透明点（A・B）の両方に参加必須  
3. 参加希望日の前日までに電話連絡が必要
4. 応募用紙を事務所へ持参必須  

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


