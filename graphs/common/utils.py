import pandas as pd
import json
from pydub import AudioSegment

import os

def collect_vocabulary(file_path):
    # Read the CSV file
    data = pd.read_csv(file_path)
    # Shuffle the rows and reset the index
    words = data.iloc[:, :2].sample(frac=1).reset_index(drop=True)
    # Extract the second column (values) and convert to a single-line string
    vocab_string = ','.join(words.iloc[:, 1].astype(str).tolist())
    return vocab_string

def render_to_html(sections):
    html = '<html><body style="text-align: left;">\n'
    for section in sections:
        html += f'<h1>{section.get("section_title", "")}</h1>\n'
        for subsection in section.get("subsections", []):
            html += f'<h2>{subsection.get("subsection_title", "")}</h2>\n'
            if "description" in subsection:
                html += f'<p>{subsection["description"]}</p>\n'
            for idx, qtopic in enumerate(subsection.get("question_topics", []), 1):
                result = qtopic.get("result", {})
                if isinstance(result, dict):
                    if "html_article" in result:
                        html += result["html_article"] + "\n"
                    if "html_question" in result:
                        html += '<div>\n'
                        html += f'<p><strong>{idx}. </strong>{result["html_question"]}</p>'
                        if "choices" in result:
                            correct = result.get("correct_answer", -1)
                            html += '<ul>\n'
                            for idx, choice in enumerate(result["choices"], 1):
                                if idx == correct:
                                    html += f"<li>{idx}. <b>{choice}</b> <span style='color:green;'>(correct)</span></li>\n"
                                else:
                                    html += f"<li>{idx}. {choice}</li>\n"
                            html += '</ul>\n'
                        html += '</div>\n'
                    if "background" in result:
                        html += f'<p><strong>Background: </strong>{result["background"]}</p>\n'
                    if "conversation" in result and isinstance(result["conversation"], list):
                        html += '<div style="margin: 1em 0; padding: 1em; border: 1px solid #ccc;">\n'
                        for turn in result["conversation"]:
                            gender = turn.get("gender", "unknown")
                            context = turn.get("context", "")
                            html += f'<p><strong>{gender.capitalize()}:</strong> {context}</p>\n'
                        html += '</div>\n'
                    if "questions" in result and isinstance(result["questions"], list):
                        for idx, q in enumerate(result["questions"],1):
                            html += f'<p><strong>{idx}.{q["html_question"]}</strong></p>\n'
                            if "choices" in q:
                                correct = q.get("correct_answer", -1)
                                html += '<ul>\n'
                                for idx, choice in enumerate(q["choices"], 1):
                                    if idx == correct:
                                        html += f"<li><b>{choice}</b> <span style='color:green;'>(correct)</span></li>\n"
                                    else:
                                        html += f"<li>{choice}</li>\n"
                                html += '</ul>\n'
    html += '</body></html>'
    return html

def _render_result(result, idx=1):
    html = '<html><body style="text-align: left;">\n'
    if isinstance(result, dict):
        if "html_article" in result:
            html += result["html_article"] + "\n"
        if "html_question" in result:
            html += '<div>\n'
            html += f'<p><strong>{idx}. </strong>{result["html_question"]}</p>'
            if "choices" in result:
                correct = result.get("correct_answer", -1)
                html += '<ul>\n'
                for idx, choice in enumerate(result["choices"], 1):
                    if idx == correct:
                        html += f"<li>{idx}. <b>{choice}</b> <span style='color:green;'>(correct)</span></li>\n"
                    else:
                        html += f"<li>{idx}. {choice}</li>\n"
                html += '</ul>\n'
            html += '</div>\n'
        if "background" in result:
            html += f'<p><strong>Background: </strong>{result["background"]}</p>\n'
        if "conversation" in result and isinstance(result["conversation"], list):
            html += '<div style="margin: 1em 0; padding: 1em; border: 1px solid #ccc;">\n'
            for turn in result["conversation"]:
                gender = turn.get("gender", "unknown")
                context = turn.get("context", "")
                html += f'<p><strong>{gender.capitalize()}:</strong> {context}</p>\n'
            html += '</div>\n'
        if "follow_up" in result:
            html += f'<p><strong>follow-up question: </strong>{result["follow_up"]}</p>\n'
        if "questions" in result and isinstance(result["questions"], list):
            for idx, q in enumerate(result["questions"],1):
                html += f'<p><strong>{idx}.{q["html_question"]}</strong></p>\n'
                if "choices" in q:
                    correct = q.get("correct_answer", -1)
                    html += '<ul>\n'
                    for idx, choice in enumerate(q["choices"], 1):
                        if idx == correct:
                            html += f"<li><b>{choice}</b> <span style='color:green;'>(correct)</span></li>\n"
                        else:
                            html += f"<li>{choice}</li>\n"
                    html += '</ul>\n'

        html += '</body></html>'
        return html

