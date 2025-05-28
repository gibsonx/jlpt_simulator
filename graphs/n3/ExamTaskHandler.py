from graphs.common.node_builder import *
from graphs.common.utils import *
from graphs.common.state import *
from libs.LLMs import azure_llm, azure_ref_llm
import random
from graphs.n3.prompts import *
from langgraph.graph import StateGraph
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ExamTaskHandler:
    def __init__(self):
        self.llm = azure_llm
        self.ref_llm = azure_llm
        self.nodes = {
            "online_search": None,
            "generator": None,
            "reflector": None,
            "formatter": None
        }


    def build_agent(self, prompt_text, example, OutType):
        self.nodes["online_search"] = online_search_node_builder()
        self.nodes["generator"] = generation_node_builder(
            llm=self.llm,
            prompt_text=prompt_text,
            example=example
        )
        self.nodes["reflector"] = reflection_node_builder(llm=self.ref_llm)
        self.nodes["formatter"] = formatter_node_builder(llm=self.ref_llm, OutType=OutType)
        graph = build_graph(StateGraph(SimpleQuestionState), self.nodes)

        return graph

    def invoke(self, word):
        instance = self.build_agent().invoke(
            {"messages": [HumanMessage(content=word)]},
            config={"configurable": {"thread_id": "1"}}
        )
        return instance['formatted_output']

    def kanji_reading(self, word):
        graph = self.build_agent(kanji_reading_teacher_prompt, kanji_reading_example, SimpleChoiceQuestionOutput)
        instance = graph.invoke(
            {"messages": [HumanMessage(content=word)]},
            config={"configurable": {"thread_id": "1"}}
        )
        return instance['formatted_output']

    def write_chinese(self, word):
        graph = self.build_agent(write_chinese_teacher_prompt, write_chinese_example, SimpleChoiceQuestionOutput)
        instance = graph.invoke(
            {"messages": [HumanMessage(content=word)]},
            config={"configurable": {"thread_id": "1"}}
        )
        return instance['formatted_output']

    def word_meaning(self, word):
        graph = self.build_agent(word_meaning_teacher_prompt, word_meaning_example, SimpleChoiceQuestionOutput)
        instance = graph.invoke(
            {"messages": [HumanMessage(content=word)]},
            config={"configurable": {"thread_id": "1"}}
        )
        return instance['formatted_output']

    def synonym_substitution(self, word):
        graph = self.build_agent(synonym_substitution_teacher_prompt, synonym_substitution_example, SimpleChoiceQuestionOutput)
        instance = graph.invoke(
            {"messages": [HumanMessage(content=word)]},
            config={"configurable": {"thread_id": "1"}}
        )
        return instance['formatted_output']

    def word_usage(self, word):
        graph = self.build_agent(word_usage_teacher_prompt, word_usage_example, SimpleChoiceQuestionOutput)
        instance = graph.invoke(
            {"messages": [HumanMessage(content=word)]},
            config={"configurable": {"thread_id": "1"}}
        )
        return instance['formatted_output']

    def sentence_grammar(self, word):
        graph = self.build_agent(sentence_grammar_teacher_prompt, sentence_grammar_example, SimpleChoiceQuestionOutput)
        instance = graph.invoke(
            {"messages": [HumanMessage(content=word)]},
            config={"configurable": {"thread_id": "1"}}
        )
        return instance['formatted_output']

    def sentence_sort(self, word):
        graph = self.build_agent(sentence_sort_teacher_prompt, sentence_sort_example, SimpleChoiceQuestionOutput)
        instance = graph.invoke(
            {"messages": [HumanMessage(content=word)]},
            config={"configurable": {"thread_id": "1"}}
        )
        return instance['formatted_output']

    def sentence_structure(self, word):
        graph = self.build_agent(structure_selection_teacher_prompt, structure_selection_example, MultipleQuestionOutput)
        instance = graph.invoke(
            {"messages": [HumanMessage(content=word)]},
            config={"configurable": {"thread_id": "1"}}
        )
        return instance['formatted_output']

    def short_passage_read(self, word):
        graph = self.build_agent(short_reading_teacher_prompt, short_reading_example, SimpleChoiceQuestionOutput)
        instance = graph.invoke(
            {"messages": [HumanMessage(content=word)]},
            config={"configurable": {"thread_id": "1"}}
        )
        return instance['formatted_output']

    def midsize_passage_read(self, word):
        graph = self.build_agent(midsize_reading_teacher_prompt, midsize_reading_example, SimpleChoiceQuestionOutput)
        instance = graph.invoke(
            {"messages": [HumanMessage(content=word)]},
            config={"configurable": {"thread_id": "1"}}
        )
        return instance['formatted_output']

    def long_passage_read(self, word):
        graph = self.build_agent(long_reading_teacher_prompt, long_reading_example, MultipleQuestionOutput)
        instance = graph.invoke(
            {"messages": [HumanMessage(content=word)]},
            config={"configurable": {"thread_id": "1"}}
        )
        return instance['formatted_output']

    def info_retrieval(self, word):
        graph = self.build_agent(information_retrieval_teacher_prompt, information_retrieval_example, MultipleQuestionOutput)
        instance = graph.invoke(
            {"messages": [HumanMessage(content=word)]},
            config={"configurable": {"thread_id": "1"}}
        )
        return instance['formatted_output']

    def topic_understanding(self, word):
        graph = self.build_agent(topic_understanding_teacher_prompt, topic_understanding_example, ListenSingleChoiceOutput)
        instance = graph.invoke(
            {"messages": [HumanMessage(content=word)]},
            config={"configurable": {"thread_id": "1"}}
        )
        return instance['formatted_output']

    def keypoint_understanding(self, word):
        graph = self.build_agent(keypoint_understanding_teacher_prompt, keypoint_understanding_example, ListenSingleChoiceOutput)
        instance = graph.invoke(
            {"messages": [HumanMessage(content=word)]},
            config={"configurable": {"thread_id": "1"}}
        )
        return instance['formatted_output']

    def summary_understanding(self, word):
        graph = self.build_agent(summary_understanding_teacher_prompt, summary_understanding_example, ListenSingleChoiceOutput)
        instance = graph.invoke(
            {"messages": [HumanMessage(content=word)]},
            config={"configurable": {"thread_id": "1"}}
        )
        return instance['formatted_output']

    def active_expression(self, word):
        graph = self.build_agent(actively_expression_teacher_prompt, actively_expression_example, ImageListenQuestionOutput)
        instance = graph.invoke(
            {"messages": [HumanMessage(content=word)]},
            config={"configurable": {"thread_id": "1"}}
        )
        return instance['formatted_output']

    def immediate_ack(self, word):
        graph = self.build_agent(immediate_ack_teacher_prompt, immediate_ack_example, ListenOpenQuestionOutput)
        instance = graph.invoke(
            {"messages": [HumanMessage(content=word)]},
            config={"configurable": {"thread_id": "1"}}
        )
        return instance['formatted_output']

