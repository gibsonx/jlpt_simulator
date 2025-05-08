from graphs.common.node_builder import *
from graphs.common.utils import *
from graphs.common.state import *
from libs.LLMs import azure_llm
import random
from prompts import *
from langgraph.graph import StateGraph

load_dotenv()

class ExamTaskHandler:
    def __init__(self, vocab):
        self.vocab = vocab
        self.online_search = online_search_node_builder()
        self.llm = azure_llm
        self.nodes = {
            "online_search": self.online_search,
            "generator": None,
            "reflector": None,
            "formatter": None
        }
        self.builder = StateGraph(SimpleQuestionState)
        self.graph = None

    def build_graph(self, prompt_text, example, OutType):
        self.nodes["generator"] = generation_node_builder(
            vocab_dict=self.vocab,
            llm=self.llm,
            prompt_text=prompt_text,
            example=example
        )
        self.nodes["reflector"] = reflection_node_builder(llm=self.llm)
        self.nodes["formatter"] = formatter_node_builder(llm=self.llm, OutType=OutType)
        self.graph = build_graph(self.builder, self.nodes)

    def invoke(self, word):
        instance = self.graph.invoke(
            {"messages": [HumanMessage(content=word)]},
            config={"configurable": {"thread_id": "1"}}
        )
        return json.dumps(instance['formatted_output'], indent=4, ensure_ascii=False)

    def kanji_reading(self, word):
        self.build_graph(kanji_reading_teacher_prompt, kanji_reading_example, SimpleChoiceQuestionOutput)
        return self.invoke(word)

    def write_chinese(self, word):
        self.build_graph(write_chinese_teacher_prompt, write_chinese_example, SimpleChoiceQuestionOutput)
        return self.invoke(word)

    def word_meaning(self, word):
        self.build_graph(word_meaning_teacher_prompt, word_meaning_example, SimpleChoiceQuestionOutput)
        return self.invoke(word)

    def synonym_substitution(self, word):
        self.build_graph(synonym_substitution_teacher_prompt, synonym_substitution_example, SimpleChoiceQuestionOutput)
        return self.invoke(word)

    def word_usage(self, word):
        self.build_graph(word_usage_teacher_prompt, word_usage_example, SimpleChoiceQuestionOutput)
        return self.invoke(word)

    def sentence_grammar(self, word):
        self.build_graph(sentence_grammar_teacher_prompt, sentence_grammar_example, SimpleChoiceQuestionOutput)
        return self.invoke(word)

    def sentence_sort(self, word):
        self.build_graph(sentence_sort_teacher_prompt, sentence_sort_example, SimpleChoiceQuestionOutput)
        return self.invoke(word)

    def sentence_structure(self, word):
        self.build_graph(structure_selection_teacher_prompt, structure_selection_example, MultipleQuestionOutput)
        return self.invoke(word)

    def short_passage_read(self, word):
        self.build_graph(short_reading_teacher_prompt, short_reading_example, SimpleChoiceQuestionOutput)
        return self.invoke(word)

    def midsize_passage_read(self, word):
        self.build_graph(midsize_reading_teacher_prompt, midsize_reading_example, SimpleChoiceQuestionOutput)
        return self.invoke(word)

    def long_passage_read(self, word):
        self.build_graph(long_reading_teacher_prompt, long_reading_example, MultipleQuestionOutput)
        return self.invoke(word)

    def info_retrieval(self, word):
        self.build_graph(information_retrieval_teacher_prompt, information_retrieval_example, MultipleQuestionOutput)
        return self.invoke(word)

    def topic_understanding(self, word):
        self.build_graph(topic_understanding_teacher_prompt, topic_understanding_example, ListenSingleChoiceOutput)
        return self.invoke(word)

    def keypoint_understanding(self, word):
        self.build_graph(keypoint_understanding_teacher_prompt, keypoint_understanding_example, ListenSingleChoiceOutput)
        return self.invoke(word)

    def summary_understanding(self, word):
        self.build_graph(summary_understanding_teacher_prompt, summary_understanding_example, ListenSingleChoiceOutput)
        return self.invoke(word)

    def active_expression(self, word):
        self.build_graph(actively_expression_teacher_prompt, actively_expression_example, ImageListenQuestionOutput)
        return self.invoke(word)

    def immediate_ack(self, word):
        self.build_graph(immediate_ack_teacher_prompt, immediate_ack_example, ListenOpenQuestionOutput)
        return self.invoke(word)

if __name__ == "__main__":
    n3_vocab = collect_vocabulary("../../Vocab/n3.csv")

    random_word = random.choice(list(json.loads(n3_vocab).values()))

    # Kanji Reading
    handler = ExamTaskHandler(vocab=n3_vocab)
    print(handler.kanji_reading(random_word))

    # Write Chinese Task
    handler = ExamTaskHandler(vocab=n3_vocab)
    print(handler.write_chinese(random_word))

    # Word Meaning Task
    handler = ExamTaskHandler(vocab=n3_vocab)
    print(handler.word_meaning(random_word))

    # Synonym Substitution Task
    handler = ExamTaskHandler(vocab=n3_vocab)
    print(handler.synonym_substitution(random_word))

    # Word Usage Task
    handler = ExamTaskHandler(vocab=n3_vocab)
    print(handler.word_usage(random_word))

    # Sentence Grammar Task
    handler = ExamTaskHandler(vocab=n3_vocab)
    print(handler.sentence_grammar(random_word))

    # Sentence Sort Task
    handler = ExamTaskHandler(vocab=n3_vocab)
    print(handler.sentence_sort(random_word))

    # Sentence Structure Task
    handler = ExamTaskHandler(vocab=n3_vocab)
    print(handler.sentence_structure(random_word))

    # Short Passage Read Task
    handler = ExamTaskHandler(vocab=n3_vocab)
    print(handler.short_passage_read(random_word))

    # Midsize Passage Read Task
    handler = ExamTaskHandler(vocab=n3_vocab)
    print(handler.midsize_passage_read(random_word))

    # Long Passage Read Task
    handler = ExamTaskHandler(vocab=n3_vocab)
    print(handler.long_passage_read(random_word))

    # Info Retrieval Task
    handler = ExamTaskHandler(vocab=n3_vocab)
    print(handler.info_retrieval(random_word))

    # Topic Understanding Task
    handler = ExamTaskHandler(vocab=n3_vocab)
    print(handler.topic_understanding(random_word))

    # Keypoint Understanding Task
    handler = ExamTaskHandler(vocab=n3_vocab)
    print(handler.keypoint_understanding(random_word))

    # Summary Understanding Task
    handler = ExamTaskHandler(vocab=n3_vocab)
    print(handler.summary_understanding(random_word))

    # Active Expression Task
    handler = ExamTaskHandler(vocab=n3_vocab)
    print(handler.active_expression(random_word))

    # Immediate Ack Task
    handler = ExamTaskHandler(vocab=n3_vocab)
    print(handler.immediate_ack(random_word))