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

Task: Your job is to write a vocabulary question for candidates to identify the correct kanji writing of a given word in hiragana for a JLPT N3 level exam paper.
Each question presents a word in hiragana within a sentence, and candidates must choose the correct kanji representation from four options. 
The options should include one correct kanji form and three distractors that are plausible but incorrect.

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
15. 大雪で朝から電車が（　）している。
	1.	縮小
	2.	滞在
	3.	延期
	4.	運休

16. 今日は暑かったので、シャツが（　）でぬれてしまった。
	1.	いびき
	2.	あくび
	3.	あせ
	4.	いき

17. 答えさんに声がよく聞こえるように、（　）を使って話してください。
	1.	サイレン
	2.	エンジン
	3.	ノック
	4.	マイク

18. 昨日は早く寝たが、夜中に大きな音がして目が（　）しまった。
	1.	嫌がって
	2.	覚めて
	3.	驚いて
	4.	怖がって

19. 林さんはいつも冗談ばかり言うので、その話も本当かどうか（　）。
	1.	あやしい
	2.	おそろしい
	3.	にくらしい
	4.	まずしい

20. 本日の面接の結果は、1 週間以内にメールで（　）します。
	1.	広告
	2.	合図
	3.	通知
	4.	伝言

21. 兄はいつも（　）シャツを着ているので、遠くにいてもすぐに見つかる。
	1.	派手な
	2.	盛んな
	3.	わがままな
	4.	身近な

22. ここに車を止めることは規則で（　）されていますから、すぐに移動してください。
	1.	支配
	2.	英殺
	3.	禁止
	4.	批判

23. このコートは古いがまだ着られるので、捨ててしまうのは（　）。
	1.	もったいない
	2.	しかたない
	3.	かわいらしい
	4.	こいかない

24. 弟への誕生日プレゼントは、誕生日まで弟に見つからないように、たんすの奥に（　）。
	1.	包んだ
	2.	隠した
	3.	囲んだ
	4.	閉じた

25. 山口さんは今度のパーティーには来られないかもしれないが、（　）誘うつもりだ。
	1.	十分
	2.	一応
	3.	けっこう
	4.	たいてい
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
word_meaning_graph = builder.compile()

if __name__ == "__main__":
    random_word = random.choice(list(json.loads(n3_vocab).values()))

    print(f"Randomly chosen definition: {random_word}")

    word_meaning_question = word_meaning_graph.invoke(
        {
            "messages": [
                HumanMessage(
                    content=random_word
                )
            ],
        },
        config={"configurable": {"thread_id": "1"}}
    )

    display(word_meaning_question["question"])


