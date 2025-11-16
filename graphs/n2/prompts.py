kanji_reading_teacher_prompt = """
Role: You are a Japanese teacher writing a test paper for JLPT N2 level.

Task: Your job is to write a pronunciation question corresponding to Japanes kanji for the JLPT N2 level exam paper.

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
Content: Ensure vocabulary is limited to N2 level.  
Reference: Generate new content based on the user-provided "Topic", taking into account any previous feedback and critique. Also, avoid repeating previously asked questions or given answers in Historical Generation.  
Additional requirement: Do not display problem descriptions and serial numbers in the generated content.  

Formal exam paper: {example}
Historical Generation : {gan_history}
"""

kanji_reading_example = """  
--- example 1 ---
<a>状況を<u>詳細</u>に書いてださい。</a>
<ul>
    <li>そうざい</li>
    <li>そうさい</li>
    <li>しょうざい</li>
    <li>しょうさい</li>
</ul>

--- example 2 ---
<a>とても<u>鮮やか</u>だったことを覚えています。</a>
<ul>
    <li>おだやか</li>
    <li>さわやか</li>
    <li>あざやか</li>
    <li>なごやか</li>
</ul>
"""

write_kanji_teacher_prompt = """
Role: You are a Japanese teacher writing an exam paper for the JLPT N2 level. 

Task: Your job is to write a question for a JLPT N2 level exam paper.
You should write a short sentence and ask candidate to identify the correct kanji writing of a given word in hiragana.
The number of kanji characters in the options must be the same. The kanji characters must be usded in Japanese daily life.
The word in hiragana being tested needs to be underlined with <u></u>, no other tags can appear in the sentence.

Instructions:
Format: follow the format of the example in the formal exam paper but not the content.  The output must be in html format and remove line change tag.
Content: Ensure the vocabulary is restricted to N2 level. 
Reference: Generate new content based on the user-provided "Topic", taking into account any previous feedback and critique. Also, avoid repeating previously asked questions or given answers in Historical Generation.   
Additional Requirement: 
- Don't show question instructions and sequence number in the generated content. 
- The word in the sentence can neither be used in the question nor options.
- You must show the correct answer in the output, for example: 正解: n . The options are 1,2,3,4. ensuring a balanced distribution of correct answers across options.


Formal exam paper: {example}
Historical Generation : {gan_history}
"""

write_kanji_example = """
--- example 1 ---
<a>この会社を<u>しぼう</u>した理由を教えてください。</a>
<ul>
    <li>希望</li>
    <li>志望</li>
    <li>指望</li>
    <li>貴望</li>
</ul>

--- example 2 ---
<a>このセーターにはとても<u>やわらかい</u>毛系が使われている。</a>
<ul>
    <li>伸らかい</li>
    <li>軽らかい</li>
    <li>暖らかい</li>
    <li>柔らかい</li>
</ul>
"""

words_collocation_teacher_prompt = """
Role: You are a Japanese teacher writing an exam paper for the JLPT N2 level. 

Task: Your job is to write a question for a JLPT N2 level exam paper.
You should write a short sentence and give a parenthesis in the sentence.
Next, require candidates to fill the most semantically and grammatically appropriate word from the options based on the context of the sentence in the parenthesis 
This mainly tests students' fixed collocations of Japanese nouns and compound verbs.
The word in the sentence should not be used in the options
Options are written either entirely in kanji or entirely in kana.


Instructions:
Format: follow the format of the 2 examples in the formal exam paper but not the content. The output must be in html format and remove line change tag.
Content: Ensure the vocabulary is restricted to N2 level. 
Reference: Generate new content based on the user-provided "Topic", taking into account any previous feedback and critique. Also, avoid repeating previously asked questions or given answers in Historical Generation.   
Additional Requirement: 
- Don't show question instructions and sequence number in the generated content. 
- The word in the sentence can neither be used in the question nor options.
- You must show the correct answer in the output, for example: 正解: n . The options are 1,2,3,4. ensuring a balanced distribution of correct answers across options.


Formal exam paper: {example}
Historical Generation : {gan_history}
"""

words_collocation_example = """
--- example 1 ---
<a>しょうゆの（　）原料は大豆です。</a>
<ul class='options'>
  <li>主</li>
  <li>要</li>
  <li>正</li>
  <li>本</li>
</ul>

--- example 2 ---
<a>子どもたちの読書（　）が進んでいるらしい。</a>
<ul class='options'>
  <li>抜け</li>
  <li>逃げ</li>
  <li>別れ</li>
  <li>離れ</li>
</ul>
"""

word_meaning_teacher_prompt = """
Role: You are a Japanese teacher writing an exam paper for the JLPT N2 level. 

Task: Your job is to write a question for a JLPT N2 level exam paper.
You should write a short sentence and give a parenthesis in the sentence,
Next, require candidates to fill the most semantically and grammatically appropriate word from the options based on the context of the sentence in the parenthesis 
This mainly tests students the ability to identify the part of speech of a word in a sentence.
The word in the sentence should not be used in the options
Options are written either entirely in kanji or entirely in kana.


Instructions:
Format: follow the format of the 2 examples in the formal exam paper but not the content. The output must be in html format and remove line change tag.
Content: Ensure the vocabulary is restricted to N2 level. 
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
<a>両親はおいしい料理で客を（　）のが好きだ。</a>
<ul class='options'>
  <li>もてなす</li>
  <li>おだてる</li>
  <li>許す</li>
  <li>救う</li>
</ul>

--- example 2 ---
<a>西川さんは転校してきたばかりだが、友達もできて、もうすっかりクラスに（　）ている。</a>
<ul class='options'>
  <li>当てはまって</li>
  <li>溶け込んで</li>
  <li>結びついて</li>
  <li>触れ合って</li>
</ul>

"""

synonym_substitution_teacher_prompt = """
Role: You are a Japanese teacher writing an exam paper for the JLPT N2 level. 

Task: Your job is to generate a JLPT N2 vocabulary question where the student must select the word closest in meaning to a given word used in a sentence.
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
Content: Ensure the vocabulary is restricted to N2 level. 
Reference: Generate new content based on the user-provided "Topic", taking into account any previous feedback and critique. Also, avoid repeating previously asked questions or given answers in Historical Generation.   
Additional Requirement: 
- Don't show question instructions and sequence number in the generated content. 
- The word in the sentence can neither be used in the question nor options.
- You must show the correct answer in the output, for example: 正解: n . The options are 1,2,3,4. ensuring a balanced distribution of correct answers across options.


Formal exam paper: {example}
Historical Generation : {gan_history}
"""

synonym_substitution_example = """
<a>出張の日程は<u>おおよそ</u>決まりました。</a>
<ul class='options'>
  <li>だいたい</li>
  <li>すべて</li>
  <li>やっと</li>
  <li>もう</li>
</ul>

<a>中西さんはいつも<u>威張って</u>いる。</a>
<ul class='options'>
  <li>眠そうにして</li>
  <li>偉そうにして</li>
  <li>暇そうにして</li>
  <li>嫌そうにして</li>
</ul>
"""

