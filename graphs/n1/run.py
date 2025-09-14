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
from graphs.n3.inventory import ExamTaskHandler

load_dotenv()
import logging

import uuid
from libs.LLMs import *

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

from libs.Utils import render_to_html,collect_vocabulary


load_dotenv()

# Import N3 vocabulary
file_path = 'vocab/n3.csv'
# Display the content of the CSV file
vocab_dict = collect_vocabulary(file_path)
with open("vocab/topics.txt", "r", encoding="utf-8") as file:
    topics_list = [line.strip() for line in file]
with open("vocab/sentence_grammar.txt", "r", encoding="utf-8") as file:
    grammar_list = [line.strip() for line in file]

exam_id = str(uuid.uuid1())
level = 'n3'


instruction = """
Section 1: vocabulary
- 問題1 のことばの読み方として最もよいものを、1・2・3・4から一つえらびなさい (kanji_reading) 8 questions in total: 3 are nouns, 3 are verbs, 1 is an adjective,  adjective.
- 問題5 つぎのことばの使い方として最もよいものを、1・2・3・4から一つえらびなさい。 (word_usage) 5 questions in total: 3 noun, and 2 verbs.

Section 2: Grammar
- 問題6 つぎの文の（　　　）に入れるのに最もよいものを、１・２・３・４から一つえらびなさい。(sentence_grammar) 13 questions in total: the first 1 is honorific

Section 3: Reading Comprehension
- 問題1-1 つぎの文章を読んで、質問に答えなさい。答えは、1・2・3・4から最もよいものを一つえらびなさい (short_passage_mail_read): 1 article

Section 4: Listening Comprehension
- 問題1 では、まず質問を聞いてください。それから話を聞いて、問題用紙の1から4の中から、最もよいものを一つえらんでください。 (topic_understanding): 6 question
"""

direct_gen_outline_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            (
                "You are a Japanese teacher tasked with creating an outline for a JLPT N3 level exam paper."
                "The overall difficulty should be appropriate for the N3 level.\n"
                "The exam paper should include a mix of moderately difficult and very difficult topics to accurately assess proficiency.\n\n"
                "Please ensure the following requirements are met:\n\n"
                "subsection_title in Subsection must be written in English.\n\n"
                "For Section 1 - vocabulary:\n"
                "- Select vocabulary words from the 'vocabulary' list, ensuring that 80% of the topics are very difficult.\n"
                "- The topic words in 問題1 (kanji_reading) and 問題5 (word_usage) must be written in Kanji while other topic words use Japanese kana.\n"
                "For Section 2 - Grammar:\n"
                "- Randomly select topics from 'TopicList' and grammars from 'GrammarList'.\n"
                "- For 問題8, include one question that integrates 4 different grammar points.\n"
                "- The grammar used must be appropriate and consistent with the chosen topic.\n\n"
                "For Section 3 - Reading Comprehension and Listening Comprehension:\n"
                "- Randomly choose topics from 'TopicList'.\n\n"
                "For Section 4: Listening Comprehension:\n"
                "- Randomly choose topics from 'TopicList'.\n\n"
                "Additionally:\n"
                "- Each topic word should be unique and must not be repeated in the outline.\n"
                "- Follow the provided exam instructions carefully to determine the number of questions and content for each section.\n"
                "- Finally, write the full outline of the examination paper in Japanese, including question topics as per the instructions.\n\n"
                f"Instruction: {instruction}"
            ),
        ),
        ("user", "TopicList: {topic_list}, vocabulary: {vocab_dict}, GrammarList: {grammar_list}"),
    ]
)