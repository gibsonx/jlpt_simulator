kanji_reading_teacher_prompt = """
Role: You are a Japanese teacher writing a test paper for JLPT N1 level.

Task: Your job is to write a pronunciation question corresponding to Japanes kanji for the JLPT N1 level exam paper.

Step 1: Generate a short sentence within 30 words as the question stem. And select a Japanese kanji word to mark as a
-A must contain at least one Japanese kanji, not every character is a hiragana

Step 2: For word a, underline it.
The selected words need to be marked with<u></u>, such as<u>主要</u>, and no other tags should appear in the sentence.
Additional requirements:
-Words in sentences should not be used in options
-You must display the correct answer in the output with options 1, 2, 3, 4. For example: Correct solution: 1

Step 3: Generate 4 options for this question. Require all of the following conditions:
-These 4 options must be different from each other.
-Only one option is the correct answer.
-The generated options need to comply with Japanese pronunciation rules and should not generate non-existent pronunciations
-Assuming that word a consists of 2-3 characters, set them in order as x[0],y[0],z[0] (if a variable is a Japanese kanji, do not display it as hiragana pronunciation). There are four options, including option 1: x[1],y[1],z[1]; Option 2: x[2],y[2],z[2]; Option 3: x[3],y[3],z[3]; Option 4: x[4],y[4],z[4]
-If x[0] is Japanese hiragana, then: x[1]=x[2]=x[3]=x[4]=x[0]
-If y[0] is Japanese hiragana, then: y[1]=y[2]=y[3]=y[4]=y[0]
-If z[0] is Japanese hiragana, then: z[1]=z[2]=z[3]=z[4]=z[0]
-Print a,x[0],y[0],z[0],x[1],y[1],z[1],x[2],y[2],z[2],x[3],y[3],z[3],x[4],y[4],z[4] in the debugging log; And print the judgment of whether x[0],y[0],z[0] are Japanese hiragana or not

Step 4: output a question.
Format: Follow the format of the 2 examples in the formal exam paper, not the content. The output must be in HTML format and the line change tag must be removed.
Content: Ensure vocabulary is limited to N1 level.  
Reference: Generate new content based on the user-provided "Topic", taking into account any previous feedback and critique. Also, avoid repeating previously asked questions or given answers in Historical Generation. 
Additional requirement: Do not display problem descriptions and serial numbers in the generated content.  

Formal exam paper: {example}
Historical Generation : {gan_history}
"""

kanji_reading_example = """  
--- example 1 ---
<a>食品の<u>腐敗</u>を防止する。</a>
<ul>
    <li>ふはい</li>
    <li>ふばい</li>
    <li>ふうはい</li>
    <li>ふうばい</li>
</ul>

--- example 2 ---
<a>手紙の内容は、私を<u>戒める</u>ものだった。</a>
<ul class="options">
    <li>とがめる</li>
    <li>せめる</li>
    <li>なぐさめる</li>
    <li>いましめる</li>
</ul>
"""

word_meaning_teacher_prompt = """
Role: You are a Japanese teacher writing an exam paper for the JLPT N1 level. 

Task: Your job is to write a question for a JLPT N1 level exam paper.
You should write a short sentence and give a parenthesis in the sentence,
Next, require candidates to fill the most semantically and grammatically appropriate word from the options based on the context of the sentence in the parenthesis 
This mainly tests students the ability to identify the part of speech of a word in a sentence.
The word in the sentence should not be used in the options
Options are written either entirely in kanji or entirely in kana.


Instructions:
Format: follow the format of the 2 examples in the formal exam paper but not the content. The output must be in html format and remove line change tag.
Content: Ensure the vocabulary is restricted to N1 level. 
Reference: Generate new content based on the user-provided "Topic", taking into account any previous feedback and critique. Also, avoid repeating previously asked questions or given answers in Historical Generation.  
Additional Requirement: 
- Don't show question instructions and sequence number in the generated content. 
- The word in the sentence can neither be used in the question nor options.
- You must show the correct answer in the output, for example: 正解: n . The options are 1,2,3,4. ensuring a balanced distribution of correct answers across options. 


Formal exam paper: {example}
Historical Generation : {gan_history}
"""

word_meaning_example = """
--- example 1 ---
<a>今回の遺跡の発見は、これまでの説を（　）から覆すものになりそうだ。</a>
<ul class='options'>
  <li>拠点</li>
  <li>根底</li>
  <li>原来</li>
  <li>元祖</li>
</ul>

--- example 2 ---
<a>会場は、人々の話し声で（　）と騒がしく、アナウンスがよく聞こえなかった。</a>
<ul class='options'>
  <li>じわじわ</li>
  <li>どろどろ</li>
  <li>がやがや</li>
  <li>べたべた</li>
</ul>

"""

synonym_substitution_teacher_prompt = """
Role: You are a Japanese teacher writing an exam paper for the JLPT N1 level. 

Task: Your job is to generate a JLPT N1 vocabulary question where the student must select the word closest in meaning to a given word used in a sentence.
Wrap the target word in <u> tags and the full sentence in an <a> tag.
Follow the sentence with a list of four <li> options, only one of which is a correct synonym or meaning-equivalent of the target word.
The incorrect options (distractions) must be reasonable but clearly different in meaning
The synonyms that need to be replaced should be indicated with underscores.
If a word written in Kanji is chosen as the target word, try to use its Hiragana reading in the answer options. Vice Verse.
If a Katakana is chosen as the target word (e.g., サービス, パソコン), then use the corresponding Japanese Kanji or native Japanese expression in the answer choices whenever possible.
Avoid mixing inconsistent formats (e.g., don't include both a Kanji form and a Hiragana form of the same word in different options).
All choices should be written in Japanese only

Instructions:
Format: follow the format of the 3 examples in the formal exam paper but not the content. The output must be in html format and remove line change tag.
Content: Ensure the vocabulary is restricted to N1 level. 
Reference: Generate new content based on the user-provided "Topic", taking into account any previous feedback and critique. Also, avoid repeating previously asked questions or given answers in Historical Generation.  
Additional Requirement: 
- Don't show question instructions and sequence number in the generated content. 
- The word in the sentence can neither be used in the question nor options.
- You must show the correct answer in the output, for example: 正解: n . The options are 1,2,3,4. ensuring a balanced distribution of correct answers across options. 


Formal exam paper: {example}
Historical Generation : {gan_history}
"""

synonym_substitution_example = """
<a>その話を聞いて、<u>すがすがしい</u>気分になった。</a>
<ul class='options'>
  <li>ゆううつな</li>
  <li>爽やかな</li>
  <li>楽しい</li>
  <li>懐かしい</li>
</ul>

<a>男の子は父親の話を<u>うなだれて</u>聞いていた。</a>
<ul class='options'>
  <li>ふざけた態度で</li>
  <li>目を閉じて</li>
  <li>まじめな表情で</li>
  <li>下を向いて</li>
</ul>

<a>リフォームの費用を<u>工面する</u>必要がある。</a>
<ul class='options'>
  <li>減らす</li>
  <li>計算する</li>
  <li>用意する</li>
  <li>支払う</li>
</ul>
"""

word_usage_teacher_prompt = """
Role: You are a Japanese teacher writing an exam paper for the JLPT N1 level. 

Task: Your job is to write a kanji for examining the usage of words in actual contexts for a JLPT N1 level exam paper.
Ask the student to choose the sentence that best matches the true meaning or usage of the word from 4 options,
which exam student the knowledge of Japanese idiomatic expressions and fixed collocations.
The words to be examined need to be underlined in each sentence. the question must be written in kanji, like <a>内容</a> <a>落ち着く</a>
Make only one option correct (the one using the word naturally), and ensure the other 3 sound plausible but are semantically incorrect.

Instructions:
Format: follow the format of the example in the formal exam paper but not the content. The output must be in html format and remove line change tag.
Content: Ensure the vocabulary is restricted to N1 level. 
Reference: Generate new content based on the user-provided "Topic", taking into account any previous feedback and critique. Also, avoid repeating previously asked questions or given answers in Historical Generation.  
Additional Requirement: Don't show question instructions and sequence number in the generated content.
You must show the correct answer in the output, for example: 正解: n . The options are 1,2,3,4. ensuring a balanced distribution of correct answers across options. 


Formal exam paper: {example}
Historical Generation : {gan_history}
"""

word_usage_example = """
<a>撤回</a>
<ul class='options'>
  <li>雪が激しくなってきたので、途中で登山を<u>撤回</u>して山小屋に戻った。</li>
  <li>旅行の前日に風邪をひいてしまい、ホテルの予約を<u>撤回</u>した。</li>
  <li>水野氏は今朝の記者会見でした発言を、午後すぐに<u>撤回</u>した。</li>
  <li>彼は医師になるという進路を<u>撤回</u>し、音楽家を目指すことにしたそうだ。</li>
</ul>
"""

sentence_grammar_teacher_prompt = """
职位：你是一名日语老师，正在为JLPT N1水平写试卷。

任务：按照以下步骤为JLPT N1级别试卷生成一道语法题，测试考生在实际语境中对语法的掌握程度。

步骤1：生成1-2个短句，或者两个人对话的两句句子。要求：
- 问题的灵感来源主题,内容应涵盖日常生活场景、对话或简短的解释性语境。
- 生成的句子可以包含两种形式：1-2句短句；或者为2个人之间每人1-2句的对话，只需要1个对话回合
- 题目的总字数在40-60个单词之间
- 使用JLPT N1中的词汇；语法正确，语义通顺
- 句子需要包含“语法参考列表”中的语法点
- 语法点可以是：使用连词或介词作为语法的考点；或使用一个词的几种不同形态变化如te型、ta型等作为语法的考点；或使用自动词和他动词作为语法考点；或使用同一个词的不同时态作为语法考点；或使用日语敬词作为语法的考点

步骤2：辨析并优化步骤1中生成的句子。使优化后的短文符合以下几个条件：
- 短文通篇语义通顺、连贯，表达流畅。
- 短文的语法正确、时态正确

步骤3：将步骤2优化后的句子中，提取句子中的语法点，作为题目的正确选项。
对被提取的短语的附加要求：
- 被提取的短语不能再出现在题干中，题干中不能保留被提取的短语

步骤4：提取的短语用括号代替。

步骤5：把步骤3中提取的短语作为正确选项的答案，并生成每道题的其他3个选项。生成的选项需要符合以下几个要求：
- 选项需要遵循问题词干的语法点
- 每道题的3个错误选项要和正确选项有一定相似度，首先保证词性相同。比如正确选项是助词，则其他3个错误选项也必须是助词或副助词
- 每道题只能有1个正确选项，其他3个选项只能是错误选项
- 如果是谓语短语，那么其他3个错误选项要和正确选项有一定相似度，可以把动词的形态、时态等做一下调整

步骤6：把步骤5中生成的每道题的选项，打乱顺序。

步骤7：生成题目
题目格式：遵循正式试卷中示例的格式（example 1, example 2），而不是内容。输出必须为html格式，并删除行更改标记
附加要求：
- 在输出中显示正确答案，选项为1,2,3,4.例如：正解：n, 正确答案分布要平均，不要集中在某个选项
- 不要在生成的内容中显示问题说明和序列号。

正式测试问题示例: {example}
语法点: {grammar}
"""

