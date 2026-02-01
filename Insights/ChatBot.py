import os
import json
import re
import asyncio
import importlib
from libs.LLMs import *
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage,trim_messages
from langgraph.graph.message import add_messages
from pymongo import MongoClient
import getpass
from langgraph.checkpoint.mongodb import MongoDBSaver
import os
from dotenv import load_dotenv
from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.memory import InMemorySaver
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, MessagesState, START, END
from libs.Utils import logger
from typing import *
from langchain_core.messages import (
    AnyMessage,
    BaseMessage,
    BaseMessageChunk,
    MessageLikeRepresentation,
    RemoveMessage,
    convert_to_messages,
    message_chunk_to_message,
)

load_dotenv()

class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    questions: List[str]
    level: str
    question_type: str
    route: str


class SuggestedQuestions(BaseModel):
    questions: List[str] = Field(
        ...,
        title="Suggested Questions for student to ask",
        description="A list of suggested JLPT-style questions student may ask"
    )

def intent_router(state: MessagesState):
    return state["route"]

def jlpt_question_explain_node(state: MessagesState):
    logger.info("---Teacher---")

    question_type = state.get("question_type")
    level = state.get("level","根据内容判断")
    question_prompt = None

    if question_type:
        prompt_data = importlib.import_module(f"graphs.{level}.prompts")
        var_name = f"{question_type}_teacher_prompt"

        if not hasattr(prompt_data, var_name):
            print(f"警告: 未找到变量 {var_name}")
        else:
            question_prompt =  re.sub(r"\{[^}]*\}", "", getattr(prompt_data, var_name)) # remove {} from the context as template looks it as a variable

    system_content = f"""
    你是一名资深的日语教育专家，从事JLPT（日语能力考试的教学、出题分析与试卷评阅。
    本题的JLPT级别是: {level}

    如果最下面给出明确的 "出题老师的提示词”, 你可以参考。
    出题老师的提示词: {question_prompt}

   你的任务是：
        - 讲解与分析该道JLPT题目的题型、出题思路、易错点
        - 对学生答案进行考试角度的评价与纠错
        - 按需提供备考建议与应试技巧
    回答规范：
        - 回答内容应符合 JLPT 官方考试标准
        - 语言表达清晰简洁、结构化，适合以中文为母语的学生理解
        - 必要时可对比中文与日语用法，指出常见中式误区
    约束条件：
        - 你只回答与 JLPT 等级、题型、语法、词汇、汉字或考试评估相关的问题
        - 不回答与 JLPT考试无关的闲聊、常识、技术或其他话题
    当学生提出与 JLPT 无关的问题时：
        - 请礼貌说明该问题不在 JLPT 复习范围内  
    
    如果问题包含在一个结构化数据对象内，你可以参考以下字段解释：
    - html_article：整篇文章内容，使用单行 HTML 字符串表示。
    - questions：题目列表，每一项是一个选择题对象
    - gender：说话者或角色标识，单人对话时为 male / female，多人物对话时为 male1、male2、female1、female2，用于区分不同人物。
    - context：具体的日语对话内容文本，不包含性别或角色信息。
    - background：对话或场景的背景说明，用于帮助理解情境；在图片听力题中还作为生成图片的详细背景描述提示词。
    - follow_up：在听完对话或结合场景后提出的问题。
    - conversation：对话内容主体，是一个列表，元素为单人对话结构或多人物对话结构。
    - choices：答案选项列表，每个元素是一个字符串形式的选项内容。
    - correct_answer：正确答案的选项
    - user_answer: 学生答题的选项
    - listen_questions：基于同一段多人物对话生成的多道题目列表，每一项包含该题的问题、选项以及正确答案编号。
    
    用下列格式输出, 如果有html_article或者有男女对话conversation,background的, 提供文章的中文翻译作为一个补充点【文章翻译】放在【问题翻译】之后, 要求中文自然流畅, 不再显示日语原文。
    尽量保留格式、如果是表格必须保留table样式, 但是里面的内容需要中文翻译
              
    格式参考(不要参考内容):
    ### 【问题翻译】
    xxx 
    
    ### 【考点分析】
    - xxx  
    - xx
    - xx
    
    ### 【选项难点解析】
    - xxx  
    - xx
    - xx
    
    ### 【错误原因分析】
    - xxx  
    - xx
    - xx
    
    ### 【改正 / 加强练习建议】
    - xxx  
    - xx
    - xx
    """