if __name__ == "__main__":
    n3_vocab = collect_vocabulary("../../Vocab/n3.csv")

    random_word = random.choice(n3_vocab.split(","))

    # Kanji Reading
    handler = ExamTaskHandler()
    print(handler.kanji_reading(random_word))
    
    # # Write Chinese Task
    # handler = ExamTaskHandler()
    # print(handler.write_chinese(random_word))
    #
    # # Word Meaning Task
    # handler = ExamTaskHandler()
    # print(handler.word_meaning(random_word))
    #
    # # Synonym Substitution Task
    # handler = ExamTaskHandler()
    # print(handler.synonym_substitution(random_word))
    #
    # # Word Usage Task
    # handler = ExamTaskHandler()
    # print(handler.word_usage(random_word))
    #
    # # Sentence Grammar Task
    # handler = ExamTaskHandler()
    # print(handler.sentence_grammar(random_word))
    #
    # # Sentence Sort Task
    # handler = ExamTaskHandler()
    # print(handler.sentence_sort(random_word))
    #
    # # Sentence Structure Task
    # handler = ExamTaskHandler()
    # print(handler.sentence_structure(random_word))
    #
    # # Short Passage Read Task
    # handler = ExamTaskHandler()
    # print(handler.short_passage_read(random_word))
    #
    # # Midsize Passage Read Task
    # handler = ExamTaskHandler()
    # print(handler.midsize_passage_read(random_word))
    #
    # # Long Passage Read Task
    # handler = ExamTaskHandler()
    # print(handler.long_passage_read(random_word))

    # Info Retrieval Task
    # handler = ExamTaskHandler()
    # print(handler.info_retrieval(random_word))

    # # Topic Understanding Task
    # handler = ExamTaskHandler()
    # print(handler.topic_understanding(random_word))
    #
    # # Keypoint Understanding Task
    # handler = ExamTaskHandler()
    # print(handler.keypoint_understanding(random_word))
    #
    # # Summary Understanding Task
    # handler = ExamTaskHandler()
    # print(handler.summary_understanding(random_word))
    #
    # # Active Expression Task
    # handler = ExamTaskHandler()
    # print(handler.active_expression(random_word))
    #
    # # Immediate Ack Task
    # handler = ExamTaskHandler()
    # print(handler.immediate_ack(random_word))