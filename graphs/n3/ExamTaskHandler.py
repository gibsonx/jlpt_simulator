from graphs.common.node_builder import *
from libs.Utils import _generate_dialogue,_generate_express,_generate_image,collect_vocabulary
from graphs.common.state import *
from libs.LLMs import azure_llm
import random
from graphs.n3.prompts import *
from langgraph.graph import StateGraph

load_dotenv()
#
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
        # with open("Vocab/sentence_grammar.txt", "r", encoding="utf-8") as file:
        #     self.ss = [line.strip() for line in file]

    def build_agent(self, prompt_text, example, OutType, grammar=None):
        self.nodes["online_search"] = online_search_node_builder()

        if grammar:
            self.nodes["generator"] = generation_node_builder(
                llm=self.llm,
                prompt_text=prompt_text,
                example=example,
                grammar=grammar
            )
        else:
            self.nodes["generator"] = generation_node_builder(
                llm=self.llm,
                prompt_text=prompt_text,
                example=example
            )
        self.nodes["reflector"] = reflection_node_builder(llm=self.ref_llm)
        self.nodes["formatter"] = formatter_node_builder(llm=self.ref_llm, OutType=OutType)
        graph = build_graph(StateGraph(GraphState), self.nodes)

        return graph

    # def invoke(self, word):
    #     instance = self.build_agent().invoke(
    #         {"messages": [HumanMessage(content=f"Generate a JLPT question regrading Topic: {word}")]},
    #         config={"configurable": {"thread_id": "1"}}
    #     )
    #     return instance['formatted_output']

    def kanji_reading(self, word, seq=1):
        graph = self.build_agent(kanji_reading_teacher_prompt, kanji_reading_example, SimpleChoiceQuestionOutput)
        instance = graph.invoke(
            {"messages": [HumanMessage(content=f"Generate a JLPT question regrading Topic: {word}")]},
            config={"configurable": {"thread_id": "1"}}
        )
        return instance['formatted_output']

    def write_kanji(self, word, seq=1):
        graph = self.build_agent(write_kanji_teacher_prompt, write_kanji_example, SimpleChoiceQuestionOutput)
        instance = graph.invoke(
            {"messages": [HumanMessage(content=f"Generate a JLPT question regrading Topic: {word}")]},
            config={"configurable": {"thread_id": "1"}}
        )
        return instance['formatted_output']

    def word_meaning(self, word, seq=1):
        graph = self.build_agent(word_meaning_teacher_prompt, word_meaning_example, SimpleChoiceQuestionOutput)
        instance = graph.invoke(
            {"messages": [HumanMessage(content=f"Generate a JLPT question regrading Topic: {word}")]},
            config={"configurable": {"thread_id": "1"}}
        )
        return instance['formatted_output']

    def synonym_substitution(self, word, seq=1):
        graph = self.build_agent(synonym_substitution_teacher_prompt, synonym_substitution_example, SimpleChoiceQuestionOutput)
        instance = graph.invoke(
            {"messages": [HumanMessage(content=f"Generate a JLPT question regrading Topic: {word}")]},
            config={"configurable": {"thread_id": "1"}}
        )
        return instance['formatted_output']

    def word_usage(self, word, seq=1):
        graph = self.build_agent(word_usage_teacher_prompt, word_usage_example, SimpleChoiceQuestionOutput)
        instance = graph.invoke(
            {"messages": [HumanMessage(content=f"Generate a JLPT question regrading Topic: {word}")]},
            config={"configurable": {"thread_id": "1"}}
        )
        return instance['formatted_output']

    def sentence_grammar(self, word, grammar, seq=1):
        graph = self.build_agent(sentence_grammar_teacher_prompt, sentence_grammar_example, SimpleChoiceQuestionOutput, grammar)
        instance = graph.invoke(
            {"messages": [HumanMessage(content=f"Generate a JLPT question regrading Topic: {word}")]},
            config={"configurable": {"thread_id": "1"}}
        )
        return instance['formatted_output']

    def sentence_sort(self, word, grammar, seq=1):
        graph = self.build_agent(sentence_sort_teacher_prompt, sentence_sort_example, SimpleChoiceQuestionOutput, grammar)
        instance = graph.invoke(
            {"messages": [HumanMessage(content=f"Generate a JLPT question regrading Topic: {word}")]},
            config={"configurable": {"thread_id": "1"}}
        )
        return instance['formatted_output']

    def sentence_structure(self, word, grammar, seq):
        graph = self.build_agent(structure_selection_teacher_prompt, structure_selection_example, MultipleQuestionOutput, grammar)
        instance = graph.invoke(
            {"messages": [HumanMessage(content=f"Generate a JLPT question regrading Topic: {word}")]},
            config={"configurable": {"thread_id": "1"}}
        )
        return instance['formatted_output']

    def short_passage_narrative_read(self, word, seq):
        graph = self.build_agent(short_reading_narrative_teacher_prompt, short_reading_narrative_example, MultipleQuestionOutput)
        instance = graph.invoke(
            {"messages": [HumanMessage(content=f"Generate a JLPT question regrading Topic: {word}")]},
            config={"configurable": {"thread_id": "1"}}
        )
        return instance['formatted_output']

    def short_passage_mail_read(self, word, seq):
        graph = self.build_agent(short_reading_mail_teacher_prompt, short_reading_mail_example, MultipleQuestionOutput)
        instance = graph.invoke(
            {"messages": [HumanMessage(content=f"Generate a JLPT question regrading Topic: {word}")]},
            config={"configurable": {"thread_id": "1"}}
        )
        return instance['formatted_output']

    def short_passage_notification_read(self, word, seq):
        graph = self.build_agent(short_reading_notification_teacher_prompt, short_reading_notification_example, MultipleQuestionOutput)
        instance = graph.invoke(
            {"messages": [HumanMessage(content=f"Generate a JLPT question regrading Topic: {word}")]},
            config={"configurable": {"thread_id": "1"}}
        )
        return instance['formatted_output']

    def midsize_passage_read(self, word, seq):
        graph = self.build_agent(midsize_reading_teacher_prompt, midsize_reading_example, MultipleQuestionOutput)
        instance = graph.invoke(
            {"messages": [HumanMessage(content=f"Generate a JLPT question regrading Topic: {word}")]},
            config={"configurable": {"thread_id": "1"}}
        )
        return instance['formatted_output']

    def long_passage_read(self, word, seq):
        graph = self.build_agent(long_reading_teacher_prompt, long_reading_example, MultipleQuestionOutput)
        instance = graph.invoke(
            {"messages": [HumanMessage(content=f"Generate a JLPT question regrading Topic: {word}")]},
            config={"configurable": {"thread_id": "1"}}
        )
        return instance['formatted_output']

    def info_retrieval(self, word, seq):
        graph = self.build_agent(information_retrieval_teacher_prompt, information_retrieval_example, MultipleQuestionOutput)
        instance = graph.invoke(
            {"messages": [HumanMessage(content=f"Generate a JLPT question regrading Topic: {word}")]},
            config={"configurable": {"thread_id": "1"}}
        )
        return instance['formatted_output']

    def topic_understanding(self, word, seq):
        graph = self.build_agent(topic_understanding_teacher_prompt, topic_understanding_example, ListenSingleChoiceOutput)
        instance = graph.invoke(
            {"messages": [HumanMessage(content=f"Generate a JLPT question regrading Topic: {word}")]},
            config={"configurable": {"thread_id": "1"}}
        )
        obj = instance['formatted_output']
        obj['audio'] = _generate_dialogue(content=obj, type="topic_understanding", seq=seq)
        return obj

    def keypoint_understanding(self, word, seq):
        graph = self.build_agent(keypoint_understanding_teacher_prompt, keypoint_understanding_example, ListenSingleChoiceOutput)
        instance = graph.invoke(
            {"messages": [HumanMessage(content=f"Generate a JLPT question regrading Topic: {word}")]},
            config={"configurable": {"thread_id": "1"}}
        )
        obj = instance['formatted_output']
        obj['audio'] = _generate_dialogue(content=obj, type="keypoint_understanding", seq=seq)
        return obj

    def summary_understanding(self, word, seq):
        graph = self.build_agent(summary_understanding_teacher_prompt, summary_understanding_example, ListenSingleChoiceOutput)
        instance = graph.invoke(
            {"messages": [HumanMessage(content=f"Generate a JLPT question regrading Topic: {word}")]},
            config={"configurable": {"thread_id": "1"}}
        )
        obj = instance['formatted_output']
        obj['audio'] = _generate_dialogue(content=obj, type="summary_understanding", seq=seq)
        return obj

    def active_expression(self, word, seq):
        graph = self.build_agent(actively_expression_teacher_prompt, actively_expression_example, ImageListenQuestionOutput)
        instance = graph.invoke(
            {"messages": [HumanMessage(content=f"Generate a JLPT question regrading Topic: {word}")]},
            config={"configurable": {"thread_id": "1"}}
        )
        obj = instance['formatted_output']
        obj['audio'] = _generate_express(content=obj, type="active_expression", seq=seq)
        obj['image'] = _generate_image(obj['background'])
        return obj

    def immediate_ack(self, word, seq):
        graph = self.build_agent(immediate_ack_teacher_prompt, immediate_ack_example, ListenImmediateQuestionOutput)
        instance = graph.invoke(
            {"messages": [HumanMessage(content=f"Generate a JLPT question regrading Topic: {word}")]},
            config={"configurable": {"thread_id": "1"}}
        )
        obj = instance['formatted_output']
        obj['audio'] = _generate_express(content=obj, type="immediate_ack", seq=seq)
        return obj

if __name__ == "__main__":
    n3_vocab = collect_vocabulary("../../Vocab/n3.csv")
    with open("../../Vocab/topics.txt", "r", encoding="utf-8") as file:
        topics_list = [line.strip() for line in file]
    random_word = random.choice(n3_vocab.split(","))
    random_topic = random.choice(topics_list)
    # ra

    # Kanji Reading
    # handler = ExamTaskHandler()
    # print(handler.kanji_reading(random_word))
    
    # # Write Chinese Task
    # handler = ExamTaskHandler()
    # print(handler.write_kanji(random_word))

    # # Word Meaning Task
    # handler = ExamTaskHandler()
    # print(handler.word_meaning(random_word))
    #
    # # Synonym Substitution Task
    # handler = ExamTaskHandler()
    # print(handler.synonym_substitution(random_word))
    #
    # Word Usage Task
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
    # Sentence Structure Task
    # handler = ExamTaskHandler()
    # print(handler.sentence_structure(random_topic))

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
    # Immediate Ack Task
    handler = ExamTaskHandler()
    print(handler.immediate_ack(random_word))