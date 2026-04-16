from graphs.common.GraphBuilder import *
from libs.Utils import _generate_dialogue,_generate_express,_generate_multi_dialogue, _generate_image, _generate_comic_strip
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

    def _run_task(self, prompt, example, reflection_prompt, output_cls, word, q_seq, gan_history: Optional[str] = "", grammar: Optional[str] = None ):
        """Generic task runner."""
        if grammar:
            graph = self.graph.build_agent(
                prompt_text=prompt,
                example=example,
                reflection_prompt=reflection_prompt,
                output_cls=output_cls,
                q_seq=q_seq,
                gan_history=gan_history,
                grammar=grammar
            )
        else:
            graph = self.graph.build_agent(
                prompt_text=prompt,
                example=example,
                reflection_prompt=reflection_prompt,
                output_cls=output_cls,
                q_seq=q_seq,
                gan_history=gan_history
            )

        instance = graph.invoke(
            {"messages": [HumanMessage(content=f"Generate a JLPT question regarding Topic: {word}")]},
            config={"configurable": {"thread_id": "1"}}
        )
        return instance["formatted_output"]

    # =====================
    # Vocabulary Tasks
    # =====================
    def kanji_reading(self, word, q_seq = "4", gan_history: Optional[str] = ""):
        return self._run_task(
            prompt=self.prompts_module.kanji_reading_teacher_prompt,
            example=self.prompts_module.kanji_reading_example,
            reflection_prompt=self.prompts_module.kanji_reading_reflection_prompt,
            output_cls=SimpleChoiceQuestionOutput,
            word=word,
            q_seq=q_seq,
            gan_history=gan_history
        )

    def write_kanji(self, word, q_seq = "4", gan_history: Optional[str] = ""):
        return self._run_task(
            self.prompts_module.write_kanji_teacher_prompt,
            self.prompts_module.write_kanji_example,
            self.prompts_module.write_kanji_reflection_prompt,
            SimpleChoiceQuestionOutput,
            q_seq,
            word,
            gan_history
        )

    def word_meaning(self, word, q_seq = "4", gan_history: Optional[str] = ""):
        return self._run_task(
            self.prompts_module.word_meaning_teacher_prompt,
            self.prompts_module.word_meaning_example,
            self.prompts_module.word_meaning_reflection_prompt,
            SimpleChoiceQuestionOutput,
            word,
            q_seq,
            gan_history
        )

    def synonym_substitution(self, word, q_seq = "4", gan_history: Optional[str] = "",):
        return self._run_task(
            self.prompts_module.synonym_substitution_teacher_prompt,
            self.prompts_module.synonym_substitution_example,
            self.prompts_module.synonym_substitution_reflection_prompt,
            SimpleChoiceQuestionOutput,
            word,
            q_seq,
            gan_history
        )

    def word_usage(self, word, q_seq = "4", gan_history: Optional[str] = "",):
        return self._run_task(
            self.prompts_module.word_usage_teacher_prompt,
            self.prompts_module.word_usage_example,
            self.prompts_module.word_usage_reflection_prompt,
            SimpleChoiceQuestionOutput,
            word,
            q_seq,
            gan_history
        )

    def words_collocation(self, word, q_seq = "4", gan_history: Optional[str] = "",):
        return self._run_task(
            self.prompts_module.words_collocation_teacher_prompt,
            self.prompts_module.words_collocation_example,
            self.prompts_module.words_collocation_reflection_prompt,
            SimpleChoiceQuestionOutput,
            q_seq,
            word,
            gan_history
        )

    # =====================
    # Sentence Structure Tasks
    # =====================

    def sentence_grammar(self, word, q_seq = "4", gan_history: Optional[str] = "", grammar: Optional[str] = None):
        return self._run_task(
            self.prompts_module.sentence_grammar_teacher_prompt,
            self.prompts_module.sentence_grammar_example,
            self.prompts_module.sentence_grammar_reflection_prompt,
            SimpleChoiceQuestionOutput,
            word,
            q_seq,
            gan_history,
            grammar
        )

    def sentence_sort(self, word, q_seq = "4", gan_history: Optional[str] = "", grammar: Optional[str] = None):
        return self._run_task(
            self.prompts_module.sentence_sort_teacher_prompt,
            self.prompts_module.sentence_sort_example,
            self.prompts_module.sentence_sort_reflection_prompt,
            SimpleChoiceQuestionOutput,
            word,
            q_seq,
            gan_history,
            grammar
        )

    def sentence_structure(self, word, q_seq = "4,1,2,3,3", gan_history: Optional[str] = "", grammar: Optional[str] = None):
        return self._run_task(
            self.prompts_module.sentence_structure_teacher_prompt,
            self.prompts_module.sentence_structure_example,
            self.prompts_module.sentence_structure_reflection_prompt,
            MultipleQuestionOutput,
            word,
            q_seq,
            gan_history,
            grammar
        )

    # =====================
    # Reading Tasks
    # =====================

    def short_passage_narrative_read(self, word, q_seq = "4", gan_history: Optional[str] = "",):
        return self._run_task(
            self.prompts_module.short_passage_narrative_read_teacher_prompt,
            self.prompts_module.short_passage_narrative_read_example,
            self.prompts_module.short_passage_narrative_read_reflection_prompt,
            MultipleQuestionOutput,
            word,
            q_seq,
            gan_history
        )

    def short_passage_mail_read(self, word, q_seq = "4", gan_history: Optional[str] = "",):
        return self._run_task(
            self.prompts_module.short_passage_mail_read_teacher_prompt,
            self.prompts_module.short_passage_mail_read_example,
            self.prompts_module.short_passage_mail_read_reflection_prompt,
            MultipleQuestionOutput,
            q_seq,
            word,
            gan_history
        )

    def short_passage_notification_read(self, word, q_seq = "4", gan_history: Optional[str] = "",):
        return self._run_task(
            self.prompts_module.short_passage_notification_read_teacher_prompt,
            self.prompts_module.short_passage_notification_read_example,
            self.prompts_module.short_passage_notification_read_reflection_prompt,
            MultipleQuestionOutput,
            q_seq,
            word,
            gan_history
        )

    def midsize_passage_read(self, word, q_seq = "3,1,2", gan_history: Optional[str] = "",):
        return self._run_task(
            self.prompts_module.midsize_passage_read_teacher_prompt,
            self.prompts_module.midsize_passage_read_example,
            self.prompts_module.midsize_passage_read_reflection_prompt,
            MultipleQuestionOutput,
            word,
            q_seq,
            gan_history
        )

    def comprehensive_read(self, word, q_seq = "4,1", gan_history: Optional[str] = "",):
        return self._run_task(
            self.prompts_module.comprehensive_read_teacher_prompt,
            self.prompts_module.comprehensive_read_example,
            self.prompts_module.comprehensive_read_reflection_prompt,
            MultipleQuestionOutput,
            word,
            q_seq,
            gan_history
        )

    def long_passage_read(self, word, q_seq = "4,1,2,2", gan_history: Optional[str] = ""):
        return self._run_task(
            self.prompts_module.long_passage_read_teacher_prompt,
            self.prompts_module.long_passage_read_example,
            self.prompts_module.long_passage_read_reflection_prompt,
            MultipleQuestionOutput,
            word,
            q_seq,
            gan_history
        )

    def understanding_read(self, word, q_seq = "3,4,1", gan_history: Optional[str] = ""):
        return self._run_task(
            self.prompts_module.understanding_read_teacher_prompt,
            self.prompts_module.understanding_read_example,
            self.prompts_module.understanding_read_reflection_prompt,
            MultipleQuestionOutput,
            word,
            q_seq,
            gan_history
        )

    def info_retrieval(self, word, q_seq = "3,2", gan_history: Optional[str] = ""):
        return self._run_task(
            self.prompts_module.info_retrieval_teacher_prompt,
            self.prompts_module.info_retrieval_example,
            self.prompts_module.info_retrieval_reflection_prompt,
            MultipleQuestionOutput,
            word,
            q_seq,
            gan_history
        )

    # =====================
    # Listening Tasks
    # =====================

    def topic_understanding_img(self, word, q_seq =  "4", gan_history: Optional[str] = "", seq: int = 1):
        obj = self._run_task(
            self.prompts_module.topic_understanding_img_teacher_prompt,
            self.prompts_module.topic_understanding_img_example,
            self.prompts_module.topic_understanding_img_reflection_prompt,
            ListenSingleChoiceOutput,
            word,
            q_seq,
            gan_history,
        )
        obj["audio"] = _generate_dialogue(content=obj, type="topic_understanding_img", seq=seq, uid=self.graph.exam_uid)

        # Retry logic for image generation
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                obj["image"] = _generate_comic_strip(obj)
                break
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt == max_attempts - 1:
                    raise
                import time
                time.sleep(5)
        return obj

    def topic_understanding_txt(self, word, q_seq = "4", gan_history: Optional[str] = "", seq: int = 1):
        obj = self._run_task(
            self.prompts_module.topic_understanding_txt_teacher_prompt,
            self.prompts_module.topic_understanding_txt_example,
            self.prompts_module.topic_understanding_txt_reflection_prompt,
            ListenSingleChoiceOutput,
            word,
            q_seq,
            gan_history,
        )
        obj["audio"] = _generate_dialogue(content=obj, type="topic_understanding_txt", seq=seq, uid=self.graph.exam_uid)
        return obj

    def keypoint_understanding(self, word, q_seq = "4", gan_history: Optional[str] = "", seq: int = 1):
        obj = self._run_task(
            self.prompts_module.keypoint_understanding_teacher_prompt,
            self.prompts_module.keypoint_understanding_example,
            self.prompts_module.keypoint_understanding_reflection_prompt,
            ListenSingleChoiceOutput,
            word,
            q_seq,
            gan_history,
        )
        obj["audio"] = _generate_dialogue(content=obj, type="keypoint_understanding", seq=seq, uid=self.graph.exam_uid)

        return obj

    def summary_understanding(self, word, q_seq = "4",  gan_history: Optional[str] = "", seq: int = 1):
        obj = self._run_task(
            self.prompts_module.summary_understanding_teacher_prompt,
            self.prompts_module.summary_understanding_example,
            self.prompts_module.summary_understanding_reflection_prompt,
            ListenSingleChoiceOutput,
            word,
            q_seq,
            gan_history,
        )
        obj["audio"] = _generate_dialogue(content=obj, type="summary_understanding", seq=seq, uid=self.graph.exam_uid)
        return obj

    def active_expression(self, word, q_seq = "4", gan_history: Optional[str] = "", seq: int = 1):
        obj = self._run_task(
            self.prompts_module.actively_expression_teacher_prompt,
            self.prompts_module.actively_expression_example,
            self.prompts_module.actively_expression_reflection_prompt,
            ImageListenQuestionOutput,
            word,
            q_seq,
            gan_history,
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

    def immediate_ack(self, word, q_seq = "4", gan_history: Optional[str] = "", seq: int = 1):
        obj = self._run_task(
            self.prompts_module.immediate_ack_teacher_prompt,
            self.prompts_module.immediate_ack_example,
            self.prompts_module.immediate_ack_reflection_prompt,
            ListenImmediateQuestionOutput,
            word,
            q_seq,
            gan_history,
        )
        obj["audio"] = _generate_express(content=obj, type="immediate_ack", seq=seq, uid=self.graph.exam_uid)
        return obj

    def comprehensive_expression_listen_answer(self, word, q_seq = "4", gan_history: Optional[str] = "", seq: int = 1):
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
            ListenMultiPersonOutput,
            word,
            q_seq,
            gan_history,
        )
        obj["audio"] = _generate_multi_dialogue(content=obj, type="comprehensive_expression_listen_answer", seq=seq, uid=self.graph.exam_uid)
        return obj

    def comprehensive_expression_show_answer(self, word, q_seq = "4", gan_history: Optional[str] = "", seq: int = 1):
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
            ListenMultiPersonAndQuestionOutput,
            word,
            q_seq,
            gan_history,
        )
        obj["audio"] = _generate_multi_dialogue(content=obj, type="comprehensive_expression_show_answer", seq=seq, uid=self.graph.exam_uid)
        return obj