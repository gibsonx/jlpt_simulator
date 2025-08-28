import pandas as pd
import json
from pydub import AudioSegment
import requests
import os
import azure.cognitiveservices.speech as speechsdk

from dotenv import load_dotenv
load_dotenv()

# Voice mappings
voices = {
    "nanami": "ja-JP-NanamiNeural",   # Standard Nanami
    "masaru": "ja-JP-MasaruNeural",   # Standard Masaru
    "shiori": "ja-JP-ShioriNeural",   # Standard Shiori
    "mayu": "ja-JP-MayuNeural"        # Standard Mayu
}

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
                    html += _render_result(result, idx=1)
    html += '</body></html>'
    return html

def _render_result(result, idx=1):
    html = ''
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
        if "audio" in result:
            html += f'<audio controls style="margin-left:1em;">\n'
            html += f'  <source src="{result["audio"]}" type="audio/mpeg">\n'
            html += 'Your browser does not support the audio element.\n'
            html += '</audio>\n'
        if "image" in result:
            html += f'<div style="margin:1em 0;">\n'
            html += f'  <img src="{result["image"]}" alt="Result image" style="max-width:30%; border:1px solid #ccc; border-radius:8px;">\n'
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
        return html


def AzureAIVoice(text, voice_name, filename, speed="0%"):
    speech_config = speechsdk.SpeechConfig(subscription=os.environ["SPEECH_KEY"], endpoint=os.environ["SPEECH_ENDPOINT"])
    speech_config.speech_synthesis_voice_name = voice_name
    audio_config = speechsdk.audio.AudioOutputConfig(filename=filename)
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    # Wrap the text in SSML with prosody rate
    ssml = f"""
    <speak version='1.0' xml:lang='en-US'>
        <voice name='{voice_name}'>
            <prosody rate='{speed}'>{text}</prosody>
        </voice>
    </speak>
    """

    synthesizer.speak_ssml_async(ssml).get()

def _generate_dialogue(content, type, seq):

    voice_tmp = os.path.join(os.environ["PROJECT_PATH"],'tmp')
    voice_source = os.path.join(os.environ["PROJECT_PATH"],'voice')
    voice_output = os.path.join(os.environ["PROJECT_PATH"],'output')

    voice_map = {
        'male': 'masaru',
        'female': 'nanami',
    }

    # Convert to dialogue format
    # [
    #     ("nanami", "こんにちは、マサルさん。週末は何をする予定ですか？"),
    #     ("masaru", "こんにちは、ナナミさん。まだ決めていませんが、ハイキングに行くかもしれません。")
    # ]
    dialogue = [(voice_map[line['gender']], line['context']) for line in content['conversation']]

    output_files = []

    output_files.append(os.path.join(voice_source, f"ding.wav"))

    seq_file = os.path.join(voice_tmp, f"{type}_{seq}.wav")
    AzureAIVoice(f"{seq}番", voices['masaru'], seq_file, speed="0%")
    output_files.append(seq_file)

    background_file = os.path.join(voice_tmp, f"{type}_{seq}_background.wav")
    AzureAIVoice(content['background'], voices['nanami'], background_file, speed="-5%")
    output_files.append(background_file)
    output_files.append(os.path.join(voice_source, f"empty_1s.wav"))

    follow_up_file = os.path.join(voice_tmp, f"{type}_{seq}_follow_up.wav")
    AzureAIVoice(content['follow_up'], voices['nanami'], follow_up_file, speed="-5%")
    output_files.append(follow_up_file)
    output_files.append(os.path.join(voice_source, f"empty_1s.wav"))

    # Generate audio for the conversation
    for i, (speaker, text) in enumerate(dialogue):
        filename = os.path.join(voice_tmp, f"{type}_{seq}_{i}_speaker.wav")
        AzureAIVoice(text, voices[speaker], filename, speed="-5%")
        output_files.append(filename)

    follow_up_file = os.path.join(voice_tmp, f"{type}_{seq}_follow_up.wav")
    output_files.append(os.path.join(voice_source, f"ding.wav"))
    output_files.append(follow_up_file)

    # Generate audio for the choices
    if type == "summary_understanding":
        for i, text in enumerate(content['choices'],start=1):
            option_seq = os.path.join(voice_tmp, f"{type}_{seq}_{i}_seq.wav")
            AzureAIVoice(f"{i}", voices['masaru'], option_seq, speed="-5%")

            option = os.path.join(voice_tmp, f"{type}_{seq}_{i}_option.wav")
            AzureAIVoice(text, voices['nanami'], option, speed="-5%")

            output_files.append(option_seq)
            output_files.append(option)

    # Merge audio files using pydub
    combined = AudioSegment.empty()
    for file in output_files:
        print(file)
        combined += AudioSegment.from_wav(file)

    target_file = os.path.join(voice_output, f"{type}_{seq}_conversation_output.wav")

    # Export final conversation
    combined.export(target_file, format="wav")
    print(f"Conversation audio saved as {target_file}")

    return target_file

