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

Task: Your job is to write a listening question for candidates to prepare original text and options for the listening dialogue. 
Students need to listen to dialogues and choose options that match the meaning of the question based on the listening content.
Some questions have picture options, while others are mostly text options. 
There will be 3-5 back and forth dialogues with around 200-300 words. The roll only displays options. Listen often
After the conversation, ask one person in the conversation what they want to do next. Only refer to the format, not the content.The JLPT exam paper includes a mix of easy, moderate, and difficult questions to accurately assess the test-taker’s proficiency across different aspects of the language.

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

 1 番 正解：3

> 会社で課長と男の人が話しています。男の人は出張レポートのことを国きなればなみませんか。
>
> 女：田中さん。初めての出張、お疲れ様でした、この出張のレポート詳みました。
> 男：はい。
> 女：出張の目的と訪問した会社で誰に会ったのかはこれています。ただ、話し合いについては最終的にどうなったのかがわかりくいています。そこを直してください。
> 男：はい、わかりました。
> 女：次の訪問日は3ヶ月後になつたんですね。
> 男：はい。
>
> 男の人は出張レポートのことを直きなければなりませんか。

 2 番 正解：3

> 図書館で男の学生と受付の人が話しています。男の学生は本の子をずるためにこの後、何をしますか。
>
> 男：すみません。昔れたし本があるんですが、図書館のパソコンで調べたら貸し出し中になっていて、子でっていう件があきけと押せんいんです。
> 女：すみません。その本の名前は今、問題があって使えないてなっています。あの、図書館の利用カードは持っていますか。
> 男：はい。
> 女：それではうちの図書館に貸して出してしたければ予约できますよ。
> 男：あ、そうですか。わかりました。
> 女：あ、ただ、借りているつしゃの本の中に貸し出し期限を過ぎた本があると予約できるって子的できるが…。
> 男：それは大丈夫です。ありがとうごさいます。

男の学生は本の予約をするためにこの後、何をしますか。

 3番 正解：1

> 大学の音楽クラブの部室で女の学生と男の学生が話しています。女の学生は之後、何をしますか。
>
> 女：遅くなってごめん。明日のコンサートの準備、もう始まってると聞いた？みんなもう会場の準備してる？
> 男：あ、伊藤さん。みんな体育館に椅子を並べに行ったよ。伊藤さんも行ってくれる？
> 女：今、ちょっとプログラム印刷し終わったから持って、体育館の入口で受け用的テーブルがあるからその上に置いて。
> 男：わかりました。
> 女：わかって。
> 男：その後、みんなと一緒に椅子、並べくれる？
> 女：OK。楽器を運ぶのはその後？大家い内的に今日のうちに運びだせな。
> 男：ああ、さっき体育館に行った時に最初に運んでもらった。僕は先生に明日のこと相談して行ったから体育館に向かうね。
> 女：わかって。

女の学生はこの後、何をしますか。

 4番 正解：2

> 会社で女の人と男の人が話しています。女の人は之後まず何しますか。
>
> 女：村上さん。今年の新入社員のセミナー、来月ですが、1日目的予定表はこれでよろしいですか？
> 男：ああ、はい。えっと、9時スタートで社長の話。その後、昼までビジネスマナーの先生の講義、去年と同じだね。あー、毎年9時スタートで朝から準備で忙しいという意見が多くて。
> 女：そうでしたか。
> 男：それで今年は30分遅くして9時半開始にしようという話になったんだ。終わるのは１２時じゃなくて１２時半になるけど。  
> 女：はい。  
> 男：会場は一応、午後１時まで使ってるから問題ないよ。社員に去年より３０分遅くなってもいいか、言合せ聞いてなくて、いちいちのは最初のところだけだから大丈夫だと思うけど。  
> 女：わかりました。  
> 男：先生には今日会うことになってるから確認しておくよ。全部確認取れてから予定表、直してくれる？  
> 女：はい。

女の人はこの後まず何をしますか。

---

 1ばん

1. しゅっちょうの　もくてき  
2. 会った人のじょうほう  
3. 話し合いのけっか  
4. つぎのほうもん日  

 2ばん

1. パソコンでもうしこむ  
2. 利用カードを作る  
3. もうしこみ用紙に書いて出す  
4. かりている本をかえす  

 3ばん

1. アイ  
2. アイウ  
3. アエ  
4. イウエ  

 4ばん

1. 会場のよやく時間をかえる  
2. しゃちょうに予定を聞く  
3. 先生に会いに行く  
4. よていひょうをなおす  
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


