from langchain_core.prompts import ChatPromptTemplate
import inspect
import json
import logging
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
from libs.Utils import _load_vocab_and_resources
from graphs.common.Schema import Outline
from libs.Logger import logger


ExamType = Literal["full_exam", "quick_test", "vocabulary", "grammar", "listening", "reading"]



class ExamGenerator:
    def __init__(self, level: str, exam_type: ExamType, db_collection: str):
        self.level = level
        self.exam_type = exam_type
        self.db_collection = db_collection
        self.exam_uid = str(uuid.uuid1())

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

    def _generate_and_store_paper(self, instruction: Any) -> Tuple[Optional[str], Optional[Dict[str, Any]]]:
        try:
            vocab, topics, grammar = _load_vocab_and_resources(self.level)
        except Exception as e:
            logger.error("Failed to load resources for level %s: %s", self.level, e, exc_info=True)
            return None, None

        try:
            generate_outline_direct = instruction | azure_llm.with_structured_output(Outline)
            initial_outline = generate_outline_direct.invoke({
                "topic_list": topics,
                "vocab_dict": vocab,
                "grammar_list": grammar
            })
            logger.info("Outline of the exam:\n\n%s", initial_outline.as_str)
        except Exception as e:
            logger.error("Failed to generate outline for exam_uid=%s: %s", self.exam_uid, e, exc_info=True)
            return None, None

        try:
            output_data = self._write_paper(initial_outline, topics)
        except Exception as e:
            logger.error("Failed to build output data for exam_uid=%s: %s", self.exam_uid, e, exc_info=True)
            return None, None

        try:
            db_client = CosmosMongoDB(
                os.environ['AZURE_MONGO_CONNECTION'],
                os.environ['AZURE_MONGO_DBNAME'],
                self.db_collection
            )
            inserted_id = db_client.insert_one(output_data)
            logger.info("Inserted document ID: %s", inserted_id)
            return inserted_id, output_data
        except Exception as e:
            logger.error("Failed to insert document for exam_uid=%s: %s", self.exam_uid, e, exc_info=True)
            return None, output_data