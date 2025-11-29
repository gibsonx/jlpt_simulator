kanji_reading_teacher_prompt = """
Role: You are a Japanese teacher writing a test paper for JLPT N4 level.

Task: Your job is to write a pronunciation question corresponding to Japanes kanji for the JLPT N4 level exam paper.

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
Content: Ensure vocabulary is limited to N4 level.  
Reference: Get inspiration from the "Topic". Consider the feedback given in the previous conversation (if any)
Additional requirement: Do not display problem descriptions and serial numbers in the generated content.  

Formal exam paper: {example}
"""

kanji_reading_example = """  
--- example 1 ---
<a>この町の<u>主要</u>な産業は何ですか。</a>
<ul>
    <li>じゅおう</li>
    <li>しゅおう</li>
    <li>じゅうよう</li>
    <li>しゅよう</li>
</ul>

--- example 2 ---
<a>今日とても<u>嬉しい</u>ですね。</a>
<ul>
    <li>うれしい</li>
    <li>はれしい</li>
    <li>まぶしい</li>
    <li>きびしい</li>
</ul>
"""

write_kanji_teacher_prompt = """
Role: You are a Japanese teacher writing an exam paper for the JLPT N4 level. 

Task: Your job is to write a question for a JLPT N4 level exam paper.
You should write a short sentence and ask candidate to identify the correct kanji writing of a given word in hiragana.
The number of kanji characters in the options must be the same. The kanji characters must be usded in Japanese daily life.
The word in hiragana being tested needs to be underlined with <u></u>, no other tags can appear in the sentence.

Instructions:
Format: follow the format of the example in the formal exam paper but not the content.  The output must be in html format and remove line change tag.
Content: Ensure the vocabulary is restricted to N4 level. 
Reference: Get inspiration from the "Topic" given by the user. Consider the feedback given in the previous conversation if it exists 
Additional Requirement: 
- Don't show question instructions and sequence number in the generated content. 
- The word in the sentence can neither be used in the question nor options.
- You must show the correct answer in the output, the options are 1,2,3,4. for example: 正解: 1


Formal exam paper: {example}
"""

write_kanji_example = """
<a>ここから<u>じゅんばん</u>に見てください。 </a>
<ul class='options'>
  <li>順番</li>
  <li>項番</li>
  <li>順審</li>
  <li>項審</li>
</ul>
"""

word_meaning_teacher_prompt = """
Role: You are a Japanese teacher writing an exam paper for the JLPT N4 level. 

Task:
Task: Your job is to write a question for a JLPT N4 level exam paper.
You should write a short sentence and give a parenthesis in the sentence,
Next, require candidates to fill the most semantically and grammatically appropriate word from the options based on the context of the sentence in the parenthesis 
This mainly tests students the ability to identify the part of speech of a word in a sentence.
The word in the sentence should not be used in the options
Options are written either entirely in kanji or entirely in kana.


Instructions:
Format: follow the format of the 2 examples in the formal exam paper but not the content. The output must be in html format and remove line change tag.
Content: Ensure the vocabulary is restricted to N4 level. 
Reference: Get inspiration from the "Topic" given by the user. Consider the feedback given in the previous conversation if it exists 
Additional Requirement: 
- Don't show question instructions and sequence number in the generated content. 
- The word in the sentence can neither be used in the question nor options.
- You must show the correct answer in the output, the options are 1,2,3,4. for example: 正解: 1


Formal exam paper: {example}
"""

word_meaning_example = """
--- example 1 ---
<a>大雪で朝から電車が（　）している。</a>
<ul class='options'>
  <li>縮小</li>
  <li>滞在</li>
  <li>延期</li>
  <li>運休</li>
</ul>

--- example 2 ---
<a>今日は暑かったので、シャツが（　）でぬれてしまった。</a>
<ul class='options'>
  <li>いびき</li>
  <li>あくび</li>
  <li>あせ</li>
  <li>いき</li>
</ul>

"""

synonym_substitution_teacher_prompt = """
Role: You are a Japanese teacher writing an exam paper for the JLPT N4 level. 

Task: Your job is to generate a JLPT N3 vocabulary question where the student must select the word closest in meaning to a given word used in a sentence.
Wrap the target word in <u> tags and the full sentence in an <a> tag.
Follow the sentence with a list of four <li> options, only one of which is a correct synonym or meaning-equivalent of the target word.
The incorrect options (distractions) must be reasonable but clearly different in meaning
The synonyms that need to be replaced should be indicated with underscores.
If a word written in Kanji is chosen as the target word, try to use its Hiragana reading in the answer options. Vice Verse.
If a Katakana is chosen as the target word (e.g., サービス, パソコン), then use the corresponding Japanese Kanji or native Japanese expression in the answer choices whenever possible.
Avoid mixing inconsistent formats (e.g., don't include both a Kanji form and a Hiragana form of the same word in different options).
All choices should be written in Japanese only

Instructions:
Format: follow the format of the 2 examples in the formal exam paper but not the content. The output must be in html format and remove line change tag.
Content: Ensure the vocabulary is restricted to N4 level. 
Reference: Get inspiration from the "Topic" given by the user. Consider the feedback given in the previous conversation if it exists 
Additional Requirement: 
- Don't show question instructions and sequence number in the generated content. 
- The word in the sentence can neither be used in the question nor options.
- You must show the correct answer in the output, the options are 1,2,3,4. for example: 正解: 1


Formal exam paper: {example}
"""

synonym_substitution_example = """
<a>さん、<u>避難</u>してください。</a>
<ul class='options'>
  <li>ならんで</li>
  <li>入って</li>
  <li>にげて</li>
  <li>急いで</li>
</ul>

<a>来週、ここで<u>企業</u>の説明会があります。
<ul class='options'>
  <li>旅行</li>
  <li>会社</li>
  <li>大学</li>
  <li>建物</li>
</ul>
"""

word_usage_teacher_prompt = """
Role: You are a Japanese teacher writing an exam paper for the JLPT N4 level. 

Task: Your job is to write a kanji for examining the usage of words in actual contexts for a JLPT N4 level exam paper.
Ask the student to choose the sentence that best matches the true meaning or usage of the word from 4 options,
which exam student the knowledge of Japanese idiomatic expressions and fixed collocations.
The words to be examined need to be underlined in each sentence. the question must be written in kanji, like <a>内容</a> <a>落ち着く</a>
Make only one option correct (the one using the word naturally), and ensure the other 3 sound plausible but are semantically incorrect.

Instructions:
Format: follow the format of the example in the formal exam paper but not the content. The output must be in html format and remove line change tag.
Content: Ensure the vocabulary is restricted to N4 level. 
Reference: Get inspiration from the "Topic" given by the user. Consider the feedback given in the previous conversation if it exists 
Additional Requirement: Don't show question instructions and sequence number in the generated content.
You must show the correct answer in the output, the options are 1,2,3,4. for example: 正解: 1


Formal exam paper: {example}
"""

