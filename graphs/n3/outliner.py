from graphs.common.ExamGenerator import ExamGenerator
from langchain_core.prompts import ChatPromptTemplate
from graphs.common.Schema import *

full_exam_instruction = """
Section 1: vocabulary
- 問題1 のことばの読み方として最もよいものを、1・2・3・4から一つえらびなさい (kanji_reading) 8 questions in total: 3 are nouns, 3 are verbs, 1 is an adjective, and 1 is an adverb
- 問題2 このことばを漢字で書くとき、最もよいものを、1・2・3・4から一つえらびなさい (write_kanji) 6 questions in total: 2 nouns, 2 verbs, 1 adjective, and 1 adverb.
- 問題3（　）に入れるのに最もよいものを、1・2・3・4から一つえらびなさい。 (word_meaning) 11 questions in total: 4 are nouns, 4 are verbs, 2 are adjectives, and 1 is an adverb.
- 問題4 に意味が最も近いものを、1・2・3・4から一つえらびなさい。(synonym_substitution) 5 questions in total: 2 are nouns, 2 are verbs, and 1 is an adjective.
- 問題5 つぎのことばの使い方として最もよいものを、1・2・3・4から一つえらびなさい。 (word_usage) 5 questions in total: 3 noun, and 2 verbs.

Section 2: Grammar
- 問題6 つぎの文の（　　　）に入れるのに最もよいものを、１・２・３・４から一つえらびなさい。(sentence_grammar) 13 questions in total: the first 1 is honorific speech, next 1 adverb, 1 auxiliary word, and other 10 different sentence structures
- 問題7 つぎの文の ★ に入る最もよいものを、1・2・3・4から一つえらびなさい。(sentence_sort) 5 questions in total.
- 問題8 つぎの文章を読んで、文章全体の内容を考えて、文中の 19 から 22 の中に入る最もよいものを、1・2・3・4から一つえらびなさい (sentence_structure) 1 question

Section 3: Reading Comprehension
- 問題1-1 つぎの文章を読んで、質問に答えなさい。答えは、1・2・3・4から最もよいものを一つえらびなさい (short_passage_mail_read): 1 article
- 問題1-2 つぎの文章を読んで、質問に答えなさい。答えは、1・2・3・4から最もよいものを一つえらびなさい (short_passage_notification_read): 1 article
- 問題1-3 つぎの文章を読んで、質問に答えなさい。答えは、1・2・3・4から最もよいものを一つえらびなさい (short_passage_narrative_read): 2 articles
- 問題2 つぎの(1)と(2)の文章を読んで、質問に答えなさい。答えは、1・2・3・4から最もよいものを一つえらびなさい。 (midsize_passage_read): 2 articles
- 問題3 つぎの文章を読んで、質問に答えなさい。答えは、1・2・3・4から最もよいものを一つえらびなさい。(long_passage_read): 1 article
- 問題4 これを読んで、下の質問に答えなさい。答えは、1・2・3・4から最もよいものを一つえらびなさい Information retrieval (info_retrieval): 1 article

Section 4: Listening Comprehension
- 問題1-1 では、まず質問を聞いてください。それから話を聞いて、問題用紙の1から4の中から、最もよいものを一つえらんでください。 (topic_understanding_img): 2 questions
- 問題1-2 では、まず質問を聞いてください。それから話を聞いて、問題用紙の1から4の中から、最もよいものを一つえらんでください。 (topic_understanding_txt): 4 questions
- 問題2 では、まず質問を聞いてください。そのあと、問題用紙を見てください。読む時間があります。それから話を聞いて、問題用紙の1から4の中から、最もよいものを一つえらんでください。 (keypoint_understanding): 6 question
- 問題3では、問題用紙（もんだいようし）に何（なに）も いんさつされていません。この問題（もんだい）は、ぜんたいとして どんな ないようかを聞（き）く 問題（もんだい）です。話（はなし）の前（まえ）に 質問（しつもん）は ありません。まず 話（はなし）を 聞（き）いてください。それから、質問（しつもん）と せんたくし を聞（き）いて、1から4の中（なか）から、最（もっと）も よい ものを 一（ひと）つ えらんでください。(summary_understanding) 3 questions
- 問題4 では、元を見ながら質問を聞いてください。やじるし（➔）の人は何と言いますか。1 から 3 の中から、最もよいものを一つえらんでください。 (active_expression): 4 questions
- 問題5 では、問題用紙に何もいんさつしていません。まず文を聞いてください。それから、そのへんしを聞いて、1 から 3 の中から、最もよいものを一つえらんでください。 (immediate_ack): 9 questions
"""

