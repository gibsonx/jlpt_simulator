# from langchain_community.embeddings import XinferenceEmbeddings
from typing import Annotated,Literal
from typing import List

from langgraph.graph.message import add_messages
from typing_extensions import TypedDict


# Graph state

class SimpleChoiceQuestionOutput(TypedDict):
    """Simple Question Formatted Output"""
    html_question: Annotated[str, "the question in html format at a single line"]
    correct_answer: Annotated[int, "correct option in 1,2,3,4"]
    choices: Annotated[List, "answer options as a list, each option is in html format"]

class GraphState(TypedDict):
    topic: str
    question: str
    requirement: str
    documents: str
    formatted_output: dict
    messages: Annotated[list, add_messages]

class MultipleQuestionOutput(TypedDict):
    """An Article with several Question Formatted Output"""
    html_article: Annotated[str, "the article in HTML format at a single line"]
    questions: List[SimpleChoiceQuestionOutput]

class ListenConversation(TypedDict):
    gender: Literal['male','female']
    context: Annotated[str, "context for the conversation in Japanese"]

class ListenSingleChoiceOutput(TypedDict):
    """Listen Simple Question Formatted Output"""
    background: Annotated[str, "the background introduction of the conversation"]
    follow_up: Annotated[str, "the follow-up question"]
    conversation: List[ListenConversation]
    html_question: Annotated[str, "the question in html format at a single line"]
    choices: Annotated[List, "answer options as a list, each option is in string format"]
    correct_answer: Annotated[int, "correct option in 1,2,3,4"]

class ImageListenQuestionOutput(TypedDict):
    """Listen Simple Question Formatted Output"""
    background: Annotated[str, "detail prompt strings for describing the background to generate image"]
    follow_up: Annotated[str, "the follow-up question"]
    conversation: List[ListenConversation]
    choices: Annotated[List, "answer options as a list, each option is in string format"]
    correct_answer: Annotated[int, "correct option in 1,2,3"]

class ListenImmediateQuestionOutput(TypedDict):
    """Listen Simple Question Formatted Output"""
    follow_up: Annotated[str, "the follow-up question"]
    conversation: List[ListenConversation]
    choices: Annotated[List, "answer options as a list, each option is in string format"]
    correct_answer: Annotated[int, "correct option in 1,2,3"]