word_usage_teacher_prompt = """
Role: You are a Japanese teacher writing an exam paper for the JLPT N2 level. 

Task: Your job is to write a kanji for examining the usage of words in actual contexts for a JLPT N2 level exam paper.
Ask the student to choose the sentence that best matches the true meaning or usage of the word from 4 options,
which exam student the knowledge of Japanese idiomatic expressions and fixed collocations.
The words to be examined need to be underlined in each sentence. the question must be written in kanji, like <a>内容</a> <a>落ち着く</a>
Make only one option correct (the one using the word naturally), and ensure the other 3 sound plausible but are semantically incorrect.

Instructions:
Format: follow the format of the example in the formal exam paper but not the content. The output must be in html format and remove line change tag.
Content: Ensure the vocabulary is restricted to N2 level. 
Reference: Generate new content based on the user-provided "Topic", taking into account any previous feedback and critique. Also, avoid repeating previously asked questions or given answers in Historical Generation.   
Additional Requirement: Don't show question instructions and sequence number in the generated content.
You must show the correct answer in the output, the options are 1,2,3,4. for example: 正解: 1


Formal exam paper: {example}
Historical Generation : {gan_history}
"""

word_usage_example = """
<a>共有</a>
<ul class='options'>
  <li>市民ボランティアの<u>共有</u>で、留学生のスピーチコンテストが行われた</li>
  <li>大学と企業が<u>共有</u>で新しい技術の研究を行っている</li>
  <li>これらの事件には、発生場所に<u>共有</u>の特徴があることが分かった</li>
  <li>結婚してから購入した物は、夫婦の<u>共有</u>財産になる</li>
</ul>
"""

sentence_grammar_teacher_prompt = """
职位：你是一名日语老师，正在为JLPT N2水平写试卷。

任务：按照以下步骤为JLPT N2级别试卷生成一道语法题，测试考生在实际语境中对语法的掌握程度。

步骤1：生成1-2个短句，或者两个人对话的两句句子。要求：
- 问题的灵感来源主题,内容应涵盖日常生活场景、对话或简短的解释性语境。
- 生成的句子可以包含两种形式：1-2句短句；或者为2个人之间每人1-2句的对话，只需要1个对话回合
- 题目的总字数在40-60个单词之间
- 使用JLPT N2中的词汇；语法正确，语义通顺
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
<a>携帯電話を一人一台持つのは当たり前と言われる現代で、私のように携帯電話なしで生活している人は（　　　）いるのだろうか。</a>
<ul class='options'>
  <li>どうも</li>
  <li>どれほど</li>
  <li>どうしても</li>
  <li>どんなに</li>
</ul>

--- example 2 ---
<a>（カメラ屋で）<br>
客「カメラを海に落としてしまって、電源が入らないんです。中に水が入ってしまったようなのですが…。」<br>
店員「海水が入った（　　）、修理は難しいかもしれませんが、一応見てみますね」
</a>
<ul class='options'>
  <li>のであれば</li>
  <li>ことであれば</li>
  <li>のであって</li>
  <li>ことであって</li>
</ul>
"""

# The candidate must re-arrange words (don't change options order) and identify the third word according to the word positions for a sentence.
# When the third word is identified, point out its sequence number in the options.

sentence_sort_teacher_prompt = """
Role: You are a Japanese teacher who designed a sentence sorting question for the JLPT N2 exam.

Task: You should write a sentence of approximately 60 words and cut out four consecutive phrases as options for the question. The specific execution steps are as follows:

Step 1: Generate sentences. The generated sentence needs to meet the following conditions:
-The content of the sentence draws inspiration from the "Topic". Consider the feedback given in the previous conversation. Use sentence grammar from the 'Grammar reference'.
-The generated sentence can be a semantically coherent complete long sentence, or a combination of a simple sentence and a long sentence.
-The generated sentences use one or two sentence grammars from the grammar reference list, with word usage typically limited to N2 level.
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
<a>会議での西山さんのプレゼントは、普段はなかなか<u>＿＿</u> <u>＿＿</u> <u>&nbsp; &nbsp;★</u><u>&nbsp; &nbsp;</u> <u>＿＿</u>素晴らしかった。</a>
<ul class='options'>
  <li>ぐらい</li>
  <li>課長が</li>
  <li>褒める</li>
  <li>褒めることができない</li>
</ul>

--- example 2 ---
<a>さくら駅周辺の再開発事業を行う<u>＿＿</u> <u>＿＿</u> <u>&nbsp; &nbsp;★</u><u>&nbsp; &nbsp;</u> <u>＿＿</u>予定だ。</a>
<ul class='options'>
  <li>さくら市は</li>
  <li>に先立って</li>
  <li>関係者に対する</li>
  <li>説明会を開催する</li>
</ul>

"""

structure_selection_teacher_prompt = """
角色：你是一名日语老师，正在为JLPT N2水平撰写试卷。 

任务：你的工作是按照以下步骤为JLPT N2级别出一道填入正确内容的语法题。根据语法参考列表中的4个语法点出题

步骤1：问题的灵感来源"主题"。写一篇日语短文。短文需要符合以下要求：
- 短文需要有1-3个段落，350-500个词。
- 确保短文中的词汇95%限制在N2级别。
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
参考：从用户给出的“Topic”中获得灵感。考虑前一次对话中给出的反馈和批评（如果存在）,避免重复生成"历史题目"的问题(q)或给出的答案(a)。
附加要求：
- 在输出中显示正确答案，选项为1,2,3,4.例如：正解：n, 正确答案分布要平均，不要集中在某个选项
- 不要在生成的内容中显示问题说明和序列号。

历史题目: {gan_history}
正式试卷：{example}
语法参考列表：{grammar}
"""

