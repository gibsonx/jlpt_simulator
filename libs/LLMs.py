import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI



# from langchain_community.embeddings import XinferenceEmbeddings

load_dotenv()

azure_llm = AzureChatOpenAI(
    azure_endpoint="https://ai-rolandaws880125ai409947751408.openai.azure.com/openai/deployments/gpt-4.1/chat/completions?api-version=2025-01-01-preview",
    api_key=os.environ["AZURE_API_KEY"],
    model_name="gpt-4.1",
    api_version="2025-01-01-preview",
    temperature=0.3,
    top_p=0.95
)

# azure_ref_llm = AzureChatOpenAI(
#     azure_endpoint="https://ai-rolandaws880125ai409947751408.openai.azure.com/openai/deployments/model-router/chat/completions?api-version=2025-01-01-preview",
#     api_key=os.environ["AZURE_API_KEY"],
#     model_name="gpt-4.1-mini",
#     api_version="2025-01-01-preview",
#     temperature=0.5,
# )



# if __name__ == "__main__":
#     #obj = {'background': '会社の休憩室で、同僚のあきらとさおりが地域社会への貢献について話しています。', 'follow_up': 'あきらは今度、どのようにして地域活動の情報を知るつもりですか。', 'conversation': [{'gender': 'male', 'context': 'さおりさん、週末に何か予定がありますか。'}, {'gender': 'female', 'context': 'はい、実は近所の公園で行われる清掃活動に参加するつもりなんです。'}, {'gender': 'male', 'context': 'そうなんですか。地域のために活動するのはすばらしいですね。'}, {'gender': 'female', 'context': 'ありがとうございます。最近、地域のイベントやボランティアに関心が出てきて、少しでも役に立ちたいと思うようになりました。'}, {'gender': 'male', 'context': '僕も何か手伝いたいと思っていましたが、どうやって参加すればいいかわからなくて…。'}, {'gender': 'female', 'context': '市役所のホームページにいろいろな活動が紹介されていますよ。あきらさんも一緒にどうですか？'}, {'gender': 'male', 'context': 'はい、ぜひ参加してみたいです。今度、どんな活動があるか教えてもらえますか。'}, {'gender': 'female', 'context': 'もちろんです。今週末の清掃活動が終わったら、またお知らせしますね。'}], 'html_question': ' 番 ', 'choices': ['さおりから話を聞く', '市役所へ行く', '自分で探す', '家族に聞く'], 'correct_answer': 1}
#     obj = {'background': 'アパートの庭で男の人と女の人が話しています。', 'follow_up': '2人は何について話していますか?', 'conversation': [{'gender': 'female', 'context': '最近、庭がきれいになったね。何か始めたの？'}, {'gender': 'male', 'context': 'うん、先月から花を育ててみてるんだ。毎朝、水をやるのが楽しいよ。'}, {'gender': 'female', 'context': 'へえ、すごいね。どんな花を植えたの？'}, {'gender': 'male', 'context': 'チューリップとパンジーだよ。色がきれいだから選んだんだ。'}, {'gender': 'female', 'context': '私もやってみたいな。でも、虫が苦手で…。'}, {'gender': 'male', 'context': '最初は気になるけど、だんだん慣れるよ。小さいスコップとか手袋を使うと安心だよ。'}, {'gender': 'female', 'context': 'ありがとう。今度、一緒に花を選びに行かない？'}, {'gender': 'male', 'context': 'いいね！近くのホームセンターにいろいろ売ってるよ。週末に行こうか。'}], 'html_question': '2人は何について話していますか?', 'choices': ['庭の手入れの方法', '花の種類について', '趣味を始めること', '道具を買いに行く予定'], 'correct_answer': 3}
#     _generate_dialogue_with_options(type="type1", content=obj, seq=1)