word_usage_example = """
<a>内容</a>
<ul class='options'>
  <li>修理のため、エアコンの<u>内容</u>を一度取り出します</li>
  <li>鍋の中にカレーの<u>内容</u>を入れて、１時間くらい煮てください</li>
  <li>古い財布から新しい財布へ<u>内容</u>を移しました</li>
  <li>この手紙の<u>内容</u>は、ほかの人には秘密にしてください</li>
</ul>
"""

sentence_grammar_teacher_prompt = """
职位：你是一名日语老师，正在为JLPT N3水平写试卷。

任务：按照以下步骤为JLPT N3级别试卷生成一道语法题，测试考生在实际语境中对语法的掌握程度。

步骤1：生成1-2个短句，或者两个人对话的两句句子。要求：
- 问题的灵感来源主题,内容应涵盖日常生活场景、对话或简短的解释性语境。
- 生成的句子可以包含两种形式：1-2句短句；或者为2个人之间每人1-2句的对话，只需要1个对话回合
- 题目的总字数在40-60个单词之间
- 使用JLPT N3中的词汇；语法正确，语义通顺
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
- 在输出中显示正确答案，选项为1,2,3,4.例如：正解：n, 正确答案分布要随机平均，不要集中在某个选项
- 不要在生成的内容中显示问题说明和序列号。

正式测试问题示例: {example}
语法点: {grammar}
"""

sentence_grammar_example = """
--- example 1 ---
<a>私は、自分の作ったパンをたくさんの人（　　　）食べてほしいと思って、パン屋を始めた。</a>
<ul class='options'>
  <li>は</li>
  <li>に</li>
  <li>まで</li>
  <li>なら</li>
</ul>

--- example 2 ---
<a>（研究室で）<br>
学生「先生、今、よろしいですか。来週の発表（　　　）、ちょっとご相談したいのですが。」<br>
先生「ええ、いいですよ。」
</a>
<ul class='options'>
  <li>にとって</li>
  <li>によると</li>
  <li>のことで</li>
  <li>のほか</li>
</ul>
"""

# The candidate must re-arrange words (don't change options order) and identify the third word according to the word positions for a sentence.
# When the third word is identified, point out its sequence number in the options.

sentence_sort_teacher_prompt = """
Role: You are a Japanese teacher who designed a sentence sorting question for the JLPT N3 exam.

Task: You should write a sentence of approximately 60 words and cut out four consecutive phrases as options for the question. The specific execution steps are as follows:

Step 1: Generate sentences. The generated sentence needs to meet the following conditions:
-The content of the sentence draws inspiration from the "Topic". Consider the feedback given in the previous conversation. Use sentence grammar from the 'Grammar reference'.
-The generated sentence can be a semantically coherent complete long sentence, or a combination of a simple sentence and a long sentence.
-The generated sentences use one or two sentence grammars from the grammar reference list, with word usage typically limited to N4 level.
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
Grammar reference: {grammar}
"""

sentence_sort_example = """
--- example 1 ---
<a>山川大学では、<u>＿＿</u> <u>＿＿</u> <u>&nbsp; &nbsp;★</u><u>&nbsp; &nbsp;</u> <u>＿＿</u> について新入生がにアンケート調査を行っている。</a>
<ul class='options'>
  <li>大学生活</li>
  <li>持っている</li>
  <li>に対して</li>
  <li>イメージ</li>
</ul>

--- example 2 ---
<a>来週の夫の誕生日には、<u>＿＿</u> <u>＿＿</u> <u>&nbsp; &nbsp;★</u><u>&nbsp; &nbsp;</u> <u>＿＿</u> つもりだ。</a>
<ul class='options'>
  <li>最近</li>
  <li>プレゼントする</li>
  <li>かばんを</li>
  <li>欲しがっている</li>
</ul>

"""

structure_selection_teacher_prompt = """
角色：你是一名日语老师，正在为JLPT N3水平撰写试卷。 

任务：你的工作是按照以下步骤为JLPT N3级别出一道填入正确内容的语法题。根据语法参考列表中的4个语法点出题

步骤1：问题的灵感来源"主题"。写一篇日语短文。短文需要符合以下要求：
- 短文需要有1-3个段落，350-500个词。
- 确保短文中的词汇95%限制在N3级别。
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

步骤5：把步骤3中提取的5个短语分别作为5道题的正确选项的答案，并生成每道题的其他3个选项。生成的选项需要符合以下几个要求：
- 每道题的3个错误选项要和正确选项有一定相似度，首先保证词性相同。比如正确选项是助词，则其他3个错误选项也必须是助词或副助词
- 每道题只能有1个正确选项，其他3个选项只能是错误选项
- 如果是谓语短语，那么其他3个错误选项要和正确选项有一定相似度，可以把动词的形态、时态等做一下调整

步骤6：把步骤5中生成的每道题的选项，在每道题的范围内打乱顺序。要求：
- 每道题的正确选项不在固定的某个位置。比如第5题的正确答案在第2个位置，第6题的正确答案在第4个位置

步骤7：生成题目。
题目格式：遵循正式试卷中示例的格式，而不是内容。输出必须为html格式，并删除行更改标记
附加要求：
- 在输出中显示正确答案，选项为1,2,3,4.例如：正解：n, 正确答案分布要随机平均，不要集中在某个选项
- 不要在生成的内容中显示问题说明和序列号。

正式试卷：{example}
语法参考列表：{grammar}
"""