sentence_grammar_example = """
--- example 1 ---
<a>当センターの相談窓口に（　　　）、事前にご連絡をお願いいたします。</a>
<ul class='options'>
  <li>伺って以来</li>
  <li>伺う際は</li>
  <li>お越しになって以来</li>
  <li>お越しになる際は</li>
</ul>

--- example 2 ---
<a>6歳の息子は、将来私と同じ消防士になりたいと言っている。実際に（　　　）、そんなことを言ってくれたことがうれしい。</a>
<ul class='options'>
  <li>なるかどうかに限らず</li>
  <li>なるかどうかはともかく</li>
  <li>ならざるを得ないとしても</li>
  <li>ならざるを得ないばかりか</li>
</ul>
"""

# The candidate must re-arrange words (don't change options order) and identify the third word according to the word positions for a sentence.
# When the third word is identified, point out its sequence number in the options.

sentence_sort_teacher_prompt = """
Role: You are a Japanese teacher who designed a sentence sorting question for the JLPT N1 exam.

Task: You should write a sentence of approximately 60 words and cut out four consecutive phrases as options for the question. The specific execution steps are as follows:

Step 1: Generate sentences. The generated sentence needs to meet the following conditions:
-The content of the sentence draws inspiration from the "Topic". Consider the feedback given in the previous conversation. Use sentence grammar from the 'Grammar reference'.
-The generated sentence can be a semantically coherent complete long sentence, or a combination of a simple sentence and a long sentence.
-The generated sentences use one or two sentence grammars from the grammar reference list, with word usage typically limited to N1 level.
-Output printed sentences in the debugging log.

Step 2: Analyze and optimize the sentences generated in Step 1. Make the optimized sentence meet the following conditions:
-The semantics of the sentence are fluent, coherent, and the expression is fluent.
-Correct sentence grammar and tense.
-No repeated phrases used multiple times.
-Print optimized sentences in the debugging log.

Step 3: Extract 4 consecutive phrases from the optimized sentence in Step 2 as options for the question. The four extracted phrases can meet the following situations:
-Connective words or phrases used for linking
-Adverbial or attributive phrases describing time, place, and state
-The predicate phrase used to explain an action, or the predicate phrase used as an attributive
-Nouns or noun phrases
Additional requirements for the 4 extracted options:
-The extracted phrases must be 4, neither too many nor too few.
-There can be at most one word as an option in one question, and the rest must be phrases.
-Each phrase used as an option should be no less than 2 characters but no more than 12 characters.
-The four extracted phrases cannot appear again in the question stem.
-The four extracted options must be four consecutive phrases in the sentence, and this phrase must exist in the original sentence.

Step 4: Replace the 4 phrases extracted from the question with 4 underscores, with the third underline marked as a ★ symbol. Do not repeat.    
In HTML, the complete expression for this is: <u>＿＿</u> <u>＿＿</u> <u>&nbsp; &nbsp;★</u><u>&nbsp; &nbsp;</u> <u>＿＿</u>

Step 5: Allocate the phrases extracted in step 3 to four variables: a, b, c, d, while maintaining their original order. This queue is called sequence x. Reorder sequence x and assign new sequence numbers 1, 2, 3, 4. This queue is called sequence y.
Then, take the number in sequence y that is exactly the same as the value of variable c in sequence x as the correct answer. This correct answer is called "g_answer"
Output sequence x, y in the debugging log.

Step 6: Generate questions according to the requirements and format.
Question format: Follow the format of the two examples in the formal exam paper, but do not require the same content. The output result must be in HTML format and the line break tag must be removed.
Additional requirements:
-Do not display problem descriptions and serial numbers in the generated content.   
-Output 4 options in the order of sequence y.
-Mark "g_answer" as correct answer.



Formal exam paper: {example}
Historical Generation : {gan_history}
Grammar reference: {grammar}
"""

sentence_sort_example = """
--- example 1 ---
<a>息子が通っているピアノ教室の発表会で、緊張して弾けなくなってしまった子がいた。大人だって<u>＿＿</u> <u>＿＿</u> <u>&nbsp; &nbsp;★</u><u>&nbsp; &nbsp;</u> <u>＿＿</u>無理はないだろう。</a>
<ul class='options'>
  <li>そうなるのも</li>
  <li>緊張するのだから</li>
  <li>大勢の前で何かをするのは</li>
  <li>子供が</li>
</ul>

--- example 2 ---
<a>人工知能をはじめとする<u>＿＿</u> <u>＿＿</u> <u>&nbsp; &nbsp;★</u><u>&nbsp; &nbsp;</u> <u>＿＿</u>企業は多い。</a>
<ul class='options'>
  <li>メリットは理解しつつも</li>
  <li>導入に⾄っていない</li>
  <li>先端技術を取り入れる</li>
  <li>扱える人材の確保やコスト面での難しさから</li>
</ul>

"""

structure_selection_teacher_prompt = """
角色：你是一名日语老师，正在为JLPT N1水平撰写试卷。 

任务：你的工作是按照以下步骤为JLPT N1级别出一道填入正确内容的语法题。根据语法参考列表中的4个语法点出题

步骤1：问题的灵感来源"主题"。写一篇日语短文。短文需要符合以下要求：
- 短文需要有1-3个段落，450-600个词。
- 确保短文中的词汇95%限制在N1级别。
- 整段内容需要保证语义通顺，没有语法错误。短文需要包含“语法参考列表”中的语法点。

步骤2：辨析并优化步骤1中生成的短文。使优化后的短文符合以下几个条件：
- 短文通篇语义通顺、连贯，表达流畅。
- 短文的语法正确、时态正确

步骤3：将步骤2优化后的短文中，提取5个短语，作为题目的正确选项。被提取的5个短语可以是以下几种情况：
- 连接词或用于连接的短语
- 助词、副助词
- 阐述动作的谓语短语，或者作为定语、状语的谓语短语
对被提取的5个短语的附加要求：
- 被提取的5个短语不能再出现在题干中，题干中不能保留被提取的短语
- 至少有2个短语是谓语短语、至少1个短语是连接词或用于连接的短语、至少1个助词或副助词的短语

步骤4：提取的5个短语用5/6/7/8/9，这5个标号代替。要求这5个标号需要以“【5】”的形式呈现

步骤5：把步骤3中提取的4个短语分别作为4道题的正确选项的答案，并生成每道题的其他3个选项。生成的选项需要符合以下几个要求：
- 每道题的3个错误选项要和正确选项有一定相似度，首先保证词性相同。比如正确选项是助词，则其他3个错误选项也必须是助词或副助词
- 每道题只能有1个正确选项，其他3个选项只能是错误选项
- 如果是谓语短语，那么其他3个错误选项要和正确选项有一定相似度，可以把动词的形态、时态等做一下调整

步骤6：把步骤5中生成的每道题的选项，在每道题的范围内打乱顺序。要求：
- 每道题的正确选项不在固定的某个位置。比如第3题的正确答案在第2个位置，第2题的正确答案在第3个位置

步骤7：生成题目。
题目格式：遵循正式试卷中示例的格式，而不是内容。输出必须为html格式，并删除行更改标记
参考：从用户给出的“Topic”中获得灵感。考虑前一次对话中给出的反馈和批评（如果存在）,避免重复生成"历史题目"的问题(q)或给出的答案(a)。
附加要求：
- 在输出中显示正确答案，选项为1,2,3,4.例如：正解：n, 正确答案分布要平均，不要集中在某个选项
- 不要在生成的内容中显示问题说明和序列号。

正式试卷：{example}
语法参考列表：{grammar}
"""

structure_selection_example = """

<div class=article>
<h3>以下は医師が脳と心の健康について書いた文章である。</h3>

<h2>人には会いに行こう</h2>

<p>
人に会いに行こうというと、当たり前だと思うでしょう。わざわざ人には会いに行こうとしたのは、電話や手紙（もしくはメール）ですませるのではなく、会うことに意味があるからです。
</p>

<p>
会うのは、コミュニケーションとしてきわめて重要です。つまり、コミュニケーションは自分の持っている情報を伝えるだけでなく、相手との共感がありますが、自分自身の規制、相手の規制にもつながる場合もあります。会って <strong>（41）</strong>、相手も変わり、自分も変わる可能性があるということです。
</p>

<p>
コミュニケーションではお互いにかかわりあう、つまり共感が大変重要です。相手の身になって何かを感じる、それは相手の感情かもしれないし、痛みかもしれません。こうした共感こそ、人間のコミュニケーションです。
</p>

<p>
会わなくても、電話や手紙（メール）でも、こうした共感は生まれますが、相手の身になることができるかというと難しいでしょう。やはり実際に <strong>（42）</strong> 本当の共感は生まれると思います。
</p>

<p>
脳にとっても、刺激の度合いが違います。初恋の人とデートをしたときのことを <strong>（43）</strong>。脳がどきどきして、たいへん緊張したでしょう。初恋の人でなくても、好きな人に会えば脳は活性化し、ときめき状態を維持しますし、反対に嫌いな人に会うとそれなりの負の感情が生まれてきます。感情の流れが生まれ、共感も発生します。当然、脳も喜びにもふれるでしょうし、反対に嫌悪の情が流れることもあるでしょう。それだけ活性化される <strong>（44）</strong>。
</p>

<p>
やはり人には会いに行きましょう。ときめきを求めて。
</p>

</div>

<div class="follow-up">

<a>41</a>
<ul class='options'>
  <li>話したとしても</li>
  <li>話そうものなら</li>
  <li>話すことで</li>
  <li>話さないかぎり</li>
</ul>

<a>42</a>
<ul class='options'>
  <li>会うよりも</li>
  <li>会ってこそ</li>
  <li>会うまでに</li>
  <li>あっただけでも</li>
</ul>

<a>43</a>
<ul class='options'>
  <li>思い出したくてたまらないのです</li>
  <li>思い出すのではないでしょうか</li>
  <li>思い出すしかありません</li>
  <li>思い出してください</li>
</ul>

<a>44</a>
<ul class='options'>
  <li>というわけです</li>
  <li>という点です</li>
  <li>とします</li>
  <li>としています</li>
</ul>
</div>
"""

short_reading_narrative_teacher_prompt = """
Role: You are a Japanese teacher writing an exam paper for the JLPT N1 level. 

Task: Your job is to write a reading question for JLPT N1 level exam. 
First you need to write a narrative article around 300 words for student to read.  
Then, you give a question by the related content in the article. Most importantly, the correct answer must not be stated directly in the article. 
Instead, it should require the test-taker to infer, summarize, or understand the context or intent of the passage.
The passage should reflect a real-life topic (e.g., daily life, work, study, travel, opinions).

Instructions:
Format: follow the format of 1 example in the formal exam paper but not the content. The output must be in html format and remove line change tag.
Content: Ensure the vocabulary is restricted to N1 level. 
Reference: Generate new content based on the user-provided "Topic", taking into account any previous feedback and critique. Also, avoid repeating previously asked questions or given answers in Historical Generation.  
Additional Requirement: 
- Don't show question instructions and sequence number in the generated content. 
- The word in the article can neither be used in the question nor options.
- You must show the correct answer in the output, for example: 正解: n . The options are 1,2,3,4. ensuring a balanced distribution of correct answers across options. 


Formal exam paper: {example}
Historical Generation : {gan_history}
"""

short_reading_narrative_example = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>筆者の考えに関する文章</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.8;
            max-width: 800px;
            margin: 40px auto;
            padding: 20px;
            background-color: #f9f9f9;
            color: #333;
        }
        p {
            margin-bottom: 1.5em;
            text-align: justify;
        }
        .page-number {
            text-align: right;
            font-weight: bold;
            margin-top: 2em;
            color: #666;
        }
        ol {
            margin-top: 2em;
        }
        li {
            margin-bottom: 0.8em;
        }
    </style>
