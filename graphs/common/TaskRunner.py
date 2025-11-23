from graphs.common.ExamGenerator import ExamGenerator
from typing import *
import os
import importlib
from libs.Utils import render_to_html
from libs.Logger import logger
from graphs.common.Schema import ExamType
from libs.CosmosMongoDB import CosmosMongoDB
import requests
import time
from dotenv import load_dotenv
load_dotenv()

class TaskRunner:
    """
    Class-based handler for generating and storing exam outlines and papers.
    """

    def __init__(self, level: str, exam_type: ExamType, task_id: Optional[str] = None):
        self.task_id = task_id
        self.level = level.lower()
        self.exam_type = exam_type
        self.level_lower = level.lower()
        self.exam_type_lower = exam_type.lower()
        self.module_name = f"graphs.{self.level_lower}.outliner"
        self.level_module = self._import_level_module()

        logger.info(f"Current Task ID {task_id} is being initialized")

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

    def callback_system_api(self):
        """
        Executes a GET request equivalent to:
          curl -X GET --location "https://jlpt.kongxuan.com/api/mongo/loadData/n3/full_exam"
          -H "clientid: ..."
          -H "x-auth: Bearer <token>"
        Retries 3 times automatically if any error occurs.
        Always continues regardless of success or failure.
        """
        url = f"https://jlpt.kongxuan.com/api/mongo/loadData/{self.level}/{self.exam_type}"
        headers = {
            "clientid": os.environ["EXAM_SYSTEM_CLIENT_ID"],
            # If 401 persists, try changing "x-auth" to "Authorization"
            "x-auth": os.environ["EXAM_SYSTEM_TOKEN"],
        }

        RETRY_COUNT = 3
        RETRY_DELAY = 2  # seconds

        last_exception = None
        result = None

        for attempt in range(1, RETRY_COUNT + 1):
            try:
                logger.info(f"Attempt {attempt} of {RETRY_COUNT}...")
                response = requests.get(
                    url,
                    headers=headers,
                    params={"id": self.task_id},  # fixed param key
                    timeout=10,
                )
                response.raise_for_status()

                logger.info("Request successful")
                result = response.json()
                break  # 成功后就跳出循环

            except requests.RequestException as e:
                logger.info(f"Attempt {attempt} failed: {e}")
                last_exception = e
                if attempt < RETRY_COUNT:
                    logger.info(f"Retrying in {RETRY_DELAY} seconds...\n")
                    time.sleep(RETRY_DELAY)
                else:
                    logger.error("All retry attempts failed.")

        # ✅ 无论成功失败都继续，不中断流程
        if result is None:
            logger.warning("Returning empty result due to failure.")
            result = {"success": False, "error": str(last_exception) if last_exception else "unknown error"}

        return result

    def run(self):
        """
        Run the exam generation pipeline.

        Returns:
            tuple:
                (outline, exam_paper) if both are generated successfully,
                (outline, None) if paper generation or storage fails,
                (None, None) if outline generation fails completely.

        Raises:
            ValueError: If outline generation fails irrecoverably.
        """
        conn_str = os.getenv("AZURE_MONGO_CONNECTION")
        db_name = os.getenv("AZURE_MONGO_DBNAME")
        project_path = os.environ['PROJECT_PATH']

        collection_name = f"{self.level_lower}_{self.exam_type_lower}"
        db_client = CosmosMongoDB(conn_str, db_name, collection_name)

        # Check task_id unique key
        if self.task_id:
            existing = db_client.exists(self.task_id)
            if existing:
                logger.warning(f"Exam with _id={self.task_id} already exists. Skipping execution.")
            else:
                logger.info("Safe to process as task_id [%s] is new", self.task_id)

        prompt = self._get_prompt()
        exam_generator = ExamGenerator(
            task_id=self.task_id,
            level=self.level,
            exam_type=self.exam_type,
        )

        # --- Step 1: Generate Outline ---
        outline = exam_generator._generate_outline(prompt)

        # If outline generator returned None, throw exception to celery
        if outline is None:
            raise RuntimeError("Outline generation returned None")

        # --- Step 2: Generate exam paper ---
        exam_paper = exam_generator._write_paper(outline)

        if exam_paper is None:
            # _write_paper() returns None when retry fails
            logger.error("Paper generation returned None")
            raise RuntimeError("Outline generation returned None")
        else:
            # Save Object as HTML (debug output)
            filename = f"{project_path}/output/JLPT_{self.level}_{self.task_id}.html"
            html_output = render_to_html(exam_paper['sections'])

            with open(filename, "w", encoding="utf-8") as file:
                file.write(html_output)

            logger.info(f" ### Exam Paper is Save as {filename} ###")

            # Save Object to MongoDB
            inserted_id = db_client.safe_insert_one(exam_paper)

            # Inform Exam System via API
            if inserted_id:
                logger.info("Inserted document ID: %s", inserted_id)
                self.callback_system_api()
                logger.info("Callback system API triggered successfully.")
            else:
                logger.warning("MongoDB insertion returned no document ID.")

        return outline, exam_paper


        # outline, exam_paper = exam_generator._generate_paper(instruction=prompt)
        # if outline:
        #     logger.info(" ### OUTLINE ### \n\n %s", outline.as_str)
        # else:
        #     logger.error("Exam paper generation returned None.")
        #
        # if outline and not exam_paper:
        #     logger.warning("Exam paper not generated; returning outline only.")
        #     return outline, None
        #
        # if exam_paper:
        #     logger.info(" ### Exam Paper ### \n\n %s", exam_paper)
        #
        #     if not conn_str or not db_name:
        #         raise EnvironmentError("Missing MongoDB connection settings.")
        #
        #     inserted_id = db_client.safe_insert_one(exam_paper)
        #
        #     if inserted_id:
        #         logger.info("Inserted document ID: %s", inserted_id)
        #         self.callback_system_api()
        #         logger.info("Callback system API triggered successfully.")
        #     else:
        #         logger.warning("MongoDB insertion returned no document ID.")
        #     # except Exception as e:
        #     #     logger.exception("Failed to insert exam paper into MongoDB: %s", e)
        #     #     return outline, None
        # return outline, exam_paper