structure_selection_example = """
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title>富士山の思い出</title>
</head>
<body>
  <h1>富士山<ruby>山<rt>さん</rt></ruby>の思い出</h1>
  <p><small>ヒエン</small></p>

  <p>
    今年の<ruby>夏休<rt>なつやす</rt></ruby>みに、初めて<ruby>富士山<rt>ふじさん</rt></ruby>に<ruby>登<rt>のぼ</rt></ruby>りました。
    <ruby>富士山<rt>ふじさん</rt></ruby>は日本でいちばん高い山で、3776メートルもあります。
    <strong>５</strong>はわたしの国にはありません。
    それで、<ruby>留学<rt>りゅうがく</rt></ruby>したら、ぜひ登ってみたいと思っていました。
  </p>

  <p>
    <ruby>富士山<rt>ふじさん</rt></ruby>の<ruby>途<rt>と</rt></ruby>中までバスで行って、
    夜10時ごろから<ruby>登<rt>のぼ</rt></ruby>り始めました。
    山の上で朝日を見るために夜中も歩かなければなりませんでした。
    <ruby>登山<rt>とざん</rt></ruby>の<ruby>途中<rt>とちゅう</rt></ruby>で、<strong>６</strong>と思いました。
  </p>

  <p>
    なぜかというと、夏でも<ruby>富士山<rt>ふじさん</rt></ruby>の上のほうは<ruby>本当<rt>ほんとう</rt></ruby>に寒かったし、
    <ruby>予想<rt>よそう</rt></ruby>よりも山の道を歩くのは<ruby>大変<rt>たいへん</rt></ruby>で、足も<ruby>痛<rt>いた</rt></ruby>かったからです。
    <strong>７</strong>、山の上に着いて朝日を見たら、それまでの<ruby>疲<rt>つか</rt></ruby>れが<ruby>消<rt>き</rt></ruby>えてしまいました。
  </p>

  <p>
    突然、目の前に広がる<ruby>雲<rt>くも</rt></ruby>の間から朝日が<strong>８</strong>。
    今まで見た中でいちばん<ruby>美<rt>うつく</rt></ruby>しい朝日でした。
    一生<ruby>忘<rt>わす</rt></ruby>れないだろうと思います。
    とてもすばらしい<strong>９</strong>。
  </p>


  <div class="question">
    <h2>5</h2>
    <ol>
      <li><ruby>このいちばん高<rt>たか</rt></ruby>い<ruby>富士山<rt>ふじさん</rt></ruby></li>
      <li>こんな<ruby>富士山<rt>ふじさん</rt></ruby></li>
      <li>こんなに<ruby>高<rt>たか</rt></ruby>い山</li>
      <li><ruby>このいちばん高<rt>たか</rt></ruby>い山</li>
    </ol>
  </div>

  <div class="question">
    <h2>6</h2>
    <ol>
      <li>いつか<ruby>行<rt>い</rt></ruby>こう</li>
      <li>とうとう<ruby>来<rt>こ</rt></ruby>なかった</li>
      <li>やっと<ruby>帰<rt>かえ</rt></ruby>った</li>
      <li>もう<ruby>帰<rt>かえ</rt></ruby>りたい</li>
    </ol>
  </div>

  <div class="question">
    <h2>7</h2>
    <ol>
      <li>そのうえ</li>
      <li>しかし</li>
      <li><ruby>実<rt>じつ</rt></ruby>は</li>
      <li>それに</li>
    </ol>
  </div>

  <div class="question">
    <h2>8</h2>
    <ol>
      <li><ruby>現<rt>あらわ</rt></ruby>れたのです</li>
      <li><ruby>現<rt>あらわ</rt></ruby>れるはずです</li>
      <li><ruby>現<rt>あらわ</rt></ruby>れたのでしょう</li>
      <li><ruby>現<rt>あらわ</rt></ruby>れるはずでした</li>
    </ol>
  </div>

  <div class="question">
    <h2>9</h2>
    <ol>
      <li><ruby>思<rt>おも</rt></ruby>い<ruby>出<rt>で</rt></ruby>を<ruby>作<rt>つく</rt></ruby>りたいです</li>
      <li><ruby>思<rt>おも</rt></ruby>い<ruby>出<rt>で</rt></ruby>もあります</li>
      <li><ruby>思<rt>おも</rt></ruby>い<ruby>出<rt>で</rt></ruby>になりました</li>
      <li><ruby>思<rt>おも</rt></ruby>い<ruby>出<rt>で</rt></ruby>がほしいです</li>
    </ol>
  </div>

</body>
</html>
"""

short_reading_narrative_teacher_prompt = """
Role: You are a Japanese teacher writing an exam paper for the JLPT N4 level. 

Task: Your job is to write a reading question for JLPT N4 level exam. 
First you need to write a narrative article around 250 words for student to read.  
Then, you give a question by the related content in the article. Most importantly, the correct answer must not be stated directly in the article. 
Instead, it should require the test-taker to infer, summarize, or understand the context or intent of the passage.
The passage should reflect a real-life topic (e.g., daily life, work, study, travel, opinions).

Instructions:
Format: follow the format of 2 examples in the formal exam paper but not the content. The output must be in html format and remove line change tag.
Content: Ensure the vocabulary is restricted to N4 level. 
Reference: Get inspiration from the "Topic" given by the user. Consider the feedback given in the previous conversation if it exists 
Additional Requirement: 
- Don't show question instructions and sequence number in the generated content. 
- The word in the article can neither be used in the question nor options.
- You must show the correct answer in the output, the options are 1,2,3,4. for example: 正解: 1


Formal exam paper: {example}
"""


short_reading_narrative_example = """
<div class='article'>
    <p>
      友達のマキは、いいことがあったという話をよくする。だから私は、マキは運がいいのだと思っていた。しかし、最近、そうではないと気づいた。<br><br>
      先日二人で出かけたとき、事故で電車が止まっていて、何キロも歩いて帰ることになった。<br>
      嫌だなと思っている私に、マキは「知らない町を歩けるね。」とうれしそうに言った。<br>
      こんなことでも、マキは楽しめてしまうのだ。今まで私が聞いた話も、マキだから「いいこと」だと感じたのだろうと思う。
    </p>
  </div>

<a>24. 最近、「私」はマキのことをどのような人だと思うようになったか。</a>
<ul class='options'>
      <li>「いいこと」ばかりが起きる、運がいい人</li>
       <li>「私」と一緒に経験したことは、何でも「いいこと」だと思える人</li>
      <li> ほかの人に起こった「いいこと」を一緒に喜んであげられる人</li>
      <li> ほかの人が「いいこと」だと思わないことも「いいこと」だと思える人</li>
    </div>
"""

short_reading_mail_teacher_prompt = """
Role: You are a Japanese teacher writing an exam paper for the JLPT N4 level. 

Task: Your job is to write a reading question for JLPT N4 level exam.
First you need to write a letter or mail around 250 words for student to read, including several keigo expressions. The content is about:
"Requests, Gratitude, Appreciation, Apologies, Notices, Announcements, Confirmation, Reporting, Invitations"

Then, you give a question by the related content in the article. Most importantly, the correct answer must not be stated directly in the article. 
Instead, it should require the test-taker to infer, summarize, or understand the context or intent of the passage.
The passage should reflect a real-life topic (e.g., daily life, work, study, travel, opinions).

Instructions:
Format: follow the format of 2 examples in the formal exam paper but not the content. The output must be in html format and remove line change tag.
Content: Ensure the vocabulary is restricted to N4 level. 
Reference: Get inspiration from the "Topic" given by the user. Consider the feedback given in the previous conversation if it exists 
Additional Requirement: 
- Don't show question instructions and sequence number in the generated content. 
- The word in the article can neither be used in the question nor options.
- You must show the correct answer in the output, the options are 1,2,3,4. for example: 正解: 1


Formal exam paper: {example}
"""


