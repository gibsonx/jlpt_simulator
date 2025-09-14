from graphs.common.GraphBuilder import *
from libs.Utils import _generate_dialogue,_generate_express,_generate_image,collect_vocabulary
from graphs.common.State import *
load_dotenv()

class JLPTTaskFactory:
    """
    Factory for generating JLPT exam tasks.
    Each task method builds the agent, invokes the graph, and returns the formatted output.
    """

    def __init__(self, graph, level):
        """
        :param graph: ExamTaskgraph instance
        :param level: JLPT level (e.g., "n5", "n4", "n3", "n2", "n1")
        """
        self.graph = graph
        self.level = level
        self.prompts_module = self._import_prompts(level)

    def _import_prompts(self, level: str):
        """Dynamically import prompt set for the given level (n5–n1)."""
        import importlib
        return importlib.import_module(f"graphs.{level}.prompts")

    def _run_task(self, prompt, example, output_cls, word, grammar=None):
        """Generic task runner."""
        if grammar:
            graph = self.graph.build_agent(prompt, example, output_cls, grammar)
        else:
            graph = self.graph.build_agent(prompt, example, output_cls)

        instance = graph.invoke(
            {"messages": [HumanMessage(content=f"Generate a JLPT question regarding Topic: {word}")]},
            config={"configurable": {"thread_id": "1"}}
        )
        return instance["formatted_output"]

    # =====================
    # Core Task Wrappers
    # =====================

    # =====================
    # Basic Task Wrappers
    # =====================

    def kanji_reading(self, word):
        return self._run_task(self.prompts_module.kanji_reading_teacher_prompt,
                              self.prompts_module.kanji_reading_example,
                              SimpleChoiceQuestionOutput, word)

    def write_kanji(self, word):
        return self._run_task(self.prompts_module.write_kanji_teacher_prompt,
                              self.prompts_module.write_kanji_example,
                              SimpleChoiceQuestionOutput, word)

    def word_meaning(self, word):
        return self._run_task(self.prompts_module.word_meaning_teacher_prompt,
                              self.prompts_module.word_meaning_example,
                              SimpleChoiceQuestionOutput, word)

    def synonym_substitution(self, word):
        return self._run_task(self.prompts_module.synonym_substitution_teacher_prompt,
                              self.prompts_module.synonym_substitution_example,
                              SimpleChoiceQuestionOutput, word)

    def word_usage(self, word):
        return self._run_task(self.prompts_module.word_usage_teacher_prompt,
                              self.prompts_module.word_usage_example,
                              SimpleChoiceQuestionOutput, word)

    def sentence_grammar(self, word, grammar):
        return self._run_task(self.prompts_module.sentence_grammar_teacher_prompt,
                              self.prompts_module.sentence_grammar_example,
                              SimpleChoiceQuestionOutput, word, grammar)

    def sentence_sort(self, word, grammar):
        return self._run_task(self.prompts_module.sentence_sort_teacher_prompt,
                              self.prompts_module.sentence_sort_example,
                              SimpleChoiceQuestionOutput, word, grammar)

    def sentence_structure(self, word, grammar):
        return self._run_task(self.prompts_module.structure_selection_teacher_prompt,
                              self.prompts_module.structure_selection_example,
                              MultipleQuestionOutput, word, grammar)

    # =====================
    # Reading Tasks
    # =====================

    def short_passage_narrative_read(self, word):
        return self._run_task(self.prompts_module.short_reading_narrative_teacher_prompt,
                              self.prompts_module.short_reading_narrative_example,
                              MultipleQuestionOutput, word)

    def short_passage_mail_read(self, word):
        return self._run_task(self.prompts_module.short_reading_mail_teacher_prompt,
                              self.prompts_module.short_reading_mail_example,
                              MultipleQuestionOutput, word)

    def short_passage_notification_read(self, word):
        return self._run_task(self.prompts_module.short_reading_notification_teacher_prompt,
                              self.prompts_module.short_reading_notification_example,
                              MultipleQuestionOutput, word)

    def midsize_passage_read(self, word):
        return self._run_task(self.prompts_module.midsize_reading_teacher_prompt,
                              self.prompts_module.midsize_reading_example,
                              MultipleQuestionOutput, word)

    def long_passage_read(self, word):
        return self._run_task(self.prompts_module.long_reading_teacher_prompt,
                              self.prompts_module.long_reading_example,
                              MultipleQuestionOutput, word)

    def info_retrieval(self, word):
        return self._run_task(self.prompts_module.information_retrieval_teacher_prompt,
                              self.prompts_module.information_retrieval_example,
                              MultipleQuestionOutput, word)

    # =====================
    # Listening Tasks
    # =====================

    def topic_understanding(self, word, seq: int):
        obj = self._run_task(self.prompts_module.topic_understanding_teacher_prompt,
                             self.prompts_module.topic_understanding_example,
                             ListenSingleChoiceOutput, word)
        obj["audio"] = _generate_dialogue(content=obj, type="topic_understanding", seq=seq, uid=self.graph.exam_uid)
        return obj

    def keypoint_understanding(self, word, seq: int):
        obj = self._run_task(self.prompts_module.keypoint_understanding_teacher_prompt,
                             self.prompts_module.keypoint_understanding_example,
                             ListenSingleChoiceOutput, word)
        obj["audio"] = _generate_dialogue(content=obj, type="keypoint_understanding", seq=seq,
                                          uid=self.graph.exam_uid)
        return obj

    def summary_understanding(self, word, seq: int):
        obj = self._run_task(self.prompts_module.summary_understanding_teacher_prompt,
                             self.prompts_module.summary_understanding_example,
                             ListenSingleChoiceOutput, word)
        obj["audio"] = _generate_dialogue(content=obj, type="summary_understanding", seq=seq, uid=self.graph.exam_uid)
        return obj

    def active_expression(self, word, seq: int):
        obj = self._run_task(self.prompts_module.actively_expression_teacher_prompt,
                             self.prompts_module.actively_expression_example,
                             ImageListenQuestionOutput, word)
        obj["audio"] = _generate_express(content=obj, type="active_expression", seq=seq, uid=self.graph.exam_uid)
        obj["image"] = _generate_image(obj["background"])
        return obj

    def immediate_ack(self, word, seq: int):
        obj = self._run_task(self.prompts_module.immediate_ack_teacher_prompt,
                             self.prompts_module.immediate_ack_example,
                             ListenImmediateQuestionOutput, word)
        obj["audio"] = _generate_express(content=obj, type="immediate_ack", seq=seq, uid=self.graph.exam_uid)
        return obj