full_exam_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            (
                "You are a Japanese teacher tasked with creating an outline for a JLPT N3 level exam paper."
                "The overall difficulty should be appropriate for the N3 level.\n"
                "The exam paper should include a mix of moderately difficult and very difficult topics to accurately assess proficiency.\n\n"
                "Please ensure the following requirements are met:\n\n"
                "subsection_title in Subsection must be written in English.\n\n only keep English name in () from the Instruction as subsection_title"
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
                f"Instruction: {full_exam_instruction}"
            ),
        ),
        ("user", "TopicList: {topic_list}, vocabulary: {vocab_dict}, GrammarList: {grammar_list}"),
    ]
)

fast_exam_instruction = """
Section 1: vocabulary
- 問題1 のことばの読み方として最もよいものを、1・2・3・4から一つえらびなさい (kanji_reading) 2 questions in total
- 問題2 このことばを漢字で書くとき、最もよいものを、1・2・3・4から一つえらびなさい (write_kanji) 2 questions in total
- 問題3（　）に入れるのに最もよいものを、1・2・3・4から一つえらびなさい。 (word_meaning) 2 questions in total
- 問題4 に意味が最も近いものを、1・2・3・4から一つえらびなさい。(synonym_substitution) 2 questions in total
- 問題5 つぎのことばの使い方として最もよいものを、1・2・3・4から一つえらびなさい。 (word_usage) 2 questions in total

Section 2: Grammar
- 問題6 つぎの文の（　　　）に入れるのに最もよいものを、１・２・３・４から一つえらびなさい。(sentence_grammar) 2 questions in total
- 問題7 つぎの文の ★ に入る最もよいものを、1・2・3・4から一つえらびなさい。(sentence_sort) 2 questions in total
- 問題8 つぎの文章を読んで、文章全体の内容を考えて、文中の 19 から 22 の中に入る最もよいものを、1・2・3・4から一つえらびなさい (sentence_structure) 1 question

Section 3: Reading Comprehension
- 問題1-1 つぎの文章を読んで、質問に答えなさい。答えは、1・2・3・4から最もよいものを一つえらびなさい (short_passage_mail_read): 1 article
- 問題1-2 つぎの文章を読んで、質問に答えなさい。答えは、1・2・3・4から最もよいものを一つえらびなさい (short_passage_notification_read): 1 article
- 問題1-3 つぎの文章を読んで、質問に答えなさい。答えは、1・2・3・4から最もよいものを一つえらびなさい (short_passage_narrative_read): 1 article
- 問題2 つぎの(1)と(2)の文章を読んで、質問に答えなさい。答えは、1・2・3・4から最もよいものを一つえらびなさい。 (midsize_passage_read): 1 article
- 問題3 つぎの文章を読んで、質問に答えなさい。答えは、1・2・3・4から最もよいものを一つえらびなさい。(long_passage_read): 1 article
- 問題4 これを読んで、下の質問に答えなさい。答えは、1・2・3・4から最もよいものを一つえらびなさい Information retrieval (info_retrieval): 1 article

Section 4: Listening Comprehension
- 問題1-1 では、まず質問を聞いてください。それから話を聞いて、問題用紙の1から4の中から、最もよいものを一つえらんでください。 (topic_understanding_txt): 1 question
- 問題1-2 では、まず質問を聞いてください。それから話を聞いて、問題用紙の1から4の中から、最もよいものを一つえらんでください。 (topic_understanding_img): 1 question
- 問題2 では、まず質問を聞いてください。そのあと、問題用紙を見てください。読む時間があります。それから話を聞いて、問題用紙の1から4の中から、最もよいものを一つえらんでください。 (keypoint_understanding): 1 question
- 問題3では、問題用紙（もんだいようし）に何（なに）も いんさつされていません。この問題（もんだい）は、ぜんたいとして どんな ないようかを聞（き）く 問題（もんだい）です。話（はなし）の前（まえ）に 質問（しつもん）は ありません。まず 話（はなし）を 聞（き）いてください。それから、質問（しつもん）と せんたくし を聞（き）いて、1から4の中（なか）から、最（もっと）も よい ものを 一（ひと）つ えらんでください。(summary_understanding) 1 question
- 問題4 では、元を見ながら質問を聞いてください。やじるし（➔）の人は何と言いますか。1 から 3 の中から、最もよいものを一つえらんでください。 (active_expression): 1 question
- 問題5 では、問題用紙に何もいんさつしていません。まず文を聞いてください。それから、そのへんしを聞いて、1 から 3 の中から、最もよいものを一つえらんでください。 (immediate_ack): 1 question
"""