structure_selection_example = """
<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<title>紅葉の異変（続き）</title>
<style>
  body {
    font-family: "Hiragino Mincho ProN", "Yu Mincho", serif;
    margin: 40px;
    line-height: 1.8;
  }
  .container {
    border: 1px solid #000;
    padding: 20px;
  }
  .title {
    text-align: center;
    font-size: 1.5em;
    font-weight: bold;
    margin-bottom: 10px;
  }
  .author {
    text-align: right;
    margin-bottom: 20px;
  }
  .question {
    margin-top: 20px;
  }
</style>
</head>
<body>
<div class="article">
  <p>以下は、留学生がスピーチのために書いた文章である</p>

  <div class="container">
    <div class="title">紅葉の異変</div>
    <div class="author">サリム ソフィア</div>

    <p>
      私は日本の秋の景色が好きです。秋になって紅葉が始まり、緑だった葉が黄色やオレンジ、赤に変わると、とてもきれいです。秋の紅葉は、日本の四季の変化を感じさせてくれるものです。
    </p>

    <p>
      （48）ですが、先日テレビで、紅葉がピークを迎える時期が年々遅くなっているというニュースを見ました。中には、1月になってからピークを迎えたところもあるそうで、驚きました。温暖化によって平均気温が上昇していることが大きな原因だそうです。私は、夏が過ぎて気温が下がってくれば、必ず紅葉が始まると思っていました。（49）そうではありませんでした。紅葉には、条件となる気温の変化があります。
    </p>

    <p>
      葉の変色が始まるのは、1日の最低気温が大体8度以下になってからです。秋になっても、最低気温が一定の気温まで下がらなければ、紅葉は（50）その後、さらに寒くなり、5～6度まで下がると、紅葉は一気に進みます。また、5度以下の日が続くと、最も美しい新葉が見られるといわれています。
    </p>

    <p>
      紅葉に起きている異変を知り、このまま温暖化が進むと、日本の秋の景色が変わってしまう可能性もあるのではないかと思いました。もしかしたら、紅葉自体が見られなくなる日も来るかもしれません。紅葉を通して、温暖化が身近な問題であることをより強く（51）
    </p>
  </div>
</div>

  <div class="follow-up">
    <a><strong>48</strong></a>
    <div class="options">
        <li>そこの紅葉</li>
        <li>そんな紅葉</li>
        <li>そちら</li>
        <li>紅葉</li>
    </div>
    
    <a><strong>49</strong></a>
    <div class="options">
        <li>結局</li>　　
        <li>確かに</li>　　
        <li>しかし</li>　　
        <li>つまり</li>

    <p><strong>50</strong></p>
    <div class="options">
        <li>始まらないのです</li>　　
        <li>始まらないためです</li>　　
        <li>始まらないのでしょうか</li>　　
        <li>始まらないためでしょうか</li>
    </div>
    
    <p><strong>51</strong></p>
    <div class="options">
        <li>1. 感じているからだと思います</li>　　
        <li>感じられるところだと思います</li>　　
        <li>感じさせることができました</li>　　
        <li>感じるようになりました</li>
    </div>
    </div>
  </div>
</body>
</html>
"""

short_reading_narrative_teacher_prompt = """
Role: You are a Japanese teacher writing an exam paper for the JLPT N2 level. 

Task: Your job is to write a reading question for JLPT N2 level exam. 
First you need to write a narrative article around 300 words for student to read.  
Then, you give a question by the related content in the article. Most importantly, the correct answer must not be stated directly in the article. 
Instead, it should require the test-taker to infer, summarize, or understand the context or intent of the passage.
The passage should reflect a real-life topic (e.g., daily life, work, study, travel, opinions).

Instructions:
Format: follow the format of 1 example in the formal exam paper but not the content. The output must be in html format and remove line change tag.
Content: Ensure the vocabulary is restricted to N2 level. 
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
    <title>インタビューに関する文章</title>
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
        }
        .note {
            font-size: 0.9em;
            color: #555;
            margin-left: 1em;
        }
        ol {
            margin-top: 2em;
        }
        li {
            margin-bottom: 0.8em;
        }
        .page-number {
            text-align: right;
            font-weight: bold;
            margin-top: 2em;
            color: #666;
        }
    </style>
</head>
<body>
<div class="article">
<p>インタビューでは準備も重要だが、実際のインタビューの場面になったら、いったんその準備で得たものをすべて捨てなくてはならない。そして、相手の話を真剣に深く聞き、その人が何を言わんとしているのか、丸ごと捉えて、そこで出てきた素晴らしい言葉、豊かな言葉、言葉に込められた大事なメッセージをしっかりとつかむことこそが必要なのだ。</p>

<p>そこから良い対話が生まれてくる。良いインタビューは、次の質問を忘れて相手の話を聞けたときに初めて行えるものなのだ。</p>

<p class="note">（注1）言わんとしている：言おうとしている</p>
<p class="note">（注2）丸ごと：そのまま全部</p>

</div>

<a>インタビューについて、筆者の考えに合うのはどれか。</a>

<ul class="options">
    <li>準備したものから離れて、相手の話をよく聞くことが重要だ。</li>
    <li>準備した質問に沿って、相手から大事なメッセージを引き出すことが重要だ。</li>
    <li>相手の話をしっかり聞くことが大切なので、準備をする必要はない。</li>
    <li>相手から素晴らしい言葉を引き出すには、準備しすぎないほうがいい。</li>
</ul>

</body>
</html>

"""

short_reading_mail_teacher_prompt = """
Role: You are a Japanese teacher writing an exam paper for the JLPT N2 level. 

Task: Your job is to write a reading question for JLPT N2 level exam.
First you need to write a letter or mail around 250 words for student to read, including several keigo expressions. The content is about:
"Requests, Gratitude, Appreciation, Apologies, Notices, Announcements, Confirmation, Reporting, Invitations"

Then, you give a question by the related content in the article. Most importantly, the correct answer must not be stated directly in the article. 
Instead, it should require the test-taker to infer, summarize, or understand the context or intent of the passage.
The passage should reflect a real-life topic (e.g., daily life, work, study, travel, opinions).

Instructions:
Format: follow the format of 2 examples in the formal exam paper but not the content. The output must be in html format and remove line change tag.
Content: Ensure the vocabulary is restricted to N2 level. 
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
    <title>メールに関する文章</title>
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
        h3 {
            font-size: 1.2em;
            margin-top: 1.5em;
            margin-bottom: 0.5em;
        }
        p {
            margin-bottom: 1.2em;
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
        .file-note {
            font-style: italic;
            color: #555;
            margin-top: 2em;
        }
    </style>
</head>
<body>
<div class="article">
<p>以下は、ある会社で全社員に送られたメールである。</p>

<hr>

<h3>社員各位</h3>

<p>わが社の人気商品「緑山牧場チーズ詰め合わせ」を、定価の30%引き（割引後3,500円）で社員向けに特別販売します。</p>

<p>購入希望者は、添付の申込書にお名前と購入数を記入のうえ、3月9日までに営業課までメールでお申し込みください。通常、社内販売の支払いと商品のお渡しは経理課で行っていますが、今回は営業課で行います。代金と引き換えに、その場で商品をお渡しします。お渡し期間は3月16日から19日の間です。</p>

<p>以上、よろしくお願いします。</p>

<p class="file-note">添付ファイル：3月1日「緑山牧場チーズ詰め合わせ」申込書</p>

<h3>営業課 安井</h3>

</div>

<a>「緑山牧場チーズ詰め合わせ」を社内販売で購入したい社員は、期日までに営業課にメールで申し込んだあと、どうすればいいか。</a>

<ul class='options'>
    <li>経理課で支払いをして受け取る。</li>
    <li>経理課で支払いをして、営業課で受け取る。</li>
    <li>営業課で支払いをして受け取る。</li>
    <li>営業課で支払いをして、経理課で受け取る。</li>
</ul>

</body>
</html>
"""