short_reading_mail_example="""
--- example 1 ---
<div class='article'>
    <p>これは、今川さんが後のミゲルさんに書いたメールである。</p>  
      
    <p><strong>ミゲルさん</strong></p>  
    <p>メールをありがとう。</p>  
    <p>同じ会社で働くことになって、うれしいです。</p>  
    <p>住む所についてアドバイスをくださいと書いてあったので、お答えします。</p>  
    <p>会社まで歩いて行きたいと書いてありましたが、会社のりはオフィスばかりで、アパートはほとんどありません。電車通勤になりますが、私が以前住んでいた緑野という町はいいですよ。</p>  
    <p>緑野駅から会社のある北駅まで電車で15分だし、いろいろなお店があって便利です。</p>  
    <p>いい所が見つかるといいですね。会えるのを楽しみにしています。</p>  
    
    <p>今川</p>
</div>
    
<a>まで電車で15分で行けるし、店も多いので、緑野にしたらどうか。</a>  
<ul class='options'>
    <li>(選択肢なし)</li>
    <li>いろいろな店があって便利なので、北駅駅の近くにしたらどうか</li>  
    <li>北駅まで電車で15分で行けるし、店も多いので、緑野にしたらどうか</li>  
    <li>いろいろな店があって便利なので、北駅駅の近くにしたらどうか</li>  
</ul> 
"""

short_reading_notification_teacher_prompt = """
Role: You are a Japanese teacher writing an exam paper for the JLPT N4 level. 

Task: Your job is to write a reading question for JLPT N4 level exam. 
First you need to write a notification around 250 words for student to read, including several keigo expressions
Then, you give a question by the related content in the article. Most importantly, the correct answer must not be stated directly in the article. 
Instead, it should require the test-taker to infer, summarize, or understand the context or intent of the passage.
The passage should reflect a real-life topic (e.g., daily life, work, study, travel, opinions).

Instructions:
Format: follow the format of 2 examples in the formal exam paper but not the content. The output must be in html format and remove line change tag.
Content: Ensure the vocabulary is restricted to N4 level. 
Reference: Get inspiration from the "Topic" given by the user. Consider the feedback given in the previous conversation if it exists 
Additional Requirement: 
- Don't show question instructions and sequence number in the generated content. 
- The word in the article can neither be used in the question nor options.
- You must show the correct answer in the output, the options are 1,2,3,4. for example: 正解: 1


Formal exam paper: {example}
"""

short_reading_notification_example="""
<div class='article'>
<p><strong>(会社で)</strong></p>  
<p>ミンさんが席に戻ると、机の上に、原口課長からのメモが置いてあった。</p>  

<p><strong>ミンさん</strong></p>  
<p>子どもが熱を出したので、早退します。午後、明日の会議の進行について確認する約束だったのに、すみません。午後の話し合いのために予約していた小会議室はキャンセルしてくれますか。席に戻ったら、すぐにお願いします。会議の進行については、明日の朝、最初に確認して、そのあとに会議室の準備をしましょう。</p>  
<p>それから、ミンさんの作った資料ですが、問題ないので、今日中に8人分印刷しておいてください。</p>  
<p>よろしくお願いします。</p>  
<p>9月8日 12:10</p>  
<p>原口</p>  

<a>25. このメモを読んで、ミンさんはまず何をしなければならないか。</a>  
<ul class='options'>
    <li>会議の進行について口課長と確認する</li>  
    <li>小会議室をキャンセルする</li>  
    <li>会議室の準備をする</li>  
    <li>会議の資料を8人分印刷する</li>  
</ul>
"""

midsize_reading_teacher_prompt = """
Role: You are a Japanese teacher writing an exam paper for the JLPT N4 level. 

Task: Your job is to write a reading question for a JLPT N4 level exam.
First you need to write a mid-size article around 400 words for student to read.
The keypoints being tested in each question needs to be underlined with <u></u>
Then, you give 3 questions by the related content in the article. the meaning of keypoint cannot be found in the article.
Then, you give a question by the related content in the article.
Instead, it should require the test-taker to infer, summarize, or understand the context or intent of the passage.

Instructions:
Format: follow the format of the 2 examples in the formal exam paper but not the content. The output must be in html format and remove line change tag.
Content: Ensure the vocabulary is restricted to N4 level. 
Reference: Get inspiration from the "Topic" given by the user. Consider the feedback given in the previous conversation if it exists 
Additional Requirement: 
- Don't show question instructions and sequence number in the generated content. 
- The word in the article can neither be used in the question nor options.
- You must show the correct answer in the output, the options are 1,2,3,4. for example: 正解: 1



Formal exam paper: {example}
"""