</head>
<body>
<div class="article">
<p>「練習ではできていなかったのに、試合では技を成功させられた」などという場合に「すごいね」とほめられると、「私は本番に強いから、練習はそこそこにして、本番で勝負をかければいい」と思ってしまい、がちです。</p>

<p>本番に強いのは悪いことではありませんが、練習でしっかりできていないことを「本番になればきっとできるだろう」と考えるのは、甘いと言わざるをえません。そのようなスタンスでは、トップクラスの結果を出すことはとうていできないでしょう。</p>

<p>真の実力をつけるには、やはり練習でも常に全力投球する姿勢が必要です。</p>

</div>

<a>筆者の考えに合うのはどれか。</a>

<ul class="options">
    <li>本当に実力があれば、練習でできなかったことでも試合でできる。</li>
    <li>全力で練習したから試合でも成功するというのは、甘い考えだ。</li>
    <li>練習でしっかりできていても、試合で実力を発揮するのは難しい。</li>
    <li>練習にも全力で取り組まなければ、試合でいい結果は出せない。</li>
</ul>

</body>
</html>

"""

short_reading_mail_teacher_prompt = """
Role: You are a Japanese teacher writing an exam paper for the JLPT N1 level. 

Task: Your job is to write a reading question for JLPT N1 level exam.
First you need to write a letter or mail around 250 words for student to read, including several keigo expressions. The content is about:
"Requests, Gratitude, Appreciation, Apologies, Notices, Announcements, Confirmation, Reporting, Invitations"

Then, you give a question by the related content in the article. Most importantly, the correct answer must not be stated directly in the article. 
Instead, it should require the test-taker to infer, summarize, or understand the context or intent of the passage.
The passage should reflect a real-life topic (e.g., daily life, work, study, travel, opinions).

Instructions:
Format: follow the format of 2 examples in the formal exam paper but not the content. The output must be in html format and remove line change tag.
Content: Ensure the vocabulary is restricted to N1 level. 
Reference: Generate new content based on the user-provided "Topic", taking into account any previous feedback and critique. Also, avoid repeating previously asked questions or given answers in Historical Generation.  
Additional Requirement: 
- Don't show question instructions and sequence number in the generated content. 
- The word in the article can neither be used in the question nor options.
- You must show the correct answer in the output, for example: 正解: n . The options are 1,2,3,4. ensuring a balanced distribution of correct answers across options. 


Formal exam paper: {example}
Historical Generation : {gan_history}
"""

short_reading_mail_example = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>イヤホンに関するメール</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.8;
            max-width: 800px;
            margin: 40px auto;
            padding: 20px;
            background-color: #f9f9f9;
            color: #333;
        }
        hr {
            border: none;
            border-top: 1px solid #ccc;
            margin: 2em 0;
        }
        .email-header {
            font-size: 0.9em;
            color: #555;
            margin-bottom: 1.5em;
        }
        .email-header p {
            margin: 0.3em 0;
        }
        h3 {
            font-size: 1.2em;
            margin-top: 1.5em;
            margin-bottom: 0.5em;
        }
        p {
            margin-bottom: 1.2em;
        }
        .signature {
            margin-top: 2em;
        }
        .page-number {
            text-align: right;
            font-weight: bold;
            margin-top: 2em;
            color: #666;
        }
        ol {
            margin-top: 1.5em;
        }
        li {
            margin-bottom: 0.8em;
        }
    </style>
</head>
<body>
<div class='article'>
<p>以下は、ある電気店から届いたメールである。</p>

<hr>

<div class="email-header">
    <p>宛て先：syo_yasuhara@kfy.co.jp</p>
    <p>件名：イヤホン「AS-10」の件</p>
    <p>日時：9月13日 13：30</p>
</div>

<h3>安原 正一様</h3>

<p>LM電気大木店をご利用いただき、ありがとうございます。</p>

<p>ご予約いただいたイヤホン「AS-10」ですが、メーカーの生産が遅れているため、発売日（9月20日）当日に、すべてのお客様にお渡しすることが困難な状況です。</p>

<p>本日、当店で9月20日にお渡しできる数が確定し、安原様のご注文分は確保できないことが分かりました。大変申し訳ございません。</p>

<p>安原様へのお渡しは10月以降になってしまうのですが、いかがいたしましょうか。ご注文のキャンセルも承っております。</p>

<p>お忙しいところ恐縮ですが、ご返信お待ちしております。</p>

<div class="signature">
    <p>LM電気 大木店</p>
    <p>担当：上田 映子</p>
</div>
<hr>
</div>

<a>イヤホン「AS-10」について、このメールで確認していることは何か。</a>

<ul class="options">
    <li>今から予約しても発売日には渡せないが、予約するかどうか。</li>
    <li>発売日が10月以降になってしまうが、予約するかどうか。</li>
    <li>発売日に渡せるかは分からないが、予約したままでいいかどうか。</li>
    <li>発売日ではなく10月以降に渡すことになるが、予約したままでいいかどうか。</li>
</ul>

</body>
</html>
"""

short_reading_notification_teacher_prompt = """
角色：你是一名日语老师，正在为JLPT N1水平撰写试卷。 

任务：你的工作是为JLPT N1水平考试写一道阅读题。
首先，你需要写一段大约300字左右的文章，主要以散文形式呈现。内容可以是关于：
人生的哲理、做人的三观、对世事的探讨等

然后，你根据文章中的相关内容提出一个问题。最重要的是，文章中不能直接给出正确答案。 
相反，它应该要求考生推断、总结或理解文章的背景或意图。
文章应反映现实生活中的主题（例如，日常生活、工作、学习、旅行、观点）。

说明：
格式：遵循正式试卷中2个例子的格式，而不是内容。输出必须为html格式，并删除行更改标记。
内容：确保词汇量限制在N1级。 
参考：从用户给出的“主题”中获得灵感。考虑前一次对话中给出的反馈（如果存在）
附加要求：
-不要在生成的内容中显示问题说明和序列号。 
-文章中的单词既不能用于问题，也不能用于选项。
-在输出中显示正确答案，选项为1,2,3,4.例如：正解：n, 正确答案分布要平均，不要集中在某个选项


正式试卷：{example}
"""

short_reading_notification_example = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>筆者の考えに関する文章（縦書き）</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.8;
            max-width: 800px;
            margin: 40px auto;
            padding: 20px;
            background-color: #f9f9f9;
            color: #333;
        }
        .tategaki-container {
            width: 600px;
            margin: 2em auto;
            border: 1px solid #ccc;
            padding: 20px;
            background-color: #fff;
        }
        .tategaki {
            writing-mode: vertical-rl;
            text-orientation: mixed;
            height: 600px;
            font-size: 1.1em;
            line-height: 2;
            text-align: justify;
        }
        .page-number {
            text-align: right;
            font-weight: bold;
            margin-top: 2em;
            color: #666;
        }
        ol {
            margin-top: 2em;
        }
        li {
            margin-bottom: 0.8em;
        }
    </style>
</head>
<body>
<div class='article'>
    <div class="tategaki-container">
        <div class="tategaki">
            「自分の悪い部分を露にすると、嫌われたり、敬遠されたりするのではないか」という不安は、もちろんだろう。見せ方がまずいと、実際にそうなる危険性もある。しかし、世間からの評価や期待に対し、神経質になりすぎ、そのせいで常に不安を抱えながら生きていくくらいなら、他人から嫌われるほうがよほどましである。
            そもそも他人は、あなたが思っているほどあなたに対して期待などしていない。誰もが皆、自分のことで頭がいっぱいで、他人のことなど気にかけてはいない。
        </div>
    </div>
</div>

<a>筆者が言いたいことは何か。</a>

<ul class="options">
    <li>他人に嫌われることなく生きることは難しい。</li>
    <li>世間の評価や期待を気にしながら生きる必要はない。</li>
    <li>自分の悪い部分を見せなければ、他人に嫌われることはない。</li>
    <li>自分の悪い部分を見せて他人から嫌われるほうが、楽に生きられる。</li>
</ul>

</body>
</html>
"""

midsize_reading_teacher_prompt = """
Role: You are a Japanese teacher writing an exam paper for the JLPT N1 level. 

Task: Your job is to write a reading question for a JLPT N1 level exam.
First you need to write a mid-size article around 450 words for student to read.
The keypoints being tested in each question needs to be underlined with <u></u>
Then, you give 2 questions by the related content in the article. the meaning of keypoint cannot be found in the article.
Then, you give a question by the related content in the article.
Instead, it should require the test-taker to infer, summarize, or understand the context or intent of the passage.

Instructions:
Format: follow the format of the 1 example in the formal exam paper but not the content. The output must be in html format and remove line change tag.
Content: Ensure the vocabulary is restricted to N1 level. 
Reference: Generate new content based on the user-provided "Topic", taking into account any previous feedback and critique. Also, avoid repeating previously asked questions or given answers in Historical Generation.  
Additional Requirement: 
- Don't show question instructions and sequence number in the generated content. 
- The word in the article can neither be used in the question nor options.
- You must show the correct answer in the output, for example: 正解: n . The options are 1,2,3,4. ensuring a balanced distribution of correct answers across options. 

Formal exam paper: {example}
Historical Generation : {gan_history}
"""

midsize_reading_example = """
--- example1----
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>羽毛を持つ恐竜について</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.8;
            max-width: 800px;
            margin: 40px auto;
            padding: 20px;
            background-color: #f9f9f9;
            color: #333;
        }
        p {
            margin-bottom: 1.5em;
            text-align: justify;
        }
        .note {
            font-size: 0.9em;
            color: #555;
            margin-left: 1em;
        }
        .page-number {
            text-align: right;
            font-weight: bold;
            margin-top: 2em;
            color: #666;
        }
        ol {
            margin-top: 2em;
        }
        li {
            margin-bottom: 0.8em;
        }
        hr {
            border: none;
            border-top: 1px dashed #ccc;
            margin: 3em 0;
        }
    </style>
</head>
<body>
<div class='article'>
    <p>以下は、羽毛を持つ恐竜について述べられた文章である。</p>
    <p>恐竜には、鳥のように卵を温める習性があったことがわかっています。</p>
    <p class="note">（中略）</p>
    <p>気になるのは、いつから卵を温めるようになったのかということですが、羽毛を持った時点で、卵を温める習性も持っていた可能性があります。</p>
    <p>羽毛を持つことで、体温が維持できるようになるので、その体温を使って卵の温度を一定に保つことができます。特に夜間は気温が下がるので、夜に親が卵の上に座って眠っていれば、卵の保温にはとても効果的です。卵が一定の温かさで保たれていれば、さまざまな環境で卵が孵る確率が高くなります。</p>
    <p>は虫類は卵を温めません。は虫類の卵は、放置されても、1日のうちある程度の時間、気温が30度を超えるなどの条件が整っていれば、自然と孵ります。その代わり、は虫類は1年のうち気温の高い限られた時期にしか産卵しません。生息地域も限られます。</p>
    <p>羽毛のある恐竜が、鳥に近い体温を持っていたとすれば、夏以外の季節でも、寒冷地でも、安定して35～40度ほどの温度で卵を温めることが可能です。</p>
    <p>厳密に言うと、羽毛があると体の熱を逃がさないので、卵を温めるには不向きです。人間で言うと、衣服の上からでは温めにくいのと同じです。温めるなら、服の中に入れて直接体温が伝わるようにするはずです。</p>
    <p>卵を抱く時期の鳥も、卵と接する部分の羽毛がなくなり、皮膚がむき出しになります。恐竜が卵を温めていたとすれば、おそらく同じように、お腹のあたりの羽毛が抜けていたと思われます。</p>
    <p class="note">（注）生息地域：生活している地域</p>
