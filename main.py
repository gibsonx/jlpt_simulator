import pandas as pd
import json
import random
import os
import pickle
import re
import uuid
from typing import *
from langchain_openai import AzureOpenAI,AzureChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
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
from libs.LLMs import *
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

load_dotenv()

def collect_vocabulary(file_path):
    # Read the CSV file
    data = pd.read_csv(file_path)
    words = data.iloc[:, :2].sample(frac=1).reset_index(drop=True)
    # Display the content of the CSV file
    vocab_dict = words.set_index(words.columns[0])[words.columns[1]].to_dict()
    vocab_dict = json.dumps(vocab_dict, ensure_ascii=False, separators=(',', ':'))
    return vocab_dict



def create_paper(self):
    """
    第一部分：语言知识（文字・词汇・语法）
        1. 文字・词汇（30分钟）
        题型 1：读假名（汉字读音）8题
        内容：给出一个汉字词汇，要求选择正确的假名读音
        Kanji reading
    :return:
    """
    file_path = 'Vocab/n3.csv'
    vocab_lsit = collect_vocabulary(file_path)