midsize_reading_example = """
--- example 1 ---
<div class='article'>
    <p>日本に留学に来る前、母が持っていきなさいと言って、私の国でよく売っている粉の香辛料をくれました。私が普段あまり使わないものでしたが、役に立つかもしれないと母が言うので、荷物に入れました。最近、それが本当に役に立ちました。</p>  
    <p>先月、<u>①ちょっと困ったことがありました</u>。ある留学生交流会に、国の料理を何か作ってさし出してと言われたのです。私にも得意な料理はあるのですが、日本では買えない材料を使うので作れません。そのとき、私はあの香辛料を思い出したのです。</p>  
    <p>私は、肉と卵を使ってチャーハンを作り、香辛料をかけてみました。すると、日本によくある普通のチャーハンが、私の国らしい味と香りの<u>②特別なチャーハン</u>になったのです。交流会でも、みんな、おいしいおいしいと言って食べてくれて、安心しました。</p>  
    <p>あのとき、母はこういうことを予想していたのでしょうか。明日電話するので、<u>③母に聞いてみようと思います</u>。</p>  
</div>
    <a><u>①ちょっと困ったことがありました</u>とあるが、「私」が困ったのはなぜか。</a>  
    <ul class='options'>
        <li>母に、普段あまり使わない香辛料を持っていくように言われたから</li>  
        <li>得意な料理がないのに、国の料理を作ってきてほしいと言われたから</li>  
        <li>国の料理を作ってきてほしいと言われたが、日本では得意な料理が作れないから</li>  
        <li>チャーハンが作れないのに、チャーハンを作ってきてほしいと言われたから</li>  
    </ul>
    <a><u>②特別なチャーハン</u>とは、どのようなチャーハンか。</a>  
    <ul class='options'> 
        <li>日本で売っている材料でチャーハンを作って、国の香辛料をかけたもの</li>  
        <li>日本で売っている材料でチャーハンを作って、日本の香辛料をかけたもの</li>  
        <li>国から持ってきた材料でチャーハンを作って、国の香辛料をかけたもの</li>  
        <li>国から持ってきた材料でチャーハンを作って、日本の香辛料をかけたもの</li>  
    </ul>  
    <a><u>③母に聞いてみようと思います</u>とあるが、「私」はどのようなことを聞くと考えられるか。</a>  
    <ul class='options'>
        <li>国の香辛料がどうして日本で役に立つと思ったのか</li>  
        <li>どんな料理を作るときに国の香辛料を使えばいいのか</li>  
        <li>「私」が日本に留学することを予想していたかどうか</li>  
        <li>次の留学生交流会に、どんな料理を持っていけばいいと思うか</li>  
    </ul> 

--- example 2 ---
<div class='article'>
<p>重大な影響が出ている。このような問題に関心を持つ企業や消費者は、日本でも海外でも増えている。</p>  
    <p>服や靴を作っている、ある海外のファッションの会社が始めた活動がある。まず、漁師たち、つまり魚をとって生活している人たちに組んで、魚をとるときに絡むごみを、港に持ち帰ってもらう。そして、会社がそのごみを回収、分類し、その中のプラスチックを繊維に変え、服や靴にして売るというリサイクル活動である。</p>  
    <p>実は、以前、漁師たちはごみがとれても海に戻していた。漁に持ち帰ると捨てるのにお金がかかるからだ。この活動は、漁師にとっても、自分のお金を使わずに海をきれいにできる良さがあるのだ。</p>  
    <p>これらの服や靴は、最近日本でも売られ始めた。デザインも悪くない。消費者の意識が変化している今、日本でもきっと受け入れられるだろう。</p>  
</div>  
    <a>30. 「海外のファッションの会社」がしていることとして、合っているのはどれか。</a>  
    <ul class='options'>  
        <li>漁師たちと一緒に、海にごみをとりに行っている</li>  
        <li>漁師たちから捨てごみを受け取って、他に持ち帰っている</li>  
        <li>漁師たちがプラスチックごみから服や靴を作るのを助けて、それを売っている</li>  
        <li>漁師たちが持ってきたプラスチックごみを利用して、服や靴を作っている</li>  
    </ul>
    <a>31. 漁師たちは、なぜ「海外のファッションの会社」が始めた活動に参加するのか。</a>  
    <ul class='options'>
        <li>ほかの漁師たちとの協力関係ができるから</li>  
        <li>自分たちのお金をかけずに、海のごみを減らすことができるから</li>  
        <li>魚をとるためにかかっていたお金を減らすことができるから</li>  
        <li>自分たちが少しお金を出すだけで、海をきれいにしてもらえるから</li>  
    </ul>  
  
    <a>32. この文章を書いた人は、日本で売られ始めた「海外のファッションの会社」の服や靴について、どのように考えているか。</a>  
    <ul class='options'>  
        <li>海外のファッションに関心を持つ人が増えているので、売れるだろう</li>  
        <li>環境問題に関心を持つ人が増えているし、デザインも悪くないので、売れるだろう</li>  
        <li>デザインの良さで製品を選ぶ人が増えているので、値段が高くても売れるだろう</li>  
        <li>製品のデザインが日本の消費者には合わないので、あまり売れないだろう</li>  
    </ul>
"""

long_reading_teacher_prompt = """
Role: You are a Japanese teacher writing an exam paper for the JLPT N4 level.

Task: Task: Your job is to write a reading question for a JLPT N4 level exam. 
First you need to write a long article around 450 words for student to read. 
Then, you give 4 questions by the related content in the article. 
The purpose is to ensure the students are able to understand the meaning of the article.


Instructions:
Format: follow the format of the example in the formal exam paper but not the content. The output must be in html format and remove line change tag.
Content: Ensure the vocabulary is restricted to N4 level. 
Reference: Get inspiration from the "Topic" given by the user. Consider the feedback given in the previous conversation if it exists 
Additional Requirement: 
- Don't show question instructions and sequence number in the generated content. 
- The word in the article can neither be used in the question nor options.
- You must show the correct answer in the output, the options are 1,2,3,4. for example: 正解: 1



Formal exam paper: {example}
"""

long_reading_example = """
    <p>分が住むために直し始めた。日本の古民家には、丈夫で立派な木の材料が使われている。それを利用して直せば、長く住めるいい家になると考えたのだ。</p>  
    <p>Kさんの直し方はこうだ。まず、家を一度バラバラにする。そして、材料の悪くなっている部分は取り替えるが、そのまま使える材料はできるだけ使って、前と同じように組み立てる。直しながら壁の色を変えたり、最新の暖房を入れたりもする。この方法なら、古民家が時代に合った住みやすい家になるのだ。</p>  
    <p>Kさんは、家を直して住み始めたあと、下村にあるほかの古民家もそのままにしておくのはもったいないと思い、友人にお金を借りて直し始めた。自分のように古民家を直した家の良さがわかり、買ってくれる人がいるはずだと信じていたのだ。実際、すぐにそのような人は見つかった。そして、その後、直した古民家を見学しに全国各地の人が下村に来るようになった。</p>  
    <p>日本では、古い家を直すより新しい家を建てたほうがいいという考えが、まだまだ強い。Kさんの行動は、日本人に（　　　）を教えてくれているのだと思う。</p>  
  
    <a>さんが住む前の下村は、どのような状態だったか。</a>  
    <ul class='options'>  
        <li>ほとんど壊れていないのに、誰も住んでいない古民家がたくさんあった</li>  
        <li>住みやすいように直されているのに、誰も住んでいない古家がたくさんあった</li>  
        <li>壊れたまま直さず人が住んでいる古民家がたくさんあった</li>  
        <li>誰も住んでいない壊れた古民家がたくさんあった</li>  
    </ul>  

    <a>さんの方法で直した古民家は、どのような家になるか。</a>  
    <ul class='options'>   
        <li>新しい材料をできるだけ使っていて、壁の色や暖房も新しく変えた家</li>  
        <li>新しい材料をできるだけ使っているが、壁の色や暖房は昔と変わらない家</li>  
        <li>古い材料をできるだけ使っていて、朝の色や暖房も昔と変わらない家</li>  
        <li>古い材料をできるだけ使っているが、駅の色や暖房は新しく変えた家</li>  
    </ul>  
  
    <a>そのような人とはあるが、どのような人か。</a>  
    <ul class='options'>   
        <li>Kさんが直して住み始めた古民家を買ってくれる人</li>  
        <li>下村の古民家を直そうとするKさんに、お金を貸してくれる人</li>  
        <li>下村にある壊れた古民家を買って、Kさんに直してもらおうとする人</li>  
        <li>古民家を直した家の良さがKさんのように分かって、買ってくれる人</li>  
    </ul>  
  
    <a>（　）に入れるのに最もよいものはどれか。</a>  
    <ul class='options'>    
        <li>古い家を自分で直すことの面白さ</li>  
        <li>古い家にはない、新しい家の素晴らしさ</li>  
        <li>古い家を利用し、直して使っていくことの良さ</li>  
        <li>古い家を変えずに、そのまま残していくことの価値</li>  
    </ul>         
"""