def _generate_express(content, type, seq):

    voice_tmp = os.path.join(os.environ["PROJECT_PATH"], 'tmp')
    voice_source = os.path.join(os.environ["PROJECT_PATH"], 'voice')
    voice_output = os.path.join(os.environ["PROJECT_PATH"], 'output')

    voice_map = {
        'male': 'masaru',
        'female': 'nanami',
    }

    dialogue = [(voice_map[line['gender']], line['context']) for line in content['conversation']]

    output_files = []

    output_files.append(os.path.join(voice_source, f"ding.wav"))

    seq_file = os.path.join(voice_tmp, f"{type}_{seq}.wav")
    AzureAIVoice(f"{seq}番", voices['masaru'], seq_file, speed="0%")
    output_files.append(seq_file)

    # Generate audio for the conversation
    speaker, text = dialogue[0]
    filename = os.path.join(voice_tmp, f"{type}_{seq}_0_speaker.wav")
    AzureAIVoice(text, voices[speaker], filename, speed="-10%")
    output_files.append(filename)
    output_files.append(os.path.join(voice_source, f"empty_1s.wav"))

    # Determine speakers based on dialogue[0]
    if speaker == 'nanami':
        seq_speaker = 'masaru'
        option_speaker = 'nanami'
    else:
        seq_speaker = 'mayu'
        option_speaker = 'masaru'

   # Generate audio for the choices
    for i, text in enumerate(content['choices'],start=1):
        option_seq = os.path.join(voice_tmp, f"{type}_{seq}_{i}_seq.wav")
        AzureAIVoice(f"{i}", voices[seq_speaker], option_seq, speed="-10%")

        option = os.path.join(voice_tmp, f"{type}_{seq}_{i}_option.wav")
        AzureAIVoice(text, voices[option_speaker], option, speed="-10%")

        output_files.append(option_seq)
        output_files.append(option)

        # Merge audio files using pydub
    combined = AudioSegment.empty()
    for file in output_files:
        print(file)
        combined += AudioSegment.from_wav(file)

    target_file = os.path.join(voice_output, f"{type}_{seq}_conversation_output.wav")

    # Export final conversation
    combined.export(target_file, format="wav")
    print(f"Conversation audio saved as {target_file}")

    return target_file

def _generate_image(prompt="a woman is talking to a man."):

    KIA_API_KEY = os.environ["KIA_API_KEY"]

    url = "https://api.kie.ai/api/v1/gpt4o-image/generate"

    payload = {
        "filesUrl": ["https://strolandaws8409947751408.blob.core.windows.net/exjlpt/jlpt_refer01.png",
                     "https://strolandaws8409947751408.blob.core.windows.net/exjlpt/jlpt_refer02.png",
                     "https://strolandaws8409947751408.blob.core.windows.net/exjlpt/jlpt_refer03.png"],
        "prompt": "Draw a simple black-and-white line illustration in the style of JLPT exam pictures."
                  "The style should be minimal, with clean outlines"
                  "and look like an educational test question picture. Ensure no English and Japanese words appear on the generated picture."
                  "you can refer to the style of uploaded pictures."
                  "Write an arrow symbol pointing to the person who speaks first. The image describes the following scenario: \n\n" + prompt,
        "size": "3:2",
        "callBackUrl": "http://172.190.115.70:3000/4o-image-callback",
        "isEnhance": False,
        "uploadCn": False,
        "nVariants": 1,
        "enableFallback": False,
        "fallbackModel": "GPT_IMAGE_1"
    }
    headers = {
        "Authorization": f"Bearer {KIA_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    task_id = response.json()['data']['taskId']

    image_url = os.environ["AZURE_CONTAINER_URL"] + f"4o_images_{task_id}_image_1.png"

    print(image_url)

    return  image_url
