import os

from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
import azure.cognitiveservices.speech as speechsdk
from pydub import AudioSegment

# from langchain_community.embeddings import XinferenceEmbeddings

load_dotenv()

azure_llm = AzureChatOpenAI(
    azure_endpoint="https://ai-rolandaws880125ai409947751408.openai.azure.com/openai/deployments/gpt-4.1/chat/completions?api-version=2025-01-01-preview",
    api_key=os.environ["AZURE_API_KEY"],
    model_name="gpt4.1",
    api_version="2025-01-01-preview",
    temperature=0.5,
)

azure_ref_llm = AzureChatOpenAI(
    azure_endpoint="https://ai-rolandaws880125ai409947751408.openai.azure.com/openai/deployments/gpt-4.1-mini/chat/completions?api-version=2025-01-01-preview",
    api_key=os.environ["AZURE_API_KEY"],
    model_name="gpt-4.1-mini",
    api_version="2025-01-01-preview",
    temperature=0.5,
)

dialogue = [
    ("nanami", "こんにちは、マサルさん。週末は何をする予定ですか？"),
    ("masaru", "こんにちは、ナナミさん。まだ決めていませんが、ハイキングに行くかもしれません。"),
    ("nanami", "いいですね！天気も良さそうですし。"),
    ("masaru", "そうですね。自然の中でリラックスするのが一番です。")
]

# Voice mappings
voices = {
    "nanami": "ja-JP-NanamiNeural",
    "masaru": "ja-JP-Masaru:DragonHDLatestNeural"  # Dragon HD voice is typically just the latest Masaru voice
}



def synthesize_to_file(text, voice_name, filename, speed="0%"):
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

# output_files = []
# # Generate audio for each line
# for i, (speaker, text) in enumerate(dialogue):
#     filename = f"{i}_{speaker}.wav"
#     synthesize_to_file(text, voices[speaker], filename, speed="0%")
#     output_files.append(filename)
#
# # Merge audio files using pydub
# combined = AudioSegment.empty()
# for file in output_files:
#     combined += AudioSegment.from_wav(file)
#
# # Export final conversation
# combined.export("../output/conversation_output.wav", format="wav")
# print("Conversation audio saved as conversation_output.wav")