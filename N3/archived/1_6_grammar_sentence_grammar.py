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

Task: Your job is to provide a sentence with a blank space and ask the candidate to fill in the most appropriate grammatical structure.

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
問題 1

（　　）に入れるのに最もよいものを、1・2・3・4から一つ選びなさい。

1.

私は、自分の作ったパンを多くたくさんの人（　）食べてほしいと思って、パン屋を始めた。
	1.	は
	2.	に
	3.	まで
	4.	なら

2.（学校にて）

学生：「先生、今、よろしいですか。英語の発表（　）、ちょっと相談したいのですが。」
先生：「ええ、いいですよ。」
	1.	にとって
	2.	によると
	3.	のことで
	4.	のは

3.

いつもは勉強を2時間以上かかるが、今日は1時間（　）終わりそうだ。
	1.	くらい
	2.	ころで
	3.	ぐらい
	4.	ぐらいで

4.

母：「えっ、（　）ご飯食べたばかりなのに、もうおなかすいたの？」
	1.	そろそろ
	2.	だんだん
	3.	さっき
	4.	ずっと

5.

大事なレシートをズボンのポケットに（　）洗濯してしまった。
	1.	入れたまま
	2.	入ったまま
	3.	入れている間
	4.	入っている間

6.（駅のホームにて）

「急げ、9時の特急に間に合うかもしれないし、走ろうか。」
「いや、（　）もう間に合わないと思う。次の電車にしよう。」
	1.	走ってて
	2.	走ってるよ
	3.	走らさきゃ
	4.	走っちゃって

7.

私はよくインターネットで物を買い替えるが、掃除機は壊れたら、実際に（　）買いたいものだ。
	1.	見てないと
	2.	見ておきたくなった
	3.	見てから
	4.	見ておいて

8.（料亭にて）

（体を丸めてお辞儀をして）「おいしそうな料理ですね。」
店員：「どうぞたくさん（　）ください。」
	1.	召し上がって
	2.	おっしゃって
	3.	なおって
	4.	いらっし

9.

A：「最近、寒くなって（　）ね。」
B：「ええ、今日は特に冷えますね。」
	1.	いました
	2.	ありました
	3.	いきました
	4.	きました

10.（大学にて）

A：「日曜日の留学生交流会、どうだった？」
B：「楽しかったよ。初めてだったからちょっと緊張したけど、新しい友達もできたし。」
	1.	行ってよかったよ
	2.	行こうかと思うよ
	3.	行きたかったなあ
	4.	行けたらいいなあ

11.（大学の事務所で）

学生：「すみません、ペンを（　）。」
事務所の人：「あ、はい、これを使ってください。」
	1.	お貸しできますか
	2.	お貸しいたしますか
	3.	貸したらいかがですか
	4.	貸していただけませんか

12.（家にて）

娘：「ちょっと駅前の本屋に行ってくるね。」
父：「雨が降っているし、車で（　）？」
娘：「いいの？ありがとう。」
	1.	送っててない
	2.	送ってこようか
	3.	送ってあげない
	4.	送ってあげようか

13.（会社にて）

「中山さん、今、ちょっといいですか。」
中山：「あ、ごめんなさい、これからABC銀行に（　）、戻ってきてからでもいいですか。」
	1.	行くところだからです
	2.	行くとこなんです
	3.	行っているところだからです
	4.	行っているところなんです
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
sentence_grammar_graph = builder.compile()

if __name__ == "__main__":
    random_word = random.choice(list(json.loads(n3_vocab).values()))

    print(f"Randomly chosen definition: {random_word}")

    sentence_grammar_question = sentence_grammar_graph.invoke(
        {
            "messages": [
                HumanMessage(
                    content=random_word
                )
            ],
        },
        config={"configurable": {"thread_id": "1"}}
    )

    display(sentence_grammar_question["question"])


