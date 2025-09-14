from dotenv import load_dotenv
from libs.Utils import _generate_dialogue,_generate_express,_generate_image,collect_vocabulary
from graphs.common.State import *
from libs.LLMs import azure_llm
import random
from graphs.n3.prompts import *
from langgraph.graph import StateGraph
import uuid
from graphs.common.JLPTTaskFactory import JLPTTaskFactory
from graphs.common.GraphBuilder import GraphBuilder

load_dotenv()
#
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

from graphs.n3.prompts import *

import importlib
from openai import OpenAI
from langchain.schema import HumanMessage

# =====================
# Standalone Task Functions
# =====================

def kanji_reading(graph: JLPTTaskFactory, word: str):
    graph = graph.build_agent(kanji_reading_teacher_prompt, kanji_reading_example, SimpleChoiceQuestionOutput)
    instance = graph.invoke({"messages": [HumanMessage(content=f"Generate a JLPT question regarding Topic: {word}")]},
                            config={"configurable": {"thread_id": "1"}})
    return instance['formatted_output']
#
#
# def write_kanji(graph: ExamTaskgraph, word: str):
#     graph = graph.build_agent(write_kanji_teacher_prompt, write_kanji_example, SimpleChoiceQuestionOutput)
#     instance = graph.invoke({"messages": [HumanMessage(content=f"Generate a JLPT question regarding Topic: {word}")]},
#                             config={"configurable": {"thread_id": "1"}})
#     return instance['formatted_output']
#
#
# def word_meaning(graph: ExamTaskgraph, word: str):
#     graph = graph.build_agent(word_meaning_teacher_prompt, word_meaning_example, SimpleChoiceQuestionOutput)
#     instance = graph.invoke({"messages": [HumanMessage(content=f"Generate a JLPT question regarding Topic: {word}")]},
#                             config={"configurable": {"thread_id": "1"}})
#     return instance['formatted_output']
#
#
# def synonym_substitution(graph: ExamTaskgraph, word: str):
#     graph = graph.build_agent(synonym_substitution_teacher_prompt, synonym_substitution_example, SimpleChoiceQuestionOutput)
#     instance = graph.invoke({"messages": [HumanMessage(content=f"Generate a JLPT question regarding Topic: {word}")]},
#                             config={"configurable": {"thread_id": "1"}})
#     return instance['formatted_output']
#
#
# def word_usage(graph: ExamTaskgraph, word: str):
#     graph = graph.build_agent(word_usage_teacher_prompt, word_usage_example, SimpleChoiceQuestionOutput)
#     instance = graph.invoke({"messages": [HumanMessage(content=f"Generate a JLPT question regarding Topic: {word}")]},
#                             config={"configurable": {"thread_id": "1"}})
#     return instance['formatted_output']
#
#
# def sentence_grammar(graph: ExamTaskgraph, word: str, grammar: str):
#     graph = graph.build_agent(sentence_grammar_teacher_prompt, sentence_grammar_example, SimpleChoiceQuestionOutput, grammar)
#     instance = graph.invoke({"messages": [HumanMessage(content=f"Generate a JLPT question regarding Topic: {word}")]},
#                             config={"configurable": {"thread_id": "1"}})
#     return instance['formatted_output']
#
#
# def sentence_sort(graph: ExamTaskgraph, word: str, grammar: str):
#     graph = graph.build_agent(sentence_sort_teacher_prompt, sentence_sort_example, SimpleChoiceQuestionOutput, grammar)
#     instance = graph.invoke({"messages": [HumanMessage(content=f"Generate a JLPT question regarding Topic: {word}")]},
#                             config={"configurable": {"thread_id": "1"}})
#     return instance['formatted_output']
#
#
# def sentence_structure(graph: ExamTaskgraph, word: str, grammar: str):
#     graph = graph.build_agent(structure_selection_teacher_prompt, structure_selection_example, MultipleQuestionOutput, grammar)
#     instance = graph.invoke({"messages": [HumanMessage(content=f"Generate a JLPT question regarding Topic: {word}")]},
#                             config={"configurable": {"thread_id": "1"}})
#     return instance['formatted_output']
#
#
# def short_passage_narrative_read(graph: ExamTaskgraph, word: str):
#     graph = graph.build_agent(short_reading_narrative_teacher_prompt, short_reading_narrative_example, MultipleQuestionOutput)
#     instance = graph.invoke({"messages": [HumanMessage(content=f"Generate a JLPT question regarding Topic: {word}")]},
#                             config={"configurable": {"thread_id": "1"}})
#     return instance['formatted_output']
#
#
# def short_passage_mail_read(graph: ExamTaskgraph, word: str):
#     graph = graph.build_agent(short_reading_mail_teacher_prompt, short_reading_mail_example, MultipleQuestionOutput)
#     instance = graph.invoke({"messages": [HumanMessage(content=f"Generate a JLPT question regarding Topic: {word}")]},
#                             config={"configurable": {"thread_id": "1"}})
#     return instance['formatted_output']
#
#
# def short_passage_notification_read(graph: ExamTaskgraph, word: str):
#     graph = graph.build_agent(short_reading_notification_teacher_prompt, short_reading_notification_example, MultipleQuestionOutput)
#     instance = graph.invoke({"messages": [HumanMessage(content=f"Generate a JLPT question regarding Topic: {word}")]},
#                             config={"configurable": {"thread_id": "1"}})
#     return instance['formatted_output']
#
#
# def midsize_passage_read(graph: ExamTaskgraph, word: str):
#     graph = graph.build_agent(midsize_reading_teacher_prompt, midsize_reading_example, MultipleQuestionOutput)
#     instance = graph.invoke({"messages": [HumanMessage(content=f"Generate a JLPT question regarding Topic: {word}")]},
#                             config={"configurable": {"thread_id": "1"}})
#     return instance['formatted_output']
#
#
# def long_passage_read(graph: ExamTaskgraph, word: str):
#     graph = graph.build_agent(long_reading_teacher_prompt, long_reading_example, MultipleQuestionOutput)
#     instance = graph.invoke({"messages": [HumanMessage(content=f"Generate a JLPT question regarding Topic: {word}")]},
#                             config={"configurable": {"thread_id": "1"}})
#     return instance['formatted_output']
#
#
# def info_retrieval(graph: ExamTaskgraph, word: str):
#     graph = graph.build_agent(information_retrieval_teacher_prompt, information_retrieval_example, MultipleQuestionOutput)
#     instance = graph.invoke({"messages": [HumanMessage(content=f"Generate a JLPT question regarding Topic: {word}")]},
#                             config={"configurable": {"thread_id": "1"}})
#     return instance['formatted_output']
#
#
# def topic_understanding(graph: ExamTaskgraph, word: str, seq: int):
#     graph = graph.build_agent(topic_understanding_teacher_prompt, topic_understanding_example, ListenSingleChoiceOutput)
#     instance = graph.invoke({"messages": [HumanMessage(content=f"Generate a JLPT question regarding Topic: {word}")]},
#                             config={"configurable": {"thread_id": "1"}})
#     obj = instance['formatted_output']
#     obj['audio'] = _generate_dialogue(content=obj, type="topic_understanding", seq=seq, uid=graph.exam_uid)
#     return obj
#
#
# def keypoint_understanding(graph: ExamTaskgraph, word: str, seq: int):
#     graph = graph.build_agent(keypoint_understanding_teacher_prompt, keypoint_understanding_example, ListenSingleChoiceOutput)
#     instance = graph.invoke({"messages": [HumanMessage(content=f"Generate a JLPT question regarding Topic: {word}")]},
#                             config={"configurable": {"thread_id": "1"}})
#     obj = instance['formatted_output']
#     obj['audio'] = _generate_dialogue(content=obj, type="keypoint_understanding", seq=seq, uid=graph.exam_uid)
#     return obj
#
#
# def summary_understanding(graph: ExamTaskgraph, word: str, seq: int):
#     graph = graph.build_agent(summary_understanding_teacher_prompt, summary_understanding_example, ListenSingleChoiceOutput)
#     instance = graph.invoke({"messages": [HumanMessage(content=f"Generate a JLPT question regarding Topic: {word}")]},
#                             config={"configurable": {"thread_id": "1"}})
#     obj = instance['formatted_output']
#     obj['audio'] = _generate_dialogue(content=obj, type="summary_understanding", seq=seq, uid=graph.exam_uid)
#     return obj
#
#
# def active_expression(graph: ExamTaskgraph, word: str, seq: int):
#     graph = graph.build_agent(actively_expression_teacher_prompt, actively_expression_example, ImageListenQuestionOutput)
#     instance = graph.invoke({"messages": [HumanMessage(content=f"Generate a JLPT question regarding Topic: {word}")]},
#                             config={"configurable": {"thread_id": "1"}})
#     obj = instance['formatted_output']
#     obj['audio'] = _generate_express(content=obj, type="active_expression", seq=seq, uid=graph.exam_uid)
#     obj['image'] = _generate_image(obj['background'])
#     return obj
#
#
# def immediate_ack(graph: ExamTaskgraph, word: str, seq: int):
#     graph = graph.build_agent(immediate_ack_teacher_prompt, immediate_ack_example, ListenImmediateQuestionOutput)
#     instance = graph.invoke({"messages": [HumanMessage(content=f"Generate a JLPT question regarding Topic: {word}")]},
#                             config={"configurable": {"thread_id": "1"}})
#     obj = instance['formatted_output']
#     obj['audio'] = _generate_express(content=obj, type="immediate_ack", seq=seq, uid=graph.exam_uid)
#     return obj



