from graphs.common.node_builder import *
from graphs.common.utils import *
from graphs.common.state import *
from libs.LLMs import azure_llm
import random
from langgraph.graph import StateGraph

load_dotenv()

teacher_prompt = """
Role: You are a Japanese teacher.

Task: your job is to write a kanji question for the JLPT N3 exam. 
Your job is to provide a kanji vocabulary word and ask the candidate to choose the correct kana reading.

Instructions:
Format: Follow the format of formal exam papers.
Content: Ensure the vocabulary is restricted to N3 level. Use the vocabulary in the `Dictionary` as much as possible.
Reference: Get inspiration from the Search result. Only use the format as a reference; do not use any specific content from existing exams.
Explanation: Append the correct answer and an explanation of the main challenges in simplified Chinese at each question.
Additional Requirement: Don't show question requirement in the generated content.

Dictionary: {vocab_dict}
Search result: {search_result}
Formal exam paper: {example}
"""

example = """
山田さんがちらしを **配った**。
　1 ひろった　2 くばった　3 やぶった　4 はった

私の国は **石油** を輸入しています。  
　1 いしゅ　2 せきそう　3 せきゆ　4 いしう

3. 卒業式には住徒の **父母** たちもたくさん来ていた。  
　1 ふば　2 ふぼ　3 ふうぼ　4 ちちば

この町の主要な産業は何ですか。  
　1 じゅちょう　2 しゅおう　3 じゅよう　4 しゅよう

これは **加熱** して食べてください。  
　1 かわつ　2 かねつ　3 かいねつ　4 かいあつ

川はあの **辺り** で **深く** なっている。  
　1 ふかく　2 あさく　3 ひろく　4 せまく

失礼なことを言われたので、つい **感情的** になってしまった。  
　1 がんじょうてき　2 かんじょうてき　3 かんしょうてき　4 がんしょうてき

これは **残さない** でください。
　1 なさないで　2 よこさないで　3 ごぼさないで　4 のこさないで
"""

def kanji_reading(word, vocab):

    online_search = online_search_node_builder()

    generator = generation_node_builder(vocab_dict=vocab,
                                        llm=azure_llm,
                                        prompt_text=teacher_prompt,
                                        example=example)

    reflector = reflection_node_builder(llm=azure_llm)

    formatter = formatter_node_builder(llm=azure_llm, OutType=SimpleChoiceQuestionOutput)

    nodes = {
        "online_search": online_search,
        "generator": generator,
        "reflector": reflector,
        "formatter": formatter
    }

    builder = StateGraph(SimpleQuestionState)

    graph = build_kanji_graph(builder, nodes)

    instance = graph.invoke(
        {"messages": [HumanMessage(content=word)]},
        config={"configurable": {"thread_id": "1"}}
    )

    return json.dumps(instance['formatted_output'], indent=4, ensure_ascii=False)


if __name__ == "__main__":
    n3_vocab = collect_vocabulary("../../Vocab/n3.csv")
    random_word = random.choice(list(json.loads(n3_vocab).values()))
    print(kanji_reading(vocab=n3_vocab,
          word=random_word))


