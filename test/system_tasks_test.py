from graphs.common.TaskRunner import TaskRunner
import unittest
class TestTaskRunner(unittest.TestCase):
    def test_fast_exam(self):
        runner = TaskRunner(level="N3", exam_type="fast_exam")
        inserted_id, outline, exam_paper = runner.run()

        self.assertIsNotNone(outline, "N3 Outline should be generated")
        if inserted_id:
            self.assertIsNotNone(exam_paper, "N3 Exam paper should exist if stored")
        else:
            self.assertIsNone(exam_paper, "N3 Exam paper must be None if not stored")

    def test_grammar_exam(self):
        runner = TaskRunner(level="N3", exam_type="grammar")
        inserted_id, outline, exam_paper = runner.run()

        self.assertIsNotNone(outline, "N3 Outline should be generated")
        if inserted_id:
            self.assertIsNotNone(exam_paper, "N3 Exam paper should exist if stored")
        else:
            self.assertIsNone(exam_paper, "N3 Exam paper must be None if not stored")

    def test_vocab_exam(self):
        runner = TaskRunner(level="N3", exam_type="vocab")
        inserted_id, outline, exam_paper = runner.run()

        self.assertIsNotNone(outline, "N3 Outline should be generated")
        if inserted_id:
            self.assertIsNotNone(exam_paper, "N3 Exam paper should exist if stored")
        else:
            self.assertIsNone(exam_paper, "N3 Exam paper must be None if not stored")

    def test_reading_exam(self):
        runner = TaskRunner(level="n1", exam_type="reading")
        inserted_id, outline, exam_paper = runner.run()

        self.assertIsNotNone(outline, "N3 Outline should be generated")
        if inserted_id:
            self.assertIsNotNone(exam_paper, "N3 Exam paper should exist if stored")
        else:
            self.assertIsNone(exam_paper, "N3 Exam paper must be None if not stored")

    def test_listening_exam(self):
        runner = TaskRunner(level="N3", exam_type="listening")
        inserted_id, outline, exam_paper = runner.run()

        self.assertIsNotNone(outline, "N3 Outline should be generated")
        if inserted_id:
            self.assertIsNotNone(exam_paper, "N3 Exam paper should exist if stored")
        else:
            self.assertIsNone(exam_paper, "N3 Exam paper must be None if not stored")


#
# if __name__ == "__main__":
#     unittest.main()