def jlpt_word_explain_node(state: MessagesState):
    logger.info("---Highlight---")

    question_type = state.get("question_type")
    level = state.get("level", "根据内容判断")
    question_prompt = None

    if question_type:
        prompt_data = importlib.import_module(f"graphs.{level}.prompts")
        var_name = f"{question_type}_teacher_prompt"

        if not hasattr(prompt_data, var_name):
            print(f"警告: 未找到变量 {var_name}")
        else:
            question_prompt = re.sub(r"\{[^}]*\}", "", getattr(prompt_data,
                                                               var_name))  # remove {} from the context as template looks it as a variable

    system_content = f"""
    你是一名资深的日语教育专家，从事JLPT（日语能力考试的教学、出题分析与试卷评阅。
    本题的JLPT级别是: {level}

    如果最下面给出明确的 "出题老师的提示词”, 你可以参考。
    出题老师的提示词: {question_prompt}

   你的任务是：
        - 接收用户给出来的内容。这个是用户划词提供的。 结合本题的上下文，讲解与分析
    回答规范：
        - 回答内容应符合 JLPT 官方考试标准
        - 语言表达清晰简洁、结构化，适合以中文为母语的学生理解
        - 必要时可对比中文与日语用法，指出常见中式误区
    约束条件：
        - 你只回答与 JLPT 等级、题型、语法、词汇、汉字或考试评估相关的问题
        - 不回答与 JLPT考试无关的闲聊、常识、技术或其他话题
    当学生提出与 JLPT 无关的问题时：
        - 请礼貌说明该问题不在 JLPT 复习范围内  

    如果问题包含在一个结构化数据对象内，你可以参考以下字段解释：
    - html_article：整篇文章内容，使用单行 HTML 字符串表示。
    - questions：题目列表，每一项是一个选择题对象
    - gender：说话者或角色标识，单人对话时为 male / female，多人物对话时为 male1、male2、female1、female2，用于区分不同人物。
    - context：具体的日语对话内容文本，不包含性别或角色信息。
    - background：对话或场景的背景说明，用于帮助理解情境；在图片听力题中还作为生成图片的详细背景描述提示词。
    - follow_up：在听完对话或结合场景后提出的问题。
    - conversation：对话内容主体，是一个列表，元素为单人对话结构或多人物对话结构。
    - choices：答案选项列表，每个元素是一个字符串形式的选项内容。
    - correct_answer：正确答案的选项
    - user_answer: 学生答题的选项
    - listen_questions：基于同一段多人物对话生成的多道题目列表，每一项包含该题的问题、选项以及正确答案编号。
    
    用下列格式输出，如果用户提供的内容是个单词则增加【音标】和【词性】在【中文翻译】后面
    格式参考(不要参考内容):
    ### 【中文翻译】
    xxx
    
    ### 【解释】
    - xxx
    - xxx
    - xxx

    ### 【例句】
    - xxx
    - xxx
    - xxx
    """

    trimmer = trim_messages(strategy="last",
                            max_tokens=20,
                            token_counter=len,
                            include_system=False)
    trimmed_messages = trimmer.invoke(state["messages"])

    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content=system_content),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )

    teacher_agent = prompt | azure_chat_llm
    # explicit input mapping for clarity
    msg = teacher_agent.invoke(input={"messages": trimmed_messages })

    logger.info("Response: {}".format(msg.content))

    # Return as human feedback for the generator
    return {"messages": [AIMessage(content=msg.content)]}

# --- Suggested Question Node (Structured Output) ---
def suggested_question_node(state: MessagesState):
    logger.info("---Suggested Question Node---")

    trimmer = trim_messages(strategy="last", max_tokens=2, token_counter=len)
    trimmed_messages = trimmer.invoke(state["messages"])

    system_content = f"""
    你是一名资深的JLPT日语教育专家。
    请根据前文中给出的反馈内容，引导学生提出与JLPT考试相关的问题。
    
    你指导的学生JLPT级别是: {state["level"]}
    
    要求：
    - 语言清晰简洁，适合以中文为母语的学生理解
    - 根据之前对话，理解学生的诉求，并站在学生角度提出2-3个对应的Follow-Up提问，在一个列表内 e.g.
    "[
        "Question 1",
        "Question 2",
        ...
    ]
    """

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_content),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )  # ✅ structured output

    question_agent = prompt | azure_chat_llm.with_structured_output(SuggestedQuestions)

    structured_msg = question_agent.invoke(input={"messages": trimmed_messages })

    logger.info("Structured Suggested Questions: {}".format(structured_msg))

    #Return structured output for next node
    return {"questions": structured_msg }

def entry_router_node(state: MessagesState):
    pass

def __build_graph__(checkpointer):
    # checkpointer = InMemorySaver()
    graph = StateGraph(MessagesState)
    # Add nodes
    graph.add_node(entry_router_node)
    graph.add_node(jlpt_question_explain_node)
    graph.add_node(jlpt_word_explain_node)
    # graph.add_node(suggested_question_node)

    # === Edges ===
    graph.add_edge(START, "entry_router_node")

    graph.add_conditional_edges(
        "entry_router_node",
        intent_router,
        {
            "question": "jlpt_question_explain_node",
            "word": "jlpt_word_explain_node"
        }
    )

    graph.add_edge("jlpt_question_explain_node", END)
    graph.add_edge("jlpt_word_explain_node", END)

    graph = graph.compile(checkpointer=checkpointer)


    return graph
async def generate_stream(graph, messages, config):
    """
    异步生成流式内容
    """
    async for event in graph.astream_events(
        {"messages": messages},
        config,
        stream_mode="updates"
    ):
        # 流式文本输出
        if event["event"] == "on_chat_model_stream" and event["metadata"]["langgraph_node"] == "jlpt_teacher_node":
            chunks = event["data"]["chunk"].content
            if len(chunks) > 0 and "type" in chunks[0] and chunks[0]["type"] == "text":
                text_chunk = chunks[0]["text"]
                # SSE 每条消息前加 data: 并以 \n\n 结尾
                yield f"data: {text_chunk}\n\n"

        # 链结束事件，用于发送问题列表
        elif event["event"] == "on_chain_end" and event["name"] == "suggested_question_node":
            question_list = event["data"]["output"]["questions"].questions
            wrapped_questions = {
                "type": "follow-ups",
                "text": question_list
            }
            yield f"data: {wrapped_questions}\n\n"



if __name__ == "__main__":
    config = {"configurable": {"thread_id": "thread-1"}}
    graph = __build_graph__()
    asyncio.run(generate_stream(config=config, graph=graph))
    history = graph.get_state(config)