</div>

<div class="follow-up">
    <a>筆者によると、羽毛を持つことにはどのような利点があるか。</a>
    <ul class="options">
        <li>低温の環境でも、卵を一定の温かさで保つことができる。</li>
        <li>低温の環境でも、卵の成長を促し早く孵すことができる。</li>
        <li>環境にかかわらず体温が維持でき、卵が多く産める。</li>
        <li>環境に合わせて卵の温度を調整でき、早く孵すことができる。</li>
    </ul>
    
    <a>お腹のあたりの羽毛が抜けていたと思われますとあるが、筆者はなぜそう考えるのか。</a>
    <ul class="options">
        <li>体の熱を逃がすことで、卵を温めすぎるのを防げるから</li>
        <li>皮膚から卵に直接体温が伝わることで、効率的に卵を温められるから</li>
        <li>卵に皮膚を直接当てることで、卵の温度を知ることができるから</li>
        <li>卵と接する部分の皮膚がむき出しになることで、卵が抱きやすくなるから</li>
    </ul>
</div>

</body>
</html>

---example2---
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>羽毛を持つ恐竜について</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.8;
            max-width: 800px;
            margin: 40px auto;
            padding: 20px;
            background-color: #f9f9f9;
            color: #333;
        }
        p {
            margin-bottom: 1.5em;
            text-align: justify;
        }
        .note {
            font-size: 0.9em;
            color: #555;
            margin-left: 1em;
        }
        .page-number {
            text-align: right;
            font-weight: bold;
            margin-top: 2em;
            color: #666;
        }
        .underline {
            text-decoration: underline;
            text-underline-offset: 2px;
        }
        ol {
            margin-top: 2em;
        }
        li {
            margin-bottom: 0.8em;
        }
        hr {
            border: none;
            border-top: 1px dashed #ccc;
            margin: 3em 0;
        }
    </style>
</head>
<body>
<div class='article'>
    <p>以下は、羽毛を持つ恐竜について述べられた文章である。</p>
    <p>恐竜には、鳥のように卵を温める習性があったことがわかっています。</p>
    <p class="note">（中略）</p>
    <p>気になるのは、いつから卵を温めるようになったのかということですが、羽毛を持った時点で、卵を温める習性も持っていた可能性があります。</p>
    <p>羽毛を持つことで、体温が維持できるようになるので、その体温を使って卵の温度を一定に保つことができます。特に夜間は気温が下がるので、夜に親が卵の上に座って眠っていれば、卵の保温にはとても効果的です。卵が一定の温かさで保たれていれば、さまざまな環境で卵が孵る確率が高くなります。</p>
    <p>は虫類は卵を温めません。は虫類の卵は、放置されても、1日のうちある程度の時間、気温が30度を超えるなどの条件が整っていれば、自然と孵ります。その代わり、は虫類は1年のうち気温の高い限られた時期にしか産卵しません。生息地域も限られます。</p>
    <p>羽毛のある恐竜が、鳥に近い体温を持っていたとすれば、夏以外の季節でも、寒冷地でも、安定して35～40度ほどの温度で卵を温めることが可能です。</p>
    <p>厳密に言うと、羽毛があると体の熱を逃がさないので、卵を温めるには不向きです。人間で言うと、衣服の上からでは温めにくいのと同じです。温めるなら、服の中に入れて直接体温が伝わるようにするはずです。</p>
    <p>卵を抱く時期の鳥も、卵と接する部分の羽毛がなくなり、皮膚がむき出しになります。恐竜が卵を温めていたとすれば、おそらく同じように、<span class="underline">お腹のあたりの羽毛が抜けていたと思われます。</span> </p>
    <p class="note">（注）生息地域：生活している地域</p>
</div>

<div class="follow-up">
<a>筆者によると、羽毛を持つことにはどのような利点があるか。</a>
<ul class="options">
    <li>低温の環境でも、卵を一定の温かさで保つことができる。</li>
    <li>低温の環境でも、卵の成長を促し早く孵すことができる。</li>
    <li>環境にかかわらず体温が維持でき、卵が多く産める。</li>
    <li>環境に合わせて卵の温度を調整でき、早く孵すことができる。</li>
</ul>

<a><span class="underline">お腹のあたりの羽毛が抜けていたと思われます</span>とあるが、筆者はなぜそう考えるのか。</a>
<ul class="options">
    <li>体の熱を逃がすことで、卵を温めすぎるのを防げるから</li>
    <li>皮膚から卵に直接体温が伝わることで、効率的に卵を温められるから</li>
    <li>卵に皮膚を直接当てることで、卵の温度を知ることができるから</li>
    <li>卵と接する部分の皮膚がむき出しになることで、卵が抱きやすくなるから</li>
</ul>
</div>
</body>
</html>
"""

long_reading_understanding_teacher_prompt = """
角色：你是一名日语老师，正在为JLPT N1水平撰写试卷。

任务：你的工作是为JLPT N1水平考试写一道阅读题。
首先，你需要写一篇大约800字的长篇文章供学生阅读。 
然后，根据文章中的相关内容给出3个问题。 
目的是确保学生能够理解文章的内容。

说明：
格式：遵循正式试卷中示例的格式，而不是内容。输出必须为html格式，并删除行更改标记。
内容：确保词汇量限制在N1级。 
参考：从用户给出的“主题”中获得灵感。考虑前一次对话中给出的反馈（如果存在）
附加要求：
-不要在生成的内容中显示问题说明和序列号。 
-文章中的单词既不能用于问题，也不能用于选项。
-在输出中显示正确答案，选项为1,2,3,4.例如：正解：n, 正确答案分布要平均，不要集中在某个选项


正式试卷：{example}
"""

long_reading_understanding_example = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>数学の問題を解くことについて</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.8;
            max-width: 800px;
            margin: 40px auto;
            padding: 20px;
            background-color: #f9f9f9;
            color: #333;
        }
        p {
            margin-bottom: 1.5em;
            text-align: justify;
        }
        .note {
            font-size: 0.9em;
            color: #555;
            margin-left: 1em;
        }
        .page-number {
            text-align: right;
            font-weight: bold;
            margin-top: 2em;
            color: #666;
        }
        ol {
            margin-top: 2em;
        }
        li {
            margin-bottom: 0.8em;
        }
        hr {
            border: none;
            border-top: 1px dashed #ccc;
            margin: 3em 0;
        }
        .underline {
            text-decoration: underline;
            text-underline-offset: 2px;
        }
        sup {
            font-size: 0.8em;
        }
    </style>
</head>
<body>
<div class='article'>
    <p>以下は、ある数学者が描いた文章である。</p>
    <p>数学というものは、解き方がわかってしまったあとで、力がつくことはない。解き方を身につける前の、まだ解き方のわからない間だけが、力をつけるチャンスである。解けるようになるのは同じでも、それまでのあり方で、力が身につくかどうかが、きまってくる。</p>
    <p>それに、おもしろいのも、本当は、まだ解けないで、いろいろと考えている間である。解けなきゃつまらないようだが、それは早く解こうとあせるからで、楽しみは解けるまでのほうにある。解けるようになったあとは、むしろむなしい。だいたい、「答えのわかっている謎」なんて、意味がない。解き方がわからないからこそ、問題の名にあたいするのだ。</p>
    <p>もちろん、まったく手がつかないのでは、おもしろくもないが、案外に、多少はわからないでも、うまく<span class="underline">頭のなかに飼っておくと</span>、そのうちに馴れてくれて、わかってきたりする。その、だんだん少しずつ、わかりかけというのも、オツなものだ。そのためには、それを飼っておく、頭の牧場がゆたかでなければならない。本当のところは、数学の力というのは、いろいろとわかったことをためこむより、わからないのを飼っておける、その牧場のゆたかさのほうにあるのかもしれない。</p>
    <p>とくに、公式などをおぼえるのには、ぼくは反対である。それは簡単すぎて、少しもおもしろくないし、おぼえたものは忘れるものだ。とくに、急いでおぼえたものは、早く忘れる。同じおぼえるにしても、なるべくなら時間をかけたほうが、長持ちする。</p>
    <p class="note">（中略）</p>
    <p>このごろは、テストでおどされることが多いので、わかること、解けることを急ぐ傾向にある。たしかに、テストなどでは、時間がかぎられているので、急ぐのも多少は仕方がない。しかしながら、時間を制限されたときに急いでできるためには、時間の制限されていないときに、時間を気にしないでやっておいたほうがよい。テストで急ぐためには、テスト以外で急がないほうがよいのである。</p>
    <p>どんなやり方でも、わかって、問題が解けるようになる、という結果は同じかもしれない。しかし、ゆったりとやると、そのわかり方にコクが出てくるものだ。そして、その結果に達するまでの道筋を楽しむことで、力がつく。</p>
    <p>勉強を楽しむなんて、と思うかもしれないが、それは目的ばかり見てあせるからで、楽しむ気になれば、なんだって楽しめるものだ。</p>
    <p class="note">(注1)手がつかない：ここでは、できない</p>
    <p class="note">(注2)オツな：ここでは、おもしろい</p>
    <p class="note">(注3)おどされる：ここでは、早く問題を解かされる</p>
    <p class="note">(注4)コク：深み。</p>
</div>

<a>数学の問題を解くことについて、筆者の考えに合うのはどれか。</a>
<ul class="options">
    <li>早く解けなくても、解き方を身につけることが大切だ。</li>
    <li>解けても解けなくても、問題に取り組むことが大切だ。</li>
    <li>解けなかった問題が解けるようになったらおもしろくなる。</li>
    <li>解き方のわからない問題を解こうとすることに意味がある。</li>
</ul>

<a><span class="underline">頭のなかに飼っておく</span>とはどういうことか。</a>
<ul class="options">
    <li>わかる問題を手がかりにして、わからない問題を考えること</li>
    <li>わかる問題とわからない問題を、頭のなかで区別しておくこと。</li>
    <li>わからない問題をわかるまで解き続けていること</li>
    <li>わからない状態のまま、問題を頭のなかに残しておくこと</li>
</ul>

<a>筆者によると、どのように勉強すればよいか。</a>
<ul class="options">
    <li>結果を急がずに、考えることを楽しむ。</li>
    <li>結果に達することができれば、どんなやり方でもよい。</li>
    <li>目的を忘れないで、あせらずに勉強を楽しめばよい。</li>
    <li>自分に合ったやり方を探して、時間を気にせず取り組む。</li>
</ul>

</body>
</html>
"""


comprehensive_read_teacher_prompt = """
Role: You are a Japanese teacher writing an exam paper for the JLPT N1 level.

Task: Task: Your job is to write a reading question for a JLPT N1 level exam. 
First you need to write a long article around 450 words for student to read. 
Then, you give 2 questions by the related content in the article. 
The purpose is to ensure the students are able to understand the meaning of the article.


Instructions:
Format: follow the format of the example in the formal exam paper but not the content. The output must be in html format and remove line change tag.
Content: Ensure the vocabulary is restricted to N1 level. 
Reference: Generate new content based on the user-provided "Topic", taking into account any previous feedback and critique. Also, avoid repeating previously asked questions or given answers in Historical Generation.  
Additional Requirement: 
- Don't show question instructions and sequence number in the generated content. 
- The word in the article can neither be used in the question nor options.
- You must show the correct answer in the output, for example: 正解: n . The options are 1,2,3,4. ensuring a balanced distribution of correct answers across options. 


Formal exam paper: {example}
Historical Generation : {gan_history}
"""

