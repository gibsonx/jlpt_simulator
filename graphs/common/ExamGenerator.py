import inspect
import json
import logging
import os
import random
import time
import uuid
from typing import *
from tqdm import tqdm
import requests

from graphs.common.GraphBuilder import GraphBuilder
from graphs.common.JLPTTaskFactory import JLPTTaskFactory
from libs.CosmosMongoDB import CosmosMongoDB
from libs.LLMs import *

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
from libs.Utils import _load_vocab_and_resources
from graphs.common.Schema import Outline,ExamType
from libs.Logger import logger
from libs.Utils import render_to_html

from dotenv import load_dotenv
load_dotenv()

class ExamGenerator:
    def __init__(self, level: str, exam_type: ExamType, db_collection: str, task_id: Optional[str] = None):
        self.level = level
        self.exam_type = exam_type
        self.db_collection = db_collection
        self.exam_uid = task_id or str(uuid.uuid1())
        self.vocab, self.topics, self.grammar = self._load_resources()

    def _write_paper(self, initial_outline: Any, topics_list: List[str]) -> Dict[str, Any]:
        outliner_json = initial_outline.model_dump_json()
        data = json.loads(outliner_json)

        output_data = {
            "_id": self.exam_uid,
            "level": self.level,
            "type": self.exam_type,
            "sections": []
        }

        start_time = time.time()

        for section in data['sections']:
            output_section = {'section_title': section['section_title'], 'subsections': []}

            for subsection in tqdm(section['subsections'], desc=f"Processing {section['section_title']}"):
                function_name = subsection['subsection_title']
                questions = subsection['question_topics']
                seq = 1

                for question in tqdm(questions, desc=f"Processing {subsection['subsection_title']}"):
                    graph = GraphBuilder(exam_uid=self.exam_uid)
                    handler = JLPTTaskFactory(graph=graph, level=self.level)
                    func = getattr(handler, function_name, None)

                    if func:
                        max_attempts = 2
                        for attempt in range(max_attempts):
                            try:
                                sig = inspect.signature(func)
                                params = sig.parameters
                                args = [question['topic']]
                                if 'grammar' in question and question['grammar']:
                                    args.append(question['grammar'])
                                if 'seq' in params:
                                    args.append(seq)

                                result = func(*args)
                                question['result'] = result
                                seq += 1
                                break
                            except Exception as e:
                                print(f"Error {e} on {question['topic']}")
                                if attempt < max_attempts - 1:
                                    question['topic'] = random.choice(topics_list)
                    else:
                        question['result'] = f"Method {function_name} not found"

                output_subsection = {
                    'subsection_title': subsection['subsection_title'],
                    'description': subsection['description'],
                    'question_topics': questions
                }
                output_section['subsections'].append(output_subsection)

            output_data['sections'].append(output_section)

        end_time = time.time()
        print(f"Total execution time: {end_time - start_time:.2f} seconds")

        return output_data

    def _load_resources(self) -> Tuple[Dict[str, Any], list, list]:
        """Load vocab, topics, and grammar for the exam level."""
        return _load_vocab_and_resources(self.level)

    def _generate_outline(
        self, instruction: Any
    ) -> str:
        """Generate structured exam outline using LLM."""
        try:
            generate_outline = instruction | azure_llm.with_structured_output(Outline)
            outline = generate_outline.invoke({
                "topic_list": self.topics,
                "vocab_dict": self.vocab,
                "grammar_list": self.grammar
            })
            logger.info("Outline of the exam:\n\n%s", outline.as_str)
        except Exception as e:
            logger.error("Failed to generate outline for exam_uid=%s: %s", self.exam_uid, e, exc_info=True)
        return outline

    def _build_output(self, outline: Any) -> Dict[str, Any]:
        """Build the final exam paper data."""
        return self._write_paper(outline, self.topics)

    def _insert_to_db(self, task_id: int, output_data: Dict[str, Any]) -> str:
        """Insert exam data into Cosmos MongoDB."""
        if task_id:
            output_data["_id"] = task_id

        db_client = CosmosMongoDB(
            os.environ['AZURE_MONGO_CONNECTION'],
            os.environ['AZURE_MONGO_DBNAME'],
            self.db_collection
        )
        inserted_id = db_client.insert_one(output_data)
        logger.info("Inserted document ID: %s", inserted_id)
        return inserted_id

    # ---------------- Main Function ---------------- #

    def _generate_and_store_paper(
        self, outline: Any
    ) -> Tuple[Optional[str], Optional[Dict[str, Any]]]:
        """
        Generate an exam outline, build paper, and store it in DB.
        Returns: (inserted_id, outline_str, output_data)
        """
        project_path = os.environ['PROJECT_PATH']

        try:
            output_data = self._build_output(outline)

            # insert it into mongoDB
            self._insert_to_db(output_data)

            # render paper to output folder for debug
            filename = f"{project_path}/output/JLPT_{self.exam_uid}.html"
            html_output = render_to_html(output_data['sections'])

            with open(filename, "w", encoding="utf-8") as file:
                file.write(html_output)

            return output_data
        except Exception as e:
            logger.error("Failed to generate and store paper for exam_uid=%s: %s", self.exam_uid, e, exc_info=True)
            # Return a consistent tuple on error
            return None

    def callback_system_api(self):
        """
        Executes a GET request equivalent to:
          curl -X GET --location "https://jlpt.kongxuan.com/api/mongo/loadData/n3/full_exam"
          -H "clientid: ..."
          -H "x-auth: Bearer <token>"
        Retries 3 times automatically if any error occurs.
        """
        url = f"https://jlpt.kongxuan.com/api/mongo/loadData/{self.level}/{self.exam_type}"
        headers = {
            "clientid": "e5cd7e4891bf95d1d19206ce24a7b32e",
            # If 401 persists, try changing "x-auth" to "Authorization"
            "x-auth": os.environ["EXAM_SYSTEM_TOKEN"],
        }

        RETRY_COUNT = 3
        RETRY_DELAY = 2  # seconds

        for attempt in range(1, RETRY_COUNT + 1):
            try:
                print(f"Attempt {attempt} of {RETRY_COUNT}...")
                response = requests.get(url, headers=headers, params={id: self.exam_uid}, timeout=10)
                response.raise_for_status()

                print("✅ Request successful")
                return response.json()

            except requests.RequestException as e:
                print(f"⚠️ Attempt {attempt} failed: {e}")
                if attempt < RETRY_COUNT:
                    print(f"⏳ Retrying in {RETRY_DELAY} seconds...\n")
                    time.sleep(RETRY_DELAY)
                else:
                    print("❌ All retry attempts failed.")
                    return None


