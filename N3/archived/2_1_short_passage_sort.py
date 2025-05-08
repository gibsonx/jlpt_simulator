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

Task: Your job is to write a question for candidate to read a short article around 200 words.
The article is composed as 5-6 lines, you must split lines. Then, give the question and ask candidate to choose the correct answer. 
The content is specific for emails Notification and letter articles.

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
(1)

これは、今川さんが後のミゲルさんに書いたメールである。


ミゲルさん

メールをありがとう。

同じ会社で働くことになって、うれしいです。

住む所についてアドバイスをくださいと書いてあったので、お答えします。

会社まで歩いて行きたいと書いてありましたが、会社の周りはオフィスばかりで、アパートはほとんどありません。電車通勤になりますが、私が以前住んでいた緑野という町はいいですよ。

緑野駅から会社のある北駅まで電車で15分だし、いろいろなお店があって便利です。

いい所が見つかるといいですね。会えるのを楽しみにしています。

今川


23. まで電車で15分で行けるし、店も多いので、緑野にしたらどうか。
	1.	(選択肢なし)
	2.	いろいろな店があって便利なので、北園駅の近くにしたらどうか
	3.	北駅まで電車で15分で行けるし、店も多いので、緑野にしたらどうか
	4.	いろいろな店があって便利なので、北園駅の近くにしたらどうか
    
(2)

友達のマキは、いいことがあったという話をよくする。だから私は、マキは運がいいのだと思っていた。しかし、最近、そうではないと気づいた。

先日二人で出かけたとき、事故で電車が止まっていて、何キロも歩いて帰ることになった。嫌だなと思っている私に、マキは「知らない町を歩けるね。」と嬉しそうに言った。とても不思議だった。でも、マキは楽しめてしまうのだ。今まで私が聞いた話も、マキだから「いいこと」だと感じたのだろうと思う。


24. 最近、「私」はマキのことをどのような人だと思うようになったか。
	1.	「いいこと」ばかりが起きる。運がいい人
	2.	「私」と一緒に経験したことは、何でも「いいこと」だと思える人
	3.	ほかの人に起こった「いいこと」を一緒に喜んであげられる人
	4.	ほかの人が「いいこと」だと思わないことも「いいこと」だと思える人

 (3)

(会社で)

ミンさんが席に戻ると、机の上に、原口課長からのメモが置いてあった。

ミンさん

子どもが熱を出したので、早退します。午後、明日の会議の進行について確認する約束だったのに、すみません。午後の話し合いのために予約していた小会議室はキャンセルしてくれますか。席に戻ったら、すぐにお願いします。会議の進行については、明日の朝、最初に確認して、そのあとに会議室の準備をしましょう。

それから、ミンさんの作った資料ですが、問題ないので、今日中に8人分印刷しておいてください。

よろしくお願いします。

9月8日 12:10
原口

25. このメモを読んで、ミンさんはまず何をしなければならないか。
	1.	会議の進行について口課長と確認する
	2.	小会議室をキャンセルする
	3.	会議室の準備をする
	4.	会議の資料を8人分印刷する

    (4)

日本のファミリーレストランは、店の壁やソファーなどに、赤やオレンジ色のような暖かさを感じさせる色、つまり、暖色を使うことが多い。

暖色には食欲を感じさせる効果があるので、暖色に囲まれていると、料理がおいしそうに見える。また、暖色は、時間を実際より長く感じさせる効果もある。客は、店にいた時間が短くても、ゆっくりできたように感じるのだ。


26.

日本のファミリーレストランで暖色が使われる理由は何か。
	1.	店の暖房にあまりお金がかからないようにするため
	2.	客に、店の料理と店で過ごす時間にいい印象を持ってもらうため
	3.	店をおしゃれに見せて、客に店に入りたいと思ってもらうため
	4.	客に長く店にいてもらって、料理をたくさん注文してもらうため       
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


