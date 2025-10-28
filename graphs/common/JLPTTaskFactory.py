from graphs.common.GraphBuilder import *
from libs.Utils import _generate_dialogue,_generate_express,_generate_image, _generate_comic_strip
from graphs.common.Schema import *
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

    def _run_task(self, prompt, example, reflection_prompt, output_cls, word, grammar=None):
        """Generic task runner."""
        if grammar:
            graph = self.graph.build_agent(prompt, example, reflection_prompt, output_cls, grammar)
        else:
            graph = self.graph.build_agent(prompt, example, reflection_prompt, output_cls)

        instance = graph.invoke(
            {"messages": [HumanMessage(content=f"Generate a JLPT question regarding Topic: {word}")]},
            config={"configurable": {"thread_id": "1"}}
        )
        return instance["formatted_output"]

    # =====================
    # Vocabulary Tasks
    # =====================

    def kanji_reading(self, word):
        return self._run_task(
            self.prompts_module.kanji_reading_teacher_prompt,
            self.prompts_module.kanji_reading_example,
            self.prompts_module.kanji_reading_reflection_prompt,
            SimpleChoiceQuestionOutput,
            word
        )

    def write_kanji(self, word):
        return self._run_task(
            self.prompts_module.write_kanji_teacher_prompt,
            self.prompts_module.write_kanji_example,
            self.prompts_module.write_kanji_reflection_prompt,
            SimpleChoiceQuestionOutput,
            word
        )

    def word_meaning(self, word):
        return self._run_task(
            self.prompts_module.word_meaning_teacher_prompt,
            self.prompts_module.word_meaning_example,
            self.prompts_module.word_meaning_reflection_prompt,
            SimpleChoiceQuestionOutput,
            word
        )

    def synonym_substitution(self, word):
        return self._run_task(
            self.prompts_module.synonym_substitution_teacher_prompt,
            self.prompts_module.synonym_substitution_example,
            self.prompts_module.synonym_substitution_reflection_prompt,
            SimpleChoiceQuestionOutput,
            word
        )

    def word_usage(self, word):
        return self._run_task(
            self.prompts_module.word_usage_teacher_prompt,
            self.prompts_module.word_usage_example,
            self.prompts_module.word_usage_reflection_prompt,
            SimpleChoiceQuestionOutput,
            word
        )

    def words_collocation(self, word):
        return self._run_task(
            self.prompts_module.words_collocation_teacher_prompt,
            self.prompts_module.words_collocation_example,
            self.prompts_module.words_collocation_reflection_prompt,
            SimpleChoiceQuestionOutput,
            word
        )

    # =====================
    # Sentence Structure Tasks
    # =====================

    def sentence_grammar(self, word, grammar):
        return self._run_task(
            self.prompts_module.sentence_grammar_teacher_prompt,
            self.prompts_module.sentence_grammar_example,
            self.prompts_module.sentence_grammar_reflection_prompt,
            SimpleChoiceQuestionOutput,
            word, grammar
        )

    def sentence_sort(self, word, grammar):
        return self._run_task(
            self.prompts_module.sentence_sort_teacher_prompt,
            self.prompts_module.sentence_sort_example,
            self.prompts_module.sentence_sort_reflection_prompt,
            SimpleChoiceQuestionOutput,
            word, grammar
        )

    def sentence_structure(self, word, grammar):
        return self._run_task(
            self.prompts_module.structure_selection_teacher_prompt,
            self.prompts_module.structure_selection_example,
            self.prompts_module.structure_selection_reflection_prompt,
            MultipleQuestionOutput,
            word, grammar
        )

    # =====================
    # Reading Tasks
    # =====================

    def short_passage_narrative_read(self, word):
        return self._run_task(
            self.prompts_module.short_reading_narrative_teacher_prompt,
            self.prompts_module.short_reading_narrative_example,
            self.prompts_module.short_reading_narrative_reflection_prompt,
            MultipleQuestionOutput,
            word
        )

    def short_passage_mail_read(self, word):
        return self._run_task(
            self.prompts_module.short_reading_mail_teacher_prompt,
            self.prompts_module.short_reading_mail_example,
            self.prompts_module.short_reading_mail_reflection_prompt,
            MultipleQuestionOutput,
            word
        )

    def short_passage_notification_read(self, word):
        return self._run_task(
            self.prompts_module.short_reading_notification_teacher_prompt,
            self.prompts_module.short_reading_notification_example,
            self.prompts_module.short_reading_notification_reflection_prompt,
            MultipleQuestionOutput,
            word
        )

    def midsize_passage_read(self, word):
        return self._run_task(
            self.prompts_module.midsize_reading_teacher_prompt,
            self.prompts_module.midsize_reading_example,
            self.prompts_module.midsize_reading_reflection_prompt,
            MultipleQuestionOutput,
            word
        )

    def comprehensive_read(self, word):
        return self._run_task(
            self.prompts_module.comprehensive_reading_teacher_prompt,
            self.prompts_module.comprehensive_reading_example,
            self.prompts_module.comprehensive_reading_reflection_prompt,
            MultipleQuestionOutput,
            word
        )

    def long_passage_read(self, word):
        return self._run_task(
            self.prompts_module.long_reading_teacher_prompt,
            self.prompts_module.long_reading_example,
            self.prompts_module.long_reading_reflection_prompt,
            MultipleQuestionOutput,
            word
        )

    def info_retrieval(self, word):
        return self._run_task(
            self.prompts_module.information_retrieval_teacher_prompt,
            self.prompts_module.information_retrieval_example,
            self.prompts_module.information_retrieval_reflection_prompt,
            MultipleQuestionOutput,
            word
        )

    # =====================
    # Listening Tasks
    # =====================

    def topic_understanding_img(self, word, seq: int):
        obj = self._run_task(
            self.prompts_module.topic_understanding_img_teacher_prompt,
            self.prompts_module.topic_understanding_img_example,
            self.prompts_module.topic_understanding_img_reflection_prompt,
            ListenSingleChoiceOutput,
            word
        )
        obj["audio"] = _generate_dialogue(content=obj, type="topic_understanding_img", seq=seq, uid=self.graph.exam_uid)

        # Retry logic for image generation
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                obj["image"] = _generate_comic_strip(",".join(obj["choices"]))
                break
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt == max_attempts - 1:
                    raise
                import time
                time.sleep(5)
        return obj

    def topic_understanding_txt(self, word, seq: int):
        obj = self._run_task(
            self.prompts_module.topic_understanding_txt_teacher_prompt,
            self.prompts_module.topic_understanding_txt_example,
            self.prompts_module.topic_understanding_txt_reflection_prompt,
            ListenSingleChoiceOutput,
            word
        )
        obj["audio"] = _generate_dialogue(content=obj, type="topic_understanding_txt", seq=seq, uid=self.graph.exam_uid)
        return obj

    def keypoint_understanding(self, word, seq: int):
        obj = self._run_task(
            self.prompts_module.keypoint_understanding_teacher_prompt,
            self.prompts_module.keypoint_understanding_example,
            self.prompts_module.keypoint_understanding_reflection_prompt,
            ListenSingleChoiceOutput,
            word
        )
        obj["audio"] = _generate_dialogue(content=obj, type="keypoint_understanding", seq=seq, uid=self.graph.exam_uid)

        return obj

    def summary_understanding(self, word, seq: int):
        obj = self._run_task(
            self.prompts_module.summary_understanding_teacher_prompt,
            self.prompts_module.summary_understanding_example,
            self.prompts_module.summary_understanding_reflection_prompt,
            ListenSingleChoiceOutput,
            word
        )
        obj["audio"] = _generate_dialogue(content=obj, type="summary_understanding", seq=seq, uid=self.graph.exam_uid)
        return obj

    def active_expression(self, word, seq: int):
        obj = self._run_task(
            self.prompts_module.actively_expression_teacher_prompt,
            self.prompts_module.actively_expression_example,
            self.prompts_module.actively_expression_reflection_prompt,
            ImageListenQuestionOutput,
            word
        )
        obj["audio"] = _generate_express(content=obj, type="active_expression", seq=seq, uid=self.graph.exam_uid)

        # Retry logic for image generation
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                obj["image"] = _generate_image(obj["background"])
                break
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt == max_attempts - 1:
                    raise
                import time
                time.sleep(5)
        return obj

    def immediate_ack(self, word, seq: int):
        obj = self._run_task(
            self.prompts_module.immediate_ack_teacher_prompt,
            self.prompts_module.immediate_ack_example,
            self.prompts_module.immediate_ack_reflection_prompt,
            ListenImmediateQuestionOutput,
            word
        )
        obj["audio"] = _generate_express(content=obj, type="immediate_ack", seq=seq, uid=self.graph.exam_uid)
        return obj

    def comprehensive_expression_show_answer(self, word, seq: int):
        """
        specific for N2
        :param word:
        :param seq:
        :return:
        """
        obj = self._run_task(
            self.prompts_module.comprehensive_expression_show_answer_teacher_prompt,
            self.prompts_module.comprehensive_expression_show_answer_example,
            self.prompts_module.comprehensive_expression_show_answer_reflection_prompt,
            ImageListenQuestionOutput,
            word
        )
        obj["audio"] = _generate_dialogue(content=obj, type="comprehensive_expression_show_answer", seq=seq, uid=self.graph.exam_uid)
        return obj


    def comprehensive_expression_listen_answer(self, word, seq: int):
        """
        specific for N2
        :param word:
        :param seq:
        :return:
        """
        obj = self._run_task(
            self.prompts_module.comprehensive_expression_listen_answer_teacher_prompt,
            self.prompts_module.comprehensive_expression_listen_answer_example,
            self.prompts_module.comprehensive_expression_listen_answer_reflection_prompt,
            ImageListenQuestionOutput,
            word
        )
        obj["audio"] = _generate_dialogue(content=obj, type="comprehensive_expression_listen_answer", seq=seq, uid=self.graph.exam_uid)
        return obj