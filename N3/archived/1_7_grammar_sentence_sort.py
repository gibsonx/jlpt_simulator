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

Task: Your job is to provide a sentence sorting question that requires selecting the correct arrangement order.
Ask candidate to choose the correct option from the following 4 options.

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
14.

山川大学では、__★_ 新入生がにアンケート調査を行っている。
	1.	大学生活
	2.	持っている
	3.	に対して
	4.	イメージ

15.

来週の夫の誕生日には、__★_ つもりだ。
	1.	最近
	2.	プレゼントする
	3.	かばんを
	4.	欲しがっている

16.

私は、健康の__★_。
	1.	している
	2.	ために
	3.	毎日8時間以上寝る
	4.	ように

17.

部長が__★_ クッキーがとてもおいしいので、私も東京に行くことがあったら、買おうと思う。
	1.	たびに
	2.	ために
	3.	お土産の
	4.	ように

18.

私はこの図書館が好きだ。広くて本の数が多い __★_ いい。
	1.	景色を楽しみながら
	2.	大きな窓から街が見えて
	3.	だけでなく
	4.	読書ができるのも
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
                    content=random_word
                )
            ],
        },
        config={"configurable": {"thread_id": "1"}}
    )

    display(sentence_sort_question["question"])


