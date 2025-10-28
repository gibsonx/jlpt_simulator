# from langchain_community.embeddings import XinferenceEmbeddings
from typing import Annotated,Literal
from typing import List, Optional
from pydantic import BaseModel, Field
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict

# ----------------------------
# Question Output Structures
# ----------------------------
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
    context: Annotated[str, "context for the conversation in Japanese, excluding gender"]

class ListenMultiPersonConversation(TypedDict):
    gender: Literal['male1','male2','female1','female2']
    context: Annotated[str, "context for the conversation in Japanese, excluding gender"]

class ListenSingleChoiceOutput(TypedDict):
    """Listen Simple Question Formatted Output"""
    background: Annotated[str, "the background introduction of the conversation"]
    follow_up: Annotated[str, "the follow-up question"]
    conversation: List[ListenConversation]
    choices: Annotated[List, "answer options as a list, each option is in string format"]
    correct_answer: Annotated[int, "correct option in 1,2,3,4"]

class ListenMultiPersonOutput(TypedDict):
    """Listen Simple Question Formatted Output"""
    background: Annotated[str, "the background introduction of the conversation"]
    follow_up: Annotated[str, "the follow-up question"]
    conversation: List[ListenMultiPersonConversation]
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

# ----------------------------
# Outline Structures
# ----------------------------
class QuestionTopic(BaseModel):
    topic: str = Field(..., title="a vocabulary or topic hint for a question")
    grammar: str = Field(None, title="a grammar used for this question")

class Subsection(BaseModel):
    subsection_title: str = Field(..., title="subsection English name in () from the Instruction. example: kanji_reading")
    description: str = Field(..., title="giving the number of questions and requirements")
    question_topics: List[QuestionTopic] = Field(
        default_factory=list
    )

    @property
    def as_str(self) -> str:
        question_topics_str = "\n".join(
            f"- **{qt.topic}**{qt.grammar}" for qt in self.question_topics
        )
        return f"### {self.subsection_title}\n\n{self.description}\n\n{question_topics_str}".strip()

class Section(BaseModel):
    section_title: str = Field(..., title="Title of the section")
    subsections: Optional[List[Subsection]] = Field(
        default_factory=list,
        title="Titles and reason for each subsection of the JLPT exam page.",
    )

    @property
    def as_str(self) -> str:
        subsections = "\n\n".join(
            subsection.as_str for subsection in self.subsections or []
        )
        return f"## {self.section_title}\n\n{subsections}".strip()

class Outline(BaseModel):
    page_title: str = Field(..., title="Title of the JLPT exam page")
    sections: List[Section] = Field(
        default_factory=list,
        title="Titles and descriptions for each section of the JLPT exam paper.",
    )

    @property
    def as_str(self) -> str:
        sections = "\n\n".join(section.as_str for section in self.sections)
        return f"# {self.page_title}\n\n{sections}".strip()

ExamType = Literal["full_exam","fast_exam","vocab","grammar","reading","listening"]

ExamLevel = Literal["n1","n2","n3","n4","n5"]