# from langchain_community.embeddings import XinferenceEmbeddings
from typing import Annotated,Literal
from typing import List

from langgraph.graph.message import add_messages
from typing_extensions import TypedDict


# Graph state

class SimpleChoiceQuestionOutput(TypedDict):
    """Simple Question Formatted Output"""
    question: Annotated[str, "the question to ask candidate in Japanese in html format"]
    explanation: Annotated[str, "the key challenges and explanation in simplified Chinese"]
    correct_answer: Annotated[int, "correct option"]
    choices: Annotated[List, "options as a list for candidate to choose in Japanese"]

class ListenConversation(TypedDict):
    gender: Literal['male','female']
    context: Annotated[str, "context for the conversation in Japanese"]

class ListenOpenQuestionOutput(TypedDict):
    """Simple Question Formatted Output"""
    question: Annotated[str, "the question to ask candidate in Japanese"]
    explanation: Annotated[str, "the key challenges and explanation in simplified Chinese"]
    suggestion: Annotated[str, "the suggesting answer in Japanese"]
    conversation: List[ListenConversation]

class ListenSingleChoiceOutput(TypedDict):
    """Listen Simple Question Formatted Output"""
    questions: SimpleChoiceQuestionOutput
    conversation: List[ListenConversation]

class ImageListenQuestionOutput(TypedDict):
    """Listen Simple Question Formatted Output"""
    image_background: Annotated[str, "detail prompt words for describing the background to generate image in English"]
    questions: SimpleChoiceQuestionOutput
    conversation: List[ListenConversation]

class SimpleQuestionState(TypedDict):
    topic: str
    question: str
    documents: str
    formatted_output: SimpleChoiceQuestionOutput
    messages: Annotated[list, add_messages]

class MultipleQuestionOutput(TypedDict):
    """An Article with several Question Formatted Output"""
    html_article: Annotated[str, "the article in HTML format"]
    questions: List[SimpleChoiceQuestionOutput]

