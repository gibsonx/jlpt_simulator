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

load_dotenv()

def online_search(state):
    """
    Web search based on the re-phrased question.

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Updates documents key with appended web results
    """

    print("---WEB SEARCH---")

    topic = state['messages'][-1].content

    tavily_search_tool = TavilySearch(
        max_results=20,
        topic="news",
        days=1
    )
    # Web search
    docs = tavily_search_tool.invoke({"query": topic})

    print(docs)

    web_results = "\n".join([d["content"] for d in docs["results"]])

    print("Web results: ", web_results)

    return {"documents": web_results, "topic": topic}

# Nodes
def generation_node_builder(vocab_dict, llm,  prompt_text, example):
    def question_generator(state: QuestionState):
        """First LLM call to generate initial question"""
        print("---Generator----")

        search_result = state['documents']

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    prompt_text
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )

        params = {
            "topic": state['topic'],
            "search_result": search_result,
            "vocab_dict": vocab_dict,
            "example": example,
            "messages": state["messages"]
        }

        generate = prompt | llm

        msg = generate.invoke(input=params)

        return {"question": msg.content, "messages": [AIMessage(content=msg.content)]}

    return question_generator

def reflection_node_builder(llm,  prompt_text):
    def reflection_node(state: QuestionState) -> QuestionState:
        print("---REVISOR---")

        # Other messages we need to adjust
        cls_map = {"ai": HumanMessage, "human": AIMessage}
        # First message is the original user request. We hold it the same for all nodes
        translated = [state["messages"][0]] + [
            cls_map[msg.type](content=msg.content) for msg in state["messages"][1:]
        ]

        reflection_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                     prompt_text
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )
        reflect = reflection_prompt | llm

        res = reflect.invoke(translated)

        # We treat the output of this as human feedback for the generator
        return {"messages": [HumanMessage(content=res.content)]}

    return reflection_node


def formatter_node(state: QuestionState) -> QuestionState:
    print("--- Formatter ---")

    question = state["question"]

    print("### I am going to format: ", question)

    formatter_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are a AI assistance. your job is to format the following content to the structured output, don't modify the contextual meanings:
                {question}
                """
            )
        ]
    )
    format_pipeline = formatter_prompt | azure_llm.with_structured_output(SingleQuestionOutput)
    res = format_pipeline.invoke(input={"question": question})

    # We treat the output of this as human feedback for the generator
    return {"formatted_output": res}


def should_continue(state: QuestionState):
    if state["messages"]:
        if len(state["messages"]) > 6:
            print("--- Reach the Maximum Round ---")
            return END
        elif "GOOD ENOUGH" in state["messages"][-1].content:
            print("--- AI Reviser feels Good Enough ---")
            return END
    return "generator"