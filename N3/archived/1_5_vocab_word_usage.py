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

Task: Your job is to write a word usage question for candidates, examining the usage of words in actual contexts.
request candidates to select the most appropriate context for application of the word from options 1, 2, 3, and 4. (Includes Japanese idiomatic expressions and fixed collocations.)

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
word_usage_graph = builder.compile()

if __name__ == "__main__":
    random_word = random.choice(list(json.loads(n3_vocab).values()))

    print(f"Randomly chosen definition: {random_word}")

    word_usage_question = word_usage_graph.invoke(
        {
            "messages": [
                HumanMessage(
                    content=random_word
                )
            ],
        },
        config={"configurable": {"thread_id": "1"}}
    )

    display(word_usage_question["question"])