comprehensive_read_example = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AとBの「あきらめる」について</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.8;
            max-width: 800px;
            margin: 40px auto;
            padding: 20px;
            background-color: #f9f9f9;
            color: #333;
        }
        .section {
            margin-bottom: 3em;
            padding: 20px;
            background-color: #fff;
            border: 1px solid #ccc;
            border-radius: 12px;
        }
        .label {
            font-size: 1.4em;
            font-weight: bold;
            margin-bottom: 1em;
            display: block;
        }
        p {
            margin-bottom: 1.2em;
            text-align: justify;
        }
        .note {
            font-size: 0.9em;
            color: #555;
            margin-top: 1.5em;
        }
        .page-number {
            text-align: right;
            font-weight: bold;
            margin-top: 2em;
            color: #666;
        }
        ol {
            margin-top: 2em;
        }
        li {
            margin-bottom: 0.8em;
        }
        hr {
            border: none;
            border-top: 1px dashed #ccc;
            margin: 3em 0;
        }
        sup {
            font-size: 0.8em;
        }
    </style>
</head>
<body>
<div class='article'>
    <div class="section">
        <span class="label">A</span>
        <p>まじめで責任感が強く、負けず嫌いな人は「あきらめない」傾向があります。「あきらめない」ことは、基本的にはもちろんいいことなのですが、しかし一方、あきらめたほうがよいことも、実はけっこうあるものです。</p>
        <p>一所懸命に取り組んでも、うまくいかない、成果が出ない、充足感や満足感が得られない。そうした場合は「あきらめる」というのも、十分よい選択肢になります。</p>
        <p>こうした場合の「あきらめる」とは、「やめてしまう」ということです。</p>
        <p class="note">（中略）</p>
        <p>やめる際には、「うまくいかなかった。やめてよかった」と思うのがコツでしょうね。うまくいかなかったことを悔やみつつやめるのは、避けたいものです。それでは、うまくいかなかったことが尾をひいてしまいます。「うまくいかなくてよかった」と思うくらいがちょうどいいでしょう。それができるようになると、一時的に落ち込んでも、立ち直りが早くなります。</p>
    </div>
    
    <div class="section">
        <span class="label">B</span>
        <p>最近は仕事で悩んでいる人に対して「無理をしないであきらめたほうがよい。」というアドバイスを目にすることがある。もちろん体調を崩してしまうような場合には途中でやめるべきだ。しかしあきらめるということは、やれることはすべてやり尽くしたあとで考えるべきではないだろうか。困難な目標ほど簡単には達成できないものだ。だから、最初から、できなければあきらめてもいいんだという気持ちでいては、つらくなったときに頑張り続けることができない。</p>
        <p>仮にどうしてもうまくいかずにあきらめることになったとしても、精いっぱい努力した結果ならば納得できる。落ち込んだりくよくよしたりするのではなく気持ちを切り替えて、しっかり原因を考えて次に生かすことが重要だ。</p>
        <p class="note">(注) 尾を引く：ずっと残る</p>
    </div>
</div>

<a>あきらめることについて、AとBはどのように述べているか。</a>
<ul class="options">
    <li>AもBも、成果が出せる可能性が低いばあいには、あきらめたほうがよいと述べている。</li>
    <li>AもBも、つらくても、できるだけあきらめずに頑張ったほうがよいと述べている。</li>
    <li>Aは状況によっては、あきらめたほうがよいこともあると述べ、Bはあきらめてもいいと思ったほうが、頑張り続けられる場合もあると述べている。</li>
    <li>Aは努力しても結果に結びつかない場合は、あきらめたほうがよいと述べ、Bは十分にやってみるまでは、あきらめることを考えるべきではないと述べている。</li>
</ul>

<a>AとBの認識で共通していることは何か。</a>
<ul class="options">
    <li>あきらめることになった原因を考えるべきだ。</li>
    <li>あきらめるのが早ければ、早く立ち直れる。</li>
    <li>あきらめたことでも、再挑戦することはできる。</li>
    <li>あきらめたことを後悔してはいけない。</li>
</ul>

</body>
</html>
"""

long_reading_teacher_prompt = """
角色：你是一名日语老师，正在为JLPT N1水平撰写试卷。

任务：任务：你的工作是为JLPT N1水平考试写一道阅读题。
首先，你需要写一篇大约800字的长篇文章供学生阅读。 
然后，根据文章中的相关内容给出3个问题。 
目的是确保学生能够理解笔者的主张和观点。


说明：
格式：遵循正式试卷中示例的格式，而不是内容。输出必须为html格式，并删除行更改标记。
内容：确保词汇量限制在N1级。 
参考：从用户给出的“主题”中获得灵感。考虑前一次对话中给出的反馈（如果存在）
附加要求：
-不要在生成的内容中显示问题说明和序列号。 
-文章中的单词既不能用于问题，也不能用于选项。
-在输出中显示正确答案，选项为1,2,3,4.例如：正解：n, 正确答案分布要平均，不要集中在某个选项



正式试卷：{example}
"""

long_reading_example = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SNSと人間関係について</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.8;
            max-width: 800px;
            margin: 40px auto;
            padding: 20px;
            background-color: #f9f9f9;
            color: #333;
        }
        p {
            margin-bottom: 1.5em;
            text-align: justify;
        }
        .note {
            font-size: 0.9em;
            color: #555;
            margin-left: 1em;
        }
        .page-number {
            text-align: right;
            font-weight: bold;
            margin-top: 2em;
            color: #666;
        }
        ol {
            margin-top: 2em;
        }
        li {
            margin-bottom: 0.8em;
        }
        hr {
            border: none;
            border-top: 1px dashed #ccc;
            margin: 3em 0;
        }
        sup {
            font-size: 0.8em;
        }
    </style>
</head>
<body>
<div class="article">
    <p>SNSを含むリアルタイムウェブの本質は、時間と過程の消去にある。かつてコンテンツの拡散には一定の時間がかかった。権威やメディアをすり抜ける必要もあった。けれどもいまや、それらの面倒をすべてすっ飛ばし、無名の書き手が一晩で何百万もの支持者を集めることができる。それはSNSの良いところだ。</p>
    <p>けれども人生にはトラブルがつきものである。どれだけ誠実に生きていても、誤解や中傷に曝されることが必ずある。そしてそういうとき、SNSの支持はほとんど役に立たない。匿名の支持者は、トラブルの話題自体すぐに忘れてしまう。あっというまに集まった人々は、同じくあっというまに離れる。そこで継続的に助けてくれるのは、結局は面倒な人間関係に支えられた家族や友人たちだったりする。</p>
    <p>SNSの人間関係には面倒がない。だからSNSの知人は面倒を背負ってくれない。そんなSNSでも、たしかに人生がうまく行っているときは大きな力になる。けれども、本当の困難を抱えたときは、助けにならないのだ。</p>
    <p>これからの時代を生きるうえで、SNSのこの性格を知っておくことはとても重要なように思う。そもそも、人生の困難なるものは自分と世界のズレの表れである。自分はあることを正しいと信じるが、世界はそう思わない——そういう対立が生じたとき、困難が訪れる。だから困難そのものが悪いわけではない。むしろ、概念の発明や政治の変革は必ず困難とともに生じる。その困難を時間をかけて解消し昇華することで、はじめて自分も相手も社会も進歩するのだ。けれども、いまのSNSにはそのような熟成の余裕がほとんどない。</p>
    <p>困難な時期を支えるとは、言いかえれば、支える相手と世界の関係が変化する過程に時間をかけてつきあうということである。ひとりの人間が変わるというのはたいへんなことで、「いいね！」をつけるようにポンポン複製できるものではない。いわゆる「議論」で相手が変わると考えているひとは、人間の本質について無知である。ぼくが一生をかけて変えることができるのは、ごく少数の身の回りの人々だけであり、そしてぼくを変えることができるのもおそらくは彼らだけだ。その小さく面倒な人間関係をどれだけ濃密に作れるかで、人生の広がりが決まるのだと思う。</p>
    <p>家族も友人もあっというまには作れない。面倒な存在でもある。だからこそそれは変化の受け皿となる。面倒がないところに変化はない。情報技術は、面倒のない人間関係の調達を可能にしたが、それはまた人間から変化の可能性を奪うものでもあった。そのことを忘れずにおきたいと思う。</p>
    
    <p class="note">(注1) SNS：ウェブ上での情報のやり取りや交流の場を提供するサービス</p>
    <p class="note">(注2) リアルタイムウェブ：情報更新が即時に行われるウェブ</p>
    <p class="note">(注3) コンテンツ：ここでは、情報</p>
    <p class="note">(注4) すっ飛ばす：ここでは、省略する</p>
    <p class="note">(注5) つきもの：必ず伴うもの</p>
    <p class="note">(注6) あっというまに：短い間に</p>
    <p class="note">(注7) 昇華する：ここでは、別の良いものに変える</p>
</div>

<a>SNSの支持はほとんど役に立たないとあるが、なぜか。</a>
<ul class="options">
    <li>SNSの支持者の意見はさまざまで、すぐにはまとまらないから</li>
    <li>SNSの支持者は無名で権威を持たないひとが多いから</li>
    <li>SNSの支持者はトラブルの原因を誤解したまますぐに発信するから</li>
    <li>SNSの支持者はすぐに興味をなくし、去ってしまうから</li>
</ul>

<a>困難な時期について、筆者はどのように述べているか。</a>
<ul class="options">
    <li>自分と世界の認識のズレに気づき自分が変わろうとすれば、乗り越えられる。</li>
    <li>「議論」によって相手や自分を変化させることで、乗り越えられる。</li>
    <li>少数の身の回りの人々から人間関係を広げていけば、乗り越えられる。</li>
    <li>家族や友人のような存在との深い関係によって、乗り越えられる。</li>
</ul>

<a>筆者が言いたいことは何か。</a>
<ul class="options">
    <li>情報技術の特徴を理解したうえで活用すれば、自分自身の変化につながる。</li>
    <li>情報技術を活用すれば、面倒な人間関係を変えられる可能性がある。</li>
    <li>情報技術によって作られた人間関係では、人間の変化は期待できない。</li>
    <li>情報技術は人間の変化の可能性を奪うものであり、利用は控えるべきだ。</li>
</ul>

</body>
</html>
"""

information_retrieval_teacher_prompt = """
Role: You are a Japanese teacher writing an exam paper for the JLPT N1 level. 

Task: You are a Japanese teacher writing a retrieve information question on an exam paper for the JLPT N1 level.
you must provide 1 or 2 html format tables and with additional information for retrieve below. The content and conditions combined should be more than 400 words and complex enough for JLPT N1 level.
After that, asking candidate to answer 2 questions from the related content in the table.
Most importantly, the question and answer must not be stated directly in the table or clues. 
Instead, it should require the test-taker to infer, summarize, or understand the context.
This section is designed to simulate real-life scenarios where students need to quickly find relevant information. 
such as train or flight schedules, event, or advertisements.

Instructions:
Format: follow the format of the 2 examples in the formal exam paper but not the content. The output must be in html format and remove line change tag.
Content: Ensure the vocabulary is restricted to N1 level. 
Reference: Generate new content based on the user-provided "Topic", taking into account any previous feedback and critique. Also, avoid repeating previously asked questions or given answers in Historical Generation.  
Additional Requirement: 
- Don't show question instructions and sequence number in the generated content. 
- The word in the table and clues can neither be used in the question nor options.
- You must show the correct answer in the output, for example: 正解: n . The options are 1,2,3,4. ensuring a balanced distribution of correct answers across options. 


Formal exam paper: {example}
Historical Generation : {gan_history}
"""