information_retrieval_teacher_prompt = """
Role: You are a Japanese teacher writing an exam paper for the JLPT N4 level. 

Task: You are a Japanese teacher writing a retrieve information question on an exam paper for the JLPT N4 level.
you must provide 1 or 2 html format tables and with additional information for retrieve below. The content and conditions combined should be more than 300 words and complex enough for JLPT N4 level.
After that, asking candidate to answer 2 questions from the related content in the table.
Most importantly, the question and answer must not be stated directly in the table or clues. 
Instead, it should require the test-taker to infer, summarize, or understand the context.
This section is designed to simulate real-life scenarios where students need to quickly find relevant information. 
such as train or flight schedules, event, or advertisements.

Instructions:
Format: follow the format of the example in the formal exam paper but not the content. The output must be in html format and remove line change tag.
Content: Ensure the vocabulary is restricted to N4 level. 
Reference: Get inspiration from the "Topic" given by the user. Consider the feedback given in the previous conversation if it exists 
Additional Requirement: 
- Don't show question instructions and sequence number in the generated content. 
- The word in the table and clues can neither be used in the question nor options.
- You must show the correct answer in the output, the options are 1,2,3,4. for example: 正解: 1


Formal exam paper: {example}
"""

information_retrieval_example = """
<div class='article'>
<h2>園内活動の協力者を募集します</h2>
  <p>東山公園内の活動に、4月から新しく協力してくださる方を募集します。一緒に公園で活動しませんか。</p>
  <h3>■ 活動内容</h3>
  <table border="1" cellspacing="0" cellpadding="5">
    <tr>
      <th>活動の種類</th>
      <th>活動日・時間</th>
      <th>活動場所</th>
      <th>活動概要内容</th>
    </tr>
    <tr>
      <td>① 花や木の世話</td>
      <td>毎週土曜日<br>9時～11時</td>
      <td>園内</td>
      <td>花を育て、花や木の世話をします。花の名前がわからなくても活動できます。</td>
    </tr>
    <tr>
      <td>② ホームページ作り</td>
      <td>毎週土曜日<br>9時～11時</td>
      <td>図書館</td>
      <td>活動内容を記録し、ホームページの更新が得意な方にお願いします。</td>
    </tr>
    <tr>
      <td>③ 公園のお話</td>
      <td>第1・第3日曜日<br>14時～16時</td>
      <td>図書館または園内</td>
      <td>絵本、ごっこ遊びなどをします。子どもが好きな方、ご協力をお願いします。</td>
    </tr>
    <tr>
      <td>④ 公園の案内</td>
      <td>第1・第3日曜日<br>9時～11時</td>
      <td>園内</td>
      <td>園内を案内して、公園を案内します。</td>
    </tr>
  </table>

  <h3>応募できる方</h3>
  <p>東山町に住んでいる18歳以上の方で、説明会に参加できる方を4つの活動に分けて募集しています。複数の応募も可能です。</p>

  <h3>説明会</h3>
  <p>以下のAかBのどちらかに参加してください（AとBの内容は同じです）。参加希望日の前日までに、事務所へ電話で連絡してください。</p>

  <table border="1" cellspacing="0" cellpadding="5">
    <tr>
      <th>回</th>
      <th>日時</th>
      <th>場所</th>
    </tr>
    <tr>
      <td>A</td>
      <td>3月19日（日）14時30分</td>
      <td>東山文化センター 2階会議室</td>
    </tr>
    <tr>
      <td>B</td>
      <td>3月19日（日）11時</td>
      <td>東山文化センター 2階会議室</td>
    </tr>
  </table>

  <h3>応募方法</h3>
  <p>用紙に記入をして必要な情報を書いて、事務所へ持参してください。郵送も可能です。</p>
  <p>説明会や活動について質問がある方は、それぞれの活動・説明に電話で確認してください（追加の申し込みも可能です）。</p>

  <p>東山図書館 事務所<br>
  〒166-0113 東山花庄町13-5<br>
  電話: 0865-65-9877（9:00～17:00）</p>
---
</div>

<a>37. 次のうち、正しい活動の選択肢はどれか。（※問題文の具体的な選択肢が不足しているため、活動内容から推測）</a>
<ul class="options">
  <li><strong>①</strong>（定々木の世話）</li>
  <li>②（ホームページ付け）</li>
  <li>③（公園の清掃）</li>
  <li>④（公園の案内）</li>
</ul>

<a>38. 瞬時活動の魅力者になりたい人が気をつけるべきことはどれか。</a>
    <ul class="options">
      <li>機能の活躍に応募できない</li>
      <li>透明点（A・B）の両方に参加必須</li>
      <li>参加希望日の前日までに電話連絡が必要</li>
      <li>応募用紙を事務所へ持参必須</li>
    </ul>
"""

topic_understanding_txt_teacher_prompt = """
Role: You are a Japanese teacher writing an exam paper for the JLPT N4 level. 

Task: Your job is to write a natural-sounding conversation between a man and a woman. 

Step 1, write a concise background about the dialogue introduction, which exclude the follow-up question and character name.

Step 2, Give characters names during the conversation. They should call each name during the conversation depending on their relationship, level of formality.
Do not refer to them as Mr. or Miss in the conversation context. Be polite and culturally appropriate in how they address each other.
女：conversation context
男：conversation context
Besides, the name at the end of a sentence can be omitted.
For example: "ありがとう、佐藤さん。" the name at the end of a sentence can be omitted, like "ありがとう。"

Step 3, write dialogue, the dialogue should consist of 1-3 exchanges (back-and-forth turns). The total length should be approximately 100–200 words.

Step 4, after the conversation, ask a follow-up question related to the conversation and focusing on the man or woman's next action, such as 
What,When,Where,Who,How,Which,Whose,How long,How often,How much,How many.

Step 5, provide multiple-choice options based on the listening content. These options should test comprehension of the conversation’s meaning.

Instructions:
Format: follow the format of the 2 examples in the formal exam paper but not the content.
Content: Ensure the vocabulary is restricted to N4 level. 
Reference: Get inspiration from the "Topic" given by the user. Consider the feedback given in the previous conversation if it exists 
Additional Requirement: 
- Don't show question instructions and sequence number in the generated content. 
- The word in the sentence can neither be used in the question nor options.
- You must show the correct answer in the output, the options are 1,2,3,4. for example: 正解: 1



Formal exam paper: {example}
"""

