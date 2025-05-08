from typing import *

from dotenv import load_dotenv
# from langchain_community.embeddings import XinferenceEmbeddings
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_tavily import TavilySearch
from langgraph.graph import START, END
from typing_extensions import TypedDict

load_dotenv()

def online_search_node_builder():
    def online_search(state: Type[TypedDict]):
        """
        Web search based on the re-phrased question.

        Args:
            state (dict): The current graph state

        Returns:
            state (dict): Updates documents key with appended web results
        """

        # print("---WEB SEARCH---")

        topic = state['messages'][-1].content

        tavily_search_tool = TavilySearch(
            max_results=20,
            topic="news",
            days=1
        )
        # Web search
        docs = tavily_search_tool.invoke({"query": topic})

        web_results = "\n".join([d["content"] for d in docs["results"]])

        return {"documents": web_results, "topic": topic}

    return online_search

# Nodes
def generation_node_builder(vocab_dict, llm,  prompt_text, example):
    def question_generator(state):
        """First LLM call to generate initial question"""
        # print("---Generator----")

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

def reflection_node_builder(llm):
    def reflection_node(state):
        # print("---REVISOR---")

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
            """you are a Japanese language educator reviewing a JLPT exam paper. Generate critique and recommendations for the user's submission.
               the review focuses on content accuracy and question quality. 
               - For content accuracy, you must verify that the grammar and vocabulary questions accurately reflect the appropriate JLPT N3 level, ensuring the reading passages are clear, relevant, and appropriately challenging. 
               - For question quality, you must ensure all questions are clearly worded and free from ambiguity to comprehensively assess different language skills, and confirm that the difficulty level of the questions matches the intended JLPT N3 level.
               - During detailed refinement, you check the format and presentation of the paper, ensuring it is well-organized and the instructions are clear and concise. you also ensure the content is culturally appropriate and relevant to Japanese language and culture.
               - Finally, you make give feedback, providing detailed recommendations, including requests.If you think the exam paper is good enough, you just say "GOOD ENOUGH"
               """
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )
        reflect = reflection_prompt | llm

        res = reflect.invoke(translated)

        # We treat the output of this as human feedback for the generator
        return {"messages": [HumanMessage(content=res.content)]}

    return reflection_node


def formatter_node_builder(llm, OutType: Type[TypedDict]):
    def formatter_node(state):
        # print("--- Formatter ---")

        question = state["question"]

        formatter_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are a AI assistance. your job is to format the following context to the structured output,  
                    you must translate explanation and '説明' to simplified chinese.
                    please don't modify contextual meanings and keep markdown format for the rest of content. Context: 
                    {question}"""
                )
            ]
        )
        format_pipeline = formatter_prompt | llm.with_structured_output(OutType)
        res = format_pipeline.invoke(input={"question": question})

        # We treat the output of this as human feedback for the generator
        return {"formatted_output": res}

    return formatter_node

def should_continue(state):
    if state["messages"]:
        if len(state["messages"]) > 6:
            print("--- Reach the Maximum Round ---")
            return "formatter"
        elif "GOOD ENOUGH" in state["messages"][-1].content:
            print("--- AI Reviser feels Good Enough ---")
            return "formatter"
    return "generator"


def build_graph(builder, nodes):
    """Build and compile the state graph."""
    # Add nodes
    builder.add_node("online_search", nodes["online_search"])
    builder.add_node("generator", nodes["generator"])
    builder.add_node("reflector", nodes["reflector"])
    builder.add_node("formatter", nodes["formatter"])

    # Add edges to connect nodes
    builder.add_edge(START, "online_search")
    builder.add_edge("online_search", "generator")
    builder.add_edge("generator", "reflector")
    builder.add_conditional_edges("reflector", should_continue)
    builder.add_edge("formatter", END)

    return builder.compile()