short_reading_notification_teacher_prompt = """
Role: You are a Japanese teacher writing an exam paper for the JLPT N2 level. 

Task: Your job is to write a reading question for JLPT N2 level exam. 
First you need to write a notification around 250 words for student to read, including several keigo expressions
Then, you give a question by the related content in the article. Most importantly, the correct answer must not be stated directly in the article. 
Instead, it should require the test-taker to infer, summarize, or understand the context or intent of the passage.
The passage should reflect a real-life topic (e.g., daily life, work, study, travel, opinions).

Instructions:
Format: follow the format of 2 examples in the formal exam paper but not the content. The output must be in html format and remove line change tag.
Content: Ensure the vocabulary is restricted to N2 level. 
Reference: Generate new content based on the user-provided "Topic", taking into account any previous feedback and critique. Also, avoid repeating previously asked questions or given answers in Historical Generation.   
Additional Requirement: 
- Don't show question instructions and sequence number in the generated content. 
- The word in the article can neither be used in the question nor options.
- You must show the correct answer in the output, for example: 正解: n . The options are 1,2,3,4. ensuring a balanced distribution of correct answers across options.


Formal exam paper: {example}
Historical Generation : {gan_history}
"""

short_reading_notification_example = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>掲示板に関する文書</title>
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
        .document {
            border: 1px solid #ccc;
            padding: 20px;
            background-color: #fff;
            position: relative;
            box-shadow: 0 0 5px rgba(0,0,0,0.1);
        }
        .corner {
            position: absolute;
            width: 20px;
            height: 20px;
            background-color: #ddd;
            border-radius: 50%;
        }
        .top-left { top: 10px; left: 10px; }
        .top-right { top: 10px; right: 10px; }
        .bottom-left { bottom: 10px; left: 10px; }
        .bottom-right { bottom: 10px; right: 10px; }
        .date {
            text-align: right;
            margin-bottom: 1em;
            font-weight: bold;
        }
        h3 {
            text-align: center;
            margin: 1.5em 0;
            font-size: 1.3em;
        }
        p {
            margin-bottom: 1.2em;
            text-indent: 1em;
        }
        .signature {
            text-align: right;
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
<div class="article">
    <p>以下は、ある町の掲示板に貼られていた文書である。</p>
    <div class="document">
    <div class="corner top-left"></div>
    <div class="corner top-right"></div>
    <div class="corner bottom-left"></div>
    <div class="corner bottom-right"></div>
    
    <div class="date">10月5日</div>
    
    <p>住民の皆様へ</p>
    
    <h3>ごみに関するお願い</h3>
    
    <p>最近、「可燃ごみ」の回収日に衣類・布類が多く出されています。しかし、市の規則では、衣類・布類は毎週火曜日の「資源ごみ」の回収日に出すことになっています。資源を有効に活用するため、決められた回収日に出してください。</p>
    
    <p>衣類・布類は、市内8か所の公共施設に設置してある回収ボックスでも回収しています。回収後は、中古の衣類として再使用したり、工場で再生利用したりします。ご協力をよろしくお願いします。</p>
    
    <p class="signature">竹川市役所 市民生活課</p>
    </div>
</div

<a>この文書で最も伝えたいことは何か。</a>

<ul class="options">
    <li>「資源ごみ」として出す衣類・布類の量を減らしてほしい。</li>
    <li>「資源ごみ」の回収日に「可燃ごみ」を出さないでほしい。</li>
    <li>衣類・布類は、「資源ごみ」の回収日に出してほしい。</li>
    <li>衣類・布類は、新しく設置した回収ボックスに出してほしい。</li>
</ul>

</body>
</html>
"""

midsize_reading_teacher_prompt = """
Role: You are a Japanese teacher writing an exam paper for the JLPT N2 level. 

Task: Your job is to write a reading question for a JLPT N2 level exam.
First you need to write a mid-size article around 450 words for student to read.
The keypoints being tested in each question needs to be underlined with <u></u>
Then, you give 2 questions by the related content in the article. the meaning of keypoint cannot be found in the article.
Then, you give a question by the related content in the article.
Instead, it should require the test-taker to infer, summarize, or understand the context or intent of the passage.

Instructions:
Format: follow the format of the 1 example in the formal exam paper but not the content. The output must be in html format and remove line change tag.
Content: Ensure the vocabulary is restricted to N2 level. 
Reference: Generate new content based on the user-provided "Topic", taking into account any previous feedback and critique. Also, avoid repeating previously asked questions or given answers in Historical Generation.   
Additional Requirement: 
- Don't show question instructions and sequence number in the generated content. 
- The word in the article can neither be used in the question nor options.
- You must show the correct answer in the output, for example: 正解: n . The options are 1,2,3,4. ensuring a balanced distribution of correct answers across options.



Formal exam paper: {example}
Historical Generation : {gan_history}
"""

midsize_reading_example = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>文章内容</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.8;
            max-width: 800px;
            margin: 40px auto;
            padding: 0 20px;
            background-color: #f9f9f9;
            color: #333;
        }
        .content {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h3 {
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }
        ol {
            padding-left: 20px;
        }
        li {
            margin: 12px 0;
        }
        .question {
            font-weight: bold;
            color: #e74c3c;
            margin-top: 25px;
        }
        .article {
            margin-bottom: 40px;
            padding-bottom: 20px;
            border-bottom: 1px solid #eee;
        }
    </style>
</head>
<body>

<div class="article">
    <p>勉強にしても、仕事にしても、その能率には必ず波があり、それがな<br>いようにみえても、波が小さいだけである。つまり、人間は機械のように<br>いつも同じ調子ではたらいていないから、1 時間に 50 個の製品がつく<br>れるから、10 時間で 500 個がつくれる、という具合には計算できない。<br>従って、脳が最も快調にはたらいているときを基準にすると、たいていの<br>ときは不調ということになってしまう。</p>
    <p>それでも、全く無計画に勉強や仕事をするわけにもゆかないので、一<br>応はスケジュールを立てる。その際に、快調に脳がはたらいているときの<br>能率を基準にしてスケジュールを立てれば、そのスケジュールの通りにこ<br>とが進行することは絶対にないといってもいい。その度に、自分の才能に失<br>望していれば、失望しつづけることになる。さし迫った状態では、どうし<br>ても脳がフル回転しているときを基準にスケジュールを組むので、たいてい<br>は不完全な形で終ってしまう。スケジュールをつくるときには、せめて<br>中等度に脳がはたらいているときの能率を基準にする必要がある。スケジ<br>ュール以上にはかどっても誰もこまる人はいない。</p>
    <p>そして、スケジュールにこだわるより、脳の変動の波をできるだけ感<br>じとり、能率が悪くても悲観せずに、必ず上げ潮のときがくることを期待<br>すればいい。そして、上げ潮のときには自分でもおどろくほどに能率が上<br>がるので、そのときに一気に遅れをとり戻せばいいのである。</p>
</div>

<div class="follow-up">           
    <a>筆者によると、スケジュールを立てる際の注意点は何か。</a>
    <ul class="options">
        <li>脳の調子がいいときを基準にしない</li>
        <li>いつも脳が同じ調子ではたらけるようにする</li>
        <li>能率の変化を考えすぎない</li>
        <li>能率が悪くなったときに変更できるようにしておく</li>
    </ul>
    
    <a>筆者の考えに合うのはどれか。</a>
    <ul class="options">
        <li>能率を上げるためには、脳の状態をコントロールするといい</li>
        <li>脳の変動の波に合わせて勉強や仕事を進められる方法を探すといい</li>
        <li>計画の通りに行かなくても失望せずに、脳の調子が上がるのを待てばいい</li>
        <li>計画の通りに勉強や仕事を進めるためには、脳の変動の波を小さくすればいい</li>
    </ul>
</div>

    </div>
</body>
</html>
"""

comprehensive_read_teacher_prompt = """
Role: You are a Japanese teacher writing an exam paper for the JLPT N2 level.

Task: Task: Your job is to write a reading question for a JLPT N2 level exam. 
First you need to write a long article around 450 words for student to read. 
Then, you give 2 questions by the related content in the article. 
The purpose is to ensure the students are able to understand the meaning of the article.


Instructions:
Format: follow the format of the example in the formal exam paper but not the content. The output must be in html format and remove line change tag.
Content: Ensure the vocabulary is restricted to N2 level. 
Reference: Generate new content based on the user-provided "Topic", taking into account any previous feedback and critique. Also, avoid repeating previously asked questions or given answers in Historical Generation.   
Additional Requirement: 
- Don't show question instructions and sequence number in the generated content. 
- The word in the article can neither be used in the question nor options.
- You must show the correct answer in the output, for example: 正解: n . The options are 1,2,3,4. ensuring a balanced distribution of correct answers across options.



Formal exam paper: {example}
Historical Generation : {gan_history}
"""

comprehensive_read_example = """
<div class="article">
  <h3>A</h3>
  <p>
    新しい商品を企画するとき、いいアイデアがなかなか思いつかないことがある。そんなとき、自分には才能がないからだと思い込み、
    自信をなくしてしまうのはよくない。アイデアは生まれつきの能力に関係なく、努力次第で誰でも生み出すことができる。
    アイデアは、情報の組み合わせによって生まれることがほとんどだ。そのため、日ごろから情報を集めておくことが有効だ。
    担当する商品に関連する情報だけを集めていると、似たようなアイデアばかりになってしまう。発想の幅を広げるには、
    関連する分野以外の情報も頭に入れておくほうがいい。ふだんから視野を広げてさまざまな情報を蓄積しておけば、
    必ずアイデアの役に立つはずだ。
  </p>

  <h3>B</h3>
  <p>
    新しい商品を企画するには、これまでとは異なるアイデアが必要だ。現在流行している商品の情報を集めるだけでは、
    他社に勝つことはできないだろう。私はアイデアを生み出すために、一般的に考えられていることとは逆の発想をするようにしている。
    現在流行している商品が若者向けの物なら高齢者向けにできないかと考えたり、多機能の物なら機能を一つに絞れないかと考えたりするのである。
  </p>
  <p>
    アイデアは一部の才能がある人しか生み出せないものだという印象があるせいか、生み出し方を知ろうとしない人が多いと思う。
    才能がないからといってあきらめるのではなく、思い切って発想を転換してみれば、いいアイデアにつながっていく。
  </p>
</div>

<body>
    <a>65. アイデアを生み出すことについて、AとBが共通して述べていることは何か。</a>
    <ul class="options">
        <li>アイデアを生み出し方は、簡単に身につけることができる。</li>
        <li>多くの情報を得ることで、アイデアを生み出しやすくなる。</li>
        <li>特別な能力がなくても、アイデアを生み出すことができる。</li>
        <li>発想のしかたを大きく変えなければ、アイデアは生み出せない。</li>
    </ul>

    <a>66. 新しい商品を企画することについて、AとBはどのようなアドバイスをしているか。</a>
    <ul class="options">
        <li>AもBも、いろいろな分野の情報をできるだけ多く集めるといいと述べている。</li>
        <li>AもBも、流行している商品について詳しく調べるといいと述べている。</li>
        <li>Aは関連する分野の他社の商品の情報を集めるといいと述べ、Bは流行に逆らった考え方をするといいと述べている。</li>
        <li>AもBも、流行している商品について詳しく調べるといいと述べている。</li>
    </ul>

    <a>67. 新しい商品を企画する際の注意点について、AとBが共通して述べていることは何か。</a>
    <ul class="options">
        <li>十分な時間と資金を確保すること。</li>
        <li>多くの消費者の意見を取り入れること。</li>
        <li>市場の需要を調べる前に、デザインや機能にこだわること。</li>
        <li>競合他社の動きを分析し、それに合わせること。</li>
    </ul>
</body>
"""

long_reading_teacher_prompt = """
Role: You are a Japanese teacher writing an exam paper for the JLPT N2 level.

Task: Task: Your job is to write a reading question for a JLPT N2 level exam. 
First you need to write a long article around 600 words for student to read. 
Then, you give 3 questions by the related content in the article. 
The purpose is to ensure the students are able to understand the meaning of the article.


Instructions:
Format: follow the format of the example in the formal exam paper but not the content. The output must be in html format and remove line change tag.
Content: Ensure the vocabulary is restricted to N2 level. 
Reference: Generate new content based on the user-provided "Topic", taking into account any previous feedback and critique. Also, avoid repeating previously asked questions or given answers in Historical Generation.   
Additional Requirement: 
- Don't show question instructions and sequence number in the generated content. 
- The word in the article can neither be used in the question nor options.
- You must show the correct answer in the output, for example: 正解: n . The options are 1,2,3,4. ensuring a balanced distribution of correct answers across options.



Formal exam paper: {example}
Historical Generation : {gan_history}
"""

long_reading_example = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>文章内容</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.8;
            max-width: 800px;
            margin: 40px auto;
            padding: 0 20px;
            background-color: #f9f9f9;
            color: #333;
        }
        .content {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h3 {
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }
        ol {
            padding-left: 20px;
        }
        li {
            margin: 12px 0;
        }
        .question {
            font-weight: bold;
            color: #e74c3c;
            margin-top: 25px;
        }
    </style>
</head>
<body>
    <div class="article">
        <p>以下は、ある作家が物語などの本を読むことについて書いた文章である。</p>
        <p>読むことは、受動的な作業だと思っている人は意外に多い。（中略）読んでインプットして、書いてアウトプットする。そうではなくて、両方アウトプットなのだというのが、私の持論である。</p>
        <p>そこにある言葉を読む。すると心には、文字以上のものが広がる。たとえば、子どものころ読んだ海外作品に、聞いたこともない料理名が出てくるということが、よくあった。クロスグリのパイだとか、ジンジャークッキーだとか。食べたことのないものを、懸命に想像して味わう。それを食べる主人公の舌を、獲得するわけである。①この行為、受動ではなく能動である。「創る」作業である。本でしか読んだことのない食べものを、大人になってから実際に食べ、「違う」と思った経験を持つ人は、意外に多いのではないだろうか。もちろん違うのは私たちの想像なのだが、しかし自分の頭のなかで創った料理のほうが、断然おいしかった、ということは、よくある。</p>
        <p>本を読まない、というのは、だから、私にとって創造の放棄である。②つまらない本、相性が悪い本というのはもちろんある。しかしそこで、どこがどんなふうにつまらないのか、どう展開したらおもしろかったのか、自分のどの部分と相性が悪いのか、そんなことを考えていると、つまらない本はおもしろくなるし、相性が悪い本はいつか相性がよくなる日を待とうと思うことができる。私は、おもしろかった本よりつまらなかった本のあらすじを人に話すほうが、ずっと好きだ。どこがどんなふうにつまらなく感じたかを話すのはそれだけ創造の余地があるからだろう。</p>        
        <p>料理でも、絵画でも、あるいは家事の手順でも、創ることの喜びを知ってしまうと、なかなかそれから離れることができない。読むことの楽しみは、と訊かれれば、創ることの自由さだと私は答える。</p>        
    </div>
    
    <div class="follow-up">    
        <a>①この行為とはどういうことか</a>
        <ul class="options">
            <li>実際に、主人公が食べていた食べものを味わってみること</li>
            <li>食べたことのないものを主人公と一緒に食べているところを想像すること</li>
            <li>主人公がどんな食べものが好きかを想像してみること</li>
            <li>主人公になりきって、食べたことのないものを想像して味わうこと</li>
        </ul>
        
        <a>②つまらない本について、筆者はどのように述べているか。</a>
        <ul class="options">
            <li>つまらなく感じた点について色々考えていると、おもしろくなる</li>
            <li>つまらなく感じた理由を考えていると、自分の好みがよく分かってくる</li>
            <li>つまらないと思っても、いつか必ず相性がよくなる日がくる</li>
            <li>つまらないと思っても、人にあらすじを話すとおもしろいところが見つけられる</li>
        </ul>
        
        <a>本を読むことについて、筆者はどのように考えているか</a>
        <ul class="options">
            <li>本を読むことは、料理や絵画より創ることの喜びが大きい</li>
            <li>本を読むことは、自由に想像を膨らませる楽しい創造の作業だ</li>
            <li>本を読んでたくさん知ることができれば、創ることの喜びも増す</li>
            <li>本を読んで想像力を身につければ、生活のなかでも自由に想像が楽しめる</li>
        </ul>
    </div>
</body>
</html>
"""

information_retrieval_teacher_prompt = """
Role: You are a Japanese teacher writing an exam paper for the JLPT N2 level. 

Task: You are a Japanese teacher writing a retrieve information question on an exam paper for the JLPT N2 level.
you must provide 1 or 2 html format tables and with additional information for retrieve below. The content and conditions combined should be more than 300 words and complex enough for JLPT N2 level.
After that, asking candidate to answer 2 questions from the related content in the table.
Most importantly, the question and answer must not be stated directly in the table or clues. 
Instead, it should require the test-taker to infer, summarize, or understand the context.
This section is designed to simulate real-life scenarios where students need to quickly find relevant information. 
such as train or flight schedules, event, or advertisements.

Instructions:
Format: follow the format of the 2 examples in the formal exam paper but not the content. The output must be in html format and remove line change tag.
Content: Ensure the vocabulary is restricted to N2 level. 
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
<title>秋原テニススクール入会案内</title>
<style>
  body {
    font-family: "Hiragino Kaku Gothic ProN", "Yu Gothic", sans-serif;
    margin: 40px;
    line-height: 1.8;
  }
  .container {
    border: 1px solid #000;
    padding: 20px;
  }
  h1 {
    text-align: center;
    font-size: 1.6em;
    margin-bottom: 20px;
  }
  table {
    width: 100%;
    border-collapse: collapse;
    margin: 15px 0;
  }
  th, td {
    border: 1px solid #000;
    padding: 8px;
    text-align: left;
  }
  th {
    background-color: #f2f2f2;
  }
  .section-title {
    font-weight: bold;
    margin-top: 25px;
  }
  .note {
    font-size: 0.9em;
    color: #333;
  }
</style>
</head>
<body>
  <div class="article">
    <h1>秋原テニススクール入会案内</h1>

    <p class="section-title">コース・クラスについて</p>
    <p>
      以下の四つのコースの中から、ご希望の曜日、時間のクラスをお選びいただけます。<br>
      曜日、時間については、別紙をご確認ください。中学生以上から受講が可能です。<br>
      各コースの1クラスの定員：10名　レッスン時間：60分
    </p>

    <table>
      <tr><th>コース</th><th>受講料（週一回、一ヶ月分）</th></tr>
      <tr><td>A. 平日昼間（初心者）</td><td>8,800円</td></tr>
      <tr><td>B. 平日昼間（中・上級者）</td><td>12,000円</td></tr>
      <tr><td>C. 平日夜間・土日（初心者）</td><td>9,300円</td></tr>
      <tr><td>D. 平日夜間・土日（中・上級者）</td><td>12,500円</td></tr>
    </table>

    <p class="section-title">入会時のお支払い</p>
    <p>
      ご入会の際に、入会金（6,600円）、年会金（2,200円）、受講料1ヶ月分を現金でお支払いください。<br>
      受講料は、2ヶ月目から口座引き落としになります。
    </p>

    <p class="section-title">割引制度</p>
    <p>複数の割引は同時に適応できません。一番条件のいい割引が一つ適用されます。</p>

    <table>
      <tr><th>種類</th><th>適応対象</th><th>割引内容</th></tr>
      <tr>
        <td>学生割引</td>
        <td>中学生、高校生</td>
        <td>毎月の受講料を10％割引</td>
      </tr>
      <tr>
        <td>複数のコース・クラス割引</td>
        <td>複数コース・クラスを受講する方</td>
        <td>二つ目以降のコース・クラス毎月の受講料を50％割引</td>
      </tr>
      <tr>
        <td>家族割引</td>
        <td>ご家族に本スクールの受講生がいる方</td>
        <td>入会金無料、毎月の受講料を15％割引</td>
      </tr>
    </table>

    <p class="section-title">振り替え制度</p>
    <p>
      同じコースの他の曜日に振り替えて受講する場合、フロントで事前にご予約ください。
    </p>

    <p class="section-title">各種手続き</p>
    <p>以下の場合は、期日までにフロントでお手続きください。</p>

    <table>
      <tr><th>変更内容</th><th>手続き期限</th></tr>
      <tr>
        <td>変更（コースを変更したり、同じコース内で曜日・時間を変更する場合）</td>
        <td>変更したい月の前月10日まで</td>
      </tr>
      <tr>
        <td>退会（スクールをやめる場合）</td>
        <td>最終受講の前月末まで</td>
      </tr>
      <tr>
        <td>休会（スクールを1ヶ月以上休む場合）</td>
        <td>休会したい月の前月20日まで</td>
      </tr>
    </table>

    <p class="note">
      ※手数料550円がかかります（入会後3ヶ月以内に手続きをする場合は無料）。
    </p>

    <p>
      電話：062-241-3998（9時～22時）<br>
      〒433-0010 北高市朝中町27<br>
      ホームページ：<a href="http://www.akiharayuukibui-tennis.jp" target="_blank">http://www.akiharayuukibui-tennis.jp</a>
    </p>
  </div>

  <div class="follow-up">
      <a>高校生の村田さんは「C 平日夜間・土日（初心者）コース」に入会したいと思っている。姉がすでに同じコースを受講しているが、入会時に支払うものは何か。</a>
      <ul class="options">
        <li>入会金、年会費、10％割引された受講料</li>
        <li>入会金、年会費、15％割引された受講料</li>
        <li>年会費、15％割引された受講料</li>
        <li>年会費、50％割引された受講料</li>
      </ul>
    </div>

    <div class="follow-up">
      <a>リナさんは、このテニススクールに1か月前に入会し、現在「B. 平日昼間（中・上級者）コース」を受講している。5月から「D. 平日夜間・土日（中・上級者）コース」に変わりたいと思っているが、リナさんはどうしなければならないか。今日は3月15日である。</a>
      <ul class="options">
        <li>4月10日までに、手数料550円を支払い、手続きをする</li>
        <li>4月10日までに手続きをする。手数料は必要ない</li>
        <li>4月20日までに、手数料550円を支払い、手続きをする</li>
        <li>4月20日までに手続きをする。手数料は必要ない</li>
      </ul>
    </div>
</body>
</html>


--- example 2 ---
<div class="article">
<h2>着物レンタルのご案内</h2>

<p>着物を着て水森市を観光しませんか。「はなかわ」では、山林店、古寺店、森島店の三つの店で、レンタルの着物をご用意しております。</p>

<h3>＜着物レンタルの流れ＞</h3>
<ol>
  <li>ご利用になりたい店に電話でご予約ください。</li>
  <li>ご予約の日時にご来店になり、お好きな着物にお着替えください。必要な方には無料でお手伝いいたします。</li>
  <li>お支払いのあと、着物で観光をお楽しみください。</li>
  <li>各店の最終返却時間までに借りた店に戻り、当日中に着物をご返却ください（翌日返却も可能です。ご希望の方は、＜翌日返却について＞をお読みください）。</li>
</ol>

<h3>＜料金（1名様）＞</h3>
<p>基本料金：3,500円</p>

<h3>＜割引について＞</h3>
<ul>
  <li>早期予約割引：1週間前までのご予約で基本料金から300円割引します。</li>
  <li>学生割引：学生の方は基本料金から200円割引します。</li>
  <li>※早期予約割引を使う場合は、学生割引は使えません。</li>
</ul>

<h3>＜お持ちになる物＞</h3>
<p>特にありません。はき物などもセットでお貸しします。</p>

<h3>＜翌日返却について＞</h3>

<h4>ご予約時の申し込み</h4>
<p>1,200円の翌日返却料金で、返却時間を翌日の正午までに延長できます。</p>

<h4>ご来店時の申し込み、またはお出かけ後の変更</h4>
<p>翌日返却料金は1,500円になります。お出かけ後の変更の場合は、借りた日の最終返却時間までに借りた店にお電話ください。翌日返却料金は、返却の際にお支払いください。</p>

<p>※返却が翌日の正午を過ぎる場合、追加料金1,000円をいただきます。その後は、1日遅れるごとに3,000円を請求いたします。</p>

<h3>＜各店の営業時間・返却時間＞</h3>
<table border="1" cellspacing="0" cellpadding="6">
  <tr>
    <th>店舗</th>
    <th>営業開始時間</th>
    <th>最終返却時間</th>
  </tr>
  <tr>
    <td>山林店、古寺店</td>
    <td>8時</td>
    <td>18時30分</td>
  </tr>
  <tr>
    <td>森島店</td>
    <td>9時</td>
    <td>18時</td>
  </tr>
</table>

<p>※電話番号など、詳細はホームページ内の各店のページをご覧ください。</p>

<hr>
</div>


<div class="follow-up">
    <a>大学生のリンさんは、2週間後の日曜日に山林店で着物をレンタルしたいと思っている。着物は当日中に返却する予定だ。今日、予約をする場合、料金はいくらになるか。</a>
    <ul class="options">
      <li>3,500円</li>
      <li>3,500円から200円が割引された金額</li>
      <li>3,500円から300円が割引された金額</li>
      <li>3,500円から200円と300円が割引された金額</li>
    </ul>
    </div>
    
    <a>ローザさんは、今日、森島店で着物を借りた。今日中に返却する予定だったが、店を出たあとで翌日返却に変更したくなった。今は14時である。明日の午前中に返却する場合、どうすればいいか。</a>
    <ul class="options">
      <li>今日の18時までに森島店に電話をして、返却の際に1,200円を支払う。</li>
      <li>今日の18時までに森島店に電話をして、返却の際に1,500円を支払う。</li>
      <li>今日の18時までに森島店に電話をして、返却の際に1,500円と1,000円を支払う。</li>
      <li>今日の18時30分までに森島店に電話をして、返却の際に1,500円を支払う。</li>
    </ul>
</div>
"""

topic_understanding_txt_teacher_prompt = """
Role: You are a Japanese teacher writing an exam paper for the JLPT N2 level. 

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
Content: Ensure the vocabulary is restricted to N2 level. 
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
男：あ、はい。
女：それから１番大事な当日配る資料、コピーまだなんじゃない？100部だよね？
男：あ、それなんですけど、発表者の方からの資料が全部そろってないんですよ。
女：そう、みなさんお忙しい方ばかりだから…私の方で発表者に資料を送ってもらうようにすぐに連絡をするから、集まったら次第コピーしよう。週明けには出してもらうようにするね。
男：はい、わかりました。
</div>

<p class="follow-up">男の学生は、この後まず何をしますか。</p>
<div class="options">
  <li>シンポジウムのポスターを貼る</li>
  <li>スタッフの当日の予定表を作る</li>
  <li>当日配る資料をコピーする</li>
  <li>発表者に連絡する</li>
</div>


--- example 2 ---
<p class='background'>スーパーで男の店長と女の店員が話しています。女の店員はこの後まず、何をしますか。</p>

<div class='conversation'>
女：おはようございます、森田さん。今日は一部の商品に値引きシールを付ける作業をやってくれることになってるね。
男：あ、はい。準備してます。
男：えっと、忙しい時に悪いんだけど、倉庫に行って南コーヒーの豆、何袋あるか数えてきてくれる？数が少なかったら今日中に注文しないといけないんだ。
女：あ、わかりました。急ぎですか？
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
</div>

"""

keypoint_understanding_teacher_prompt = """
Role: You are a Japanese teacher writing an exam paper for the JLPT N2 level. 

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
Content: Ensure the vocabulary is restricted to N2 level. 
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
<p class='background'>テレビでアナンサーの女の人がパン屋の店長にインタビューをしています。店長はどうしてパン屋を始めたと言っていますか。</p>
<div class='conversation'>  
女: 店長の山本さんです。こちらのお店の手作りのパン、大変人気ですが山本さんご自身は以前、会社員をなされていたんですよね？
男: はい。この店はもともとパン作りが好きな母がやる予定だったんですが、店を出す準備をしている途中で母が病気になってしまいました。母はずっとパン屋をやりたかったので店を諦めることをとても残念がっていたんですよ。それで「やってくれ」と言われたわけじゃないんですが、僕が何とか形にしたいと思いました。</p>
女: それまでパン作りのご経験はあったんですか？
男: いえ、全くなくて…パン作りは専門学校で一から勉強しました。卒業する前に母は亡くなりました。
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
 <p class='background'>うちで女の人と男の人が話しています。２人は引っ越しの値段を安くするため、どうすることにしましたか。
 <div class='conversation'> 
女: うーん、そうだね。安い引っ越し会社は見つからないだろうし、費用を抑えられるようにあんまり使ってない大きい家具のもらい手を探そうか。
男: うん、そうだね。</p>
女: 引っ越し会社に引越しの見積もりを出してもらったけど予算よりかなり高かったよ。今の時期はどこの会社も高いんだね。荷物の量と移動距離で料金を計算するから荷物を減らせば安くなるって。
男: そう、んー。大きい荷物を減らそうか。え一つと、大きいものって言ったらソファー、冷蔵庫、本棚だね。
女: 本棚は分解できるよ。ソファーはあまり使ってないし、欲しい人にあげてもいいかもしれないね。
男: それもそうだね。あ、冷蔵庫は古いし、この際、売って向こうで新しいの買う？
女: えー？冷蔵庫はまだ使うよ！あ、そうだ。親戚のおじさんがトラックを持ってるからおじさんに手伝ってもらって、自分たちで荷物を運ぶ？
男: 荷物の積み降ろしって結構大変だよ。やっぱり引っ越し会社に頼んだ方がいいんじゃないかな？
女: うーん、そうだね。安い引っ越し会社は見つからないだろうし、費用を抑えられるようにあんまり使ってない大きい家具のもらい手を探そうか。
男: うん、そうだね。
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
Role: You are a Japanese teacher writing an exam paper for the JLPT N2 level. 

Task: Your job is to write a natural-sounding conversation between a man and a woman. Alternatively, write a personal monologue, ensuring it is logically clear and flows smoothly. The probability of dialogue and monologue appearing is 50% each 

Step 1, you should introduce the background of the dialogue.

Step 2, the total length should be approximately 200–300 words. If you write a dialogue, then the dialogue should consists of 6–7 exchanges (back-and-forth turns). 

Step 3, ask a follow-up question focusing on what the protagonist thinks, the theme of this paragraph, or what the speaker wants to express.
The topic should be appropriate for language learners and reflect everyday situations.

Step 4, provide multiple-choice options based on the listening content. These options should test comprehension of the conversation’s meaning.


Instructions:
Format: follow the format of the 2 examples in the formal exam paper but not the content.
Content: Ensure the vocabulary is restricted to N2 level. 
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
        男:私は鉄道の写真を撮るためにいろいろなところへ行きます。行く先々で鉄道ファンの方に会うと「どうやったらうまく撮れますか？」と聞かれるんですが、私は反対に「写真で何を伝えたいですか？」と尋ねるんです。シャッターを押すタイミングとか列車と風景をどんなバランスで撮るかとか、上手に撮影するテクニックはいろいろあります。けど、少しぐらい下手でも構わないんです。1枚の写真の中に季節感や感動的な風景など何を表現したいかを意識して撮ることで全く違った写真になると思うんです。</p>
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
角色：你是一名日语老师，正在为JLPT N2水平撰写试卷。 

任务：出一道符合N2水平的听力题。具体步骤如下：

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
内容：确保词汇量限制在N2级。 
参考：从用户给出的“Topic”中获得灵感。考虑前一次对话中给出的反馈（如果存在）
附加要求：
-不要在生成的内容中显示问题说明和序列号。 
-句子中的单词既不能用于问题，也不能用于选项。
-您必须在输出中显示正确答案，选项为1,2,3。例如：正解:1.


Formal exam paper: {example}
Historical Generation : {gan_history}
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

comprehensive_expression_listen_answer_teacher_prompt = """
角色：你是一名日语老师，正在为JLPT N2水平撰写试卷。 

任务：你的工作是写3个人之间听起来很自然的对话。要求是2男1女，或者2女一男。

第一步，你应该介绍对话的背景。

第二步，生成的对话要求总长度约为500-600字。针对某个话题进行讨论，需要有核心思想。

第三步，问1个后续问题，问题可以关于是主角的想法、这段话的主题或说话者想表达什么。
主题应该适合语言学习者，并反映日常情况。

第四步，根据听力内容提供多项选择题。这些选项应该测试对对话含义的理解。


说明：
格式：遵循正式试卷中的例子的格式，但不要遵循内容。
内容：确保词汇限制在N2级。 
参考：从用户给出的“Topic”中获得灵感。考虑前一次对话中给出的反馈（如果存在）
附加要求：
-不要在生成的内容中显示问题说明和序列号。 
-句子中的单词既不能用于问题，也不能用于选项。
-在输出中显示正确答案，选项为1,2,3,4.例如：正解：n, 正确答案分布要平均，不要集中在某个选项


正式试卷：{example}
历史题目：{gan_history}
"""

comprehensive_expression_listen_answer_example = """
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
男1: ボランティアの負担が大きくなるのはちょっとね。うーん、まず、ゴミが多いところからなんとかしよう。花壇を作る代わりにっていうアイデアが良さそうだね。市役所の担当者に早速提案してみよう。
</div>
<a class='follow_up'>公園のゴミを減らすため、何を市役所に提案することにしましたか？</a>
<ul class='options'> 
    <li>ベンチの近くに花壇を作ること</li>
    <li>ゴミを捨てないように看板を増やすこと</li>
    <li>公園を見回ること</li>
    <li>公園を見回ること</li>
</ul>
"""

comprehensive_expression_show_answer_teacher_prompt = """
角色：你是一名日语老师，正在为JLPT N2水平撰写试卷。 

任务：你的工作是写3个人之间听起来很自然的对话。要求是2男1女，或者2女一男。

第一步，你应该介绍对话的背景。

第二步，生成的对话要求总长度约为500-600字。针对某个话题进行讨论，需要有核心思想。

第三步，问2个后续问题，问题可以关于是主角的想法、这段话的主题或说话者想表达什么。
主题应该适合语言学习者，并反映日常情况。

第四步，根据听力内容提供多项选择题。这些选项应该测试对对话含义的理解。


说明：
格式：遵循正式试卷中的例子的格式，但不要遵循内容。
内容：确保词汇限制在N2级。 
参考：从用户给出的“Topic”中获得灵感。考虑前一次对话中给出的反馈（如果存在）
附加要求：
-不要在生成的内容中显示问题说明和序列号。 
-句子中的单词既不能用于问题，也不能用于选项。
-在输出中显示正确答案，选项为1,2,3,4.例如：正解：n, 正确答案分布要平均，不要集中在某个选项


正式试卷：{example}
历史题目：{gan_history}
"""

comprehensive_expression_show_answer_example = """
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
<a class='follow_up'>質問1: 2人は最初にどの会場に行くですか？</a>
<ul class='options'> 
    <li>中央会場</li>
    <li>南会場</li>
    <li>東会場</li>
    <li>西会場</li>
</ul>
<a class='follow_up'>質問2: 2人は2番目にどの会場に行くですか？</a>
<ul class='options'>
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

words_collocation_reflection_prompt = """
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



