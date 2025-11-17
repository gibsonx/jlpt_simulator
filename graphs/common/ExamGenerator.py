import inspect
import json
import logging
from uuid import UUID
import random
import time
import uuid
from typing import *
from tqdm import tqdm
from graphs.common.GraphBuilder import GraphBuilder
from graphs.common.JLPTTaskFactory import JLPTTaskFactory
from libs.CosmosMongoDB import CosmosMongoDB
from libs.LLMs import *

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
from libs.Utils import _load_vocab_and_resources, _extract_questions_qa_lines
from graphs.common.Schema import Outline, ExamType
from libs.Logger import logger
from libs.Utils import render_to_html

from dotenv import load_dotenv
load_dotenv()

class ExamGenerator:
    def __init__(self, level: str, exam_type: ExamType, task_id: Optional[str] = None):
        self.level = level
        self.exam_type = exam_type
        self.task_id = task_id if task_id else str(uuid.uuid1())
        self.vocab, self.topics, self.grammar = self._load_resources()

    def _write_paper(self, initial_outline: Any) -> Dict[str, Any] | None:
        outliner_json = initial_outline.model_dump_json()
        data = json.loads(outliner_json)

        output_data = {
            "_id": self.task_id,
            "level": self.level,
            "type": self.exam_type,
            "sections": []
        }

        # global live results for the entire paper
        live_results = []

        start_time = time.time()

        for section in data['sections']:
            output_section = {'section_title': section['section_title'], 'subsections': []}

            for subsection in tqdm(section['subsections'], desc=f"Processing {section['section_title']}"):
                function_name = subsection['subsection_title']
                questions = subsection['question_topics']
                seq = 1

                for question in tqdm(questions, desc=f"Processing {subsection['subsection_title']}"):
                    graph = GraphBuilder(exam_uid=self.task_id)
                    handler = JLPTTaskFactory(graph=graph, level=self.level)
                    func = getattr(handler, function_name, None)

                    if func:
                        max_attempts = 5
                        for attempt in range(max_attempts):
                            try:
                                sig = inspect.signature(func)
                                params = sig.parameters

                                # Pass the global live_results so all previous questions are included
                                args = [question['topic'], _extract_questions_qa_lines(live_results, 20)]
                                if 'grammar' in question and question['grammar']:
                                    args.append(question['grammar'])
                                if 'seq' in params:
                                    args.append(seq)

                                result = func(*args)
                                if not result:
                                    raise ValueError("No data available for processing")
                                else:
                                    question['result'] = result
                                    live_results.append(result)  # update global live results
                                seq += 1
                                break
                            except Exception as e:
                                logger.error(f"Error {e} on {question['topic']}")
                                if attempt < max_attempts - 1:
                                    question['topic'] = random.choice(self.topics)
                                    time.sleep(30)
                                    logger.info(f"Retry {attempt} after 30 seconds")
                                else:
                                    return None
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
        logger.info(f"Total execution time: {end_time - start_time:.2f} seconds")

        return output_data

    def _load_resources(self) -> Tuple[Dict[str, Any], list, list]:
        """Load vocab, topics, and grammar for the exam level."""
        return _load_vocab_and_resources(self.level)

    def _generate_outline(self, instruction: Any) -> Outline | None:
        max_retries = 3
        outline = None

        for attempt in range(1, max_retries + 1):
            try:
                generate_outline = instruction | azure_llm.with_structured_output(Outline)
                outline = generate_outline.invoke({
                    "topic_list": self.topics,
                    "vocab_dict": self.vocab,
                    "grammar_list": self.grammar
                })
                logger.info("Outline of the exam:\n\n%s", outline.as_str)
                return outline

            except Exception as e:
                logger.error(
                    "Attempt %s/%s failed for exam_uid=%s: %s",
                    attempt, max_retries, self.task_id, e, exc_info=True
                )

                if attempt < max_retries:
                    delay = 2 ** attempt  # exponential backoff: 2s, 4s, ...
                    time.sleep(delay)
                else:
                    logger.error("All retries failed for exam_uid=%s", self.task_id)
                    return None

    def _generate_paper(self, instruction: Any):
        """
        Generate an exam outline, build paper, and store it in DB.
        Returns: (inserted_id, outline_str, output_data)
        """
        outline = None
        project_path = os.environ['PROJECT_PATH']
        # --- Step 1: Generate outline ---
        try:
            outline = self._generate_outline(instruction)
        except Exception as e:
            logger.error(
                "Failed to generate exam outline for level '%s' and exam_type '%s', %s",
                self.level, self.exam_type, e
            )
        # --- Step 1: Generate exam Paper ---
        try:
            output_data = self._write_paper(outline)
            # render paper to output folder for debug
            filename = f"{project_path}/output/JLPT_{self.level}_{self.task_id}.html"
            html_output = render_to_html(output_data['sections'])

            with open(filename, "w", encoding="utf-8") as file:
                file.write(html_output)

            return outline, output_data
        except Exception as e:
            logger.error("Failed to generate and store paper for exam_uid=%s: %s", self.task_id, e, exc_info=True)
            # Return a consistent tuple on error
            return None, None