information_retrieval_example = """
--- example 1 ---
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>マスダ買い取りサービス</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.8;
            max-width: 800px;
            margin: 40px auto;
            padding: 20px;
            background-color: #f9f9f9;
            color: #333;
        }
        h1 {
            text-align: center;
            font-size: 1.5em;
            margin-bottom: 1em;
            border-bottom: 2px solid #333;
            padding-bottom: 0.5em;
        }
        h2 {
            font-size: 1.3em;
            margin-top: 2em;
            margin-bottom: 1em;
            color: #222;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 1.5em 0;
            font-size: 0.95em;
        }
        th, td {
            border: 1px solid #999;
            padding: 10px;
            text-align: left;
            vertical-align: top;
        }
        th {
            background-color: #eee;
            width: 30%;
        }
        ul {
            margin: 0.5em 0;
            padding-left: 1.2em;
        }
        .note {
            font-size: 0.9em;
            color: #555;
            margin-top: 1.5em;
        }
        .page-number {
            text-align: right;
            font-weight: bold;
            margin-top: 2em;
            color: #666;
        }
        ol {
            margin-top: 2em;
        }
        li {
            margin-bottom: 0.8em;
        }
        hr {
            border: none;
            border-top: 1px dashed #ccc;
            margin: 3em 0;
        }
    </style>
</head>
<body>
<div class="article">
    <h1>マスダ買い取りサービス</h1>
    <h2>買い取りサービスのご利用について</h2>
    <h3>◆買い取り可能な品物</h3>
    <p>冷蔵庫などの家電、机などの家具、自転車、楽器を受け付けています。詳しくは、「買い取り可能な品物」のページをご確認ください。</p>
    <h3>◆買い取り方法と流れ</h3>
    
    <table>
        <tr>
            <th>店頭買取</th>
            <td>
                <ol>
                    <li>店頭へお持ちください。</li>
                    <li>品物を確認し、買い取り金額をご提示します。</li>
                    <li>ご納得いただけた場合は、現金をお渡しします。</li>
                </ol>
            </td>
        </tr>
        <tr>
            <th>出張買取</th>
            <td>
                <ol>
                    <li>最寄りの店舗にお電話ください。</li>
                    <li>弊社スタッフがご自宅へ伺います。</li>
                    <li>ご自宅で品物を確認し、買い取り金額をご提示します。</li>
                    <li>ご納得いただけた場合は、現金をお渡しします。</li>
                </ol>
            </td>
        </tr>
        <tr>
            <th>宅配買取</th>
            <td>
                <ol>
                    <li>ホームページからご予約ください。</li>
                    <li>宅配業者が伺いますので、品物をお渡しください。</li>
                    <li>店舗への品物到着から3営業日以内に、買い取り金額をメールでご連絡します。ご納得いただけた場合は、銀行口座へお振り込みします。</li>
                </ol>
            </td>
        </tr>
    </table>
    
    <p>※買い取り金額にご納得いただけずキャンセルされる場合でも、出張料や返送料はかかりません。</p>
    
    <h3>◆受け付け可能な品数とサイズ</h3>
    
    <table>
        <tr>
            <th></th>
            <th>受け付け可能な品数</th>
            <th>1点あたりのサイズ制限</th>
        </tr>
        <tr>
            <td>店頭買取</td>
            <td>1点から</td>
            <td>なし</td>
        </tr>
        <tr>
            <td>出張買取</td>
            <td>2点から</td>
            <td>なし</td>
        </tr>
        <tr>
            <td>宅配買取</td>
            <td>1点から</td>
            <td>25kg以下で、かつ三辺（縦・横・高さ）の合計が160cm以下のもの（自転車の場合、サイズ内でも宅配買取は利用できません）</td>
        </tr>
    </table>
    
    <h3>◆ご本人確認について</h3>
    <p>店頭買取、出張買取の場合、本人確認書類（運転免許証等）をご提示いただきます。宅配買取の場合は、品物と一緒にコピーをお送りいただきます。<br>
    家電、家具、楽器の場合は、顔写真のない本人確認書類もご利用になれますが、自転車の場合は、顔写真付きのものをご用意ください。</p>
</div>

<a>チョウさんは、机1台を買い取ってもらいたいと思っている。机は、重さが12kgで、三辺の合計が220cmである。チョウさんが利用できる方法はどれか。</a>
<ul class="options">
    <li>店頭買取か出張買取か宅配買取</li>
    <li>店頭買取か出張買取</li>
    <li>店頭買取か宅配買取</li>
    <li>店頭買取</li>
</ul>

<a>森村さんは、ギター（重さ5kg、三辺の合計150cm）と自転車（重さ10kg、三辺の合計160cm）をまとめて買い取ってもらいたいと思っているが、店頭に自分で持っていかずに済む方法がいい。森村さんが利用できる方法はどれで、何を準備しなければならないか。</a>
<ul class="options">
    <li>宅配買取で、品物と顔写真付きの本人確認書類のコピーを準備する。</li>
    <li>宅配買取で、品物と本人確認書類のコピーを準備する。本人確認書類は、顔写真付きでなくてもいい。</li>
    <li>出張買取で、品物と顔写真付きの本人確認書類を準備する。</li>
    <li>出張買取で、品物と本人確認書類を準備する。本人確認書類は、顔写真付きでなくてもいい。</li>
</ul>

</body>
</html>


--- example 2 ---
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>秋川大学＞秋川大学図書館＞一般利用</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.8;
            max-width: 800px;
            margin: 40px auto;
            padding: 20px;
            background-color: #f9f9f9;
            color: #333;
        }
        h1 {
            text-align: center;
            font-size: 1.5em;
            margin-bottom: 1em;
            border-bottom: 2px solid #333;
            padding-bottom: 0.5em;
        }
        h2 {
            font-size: 1.3em;
            margin-top: 2em;
            margin-bottom: 1em;
            color: #222;
            border-left: 5px solid #555;
            padding-left: 0.8em;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 1.5em 0;
            font-size: 0.95em;
        }
        th, td {
            border: 1px solid #999;
            padding: 10px;
            text-align: center;
        }
        th {
            background-color: #eee;
        }
        .note {
            font-size: 0.9em;
            color: #555;
            margin-top: 1.5em;
        }
        .page-number {
            text-align: right;
            font-weight: bold;
            margin-top: 2em;
            color: #666;
        }
        ol {
            margin-top: 2em;
        }
        li {
            margin-bottom: 0.8em;
        }
        hr {
            border: none;
            border-top: 1px dashed #ccc;
            margin: 3em 0;
        }
    </style>
</head>
<body>
<div class="article">
    <h1>秋川大学＞秋川大学図書館＞一般利用</h1>
    
    <h2>一般の方の図書館利用について</h2>
    <p>秋川大学の学生以外の一般の方も、研究等の目的のために、秋川キャンパスにある中央図書館や文学部図書館の資料が利用できます。</p>
    
    <h2>【入館方法】</h2>
    <p>・図書館利用カードをお持ちの方は、自動入退館ゲートから入退館ができます。<br>
    ・お持ちでない方は、カウンターで1日入館証を発行いたします。</p>
    
    <h2>【図書館利用カードについて】</h2>
    <p>・図書館利用カードは、図書館資料の貸し出しの際に必要になります。<br>
    ・発行をご希望の方は、身分証明書をお持ちなり、中央図書館、または文学部図書館のカウンターにお越しください(文学部図書館では平日のみ受け付けています)。<br>
    ・平日の9時から17時までの間に申請を受け付けた場合、その日のうちにカードをお渡しします。平日の17時以降、および土日に受け付けた場合は、次の平日開館日以降にお渡しします。</p>
    
    <h2>【貸し出しと返却】</h2>
    <p>・貸し出し冊数は5冊まで、貸し出し期間は2週間です。<br>
    ・中央図書館の貸し出し受付時間は閉館30分前まで、文学部図書館は閉館15分前までです。<br>
    ・閉館時の返却は、カウンターで受け付けています。閉館・休館時は、ブックポストに入れてください。</p>
    
    <h2>【資料の複写】</h2>
    <p>・館内の複写機で、図書館資料の複写ができます。<br>
    ・複写機は、中央図書館は閉館10分前まで、文学部図書館は閉館時間まで利用できます。</p>
    
    <h2>【開館時間】</h2>
    
    <table>
        <tr>
            <th rowspan="2"></th>
            <th colspan="2">期間※</th>
            <th>平日</th>
            <th>土曜・日曜</th>
        </tr>
        <tr>
            <td>授業期間</td>
            <td>9:00～22:00</td>
            <td colspan="2">9:00～17:00</td>
        </tr>
        <tr>
            <td>中央<br>図書館</td>
            <td>夏休み・春休み期間</td>
            <td>9:00～19:00</td>
            <td colspan="2">休館</td>
        </tr>
        <tr>
            <td>文学部<br>図書館</td>
            <td>授業期間</td>
            <td>9:00～21:00</td>
            <td colspan="2">9:00～17:00</td>
        </tr>
        <tr>
            <td></td>
            <td>夏休み・春休み期間</td>
            <td>9:00～18:00</td>
            <td colspan="2">休館</td>
        </tr>
    </table>
    
    <p class="note">※各期間の具体的な日程は、開館カレンダーのページをご覧ください。</p>
</div>

<a>マリーさんは、秋川大学で本を借りるために、図書館利用カードを作ろうと思っている。今日は金曜日である。明日の夜までに本を借りたいが、図書館利用カードは、どうように申請しなければならないか。</a>
<ul class="options">
    <li>今日、中央図書館か文学部図書館で9時から17時までの間に申請する。</li>
    <li>今日、中央図書館で9時から17時までの間に申請する。文学部図書館では申請できない。</li>
    <li>今日、中央図書館か文学部図書館で9時から17時までの間に申請するか、明日、中央図書館で9時から17時までの間に申請する。</li>
    <li>今日か明日、中央図書館か文学部図書館で9時から17時までの間に申請する。</li>
</ul>


<a>ケイさんは、研究のために資料を借りたい複写したりする必要があって、秋川大学の文学部図書館に来た。図書館利用カードを持っている。今日は、授業期間の火曜日である。貸し出しと複写は何時まで可能か。</p>
<ul class="options">
    <li>貸し出しは18時の15分前まで、複写は18時まで可能である。</li>
    <li>貸し出しは21時の15分前まで、複写は21時まで可能である。</li>
    <li>貸し出しは21時の15分前まで、複写は21時の10分前まで可能である。</li>
    <li>貸し出しは21時の30分前まで、複写は21時の10分前まで可能である。</li>
</ul>

</body>
</html>
"""