fast_exam_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            (
                "You are a Japanese teacher tasked with creating an outline for a JLPT N3 level exam paper."
                "The overall difficulty should be appropriate for the N3 level.\n"
                "The exam paper should include a mix of moderately difficult and very difficult topics to accurately assess proficiency.\n\n"
                "Please ensure the following requirements are met:\n\n"
                "subsection_title in Subsection must be written in English.\n\n only keep English name in () from the Instruction as subsection_title"
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
                f"Instruction: {fast_exam_instruction}"
            ),
        ),
        ("user", "TopicList: {topic_list}, vocabulary: {vocab_dict}, GrammarList: {grammar_list}"),
    ]
)

vocab_instruction = """
Section 1: vocabulary
- 問題1 のことばの読み方として最もよいものを、1・2・3・4から一つえらびなさい (kanji_reading) 8 questions in total: 3 are nouns, 3 are verbs, 1 is an adjective, and 1 is an adverb
- 問題2 このことばを漢字で書くとき、最もよいものを、1・2・3・4から一つえらびなさい (write_kanji) 6 questions in total: 2 nouns, 2 verbs, 1 adjective, and 1 adverb.
- 問題3（　）に入れるのに最もよいものを、1・2・3・4から一つえらびなさい。 (word_meaning) 11 questions in total: 4 are nouns, 4 are verbs, 2 are adjectives, and 1 is an adverb.
- 問題4 に意味が最も近いものを、1・2・3・4から一つえらびなさい。(synonym_substitution) 5 questions in total: 2 are nouns, 2 are verbs, and 1 is an adjective.
- 問題5 つぎのことばの使い方として最もよいものを、1・2・3・4から一つえらびなさい。 (word_usage) 5 questions in total: 3 noun, and 2 verbs.
"""

vocab_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            (
                "You are a Japanese teacher tasked with creating an outline for a JLPT N3 level exam paper."
                "The overall difficulty should be appropriate for the N3 level.\n"
                "The exam paper should include a mix of moderately difficult and very difficult topics to accurately assess proficiency.\n\n"
                "Please ensure the following requirements are met:\n\n"
                "subsection_title in Subsection must be written in English.\n\n only keep English name in () from the Instruction as subsection_title"
                "For Section 1 - vocabulary:\n"
                "- Select vocabulary words from the 'vocabulary' list, ensuring that 80% of the topics are very difficult.\n"
                "- The topic words in 問題1 (kanji_reading) and 問題5 (word_usage) must be written in Kanji while other topic words use Japanese kana.\n"
                "- Don't pick GrammarList"
                "Additionally:\n"
                "- Each topic word should be unique and must not be repeated in the outline.\n"
                "- Follow the provided exam instructions carefully to determine the number of questions and content for each section.\n"
                "- Finally, write the full outline of the examination paper in Japanese, including question topics as per the instructions.\n\n"
                f"Instruction: {vocab_instruction}"
            ),
        ),
        ("user", "TopicList: {topic_list}, vocabulary: {vocab_dict}, GrammarList: {grammar_list}"),
    ]
)