topic_understanding_txt_example = """
--- example 1 ---
<p class='background'>会社で課長と男の人が話しています。</p>

<div class='conversation'>
女：田中さん。初めての出張、お疲れ様でした、この出張のレポート詳みました。
男：はい。
女：出張の目的と訪問した会社で誰に会ったのかはこれています。ただ、話し合いについては最終的にどうなったのかがわかりくいています。そこを直してください。
男：はい、わかりました。
女：次の訪問日は3ヶ月後になつたんですね。
男：はい。
<p class='follow-up'>男の人は出張レポートのことを直きなければなりませんか？</p>
</div>

<ul class='options'>
    <li>しゅっちょうの　もくてき</li>
    <li>会った人のじょうほう</li>  
    <li>話し合いのけっか</li>  
    <li>つぎのほうもん日/li> 
</ul>  

--- example 2 ---
<p class='background'>会社で男の人と女の人が話しています。</p>

<div class='conversation'>
女：あ、田中さん。明日の会議、10時からでしたっけ？
男：いいえ、10時じゃなくて、午後1時からですよ。場所はいつもの会議室です。
女：あ、そうでしたね。資料はどうすればいいですか？
男：事前にメールで送ってください。当日、紙で持ってこなくても大丈夫です。
<p class='follow-up'>女の人は、何時から会議があると言われましたか。</p>
</div>

<ul class='options'>
    <li>午前10時</li>  
    <li>午後1時</li> 
    <li>午後3時</li>   
    <li>午後5時</li> 
</ul>
"""

keypoint_understanding_teacher_prompt = """
Role: You are a Japanese teacher writing an exam paper for the JLPT N4 level. 

Task: Your job is to write a natural-sounding conversation between a man and a woman. Alternatively, write a personal monologue, ensuring it is logically clear and flows smoothly. The probability of dialogue and monologue appearing is 50% each

If it's a conversation:

Step 1, write a concise background about the dialogue introduction, which exclude the follow-up question and character name.

Step 2, Give characters names during the conversation. They should call each name during the conversation depending on their relationship, level of formality.
Do not refer to them as Mr. or Miss in the conversation context. Be polite and culturally appropriate in how they address each other.
女：conversation context
男：conversation context
Besides, the name at the end of a sentence can be omitted.
For example: "ありがとう、佐藤さん。" the name at the end of a sentence can be omitted, like "ありがとう。"

Step 3, write dialogue, the dialogue should consist of 3-4 exchanges (back-and-forth turns). The total length should be approximately 150–180 words.
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
Content: Ensure the vocabulary is restricted to N4 level. 
Reference: Get inspiration from the "Topic" given by the user. Consider the feedback given in the previous conversation if it exists 
Additional Requirement: 
- Don't show question instructions and sequence number in the generated content. 
- The word in the sentence can neither be used in the question nor options.
- You must show the correct answer in the output, the options are 1,2,3,4. for example: 正解: 1



Formal exam paper: {example}
"""

keypoint_understanding_example = """
--- example 1 ---
<p class='background'>朝、家の玄関で妻と夫が話しています。</p>

<div class='conversation'>
女:あれ？どうしたの？忘れ物？書類？    
男:いや、バス停で待ってたんだけど、なぜかバスがなかなか来なくて。今日は車で会社に行くよ。車の鍵、取ってくれる？    
女:えー、私、今日車使いたいんだけど・・・会社まで送ってったあげるよ。    
男:本当？悪いね。走って戻ってきたら、喉渇いちゃった。ちょっと水飲んでくるから待ってて。    
女:あ、机の上に切手が貼ってあるハガキがあったけど、出さなくていいの？    
男:あぁ、忘れてた。取ってくるよ。 
<p class='follow-up'>夫はどうしても家に戻ってきましたか？</p> 
</div>

<a class='question'></a> 
<ul class='options'>
    <li>しょるいをわすれたから</li>
    <li>車で会社に行くことにしたから</li>    
    <li>のどがかわいたから</li>      
    <li>はがきをわすれたから</li>  
</ul>

--- example 2 ---
<p class='background'>男の人が新しいスーパーについて話しています</p>  

<div class='conversation'>
男：昨日、新しいスーパーに行ってみました。駅から歩いて5分くらいで、とても便利です。中は広くて、野菜や果物が安いし、パンも種類が多かったです。ただ、夕方だったのでレジが混んでいて、10分ぐらい待たされました。次は午前中に行こうと思います。
<p class='follow-up'>男の人は、このスーパーについてどう思っていますか。</p>
</div>    

<ul class='options'>
    <li>場所が遠くて不便だと思っている</li>    
    <li>品物が高いと思っている</li>     
    <li>品物はよいが、レジが混んでいると思っている</li>    
    <li>午後に行くのが一番いいと思っている</li>
</ul>    
"""

summary_understanding_teacher_prompt = """
Role: You are a Japanese teacher writing an exam paper for the JLPT N4 level. 

Task: Your job is to write a natural-sounding conversation between a man and a woman. Alternatively, write a personal monologue, ensuring it is logically clear and flows smoothly. The probability of dialogue and monologue appearing is 50% each 

Step 1, you should introduce the background of the dialogue.

Step 2, the total length should be approximately 200–300 words. If you write a dialogue, then the dialogue should consists of 6–7 exchanges (back-and-forth turns). 

Step 3, ask a follow-up question focusing on what the protagonist thinks, the theme of this paragraph, or what the speaker wants to express.
The topic should be appropriate for language learners and reflect everyday situations.

Step 4, provide multiple-choice options based on the listening content. These options should test comprehension of the conversation’s meaning.


Instructions:
Format: follow the format of the 2 examples in the formal exam paper but not the content.
Content: Ensure the vocabulary is restricted to N4 level. 
Reference: Get inspiration from the "Topic" given by the user. Consider the feedback given in the previous conversation if it exists 
Additional Requirement:
- Don't show question instructions and sequence number in the generated content. 
- The word in the sentence can neither be used in the question nor options.
- You must show the correct answer in the output, the options are 1,2,3,4. for example: 正解: 1


Formal exam paper: {example}
"""

