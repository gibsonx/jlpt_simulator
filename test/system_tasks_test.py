from graphs.common.ExamTaskRunner import ExamTaskRunner
import unittest
class TestExamTaskRunner(unittest.TestCase):
    def test_fast_exam(self):
        runner = ExamTaskRunner(level="N3", exam_type="fast_exam")
        inserted_id, outline, exam_paper = runner.run()

        self.assertIsNotNone(outline, "N3 Outline should be generated")
        if inserted_id:
            self.assertIsNotNone(exam_paper, "N3 Exam paper should exist if stored")
        else:
            self.assertIsNone(exam_paper, "N3 Exam paper must be None if not stored")

    def test_grammar_exam(self):
        runner = ExamTaskRunner(level="N2", exam_type="grammar")
        inserted_id, outline, exam_paper = runner.run()

        self.assertIsNotNone(outline, "N2 Outline should be generated")
        if inserted_id:
            self.assertIsNotNone(exam_paper, "N2 Exam paper should exist if stored")
        else:
            self.assertIsNone(exam_paper, "N2 Exam paper must be None if not stored")

    def test_vocab_exam(self):
        runner = ExamTaskRunner(level="N1", exam_type="vocab")
        inserted_id, outline, exam_paper = runner.run()

        self.assertIsNotNone(outline, "N1 Outline should be generated")
        if inserted_id:
            self.assertIsNotNone(exam_paper, "N1 Exam paper should exist if stored")
        else:
            self.assertIsNone(exam_paper, "N1 Exam paper must be None if not stored")

    def test_reading_exam(self):
        runner = ExamTaskRunner(level="n4", exam_type="reading")
        inserted_id, outline, exam_paper = runner.run()

        self.assertIsNotNone(outline, "N4 Outline should be generated")
        if inserted_id:
            self.assertIsNotNone(exam_paper, "N4 Exam paper should exist if stored")
        else:
            self.assertIsNone(exam_paper, "N4 Exam paper must be None if not stored")

    def test_listening_exam(self):
        runner = ExamTaskRunner(level="N5", exam_type="listening")
        inserted_id, outline, exam_paper = runner.run()

        self.assertIsNotNone(outline, "N5 Outline should be generated")
        if inserted_id:
            self.assertIsNotNone(exam_paper, "N5 Exam paper should exist if stored")
        else:
            self.assertIsNone(exam_paper, "N5 Exam paper must be None if not stored")


#
# if __name__ == "__main__":
#     unittest.main()