if __name__ == "__main__":
    n3_vocab = collect_vocabulary("../../vocab/n3.csv")
    with open("../../vocab/topics.txt", "r", encoding="utf-8") as file:
        topics_list = [line.strip() for line in file]
    random_word = random.choice(n3_vocab.split(","))
    random_topic = random.choice(topics_list)
    # ra

    #Kanji Reading
    # graph = GraphBuilder()
    # print(kanji_reading(random_word))

    # # Write Chinese Task
    # graph = ExamTaskgraph()
    # print(graph.write_kanji(random_word))

    # # Word Meaning Task
    # graph = ExamTaskgraph()
    # print(graph.word_meaning(random_word))
    #
    # # Synonym Substitution Task
    # graph = ExamTaskgraph()
    # print(graph.synonym_substitution(random_word))
    #
    # Word Usage Task
    # graph = ExamTaskgraph()
    # print(graph.word_usage(random_word))
    #
    # # Sentence Grammar Task
    # graph = ExamTaskgraph()
    # print(graph.sentence_grammar(random_word))
    #
    # # Sentence Sort Task
    # graph = ExamTaskgraph()
    # print(graph.sentence_sort(random_word))
    #
    # Sentence Structure Task
    # graph = ExamTaskgraph()
    # print(graph.sentence_structure(random_topic))

    # # Short Passage Read Task
    # graph = ExamTaskgraph()
    # print(graph.short_passage_read(random_word))
    #
    # # Midsize Passage Read Task
    # graph = ExamTaskgraph()
    # print(graph.midsize_passage_read(random_word))
    #
    # # Long Passage Read Task
    # graph = ExamTaskgraph()
    # print(graph.long_passage_read(random_word))

    # Info Retrieval Task
    # graph = ExamTaskgraph()
    # print(graph.info_retrieval(random_word))

    # # Topic Understanding Task
    # graph = ExamTaskgraph()
    # print(graph.topic_understanding(random_word))
    #
    # # Keypoint Understanding Task
    # graph = ExamTaskgraph()
    # print(graph.keypoint_understanding(random_word))
    #
    # # Summary Understanding Task
    # graph = ExamTaskgraph()
    # print(graph.summary_understanding(random_word))
    #
    # # Active Expression Task
    # graph = ExamTaskgraph()
    # print(graph.active_expression(random_word))
    #
    # Immediate Ack Task
    graph = GraphBuilder(exam_id=uuid.uuid1())
    factory = JLPTTaskFactory(graph, level="n3")
    q1 = factory.kanji_reading("学校")

    # graph = ExamTaskgraph('n3',uuid.uuid1())
    # immediate_ack(graph, random_word, seq=1)