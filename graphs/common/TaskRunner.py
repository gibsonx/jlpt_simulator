from graphs.common.ExamGenerator import ExamGenerator
from typing import *
import importlib
from libs.Logger import logger
from graphs.common.Schema import ExamType

class TaskRunner:
    """
    Class-based handler for generating and storing exam outlines and papers.
    """

    def __init__(self, level: str, exam_type: ExamType, task_id: Optional[int] = None):
        self.task_id = task_id
        self.level = level.lower()
        self.exam_type = exam_type
        self.level_lower = level.lower()
        self.exam_type_lower = exam_type.lower()
        self.module_name = f"graphs.{self.level_lower}.outliner"
        self.level_module = self._import_level_module()

    def _import_level_module(self):
        try:
            module = importlib.import_module(self.module_name)
            logger.info("Module '%s' imported successfully.", self.module_name)
            return module
        except ModuleNotFoundError:
            logger.exception(
                "Module not found for level '%s'. Expected module: '%s'",
                self.level,
                self.module_name,
            )
            raise ValueError(
                f"No module found for level '{self.level}'. "
                f"Expected module: {self.module_name}"
            )

    def _get_prompt(self) -> Any:
        prompt_registry: dict[str, Optional[Any]] = {
            "full_exam": getattr(self.level_module, "full_exam_prompt", None),
            "fast_exam": getattr(self.level_module, "fast_exam_prompt", None),
            "reading": getattr(self.level_module, "reading_prompt", None),
            "listening": getattr(self.level_module, "listening_prompt", None),
            "grammar": getattr(self.level_module, "grammar_prompt", None),
            "vocab": getattr(self.level_module, "vocab_prompt", None),
        }

        prompt = prompt_registry.get(self.exam_type_lower)
        if not prompt:
            available = [k for k, v in prompt_registry.items() if v is not None]
            logger.error(
                "No prompt defined for exam_type '%s'. Available prompts: %s",
                self.exam_type,
                available,
            )
            raise ValueError(
                f"No prompt defined for exam_type '{self.exam_type}'. "
                f"Available: {available}"
            )
        return prompt

    def run(self) -> None:
        """
        Run exam generation pipeline.
        Returns:
            - (inserted_id, outline, exam_paper) if success.
            - (None, outline, None) if paper storage failed but outline was generated.
        """
        prompt = self._get_prompt()

        try:
            exam_generator = ExamGenerator(
                task_id=self.task_id,
                level=self.level,
                exam_type=self.exam_type,
                db_collection=f"{self.level_lower}_{self.exam_type_lower}",
            )
            outline = exam_generator._generate_outline(instruction=prompt)
        except Exception as e:
            logger.exception(
                "Failed to generate exam outline for level '%s' and exam_type '%s'",
                self.level,
                self.exam_type,
            )
            raise ValueError("Failed to generate exam outline. Check logs for details.") from e

        try:
            exam_paper = exam_generator._generate_and_store_paper(outline=outline)
        except Exception as e:
            logger.warning("Failed to store exam paper. Returning outline only. Error: %s", e)

        if exam_paper:
            logger.info("Exam outline stored successfully! Document ID: %s", self.task_id)
        else:
            logger.warning("Exam paper storage failed, but outline was generated successfully.")