topic_understanding_txt_teacher_prompt = """
Role: You are a Japanese teacher writing an exam paper for the JLPT N1 level. 

Task: Your job is to write a natural-sounding conversation between a man and a woman. 

Step 1, write a concise background about the dialogue introduction, which exclude the follow-up question and character name.

Step 2, Give characters names during the conversation. They should call each name during the conversation depending on their relationship, level of formality.
Do not refer to them as Mr. or Miss in the conversation context. Be polite and culturally appropriate in how they address each other.
女：conversation context
男：conversation context
Besides, the name at the end of a sentence can be omitted.
For example: "ありがとう、佐藤さん。" the name at the end of a sentence can be omitted, like "ありがとう。"

Step 3, write dialogue, the dialogue should consist of 6-9 exchanges (back-and-forth turns). The total length should be approximately 300-400 words.

Step 4, after the conversation, ask a follow-up question related to the conversation and focusing on the man or woman's next action, such as 
What,When,Where,Who,How,Which,Whose,How long,How often,How much,How many.

Step 5, provide multiple-choice options based on the listening content. These options should test comprehension of the conversation’s meaning.

Instructions:
Format: follow the format of the 2 examples in the formal exam paper but not the content.
Content: Ensure the vocabulary is restricted to N1 level. 
Reference: Generate new content based on the user-provided "Topic", taking into account any previous feedback and critique. Also, avoid repeating previously asked questions or given answers in Historical Generation.  
Additional Requirement: 
- Don't show question instructions and sequence number in the generated content. 
- The word in the sentence can neither be used in the question nor options.
- You must show the correct answer in the output, for example: 正解: n . The options are 1,2,3,4. ensuring a balanced distribution of correct answers across options. 



Formal exam paper: {example}
Historical Generation : {gan_history}
"""

topic_understanding_txt_example = """
--- example 1 ---
<p class='background'>大学で女の学生と男の学生が話しています。男の学生はこの後まず、何をしますか。</p>

<div class='conversation'>
女：中村くん、シンポジウムのポスター、掲示板に貼ってくれたんだね。ありがとう。
男：ええ、他に僕がやっておくことってありますか？
女：マイクとか会場の準備は前日にすればいいし、当日のスタッフ用のスケジュール表、これないから欲しいな、今週中にお願いしていい？
男：あ、はい。<br>
女：それから１番大事な当日配る資料、コピーまだなんじゃない？100部だよね？
男：あ、それなんですけど、発表者の方からの資料が全部そろってないんですよ。
女：そう、みなさんお忙しい方ばかりだから…私の方で発表者に資料を送ってもらうようにすぐに連絡をするから、集まったら次第コピーしよう。週明けには出してもらうようにするね。<br>
男：はい、わかりました。
</div>

<p class="follow-up">男の学生は、この後まず何をしますか。</p>
<div class="options">
     1. シンポジウムのポスターを貼る<br>
     2. スタッフの当日の予定表を作る<br>
     3. 当日配る資料をコピーする<br>
     4. 発表者に連絡する
  </p>
</div>


--- example 2 ---
<p class='background'>スーパーで男の店長と女の店員が話しています。女の店員はこの後まず、何をしますか。</p>

<div class='conversation'>
女：おはようございます、森田さん。今日は一部の商品に値引きシールを付ける作業をやってくれることになってるね。
男: あ、はい。準備してます。
男： えっと、忙しい時に悪いんだけど、倉庫に行って南コーヒーの豆、何袋あるか数えてきてくれる？数が少なかったら今日中に注文しないといけないんだ。
女：あ、わかりました。急ぎですか？<br>
男：あー、そのシールを貼る作業が終わってからでいいから。袋の数を数えたらメモを私の机の上に置いといて。
女：わかりました。<br>
男：お客さんがレジにたくさん並んでるから、私もすぐレジを手伝わなきゃいけなくて。値引シールを付けた商品をレジの横の棚に並べるのは明日の開店前にみんなですればいいから。じゃ、よろしくね。
</div>

<p class="follow-up">女の店員はこの後まず、何をしますか。</p>
<div class="options">
     <li>商品に値引きシールを貼る</li>
     <li>倉庫で南コーヒーの数を数える</li>
     <li>レジの手伝いをする</li>
     <li>商品をレジの横の棚に並べる</li>
  </p>
</div>

"""

keypoint_understanding_teacher_prompt = """
Role: You are a Japanese teacher writing an exam paper for the JLPT N1 level. 

Task: Your job is to write a natural-sounding conversation between a man and a woman. Alternatively, write a personal monologue, ensuring it is logically clear and flows smoothly. The probability of dialogue and monologue appearing is 50% each

If it's a conversation:

Step 1, write a concise background about the dialogue introduction, which exclude the follow-up question and character name.

Step 2, Give characters names during the conversation. They should call each name during the conversation depending on their relationship, level of formality.
Do not refer to them as Mr. or Miss in the conversation context. Be polite and culturally appropriate in how they address each other.
女：conversation context
男：conversation context
Besides, the name at the end of a sentence can be omitted.
For example: "ありがとう、佐藤さん。" the name at the end of a sentence can be omitted, like "ありがとう。"

Step 3, write dialogue, the dialogue should consist of 6-9 exchanges (back-and-forth turns). The total length should be approximately 300-350 words.
The topic should be appropriate for language learners and reflect everyday situations.

Step 4, after the conversation, ask a follow-up question focusing on understanding of the motivation or reasoning behind it, encouraging students to think deeply.
The question should prompt students to choose the best option that matches the overall conversation or key point of the dialogue, examples:
What is the man's reason for joining this company?
Why is this tourist spot famous?
Why is the woman taking the exam?

Step 5, provide multiple-choice options based on the listening content. These options should test comprehension of the conversation’s meaning.

If it's a monologue:

Step 1, write a personal monologue of approximately 150-200 words. The following requirements must be met:
-Ensure clear thinking, logical coherence, and no grammatical errors in the copy
-A monologue can be an introduction to an object, an advertisement, or an inner thought process. But they all require specific items or events to occur, and they are relatively close to daily life

Step 2, ask a follow-up question after the monologue ends, focusing on understanding the motivation or reasoning behind it and encouraging students to think deeply.
This question should prompt students to choose the best option that matches the entire conversation or the key points of the conversation, such as:
What is the reason for this person joining this company?
Why is this tourist attraction famous?
Why did that woman take the exam?

Step 3, provide multiple-choice questions based on the listening content. These options should test understanding of the meaning of the conversation.


Instructions:
Format: follow the format of the 2 examples in the formal exam paper but not the content.
Content: Ensure the vocabulary is restricted to N1 level. 
Reference: Generate new content based on the user-provided "Topic", taking into account any previous feedback and critique. Also, avoid repeating previously asked questions or given answers in Historical Generation.  
Additional Requirement: 
- Don't show question instructions and sequence number in the generated content. 
- The word in the sentence can neither be used in the question nor options.
- You must show the correct answer in the output, for example: 正解: n . The options are 1,2,3,4. ensuring a balanced distribution of correct answers across options. 



Formal exam paper: {example}
Historical Generation : {gan_history}
"""

keypoint_understanding_example = """
--- example 1 ---
<p class='background'>テレビでアナンサーの女の人がパン屋の店長にインタビューをしています。店長はどうしてパン屋を始めたと言っていますか。  
<div class='conversation'>    
女: 店長の山本さんです。こちらのお店の手作りのパン、大変人気ですが山本さんご自身は以前、会社員をなされていたんですよね？
男: はい。この店はもともとパン作りが好きな母がやる予定だったんですが、店を出す準備をしている途中で母が病気になってしまいました。母はずっとパン屋をやりたかったので店を諦めることをとても残念がっていたんですよ。それで「やってくれ」と言われたわけじゃないんですが、僕が何とか形にしたいと思いました。
女: それまでパン作りのご経験はあったんですか？
男:いえ、全くなくて…パン作りは専門学校で一から勉強しました。卒業する前に母は亡くなりました。
女: そうでしたか。</p>
男: 母のレベルにはまだまだなんですが、おいしいパンを地元の方に食べてもらえるように頑張っています
</div>
<div class="follow-up">店長はどうしてパン屋を始めたと言っていますか</div>
<ul class='options'>
    <li>母といっしょにパン屋をやりたかったから</li>
    <li>母にたのまれたから</li>
    <li>母のゆめをかなえたかったから</li>
    <li>母のパンの味を残したかったから</li>
</ul>

--- example 2 ---
 <p class='background'>うちで女の人と男の人が話しています。２人は引っ越しの値段を安くするため、どうすることにしましたか。</p>
 <div class='conversation'>
女: うーん、そうだね。安い引っ越し会社は見つからないだろうし、費用を抑えられるようにあんまり使ってない大きい家具のもらい手を探そうか。
男: うん、そうだね。
女: 引っ越し会社に引越しの見積もりを出してもらったけど予算よりかなり高かったよ。今の時期はどこの会社も高いんだね。荷物の量と移動距離で料金を計算するから荷物を減らせば安くなるって。
男: そう、んー。大きい荷物を減らそうか。え一つと、大きいものって言ったらソファー、冷蔵庫、本棚だね。
女: 本棚は分解できるよ。ソファーはあまり使ってないし、欲しい人にあげてもいいかもしれないね。
男: それもそうだね。あ、冷蔵庫は古いし、この際、売って向こうで新しいの買う？
女: えー？冷蔵庫はまだ使うよ！あ、そうだ。親戚のおじさんがトラックを持ってるからおじさんに手伝ってもらって、自分たちで荷物を運ぶ？
男: 荷物の積み降ろしって結構大変だよ。やっぱり引っ越し会社に頼んだ方がいいんじゃないかな？
女: うーん、そうだね。安い引っ越し会社は見つからないだろうし、費用を抑えられるようにあんまり使ってない大きい家具のもらい手を探そうか。
男: うん、そうだね
</div>
<div class="follow-up">2人は引っ越しの値段を安くするため、どうすることにしましたか。</div>
<ul class='options'>
    <li>ソファーをもらってくれる人をさがす</li>
    <li>れいぞうこを売る</li>
    <li>親戚にひっこしを手伝ってもらう</li>
    <li>安いひっこし会社をさがす</li>
</ul>

"""

summary_understanding_teacher_prompt = """
Role: You are a Japanese teacher writing an exam paper for the JLPT N1 level. 

Task: Your job is to write a natural-sounding conversation between a man and a woman. Alternatively, write a personal monologue, ensuring it is logically clear and flows smoothly. The probability of dialogue and monologue appearing is 50% each 

Step 1, you should introduce the background of the dialogue.

Step 2, the total length should be approximately 200–300 words. If you write a dialogue, then the dialogue should consists of 6–7 exchanges (back-and-forth turns). 

Step 3, ask a follow-up question focusing on what the protagonist thinks, the theme of this paragraph, or what the speaker wants to express.
The topic should be appropriate for language learners and reflect everyday situations.

Step 4, provide multiple-choice options based on the listening content. These options should test comprehension of the conversation’s meaning.


Instructions:
Format: follow the format of the 2 examples in the formal exam paper but not the content.
Content: Ensure the vocabulary is restricted to N1 level. 
Reference: Generate new content based on the user-provided "Topic", taking into account any previous feedback and critique. Also, avoid repeating previously asked questions or given answers in Historical Generation.  
Additional Requirement:
- Don't show question instructions and sequence number in the generated content. 
- The word in the sentence can neither be used in the question nor options.
- You must show the correct answer in the output, for example: 正解: n . The options are 1,2,3,4. ensuring a balanced distribution of correct answers across options. 


Formal exam paper: {example}
Historical Generation : {gan_history}
"""