grammar_instruction = """
Section 2: Grammar
- 問題6 つぎの文の（　　　）に入れるのに最もよいものを、１・２・３・４から一つえらびなさい。(sentence_grammar) 13 questions in total: the first 1 is honorific speech, next 1 adverb, 1 auxiliary word, and other 10 different sentence structures
- 問題7 つぎの文の ★ に入る最もよいものを、1・2・3・4から一つえらびなさい。(sentence_sort) 5 questions in total.
- 問題8 つぎの文章を読んで、文章全体の内容を考えて、文中の 19 から 22 の中に入る最もよいものを、1・2・3・4から一つえらびなさい (sentence_structure) 1 question
"""

grammar_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            (
                "You are a Japanese teacher tasked with creating an outline for a JLPT N3 level exam paper."
                "The overall difficulty should be appropriate for the N3 level.\n"
                "The exam paper should include a mix of moderately difficult and very difficult topics to accurately assess proficiency.\n\n"
                "Please ensure the following requirements are met:\n\n"
                "subsection_title in Subsection must be written in English.\n\n only keep English name in () from the Instruction as subsection_title"
                "For Section 2 - Grammar:\n"
                "- Randomly select topics from 'TopicList' and grammars from 'GrammarList'.\n"
                "- For 問題8, include one question that integrates 4 different grammar points.\n"
                "- The grammar used must be appropriate and consistent with the chosen topic.\n\n"
                "Additionally:\n"
                "- Each topic word should be unique and must not be repeated in the outline.\n"
                "- Follow the provided exam instructions carefully to determine the number of questions and content for each section.\n"
                "- Finally, write the full outline of the examination paper in Japanese, including question topics as per the instructions.\n\n"
                f"Instruction: {grammar_instruction}"
            ),
        ),
        ("user", "TopicList: {topic_list}, vocabulary: {vocab_dict}, GrammarList: {grammar_list}"),
    ]
)

reading_instruction = """
Section 3: Reading Comprehension
- 問題1-1 つぎの文章を読んで、質問に答えなさい。答えは、1・2・3・4から最もよいものを一つえらびなさい (short_passage_mail_read): 1 article
- 問題1-2 つぎの文章を読んで、質問に答えなさい。答えは、1・2・3・4から最もよいものを一つえらびなさい (short_passage_notification_read): 1 article
- 問題1-3 つぎの文章を読んで、質問に答えなさい。答えは、1・2・3・4から最もよいものを一つえらびなさい (short_passage_narrative_read): 2 articles
- 問題2 つぎの(1)と(2)の文章を読んで、質問に答えなさい。答えは、1・2・3・4から最もよいものを一つえらびなさい。 (midsize_passage_read): 2 articles
- 問題3 つぎの文章を読んで、質問に答えなさい。答えは、1・2・3・4から最もよいものを一つえらびなさい。(long_passage_read): 1 article
- 問題4 これを読んで、下の質問に答えなさい。答えは、1・2・3・4から最もよいものを一つえらびなさい Information retrieval (info_retrieval): 1 article
"""

reading_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            (
                "You are a Japanese teacher tasked with creating an outline for a JLPT N3 level exam paper."
                "The overall difficulty should be appropriate for the N3 level.\n"
                "The exam paper should include a mix of moderately difficult and very difficult topics to accurately assess proficiency.\n\n"
                "Please ensure the following requirements are met:\n\n"
                "subsection_title in Subsection must be written in English.\n\n only keep English name in () from the Instruction as subsection_title"
                "For Section 3 - Reading Comprehension and Listening Comprehension:\n"
                "- Randomly choose topics from 'TopicList'.\n\n"
                "- Don't pick GrammarList"
                "Additionally:\n"
                "- Each topic word should be unique and must not be repeated in the outline.\n"
                "- Follow the provided exam instructions carefully to determine the number of questions and content for each section.\n"
                "- Finally, write the full outline of the examination paper in Japanese, including question topics as per the instructions.\n\n"
                f"Instruction: {reading_instruction}"
            ),
        ),
        ("user", "TopicList: {topic_list}, vocabulary: {vocab_dict}, GrammarList: {grammar_list}"),
    ]
)

