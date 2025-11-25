from typing import *

# from langchain_community.embeddings import XinferenceEmbeddings
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_tavily import TavilySearch
from langgraph.graph import START, END
from typing_extensions import TypedDict
from libs.Logger import logger
from graphs.common.GraphBuilder import *

from libs.Utils import _generate_dialogue,_generate_express,_generate_image,collect_vocabulary
from graphs.common.Schema import *
from libs.LLMs import azure_llm
import random
from graphs.n3.prompts import *
from langgraph.graph import StateGraph
import uuid

from dotenv import load_dotenv
load_dotenv()

class GraphBuilder:
    def __init__(self, exam_uid):
        self.exam_uid = exam_uid
        self.llm = azure_llm
        self.ref_llm = azure_llm
        self.nodes = {
            "online_search": None,
            "generator": None,
            "reflector": None,
            "formatter": None
        }

    def online_search_node_builder(self):
        def online_search(state: Type[TypedDict]):
            """
            Web search based on the re-phrased question.

            Args:
                state (dict): The current graph state

            Returns:
                state (dict): Updates documents key with appended web results
            """

            logger.info("---WEB SEARCH---")

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
    def generation_node_builder(self, llm,  prompt_text, example, gan_history: Optional[str] = "", grammar: Optional[str] = None):
        def question_generator(state):
            """First LLM call to generate initial question"""
            logger.info("---Generator----")

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
                "gan_history": gan_history,
                "example": example,
                "messages": state["messages"],
            }

            if grammar:
                params["grammar"] = grammar

            # Format the prompt to get the actual text
            resolved_prompt = prompt.format_messages(**params)

            state["messages"].insert(0, resolved_prompt[0])

            generate = prompt | llm

            msg = generate.invoke(input=params)

            return {"question": msg.content, "messages": [AIMessage(content=msg.content)]}

        return question_generator

    def reflection_node_builder(self, llm, reflection_prompt_text: str = None):
        def reflection_node(state):
            logger.info("---REVISOR---")

            cls_map = {"ai": HumanMessage, "human": AIMessage}

            # Check for a system message in state["messages"]
            system_msg = next((msg for msg in state["messages"] if msg.type == "system"), None)

            # Build translated list
            translated = []
            if system_msg:
                translated.append(system_msg)  # system message first

            # Always add the original user request (state["messages"][0]) next
            translated.append(state["messages"][0])

            # Then add the rest, excluding the first and system messages if already added
            for msg in state["messages"][1:]:
                if msg != system_msg:
                    translated.append(cls_map.get(msg.type, HumanMessage)(content=msg.content))

            # Use provided reflection prompt text if given, otherwise fall back to the original default.
            system_content = f"""
               You are a senior Japanese language educator reviewing a JLPT exam paper. Generate an English critique and recommendations for the Japanese teacher's submission.
               Please think deeply and give feedback on the following factors:
                 - For content accuracy, you must verify that the questions are abide by the corresponding JLPT level exam requirements and appropriately challenging. 
                 - For question and answer options quality, you must ensure all questions are clearly worded and free from ambiguity. Verify whether the context matches the difficulty level of the specified JLPT level.
                 - You must review the "Historical Generation" to ensure no previously asked questions(q) or given answers(a) in the current generation.
                 - You should also ensure the content is culturally appropriate and relevant to Japanese culture and native expression.\n\n
                 {reflection_prompt_text}
               However, Don't suggest to add any question instructions to the context. Don't suggest anything about html format. Do not suggest including instructions in the question such as whether it tests meaning, kanji, or context.     
               Finally, if you believe the submission is qualified, simply reply with "GOOD ENOUGH". Otherwise, provide a detailed critique and your recommendations for improvement.
               """

            reflection_prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", system_content),
                    MessagesPlaceholder(variable_name="messages"),
                ]
            )

            reflect = reflection_prompt | llm
            # explicit input mapping for clarity
            msg = reflect.invoke(input={"messages": translated})

            logger.info("Reflect Feedback: {}".format(msg.content))

            # Return as human feedback for the generator
            return {"messages": [HumanMessage(content=msg.content)]}

        return reflection_node

    def formatter_node_builder(self, llm, OutType: Type[TypedDict]):
        def formatter_node(state):
            logger.info("--- Formatter ---")

            logger.info(
                "Final Conversation:\n" +
                "\n".join(
                    f"{msg.type.upper()}: {msg.content}"
                    for msg in state["messages"]
                )
            )

            question = state["question"]

            formatter_prompt = ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        """You are a AI assistance. your job is to format the Context to the structured output following 
                        the instruction below: 
                        1. you should not change any context and html tags, except removing change line tags like \\n or \\n\\n from the context.
                        2. use the content inside <a></a> as the html_question. However, the content in the <ul class='options'></ul> and <p class='follow-up'></p> should not be written in html_question. 
                        3. Also, question requirements and correct answer should not be written in the html_question.
                        4. write the content in the <div class='article'></div> in html_article. but choices in <li></li> must be excluded.
                        5. use the content inside <li></li> as choices and keep html format, but <li></li> tags must be excluded.
                        6. write the content in the <div class='background'></div> in background if it exists, no modification.
                        Context: {question}"""
                    )
                ]
            )
            format_pipeline = formatter_prompt | llm.with_structured_output(OutType)

            msg = format_pipeline.invoke(input={"question": question})

            # logger.info("Formatter: {}".format(msg))

            # We treat the output of this as human feedback for the generator
            return {"formatted_output": msg }

        return formatter_node

    def should_continue(self, state):
        if state["messages"]:
            if len(state["messages"]) > 7:
                logger.info("--- Reach the Maximum Round ---")
                return "formatter"
            elif "GOOD ENOUGH" in state["messages"][-1].content:
                logger.info("--- AI Reviser feels Good Enough ---")
                return "formatter"
            else:
                logger.info("--- To be improved by regeneration ---")
        return "generator"


    def build_graph(self, builder, nodes):
        """Build and compile the state graph."""
        # Add nodes
        # builder.add_node("online_search", nodes["online_search"])
        builder.add_node("generator", nodes["generator"])
        builder.add_node("reflector", nodes["reflector"])
        builder.add_node("formatter", nodes["formatter"])

        # Add edges to connect nodes
        builder.add_edge(START, "generator")
        # builder.add_edge("online_search", "generator")
        builder.add_edge("generator", "reflector")
        builder.add_conditional_edges("reflector", self.should_continue)
        builder.add_edge("formatter", END)

        return builder.compile()

    def build_agent(self, prompt_text: str, example: str, reflection_prompt: str, output_cls: Any, gan_history: Optional[str] = "", grammar: Optional[str] = None):
        self.nodes["online_search"] = self.online_search_node_builder()
        if grammar:
            self.nodes["generator"] = self.generation_node_builder(
                llm=self.llm,
                prompt_text=prompt_text,
                example=example,
                gan_history=gan_history,
                grammar=grammar,
            )
        else:
            self.nodes["generator"] = self.generation_node_builder(
                llm=self.llm,
                prompt_text=prompt_text,
                gan_history=gan_history,
                example=example
            )

        # Pass the reflection_prompt to the reflection node builder
        self.nodes["reflector"] = self.reflection_node_builder(
            llm=self.ref_llm,
            reflection_prompt_text=reflection_prompt
        )
        self.nodes["formatter"] = self.formatter_node_builder(llm=self.ref_llm, OutType=output_cls)

        graph = self.build_graph(StateGraph(GraphState), self.nodes)
        return graph