summary_understanding_example = """
--- example 1 ---
<div class="section">
    <p class='background'>講演会で鉄道の写真家が話しています。</p>
    <div class="dialogue">
        <p><span class="speaker">男:</span>私は鉄道の写真を撮るためにいろいろなところへ行きます。行く先々で鉄道ファンの方に会うと「どうやったらうまく撮れますか？」と聞かれるんですが、私は反対に「写真で何を伝えたいですか？」と尋ねるんです。シャッターを押すタイミングとか列車と風景をどんなバランスで撮るかとか、上手に撮影するテクニックはいろいろあります。けど、少しぐらい下手でも構わないんです。1枚の写真の中に季節感や感動的な風景など何を表現したいかを意識して撮ることで全く違った写真になると思うんです。</p>
        <a class='follow-up'>講演会で鉄道の写真家が話しています</a>
    </div>
    <ul class='options'> 
        <li>鉄道の写真を撮る時に大切なこと</li>
        <li>鉄道の写真を撮るのに良い場所</li>
        <li>鉄道の美しさを表現する楽しさ</li>
        <li>鉄道の写真を上手に撮るテクニック</li>
    </ul>
</div>

--- example 2 ---
<div class="section">
    <p class='background'>テレビで工業デザイナーが話しています。</p>

    <div class="dialogue">
        <p><span class="speaker">女:</span>中学1年の時、視力が悪くなり、メガネが必要になりました。メガネ屋さんに行ったのですが、気に入るメガネが見つかりませんでした。仕方なく1つ買ったんですが、自分の気に入らないメガネをかけるのは耐えられませんでした。同じ頃、友達の家で出されたジュースのコップがすごくきれいな形で感激しました。有名なデザイナーがデザインしたコップだったのですが、ちょっと形を変えるだけでこんなにおしゃれになるんだと驚きました。今思えば、デザインということに初めて興味を持ったのがこの頃でした。</p>
        <a class='follow-up'>工業デザイナーは何について話していますか。</a>
    </div>
    <ul class='options'> 
        <li>メガネを買う人へのアドバイス</li>
        <li>人気があるメガネのデザイン</li>
        <li>おしゃれなデザインのポイント</li>
        <li>デザインを意識し始めたきっかけ</li>
    </ul>
</div>
"""

immediate_ack_teacher_prompt = """
角色：你是一名日语老师，正在为JLPT N1水平撰写试卷。 

任务：出一道符合N1水平的听力题。具体步骤如下：

步骤1：设置一个场景，两人个人a和b生成一段只有一个回合的对话。要求对话：
- a的发言字数在20-40个单词左右
- 贴近日本实际的日常生活。且a和b的对话可以是一男一女，也可以是两个相同性别的人。b对于a的回复，必须自然且符合语境，且不存在歧义，和其他模棱两可的回复
- 对话通顺、语法正确，语义连贯
- 对话的用户符合两个对话人的身份。比如学生对老师使用敬语，下属对上司也需要使用敬语，而两个年龄相同的朋友之间，使用普通的平语

步骤2：a作为首先说话的人，他说的话作为题干。b作为第二个说话的人，他说的话作为答案。

步骤3：除了b说的话之外，生成额外2个选项，共计3个选项。且要求：
- 除了b说的话之外，另外两个是错误答案。错误原因：可能因为不符合上下文的回复逻辑，或者是不符合两个对话人身份的回复
- 错误答案可以与正确答案有一定相似度，对答题人产生一定迷惑性

说明：
格式：遵循正式试卷中2个例子的格式，但不要遵循内容。
内容：确保词汇量限制在N1级。 
参考：根据用户提供的主题"Topic"汲取灵感，在生成内容时考虑前一次对话中给出的反馈和批评，并避免重复生成"历史题目"的问题(q)或给出的答案(a)。
附加要求：
-不要在生成的内容中显示问题说明和序列号。 
-句子中的单词既不能用于问题，也不能用于选项。
-在输出中显示正确答案，选项为1,2,3,4.例如：正解：n, 正确答案分布要平均，不要集中在某个选项


历史题目: {gan_history}
正式试卷：{example}
"""

immediate_ack_example = """
--- example 1 ---
<div class="conversation">
    <div class="follow-up">
        男：課長、明日の会議の資料ですが、ご覧いただけないでしょうか？
    </div>
    <ul class='options'>  
        <li>資料、見てくれるんですね</li>
        <li>資料は私が作っておきますね</li>
        <li>資料、見ておきます</li>
    </ul>
</div>


--- example 2 ---
<div class="conversation">
    <div class="follow-up">
        女：この会社、経験者に限らず応募できるって。
    </div>
    <ul class='options'>  
        <li>募集は経験が無い人だけなんだ</li>
        <li>経験がなくてもいいんだね</li>
        <li>やっぱり経験が無いといけないのか</li>
    </ul>
</div>
"""

comprehensive_expression_show_answer_teacher_prompt = """
角色：你是一名日语老师，正在为JLPT N1水平撰写试卷。 

任务：你的工作是写3个人之间听起来很自然的对话。要求是2男1女，或者2女一男。

第一步，你应该介绍对话的背景。

第二步，生成的对话要求总长度约为500-600字。针对某个话题进行讨论，需要有核心思想。

第三步，问一个后续问题，问题可以关于是主角的想法、这段话的主题或说话者想表达什么。
主题应该适合语言学习者，并反映日常情况。

第四步，根据听力内容提供多项选择题。这些选项应该测试对对话含义的理解。


说明：
格式：遵循正式试卷中的例子的格式，但不要遵循内容。
内容：确保词汇限制在N1级。 
参考：根据用户提供的主题"Topic"汲取灵感，在生成内容时考虑前一次对话中给出的反馈和批评，并避免重复生成"历史题目"的问题(q)或给出的答案(a)。
附加要求：
-不要在生成的内容中显示问题说明和序列号。 
-句子中的单词既不能用于问题，也不能用于选项。
-在输出中显示正确答案，选项为1,2,3,4.例如：正解：n, 正确答案分布要平均，不要集中在某个选项


历史题目: {gan_history}
正式试卷：{example}
"""

comprehensive_expression_show_answer_example = """
<p class='background'>地域のボランティアグループのリーダーとメンバー2人が話しています。</p>

<div class='conversation'>
男1: 僕たちが市と協力して定期的にゴミ拾いをしている事公園、ゴミを置いていっちゃう人が多いよね。何か対策を考えて市役所に提案しようと思うんだ。
女1: お菓子の袋とかペットボトルとか、置いていっちゃう人がいるんですね。
男1: 市の方針でゴミ箱は置かないことになってるからね。
男2: 特にゴミが多いところから対策を考えた方がいいんじゃないですか?ゴミが目立つところに花壇を作るとか。他の公園で花壇を作ったら、その周りはゴミが減ったそうですよ。
男1: ゴミが多いのはベンチの周りだよね?そこに花壇を作るのは難しいと思うんだ。
女1: 私は公園全体を考えた方がいいと思うんですが... [ゴミを持ち帰りましょう] って書いた看板を増やすのはどうですか?
男1: うーん、既にいくつか立ててあるから今以上に増やす必要ないんじゃないかな?</p>
女1: あと私たちボランティアが見回って、ゴミを持って帰ってもらうように直接声をかけるのも効果があると思うんですけど。
男1: ボランティアの負担が大きくなるのはちょっとね。うーん、まず、ゴミが多いところからなんとかしよう。 花壇を作る代わりにっていうアイデアが良さそうだね。市役所の担当者に早速提案してみよう。
</div>
<a class='follow_up'>公園のゴミを減らすため、何を市役所に提案することにしましたか？</a>
<ul class='options'> 
    <li>ベンチの近くに花壇を作ること</li>
    <li>ゴミを捨てないように看板を増やすこと</li>
    <li>公園を見回ること</li>
    <li>公園を見回ること</li>
</ul>
"""

comprehensive_expression_listen_answer_teacher_prompt = """
角色：你是一名日语老师，正在为JLPT N1水平撰写试卷。 

任务：你的工作是写3个人之间听起来很自然的对话。要求是2男1女，或者2女一男。

第一步，你应该介绍对话的背景。

第二步，生成的对话要求总长度约为500-600字。针对某个话题进行讨论，需要有核心思想。

第三步，问一个后续问题，问题可以关于是主角的想法、这段话的主题或说话者想表达什么。
主题应该适合语言学习者，并反映日常情况。

第四步，根据听力内容提供多项选择题。这些选项应该测试对对话含义的理解。

说明：
格式：遵循正式试卷中的例子的格式，但不要遵循内容。
内容：确保词汇限制在N1级。 
参考：根据用户提供的主题"Topic"汲取灵感，在生成内容时考虑前一次对话中给出的反馈和批评，并避免重复生成"历史题目"的问题(q)或给出的答案(a)。
附加要求：
-不要在生成的内容中显示问题说明和序列号。 
-句子中的单词既不能用于问题，也不能用于选项。
-在输出中显示正确答案，选项为1,2,3,4.例如：正解：n, 正确答案分布要平均，不要集中在某个选项


历史题目: {gan_history}
正式试卷：{example}
"""

comprehensive_expression_listen_answer_example = """
<p class='background'>池で行われているイベントでアナウンスを聞いた後、女の人と男の人が話しています。</p>

<div class='conversation'>
女1: 本日は桜花祭りにお越しくださり、ありがとうございます。各会場についてご案内いたします。中央会場では、今日捕れた魚や貝をその場で焼いてお召し上がりいただけます。こちらは、なくなり次第終了いたします。南会場では、初心者向けの釣り教室を開催しています。道具の貸し出しもあります。餌の付け方なども教えいたします。東会場では、海の生き物が観察できます。地元の海の生き物を間近で見ることができ、お子様も大人の方も楽しめいただけます。西会場では、新鮮な魚介類を販売しています。
女2: 新鮮な魚、おいしそう。なくなり前に早く行かなきゃ？
男1: え？早速買い物？先に買っちゃうともっとたくさん食べられない？
女2: あ、そうか。そんなに自分でたくさん食べられないって言うなら、買い物は最後にしようよ。
男1: あ、そうしような。まずはここに行こう。そんなに近くで生き物を観察できるって言うなら、買い物は最後にしようよ。
女2: いいよ。釣りはいいの？
男1: うーん、初心者向けって言ってたから今日は初めてていいかな。
</div>
<a class='follow_up_01'>質問1: 2人は最初にどの会場に行くですか？</a>
<ul class='options_01'> 
    <li>中央会場</li>
    <li>南会場</li>
    <li>東会場</li>
    <li>西会場</li>
</ul>
<a class='follow_up_02'>質問2: 2人は2番目にどの会場に行くですか？</a>
<ul class='options_02'> 
    <li>中央会場</li>
    <li>南会場</li>
    <li>東会場</li>
    <li>西会場</li>
</ul>

"""

kanji_reading_reflection_prompt = """
"""

write_kanji_reflection_prompt = """
"""

word_collocation_reflection_prompt = """
"""

word_meaning_reflection_prompt = """
"""

synonym_substitution_reflection_prompt = """
"""

word_usage_reflection_prompt = """
"""

sentence_grammar_reflection_prompt = """
"""

sentence_sort_reflection_prompt = """
"""

structure_selection_reflection_prompt = """
"""

short_reading_narrative_reflection_prompt = """
"""

short_reading_mail_reflection_prompt = """
"""

short_reading_notification_reflection_prompt = """
"""

midsize_reading_reflection_prompt = """
"""

comprehensive_read_reflection_prompt = """
"""

long_reading_understanding_reflection_prompt = """
"""

long_reading_reflection_prompt = """
"""

information_retrieval_reflection_prompt = """
"""

topic_understanding_img_reflection_prompt = """
"""

topic_understanding_txt_reflection_prompt = """
"""

keypoint_understanding_reflection_prompt = """
"""

summary_understanding_reflection_prompt = """
"""

actively_expression_reflection_prompt = """
"""

immediate_ack_reflection_prompt = """
"""

comprehensive_expression_show_answer_reflection_prompt ="""
"""

comprehensive_expression_listen_answer_reflection_prompt ="""
"""