listening_instruction = """
Section 4: Listening Comprehension
- 問題1-1 では、まず質問を聞いてください。それから話を聞いて、問題用紙の1から4の中から、最もよいものを一つえらんでください。 (topic_understanding_img): 2 questions
- 問題1-2 では、まず質問を聞いてください。それから話を聞いて、問題用紙の1から4の中から、最もよいものを一つえらんでください。 (topic_understanding_txt): 4 questions
- 問題2 では、まず質問を聞いてください。そのあと、問題用紙を見てください。読む時間があります。それから話を聞いて、問題用紙の1から4の中から、最もよいものを一つえらんでください。 (keypoint_understanding): 6 question
- 問題3では、問題用紙（もんだいようし）に何（なに）も いんさつされていません。この問題（もんだい）は、ぜんたいとして どんな ないようかを聞（き）く 問題（もんだい）です。話（はなし）の前（まえ）に 質問（しつもん）は ありません。まず 話（はなし）を 聞（き）いてください。それから、質問（しつもん）と せんたくし を聞（き）いて、1から4の中（なか）から、最（もっと）も よい ものを 一（ひと）つ えらんでください。(summary_understanding) 3 questions
- 問題4 では、元を見ながら質問を聞いてください。やじるし（➔）の人は何と言いますか。1 から 3 の中から、最もよいものを一つえらんでください。 (active_expression): 4 questions
- 問題5 では、問題用紙に何もいんさつしていません。まず文を聞いてください。それから、そのへんしを聞いて、1 から 3 の中から、最もよいものを一つえらんでください。 (immediate_ack): 9 questions
"""

listening_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            (
                "You are a Japanese teacher tasked with creating an outline for a JLPT N3 level exam paper."
                "The overall difficulty should be appropriate for the N3 level.\n"
                "The exam paper should include a mix of moderately difficult and very difficult topics to accurately assess proficiency.\n\n"
                "Please ensure the following requirements are met:\n\n"
                "subsection_title in Subsection must be written in English.\n\n only keep English name in () from the Instruction as subsection_title"
                "For Section 4: Listening Comprehension:\n"
                "- Randomly choose topics from 'TopicList'.\n\n"
                "- Don't pick GrammarList"
                "Additionally:\n"
                "- Each topic word should be unique and must not be repeated in the outline.\n"
                "- Follow the provided exam instructions carefully to determine the number of questions and content for each section.\n"
                "- Finally, write the full outline of the examination paper in Japanese, including question topics as per the instructions.\n\n"
                f"Instruction: {listening_instruction}"
            ),
        ),
        ("user", "TopicList: {topic_list}, vocabulary: {vocab_dict}, GrammarList: {grammar_list}"),
    ]
)

def run(level: str, exam_type: ExamType):

    PROMPT_REGISTRY: dict[str, ChatPromptTemplate] = {
        "full_exam": full_exam_prompt,
        "fast_exam": fast_exam_prompt,
        "reading": reading_prompt,
        "listening": listening_prompt,
        "grammar": grammar_prompt,
        "vocab": vocab_prompt,
    }

    prompt = PROMPT_REGISTRY.get(exam_type.lower())  # make it case-insensitive
    if not prompt:
        raise ValueError(f"No prompt defined for exam_type: {exam_type}")

    exam_generator = ExamGenerator(level=level, exam_type=exam_type, db_collection=f"{level}_{exam_type}")
    inserted_id, outline = exam_generator._generate_and_store_paper(instruction=prompt)

    if inserted_id:
        print(f"✅ Exam outline stored successfully! Document ID: {inserted_id}")
    else:
        print("❌ Failed to generate or store exam outline. Check logs for details.")

    # Optionally inspect the outline object
    if outline:
        print("\nGenerated Outline:")
        print(outline)