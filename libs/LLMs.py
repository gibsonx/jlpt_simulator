import os
from pydub import AudioSegment
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
import azure.cognitiveservices.speech as speechsdk


# from langchain_community.embeddings import XinferenceEmbeddings

load_dotenv()

azure_llm = AzureChatOpenAI(
    azure_endpoint="https://ai-rolandaws880125ai409947751408.openai.azure.com/openai/deployments/gpt-4.1/chat/completions?api-version=2025-01-01-preview",
    api_key=os.environ["AZURE_API_KEY"],
    model_name="gpt-4.1",
    api_version="2025-01-01-preview",
    temperature=0.2,
)

# azure_ref_llm = AzureChatOpenAI(
#     azure_endpoint="https://ai-rolandaws880125ai409947751408.openai.azure.com/openai/deployments/model-router/chat/completions?api-version=2025-01-01-preview",
#     api_key=os.environ["AZURE_API_KEY"],
#     model_name="gpt-4.1-mini",
#     api_version="2025-01-01-preview",
#     temperature=0.5,
# )

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

def _generate_dialogue(content):

    # conversation_data = [
    #     ("nanami", "こんにちは、マサルさん。週末は何をする予定ですか？"),
    #     ("masaru", "こんにちは、ナナミさん。まだ決めていませんが、ハイキングに行くかもしれません。"),
    #     ("nanami", "いいですね！天気も良さそうですし。"),
    #     ("masaru", "そうですね。自然の中でリラックスするのが一番です。")
    # ]

    root_folder = '../output'

    voice_map = {
        'male': 'masaru',
        'female': 'mayu',
    }

    # Convert to dialogue format
    dialogue = [(voice_map[line['gender']], line['context']) for line in content['conversation']]

    # Voice mappings
    voices = {
        "nanami": "ja-JP-NanamiNeural",
        "masaru": "ja-JP-Masaru:DragonHDLatestNeural",  # Dragon HD voice is typically just the latest Masaru voice
        "shiori": "ja-JP-ShioriNeural",
        "mayu": "ja-JP-MayuNeural"
    }

    output_files = []

    background_file = os.path.join(root_folder, f"background.wav")
    AzureAIVoice(content['background'], voices['nanami'], background_file, speed="0%")
    output_files.append(background_file)

    follow_up_file = os.path.join(root_folder, f"follow_up.wav")
    AzureAIVoice(content['follow_up'], voices['nanami'], follow_up_file, speed="0%")
    output_files.append(follow_up_file)

    # Generate audio for each line
    for i, (speaker, text) in enumerate(dialogue):
        filename =  os.path.join(root_folder, f"{i}_{speaker}.wav")
        AzureAIVoice(text, voices[speaker], filename, speed="0%")
        output_files.append(filename)

    follow_up_file = os.path.join(root_folder, f"follow_up.wav")
    output_files.append(os.path.join(root_folder, f"ding.wav"))
    output_files.append(follow_up_file)

    # Merge audio files using pydub
    combined = AudioSegment.empty()
    for file in output_files:
        combined += AudioSegment.from_wav(file)

    target_file = os.path.join(root_folder, "conversation_output.wav")

    # Export final conversation
    combined.export(target_file, format="wav")
    print("Conversation audio saved as conversation_output.wav")

if __name__ == "__main__":
    obj = {'background': '会社の休憩室で、同僚のあきらとさおりが地域社会への貢献について話しています。', 'follow_up': 'あきらは今度、どのようにして地域活動の情報を知るつもりですか。', 'conversation': [{'gender': 'male', 'context': 'さおりさん、週末に何か予定がありますか。'}, {'gender': 'female', 'context': 'はい、実は近所の公園で行われる清掃活動に参加するつもりなんです。'}, {'gender': 'male', 'context': 'そうなんですか。地域のために活動するのはすばらしいですね。'}, {'gender': 'female', 'context': 'ありがとうございます。最近、地域のイベントやボランティアに関心が出てきて、少しでも役に立ちたいと思うようになりました。'}, {'gender': 'male', 'context': '僕も何か手伝いたいと思っていましたが、どうやって参加すればいいかわからなくて…。'}, {'gender': 'female', 'context': '市役所のホームページにいろいろな活動が紹介されていますよ。あきらさんも一緒にどうですか？'}, {'gender': 'male', 'context': 'はい、ぜひ参加してみたいです。今度、どんな活動があるか教えてもらえますか。'}, {'gender': 'female', 'context': 'もちろんです。今週末の清掃活動が終わったら、またお知らせしますね。'}], 'html_question': ' 番 ', 'choices': ['さおりから話を聞く', '市役所へ行く', '自分で探す', '家族に聞く'], 'correct_answer': 1}
    _generate_dialogue(obj)