summary_understanding_example = """
--- example 1 ---
<p class='background'>日本語学校で女の留学生と男の留学生が話しています。</p>

<div class='conversation'>
女: 来月で佐藤先生、学校を辞めちゃうんだよね。  
男: 寂しくなるね。  
女: うん。ねえ、クラスのみんなで先生に何か記念になるものをあげたいね。  
男: あ、いいね。何か身に付けるものとか?  
女: 先生おしゃれだし、そういうの選ぶの難しくない? それより私たちで何か作ろうよ。  
男: あ、メッセージカードは? クラスのみんなにも書いてもらおうよ。  
女: じゃ、スポーツ大会の時に撮ったクラスの集合写真を真ん中に貼って、周りにメッセージを書いてもらう?  
男: いいね。皆にももらえるといいね。明日、休み時間にクラスのみんなに話してみよう。  
</div>

<a class='follow-up'>2人は何について話していますか? </a>
<ul class='options'>
    <li>先生が学校を辞める理由</li>   
    <li>先生に贈る物</li>     
    <li>クラスからのメッセージ</li>     
    <li>先生との思い出</li>    
</ul>

--- example 2 ---
<p class='background'>男の人が最近の生活について話しています</p>

<div class='conversation'>  
男：最近、仕事が忙しくて、毎日残業しています。帰るのが遅いので、夕食はいつもコンビニで買った弁当です。でも、栄養がよくないと思うし、体も疲れやすくなってきました。だから、これからは少し早く帰って、自分で料理を作るようにしたいと思っています。健康のために、生活を変えなければならないと感じています。
</div>

<a class='follow-up'>男の人は、何を言いたいのですか？</a>
<ul class='options'> 
    <li>忙しいので、残業をもっと増やしたい</li>   
    <li>料理を作るのがめんどうだと思っている</li>    
    <li>健康のために、生活を変えたいと思っている</li>    
    <li>コンビニの弁当はおいしくないと思っている</li>  
</ul>  
"""

actively_expression_teacher_prompt = """
Role: You are a Japanese teacher writing an exam paper for the JLPT N4 level. 

Task: Create an AI-friendly picture prompt that visually depicts a scene where a question is being asked. 
Indicate clearly who speaks first: if a woman asks the question, a man should be shown answering, and if a man asks, a woman should answer. 
The scene should be illustrated without any background text. And there is a black arrow pointing to the party who is about to answer the question. The arrow must closely follow the party who is about to answer the question.

Generate Japanese language test questions similar to JLPT situational questions.
For each question, describe a real-life situation in Japanese and then ask what the person should say in that situation. 
Provide three possible answers in Japanese.
only one of which is appropriate or most natural for the situation. 
The correct answer must be highly relevant to the question and logical. The answer needs to maintain coherence with the previous question and not be too abrupt. For example, according to different scenarios, it is best to add a "あのう〜／へ〜／すみません／わ〜" connector as a buffer.
The language used in the correct answer needs to match the identity of both interlocutors. 
For example, students must use respectful language towards their teachers, and subordinates must also use respectful language towards their superiors.
Keep the situations practical and relevant to everyday life in Japan. Do not mention or refer to blurred faces.

The picture description must be in a dedicated section named: background.
The gender of the character indicated by the arrow in the picture needs to be consistent with the gender of the character generating the conversation.

Instructions:
Format: follow the format of the 2 examples in the formal exam paper but not the content.
Content: Ensure the vocabulary is restricted to N4 level. 
Reference: Get inspiration from the "Topic" given by the user. Consider the feedback given in the previous conversation if it exists 
Additional Requirement: 
- Don't show question instructions and sequence number in the generated content. 
- The word in the sentence can neither be used in the question nor options.
- You must show the correct answer in the output, the options are 1,2,3. for example: 正解: 1


Formal exam paper: {example}
"""

actively_expression_example = """
--- example 1 ---
<p class='background'>
The scene shows a young person standing at the entrance of a house, holding a bag and facing three adults who are standing together inside the house. 
The setting is indoors and feels polite and formal, as if the young person is greeting or saying goodbye to the adults. 
Include a vase with flowers on a shelf or table near the entrance. 
There is a black arrow pointing towards the young person.
</p>

<div class='conversation'>
男: 休みの間、友達の家に泊めてもらいました。帰る時、友達の両親に挨拶します。何と言いますか？
</div>

<a class='follow_up'>休みの間、友達の家に泊めてもらいました。帰る時、友達の両親に挨拶します。何と言いますか？</a>
<ul class='options'>
    <li>お世話になりました</li>     
    <li>お邪魔します</li>    
    <li>気をつけて帰ってください</li>
</ul>

--- example 2 ---
<p class='background'>
The scene takes place in a café or restaurant. 
A woman is sitting at a table with drinks in front of her, speaking to a server who stands beside her table holding a tray with a glass. 
There are additional tables and chairs in the background, with drinks and utensils visible. 
There is a black arrow pointing towards the woman.
</p>

<div class='conversation'>
女: カフェで窓側の席が空きました。席を変われるかどうか聞きたいです。店員に何と言いますか？
</div>

<a class='follow_up'>カフェで窓側の席が空きました。席を変われるかどうか聞きたいです。店員に何と言いますか？</a>
<ul class='options'>  
    <li>あの席に変わってもらえますか</li>    
    <li>窓側の席に座らないといけませんか</li>  
    <li>あっちの席に移れますか</li>
</ul>
"""

immediate_ack_teacher_prompt = """
角色：你是一名日语老师，正在为JLPT N3水平撰写试卷。 

任务：出一道符合N3水平的听力题。具体步骤如下：

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
内容：确保词汇量限制在N3级。 
参考：从用户给出的“Topic”中获得灵感。考虑前一次对话中给出的反馈（如果存在）
附加要求：
-不要在生成的内容中显示问题说明和序列号。 
-句子中的单词既不能用于问题，也不能用于选项。问题中的单词也不能出现在选项中
-您必须在输出中显示正确答案，选项为1,2,3。例如：正解:n ; 正确答案分布要随机平均，不要集中在某个选项.


Formal exam paper: {example}
"""

immediate_ack_example = """
--- example 1 ---
<a class='follow_up'> 女：足、痛そうだね。年後のテニスの練習、休んだら？</a>
<ul class='options'>  
　<li>そうです、今日は帰るね</li>
　<li>今日は練習、ないんだね</li>
　<li>テニス、今日は休むの？</li>
</ul> 

--- example 2 ---
<a class='follow_up'>男：町の花火大会、今年はやらないことになったそうだよ。</a>
<ul class='options'> 
　<li>やらないもしれなかったね</li>
　<li>え？なんて？楽しみにしていたのに…</li>
　<li>じゃ、見に行かなきゃね</li>
"""

kanji_reading_reflection_prompt = """
"""

write_kanji_reflection_prompt = """
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



