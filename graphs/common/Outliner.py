import json
import logging
import random
import time
import pandas as pd
import yaml
import inspect
from tqdm import tqdm
import os
from datetime import datetime
from docx import Document
from html4docx import HtmlToDocx
import uuid
from libs.CosmosMongoDB import CosmosMongoDB
from libs.LLMs import *
import datetime
from libs.Utils import render_to_html,collect_vocabulary
from typing import List, Optional
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from graphs.n3.ExamTaskHandler import ExamTaskHandler

def _generate_outline(initial_outline, exam_id, level, topics_list):

    outliner_json = initial_outline.model_dump_json()
    data = json.loads(outliner_json)  # Replace with your actual JSON data
    output_data = {
        "_id": exam_id,
        "level": level,
        'sections': []
    }

    start_time = time.time()

    for section in data['sections']:
        output_section = {'section_title': section['section_title'], 'subsections': []}

        for subsection in tqdm(section['subsections'], desc=f"Processing {section['section_title']}"):
            # print(subsection['subsection_title'])
            # function_name = function_name = re.findall(r'[（(](.*?)[）)]', subsection['subsection_title'])[0]
            function_name = subsection['subsection_title']
            questions = subsection['question_topics']
            seq = 1  # Initialize sequence counter
            for question in tqdm(questions, desc=f"Processing {subsection['subsection_title']}"):
                handler = ExamTaskHandler(level=level, exam_id=exam_id)
                func = getattr(handler, function_name, None)

                if func:
                    max_attempts = 2
                    for attempt in range(max_attempts):
                        print("###########SEQUENCE########: ", seq)
                        try:
                            sig = inspect.signature(func)  # Inspect parameters
                            params = sig.parameters

                            # Build arguments dynamically
                            args = [question['topic']]
                            if 'grammar' in question and question['grammar']:
                                args.append(question['grammar'])
                            if 'seq' in params:
                                args.append(seq)

                            # Call the function safely
                            result = func(*args)
                            question['result'] = result
                            seq += 1
                            break
                        except Exception as e:
                            print("The Program encountered an error {} on {}".format(e, question['topic']))
                            if attempt < max_attempts - 1:
                                # Replace topic and retry
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

    # End the timer
    end_time = time.time()

    # Calculate the total execution time
    execution_time = end_time - start_time

    print(f"Total execution time: {execution_time:.2f} seconds")

    return output_data