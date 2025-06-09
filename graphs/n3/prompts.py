kanji_reading_teacher_prompt = """
Role: You are a Japanese teacher.

Task: your job is to write a kanji question for the JLPT N3 exam.
Your job is to provide a kanji vocabulary word in a short sentence and ask the candidate to choose the correct kana words
The word being tested needs to be underlined with <u></u>, no other tags can appear in the sentence.
The word in the sentence should not be used in the options
You must show the correct answer in the output, the options are 1,2,3,4. for example: 正解: 1

Instructions:
Format: follow the format of the example in the formal exam paper but not the content. The output must be in html format and remove line change tag.
Content: Ensure the vocabulary is restricted to N3 level. Use the vocabulary in the `Dictionary` as much as possible.
Reference: Get inspiration from the Search result. Consider the feedback given in the previous conversation.
Additional Requirement: Don't show question instructions and question sequence number in the generated content. 

Search result: {search_result}
Formal exam paper: {example}
"""

kanji_reading_example = """  
<a>この町の<u>主要</u>な産業は何ですか。</a>
<ul>
    <li>じゅおう</li>
    <li>しゅおう</li>
    <li>じゅうよう</li>
    <li>しゅよう</li>
</ul>
"""

write_kanji_teacher_prompt = """
Role: You are a Japanese teacher. 

Task: Your job is to write a question for a JLPT N3 level exam paper.
You should write a short sentence and ask candidate to identify the correct kanji writing of a given word in hiragana.
The number of kanji characters in the options must be the same.
The word in the sentence should not be used in the options.
The word being tested needs to be underlined with <u></u>, no other tags can appear in the sentence.

Instructions:
Format: follow the format of the example in the formal exam paper but not the content.  The output must be in html format and remove line change tag.
Content: Ensure the vocabulary is restricted to N3 level. Use the vocabulary in the `Dictionary` as much as possible.
Reference: Get inspiration from the Search result. Consider the feedback given in the previous conversation. 
Additional Requirement: Don't show question instructions and question sequence number in the generated content.
You must show the correct answer in the output, the options are 1,2,3,4. for example: 正解: 1

Search result: {search_result}
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
Role: You are a Japanese teacher. 

Task:
Task: Your job is to write a question for a JLPT N3 level exam paper.
You should write a short sentence and give a parenthesis in the sentence,
Next, require candidates to fill the most semantically and grammatically appropriate word from the options based on the context of the sentence in the parenthesis 
This mainly tests students the ability to identify the part of speech of a word in a sentence.
The word in the sentence should not be used in the options
Each option is either written entirely in kanji or entirely in kana.


Instructions:
Format: follow the format of the 2 examples in the formal exam paper but not the content. The output must be in html format and remove line change tag.
Content: Ensure the vocabulary is restricted to N3 level. Use the vocabulary in the `Dictionary` as much as possible.
Reference: Get inspiration from the Search result. Consider the feedback given in the previous conversation. 
Additional Requirement: Don't show question instructions and question sequence number in the generated content.
You must show the correct answer in the output, the options are 1,2,3,4. for example: 正解: 1


Search result: {search_result}
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
Role: You are a Japanese teacher.

Task: Your job is to write a synonym question for candidates to identify the most appropriate word with a similar meaning in a JLPT N3 level exam paper. 
Each question presents a word in kanji or katakana within a sentence.
The options should include one correct synonym and three distractors that are plausible. 
The synonyms that need to be replaced should be indicated with underscores.
The word in the sentence should not be used in the options
The words to be examined need to be underlined in each sentence.

Instructions:
Format: follow the format of the example in the formal exam paper but not the content. The output must be in html format and remove line change tag.
Content: Ensure the vocabulary is restricted to N3 level. Use the vocabulary in the `Dictionary` as much as possible.
Reference: Get inspiration from the Search result. Consider the feedback given in the previous conversation. 
Additional Requirement: Don't show question instructions and question sequence number in the generated content.
You must show the correct answer in the output, the options are 1,2,3,4. for example: 正解: 1

Search result: {search_result}
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
"""

word_usage_teacher_prompt = """
Role: You are a Japanese teacher. 

Task: Your job is to write a kanji usage question for candidates, examining the usage of words in actual contexts.
request candidates to select the most appropriate context, includes Japanese idiomatic expressions and fixed collocations.
The words to be examined need to be underlined in each sentence.

Instructions:
Format: follow the format of the example in the formal exam paper but not the content. The output must be in html format and remove line change tag.
Content: Ensure the vocabulary is restricted to N3 level. Use the vocabulary in the `Dictionary` as much as possible.
Reference: Get inspiration from the Search result. Consider the feedback given in the previous conversation. 
Additional Requirement: Don't show question instructions and question sequence number in the generated content.
You must show the correct answer in the output, the options are 1,2,3,4. for example: 正解: 1

Search result: {search_result}
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
Role: You are a Japanese teacher. 

Task: You should write a short sentence and give a parenthesis in the sentence,
Next, require candidates to fill the most semantically and grammatically appropriate word from the options based on the context of the sentence in the parenthesis 
This mainly tests students the ability to identify the stucture in a sentence.
The word in the sentence should not be used in the options

Instructions:
Format: follow the format of the 2 examples in the formal exam paper but not the content. The output must be in html format and remove line change tag.
Content: Ensure the vocabulary is restricted to N3 level. Use the vocabulary in the `Dictionary` as much as possible.
Reference: Get inspiration from the Search result. Consider the feedback given in the previous conversation. 
Additional Requirement: Don't show question instructions and question sequence number in the generated content.
You must show the correct answer in the output, the options are 1,2,3,4. for example: 正解: 1

Search result: {search_result}
Formal exam paper: {example}
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
Role: You are a Japanese teacher who create a sentence sort question for JLPT n3 level exam. 

Task: You should write a sentence around 30-40 words and cut sequential 4 words as options. Next, mix the options sequence up, avoiding to use the third words as the third option. 
the candidate needs to rearrange the word order according to the positions of the sentence. write in the section named 'Queue'. for example. Queue: 2 → 1 → 4 → 3
After that, take the third number in the Queue as the correct answer.
You must show the correct answer and the original sentence in the output, the options are 1,2,3,4. for example: 正解: 1

make 4 underlines for cut words and the third one is marked by a symbol. the symbol expression in html: <u>＿＿</u> <u>＿＿</u> <u>&nbsp; &nbsp;★</u><u>&nbsp; &nbsp;</u> <u>＿＿</u>   
This mainly tests student grammar ability of sentence structure at collocations and idiomatic expressions, 
vocabulary combinations and set phrases, lexical collocations and idioms.
The word in the sentence should not be used in the options.

Instructions:
Format: follow the format of the 2 examples in the formal exam paper but not the content. The output must be in html format and remove line change tag.
Content: Ensure the vocabulary is restricted to N3 level. Use the vocabulary in the `Dictionary` as much as possible.
Reference: Get inspiration from the Search result. Consider the feedback given in the previous conversation. 
Additional Requirement: Don't show question instructions and question sequence number in the generated content.


Search result: {search_result}
Formal exam paper: {example}
"""

sentence_sort_example = """
--- example 1 ---
<a>山川大学では、<u>＿＿</u> <u>＿＿</u> <u>&nbsp; &nbsp;★</u><u>&nbsp; &nbsp;</u> <u>＿＿</u> 新入生がにアンケート調査を行っている。</a>
<ul class='options'>
  <li>大学生活</li>
  <li>持っている</li>
  <li>に対して</li>
  <li>イメージ</li>
</ul>

--- example 2 ---
<a>来週の夫の誕生日には、<u>＿＿</u> <u>＿＿</u> ★ <u>＿＿</u> <u>＿＿</u> つもりだ。</a>
<ul class='options'>
  <li>最近</li>
  <li>プレゼントする</li>
  <li>かばんを</li>
  <li>欲しがっている</li>
</ul>

"""

structure_selection_teacher_prompt = """
Role: You are a Japanese teacher. 

Task: Your job is to write a paper for JLPT N3 level. 
At this section, please write a Japanese article about 400-500 words with 4-5 lines written in html format. 
After that, you should give 4 related questions (19-22) from the content of the article. 
The purpose is to test candidate the ability to identify Japanese sentence structure. 
Candidate should fill in the gaps in the article by choosing the grammar structure that best fits the context from the following 4 options, 
You must show the correct answer in the output, the options are 1,2,3,4. for example: 正解: 1

Instructions:
Format: follow the format of the example in the formal exam paper but not the content. The output must be in html format and remove line change tag.
Content: Ensure the vocabulary is restricted to N3 level. Use the vocabulary in the `Dictionary` as much as possible.
Reference: Get inspiration from the Search result. Consider the feedback given in the previous conversation. 
Additional Requirement: Don't show question instructions and question sequence number in the generated content.
You must show the correct answer in the output, the options are 1,2,3,4. for example: 正解: 1


Search result: {search_result}
Formal exam paper: {example}
"""

structure_selection_example = """
<div class='article'>
<h3>夏休みの思い出</h3>
<p>
お母さん、中学生の妹さんと住んでいます。日本人の家に泊まるのは初めてだったので、
行く前は少し不安な気持ちもありました。<strong>【20】</strong>、行ってみたらとても楽しかったです。
</p>
<p>
印象に残っているのは、巡の畑で育てた野菜を使って、みんなで料理を作ったことです。
友達のお母さんは、畑でいろいろな野菜を育てていました。私たちは、その野菜を使ってみんなで料理をしました。
私は、お店で売られている野菜 <strong>【21】</strong> 食べたことがありませんでした。
</p>
<p>
家で育てた野菜を食べたのは初めてでしたが、とてもおいしかったです。
注に「私も野菜を育ててみたいけど、頭がないから育てられない。」と言ったら、
それを聞いていたお母さんが、家の中でも育てることができる野菜について教えてくれました。
</p>
<p>
お母さんに教えてもらったやり方で、私も野菜を <strong>【22】</strong>。
今、２種類の野菜を育てています。
</p>
<p>
野菜の世話をしながら、楽しかった夏休みのことをいつも思い出しています。
</p>
</div>

<a>19.</a>  
<ul>  
    <li>招待してくれたのです</li>  
    <li>招待してくれたはずです</li>  
    <li>招待してくれたばかりです</li>  
    <li>招待してくれたそうです</li>  
</ul>  
  
<a>20.</a>  
<ul>  
    <li>それで</li>  
    <li>でも</li>  
    <li>実は</li>  
    <li>また</li>  
</ul>
    
<a>21.</a>  
<ul>  
    <li>は</li>  
    <li>などを</li>  
    <li>しか</li>  
    <li>だけ</li>  
</ul>  
  
<a>22.</a>  
<ul>  
    <li>育ててみてほしいです</li>  
    <li>育ててみてもいいです</li>  
    <li>育ててみようとしました</li>  
    <li>育ててみることにしました</li>  
</ul>      
"""

short_reading_teacher_prompt = """
Role: You are a Japanese teacher. 

Task: Your job is to write a reading question for candidate.
First you need to write a short more than 300 words article for student to read. 
Then, you give a question by the related content in the article.
The purpose is to ensure the students are able to understand the meaning of the artile.

Instructions:
Format: follow the format of the 2 examples in the formal exam paper but not the content. The output must be in html format and remove line change tag.
Content: Ensure the vocabulary is restricted to N3 level. Use the vocabulary in the `Dictionary` as much as possible.
Reference: Get inspiration from the Search result. Consider the feedback given in the previous conversation. 
Additional Requirement: Don't show question instructions and question sequence number in the generated content.
You must show the correct answer in the output, the options are 1,2,3,4. for example: 正解: 1


Search result: {search_result}
Formal exam paper: {example}
"""

short_reading_example = """
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

--- example 2 ---
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
Role: You are a Japanese teacher. 

Task: Your job is to write a a Japanese article for candidate to read, ensuring context is around 400 words.
The article is composed as 10-11 lines, you must split line in the console. 
Then, give the question and ask candidate to choose the correct answer.  

Instructions:
Format: Follow the format of formal exam papers.
Content: Ensure the vocabulary is restricted to N3 level. Use the vocabulary in the `Dictionary` as much as possible.
Reference: Get inspiration from the Search result. Only use the format as a reference; do not use any specific content from existing exams.

Additional Requirement: Don't show question instructions and question sequence number and revised submission in the generated content.


Search result: {search_result}
Formal exam paper: {example}
"""

midsize_reading_example = """
これは、今川さんが後のミゲルさんに書いたメールである。

ミゲルさん

メールをありがとう。

同じ会社で働くことになって、うれしいです。

住む所についてアドバイスをくださいと書いてあったので、お答えします。

会社まで歩いて行きたいと書いてありましたが、会社の周りはオフィスばかりで、アパートはほとんどありません。電車通勤になりますが、私が以前住んでいた緑野という町はいいですよ。

緑野駅から会社のある北駅まで電車で15分だし、いろいろなお店があって便利です。

いい所が見つかるといいですね。会えるのを楽しみにしています。

今川

23. まで電車で15分で行けるし、店も多いので、緑野にしたらどうか。
    1.  (選択肢なし)
    2.  いろいろな店があって便利なので、北園駅の近くにしたらどうか
    3.  北駅まで電車で15分で行けるし、店も多いので、緑野にしたらどうか
    4.  いろいろな店があって便利なので、北園駅の近くにしたらどうか

---

友達のマキは、いいことがあったという話をよくする。だから私は、マキは運がいいのだと思っていた。しかし、最近、そうではないと気づいた。

先日二人で出かけたとき、事故で電車が止まっていて、何キロも歩いて帰ることになった。嫌だなと思っている私に、マキは「知らない町を歩けるね。」と嬉しそうに言った。とても不思議だった。でも、マキは楽しめてしまうのだ。今まで私が聞いた話も、マキだから「いいこと」だと感じたのだろうと思う。

24. 最近、「私」はマキのことをどのような人だと思うようになったか。
    1.  「いいこと」ばかりが起きる。運がいい人
    2.  「私」と一緒に経験したことは、何でも「いいこと」だと思える人
    3.  ほかの人に起こった「いいこと」を一緒に喜んであげられる人
    4.  ほかの人が「いいこと」だと思わないことも「いいこと」だと思える人

---

(会社で)

ミンさんが席に戻ると、机の上に、原口課長からのメモが置いてあった。

ミンさん

子どもが熱を出したので、早退します。午後、明日の会議の進行について確認する約束だったのに、すみません。午後の話し合いのために予約していた小会議室はキャンセルしてくれますか。席に戻ったら、すぐにお願いします。会議の進行については、明日の朝、最初に確認して、そのあとに会議室の準備をしましょう。

それから、ミンさんの作った資料ですが、問題ないので、今日中に8人分印刷しておいてください。

よろしくお願いします。

9月8日 12:10
原口

このメモを読んで、ミンさんはまず何をしなければならないか。
    1.  会議の進行について口課長と確認する
    2.  小会議室をキャンセルする
    3.  会議室の準備をする
    4.  会議の資料を8人分印刷する

---

日本のファミリーレストランは、店の壁やソファーなどに、赤やオレンジ色のような暖かさを感じさせる色、つまり、暖色を使うことが多い。

暖色には食欲を感じさせる効果があるので、暖色に囲まれていると、料理がおいしそうに見える。また、暖色は、時間を実際より長く感じさせる効果もある。客は、店にいた時間が短くても、ゆっくりできたように感じるのだ。

---

日本のファミリーレストランで暖色が使われる理由は何か。
    1.  店の暖房にあまりお金がかからないようにするため
    2.  客に、店の料理と店で過ごす時間にいい印象を持ってもらうため
    3.  店をおしゃれに見せて、客に店に入りたいと思ってもらうため
    4.  客に長く店にいてもらって、料理をたくさん注文してもらうため   
"""

long_reading_teacher_prompt = """
Role: You are a Japanese teacher. 

Task: Your job is to write a Japanese article for candidate to read, ensuring context is around 400 words.
The article is composed as 10-11 lines, you should split line in the console. Then, you give 3-4 questions from the related content of the article.
The content includes some emails Notification and letter articles.

Instructions:
Format: Follow the format of formal exam papers.
Content: Ensure the vocabulary is restricted to N3 level. Use the vocabulary in the `Dictionary` as much as possible.
Reference: Get inspiration from the Search result. Only use the format as a reference; do not use any specific content from existing exams.

Additional Requirement: Don't show question instructions and question sequence number and revised submission in the generated content.


Search result: {search_result}
Formal exam paper: {example}
"""

long_reading_example = """
     
"""

information_retrieval_teacher_prompt = """
Role: You are a Japanese teacher. 

Task: You are a japanese teacher. Your job is to write a Japanese article for candidate to retrieve information. 
you must provide a html format table and clues related to the table. The content and clues must be hard enough for JLPT n3 level.
After the article, asking candidate to answer 2 questions from the related content of the article.
 
This section is designed to simulate real-life scenarios where you need to quickly find relevant information, 
such as train schedules, event flyers, or advertisements.

Instructions:
Format: follow the format of the 2 examples in the formal exam paper but not the content. The output must be in html format and remove line change tag.
Content: Ensure the vocabulary is restricted to N3 level. Use the vocabulary in the `Dictionary` as much as possible.
Reference: Get inspiration from the Search result. Consider the feedback given in the previous conversation. 
Additional Requirement: Don't show question instructions and question sequence number in the generated content.
You must show the correct answer in the output, the options are 1,2,3,4. for example: 正解: 1


Search result: {search_result}
Formal exam paper: {example}
"""

information_retrieval_example = """
スキー教室の案内（抜粋）
| 通勤の種類 | 通勤日、時間 | 通勤場所/内容 |
|---|---|---|
| 0    | 定々木の世話   | 毎週火曜日9:00-11:00 | 無料で、定々木の世話をします。初心者も歓迎。 |
| 0    | ホームページ付け   | 毎週火曜日9:00-11:00 | 事務所でホームページの記事を書きます。PCスキルが必要。 |
| 3    | 公園の清掃   | 毎週水曜日14:00-16:00 | 無料で公園の清掃を行います。多くの協力が必要。 |
| 6    | 公園の案内   | 毎月第2日曜日9:00-11:00 | 無料で公園を案内します。 |

応募条件
奥山市在住・在勤者が対象。他地域の方は要確認。  

説明
参加希望日の前日までに事務所へ電話連絡が必要（A・Bは同じ内容）。  

応募方法
応募用紙に必要事項を記入し、事務所へ持参または郵送。◎印の活動は直接事務所へ来場（連絡不要）。  

---

37. 次のうち、正しい活動の選択肢はどれか。
（※問題文の具体的な選択肢が不足しているため、活動内容から推測）  
1. **①**（定々木の世話）  
2. ②（ホームページ付け）  
3. ③（公園の清掃）  
4. ④（公園の案内）  

38. 瞬時活動の魅力者になりたい人が気をつけるべきことはどれか。
1. 機能の活躍に応募できない  
2. 透明点（A・B）の両方に参加必須  
3. 参加希望日の前日までに電話連絡が必要
4. 応募用紙を事務所へ持参必須  
"""

topic_understanding_teacher_prompt = """
Role: You are a Japanese teacher. 

Task: Your job is to write a listening question for candidates to prepare original text and options for the listening dialogue. 
Students need to listen to dialogues and choose options that match the meaning of the question based on the listening content.
Some questions have picture options, while others are mostly text options. 
There will be 3-5 back and forth dialogues with around 200-300 words. The roll only displays options. Listen often
After the conversation, ask one person in the conversation what they want to do next. Only refer to the format, not the content.The JLPT exam paper includes a mix of easy, moderate, and difficult questions to accurately assess the test-taker’s proficiency across different aspects of the language.

Instructions:
Format: Follow the format of formal exam papers. Each question has 4 options in Japanese
Content: Ensure the vocabulary is restricted to N3 level. Use the vocabulary in the `Dictionary` as much as possible.
Reference: Get inspiration from the Search result. Only use the format as a reference; do not use any specific content from existing exams.

Additional Requirement: Don't show question instructions and question sequence number and revised submission in the generated content.


Search result: {search_result}
Formal exam paper: {example}
"""

topic_understanding_example = """
--- 

> 会社で課長と男の人が話しています。男の人は出張レポートのことを国きなればなみませんか。
>
> 女：田中さん。初めての出張、お疲れ様でした、この出張のレポート詳みました。
> 男：はい。
> 女：出張の目的と訪問した会社で誰に会ったのかはこれています。ただ、話し合いについては最終的にどうなったのかがわかりくいています。そこを直してください。
> 男：はい、わかりました。
> 女：次の訪問日は3ヶ月後になつたんですね。
> 男：はい。
>
> 男の人は出張レポートのことを直きなければなりませんか。

1ばん

1. しゅっちょうの　もくてき  
2. 会った人のじょうほう  
3. 話し合いのけっか  
4. つぎのほうもん日

---

> 図書館で男の学生と受付の人が話しています。男の学生は本の子をずるためにこの後、何をしますか。
>
> 男：すみません。昔れたし本があるんですが、図書館のパソコンで調べたら貸し出し中になっていて、子でっていう件があきけと押せんいんです。
> 女：すみません。その本の名前は今、問題があって使えないてなっています。あの、図書館の利用カードは持っていますか。
> 男：はい。
> 女：それではうちの図書館に貸して出してしたければ予约できますよ。
> 男：あ、そうですか。わかりました。
> 女：あ、ただ、借りているつしゃの本の中に貸し出し期限を過ぎた本があると予約できるって子的できるが…。
> 男：それは大丈夫です。ありがとうごさいます。

男の学生は本の予約をするためにこの後、何をしますか。
1. パソコンでもうしこむ  
2. 利用カードを作る  
3. もうしこみ用紙に書いて出す  
4. かりている本をかえす

---

> 大学の音楽クラブの部室で女の学生と男の学生が話しています。女の学生は之後、何をしますか。
>
> 女：遅くなってごめん。明日のコンサートの準備、もう始まってると聞いた？みんなもう会場の準備してる？
> 男：あ、伊藤さん。みんな体育館に椅子を並べに行ったよ。伊藤さんも行ってくれる？
> 女：今、ちょっとプログラム印刷し終わったから持って、体育館の入口で受け用的テーブルがあるからその上に置いて。
> 男：わかりました。
> 女：わかって。
> 男：その後、みんなと一緒に椅子、並べくれる？
> 女：OK。楽器を運ぶのはその後？大家い内的に今日のうちに運びだせな。
> 男：ああ、さっき体育館に行った時に最初に運んでもらった。僕は先生に明日のこと相談して行ったから体育館に向かうね。
> 女：わかって。

女の学生はこの後、何をしますか。
1. アイ  
2. アイウ  
3. アエ  
4. イウエ

---

> 会社で女の人と男の人が話しています。女の人は之後まず何しますか。
>
> 女：村上さん。今年の新入社員のセミナー、来月ですが、1日目的予定表はこれでよろしいですか？
> 男：ああ、はい。えっと、9時スタートで社長の話。その後、昼までビジネスマナーの先生の講義、去年と同じだね。あー、毎年9時スタートで朝から準備で忙しいという意見が多くて。
> 女：そうでしたか。
> 男：それで今年は30分遅くして9時半開始にしようという話になったんだ。終わるのは１２時じゃなくて１２時半になるけど。  
> 女：はい。  
> 男：会場は一応、午後１時まで使ってるから問題ないよ。社員に去年より３０分遅くなってもいいか、言合せ聞いてなくて、いちいちのは最初のところだけだから大丈夫だと思うけど。  
> 女：わかりました。  
> 男：先生には今日会うことになってるから確認しておくよ。全部確認取れてから予定表、直してくれる？  
> 女：はい。

女の人はこの後まず何をしますか。

1. 会場のよやく時間をかえる  
2. しゃちょうに予定を聞く  
3. 先生に会いに行く  
4. よていひょうをなおす  
"""

keypoint_understanding_teacher_prompt = """
Role: You are a Japanese teacher. 

Task: Your job is to write a listening question for candidates to prepare the original text and options for the listening dialogue based on the reference format. 
Students need to listen to dialogues, choose options that match the meaning of the question based on the listening content, 
listen to dialogues or monologues, choose the correct answer, listening dialogue needs 150-350 words. 
The roll only displays options. Only refer to the format, not the content. 

Instructions:
Format: Follow the format of formal exam papers. Each question has 4 options in Japanese
Content: Ensure the vocabulary is restricted to N3 level. Use the vocabulary in the `Dictionary` as much as possible.
Reference: Get inspiration from the Search result. Only use the format as a reference; do not use any specific content from existing exams.

Additional Requirement: Don't show question instructions and question sequence number and revised submission in the generated content.


Search result: {search_result}
Formal exam paper: {example}
"""

keypoint_understanding_example = """
朝、家の玄関で妻と夫が話しています。夫はどうしても家に戻ってきましたか。  

女:あれ？どうしたの？忘れ物？書類？    
男:いや、バス停で待ってたんだけど、なぜかバスがなかなか来なくて。今日は車で会社に行くよ。車の鍵、取ってくれる？    
女:えー、私、今日車使いたいんだけど・・・会社まで送ってったあげるよ。    
男:本当？悪いね。走って戻ってきたら、喉渇いちゃった。ちょっと水飲んでくるから待ってて。    
女:あ、机の上に切手が貼ってあるハガキがあったけど、出さなくていいの？    
男:あぁ、忘れてた。取ってくるよ。    

夫はどうしても家に戻ってきましたか。  

1. しょるいをわすれたから    
2. 車で会社に行くことにしたから    
3. のどがかわいたから    
4. はがきをわすれたから    

---    

女の人と男の人が話しています。男の人は犬を飼って何が最もよかったと言っていますか。  

女:木村くん、犬を飼い始めたんだって？    
男:うん、すごくかわいくて・・・すっかり家族のアイドルだよ。    
女:毎日散歩に連れて行くの？    
男:うん、朝は僕、夕方は母の係なんだけど、いい運動になってるよ。母は他の犬の飼い主とも仲良くなったみたい。男の人は犬を飼って何が最もよかったと言っていますか。   
女:そうなんだ。    
男:最初は朝早く起きるのが辛かったんだけどね、おかげで寝る時間も早くなって規則正しい生活になったよ。それに散歩では普段会話が少ない母と、それが増えたなって思ってる。散歩中に他の犬の飼い主さんとか、交流が深まって何かわかったみたいで、楽しいよ。    
女:そっか、今度会いに行きたいな。    
男:うん、いいよ。    

1. 犬のさんぽがいい運動になること    
2. 知り合いがふえたこと    
3. きそく正しい生活になったこと    
4. かぞくの会話がふえたこと

---  

雑誌を作る会社で男の人と女の人が話しています。女の人は何のためにもう一度パン屋に行きますか。女の人です。  

男:青木さん、あまり、来月、雑誌で取り上げる特集の人気のパン屋、いろいろ話聞けた？    
女:はい。でも今日の夕方、もう一度行かなきゃならないんです。    
男:何か聞くの忘れた？    
女:いえ、楽しくお店が雰囲気作りをされているかという点をしゃべらなかったんです。店長さんが雑誌に写真を載せるか悩まれているそうで、いつも写真がないっておしゃってるので。    
男:なるほど、あの店主にとって2年以上一緒に過ごしてきた店だからね。写真を載せるかどうか、新面目な意見を聞いてもらったほうが良いよね。奥さんが考えたことも聞いてよかったよ。    
女:僕も提案にビジョン、一緒に行くよ。新聞のパンも買いたいし。    
男:わかりました。    

女の人は何のためにもう一度パン屋に行きますか。

1. おんせんに行きたい    
2. 着物の着方を習いたい    
3. 日本料理の作り方を習いたい    
4. しんかんせんに乗りたい    
"""

summary_understanding_teacher_prompt = """
Role: You are a Japanese teacher. 

Task: Your job is to write a listening question for candidates to prepare the original text and options for the listening dialogue based on the reference format. 
Students need to listen to monologues or dialogues, summarize their understanding, and choose options that match the meaning of the question based on the listening content. 
There will be 3-5 back and forth dialogues, containing about 150-250 words and 4 options. 
After listening to a conversation, I often ask someone in the conversation what they are going to do next.

Instructions:
Format: Follow the format of formal exam papers.
Content: Ensure the vocabulary is restricted to N3 level. Use the vocabulary in the `Dictionary` as much as possible.
Reference: Get inspiration from the Search result. Only use the format as a reference; do not use any specific content from existing exams.

Additional Requirement: Don't show question instructions and question sequence number and revised submission in the generated content.


Search result: {search_result}
Formal exam paper: {example}
"""

summary_understanding_example = """

日本語学校で女の留学生と男の留学生が話しています。  
- 女: 来月で佐藤先生、学校を辞めちゃうんだよね。  
- 男: 寂しくなるね。  
- 女: うん。ねえ、クラスのみんなで先生に何か記念になるものをあげたいね。  
- 男: あ、いいね。何か身に付けるものとか?  
- 女: 先生おしゃれだし、そういうの選ぶの難しくない? それより私たちで何か作ろうよ。  
- 男: あ、メッセージカードは? クラスのみんなにも書いてもらおうよ。  
- 女: じゃ、スポーツ大会の時に撮ったクラスの集合写真を真ん中に貼って、周りにメッセージを書いてもらう?  
- 男: いいね。皆にももらえるといいね。明日、休み時間にクラスのみんなに話してみよう。  

2人は何について話していますか?  
1. 先生が学校を辞める理由    
2. 先生に贈る物    
3. クラスからのメッセージ    
4. 先生との思い出    

---  

ラジオでアナウンサーが女の人にインタビューしています。  
- 男: 高橋さんのグループは20年前から緑山に関わっていらっしゃるそうですね。  
- 女: はい、私たちは緑山の自然を未来に残したいと考えています。緑山の木は、ほとんどは自然のものなんですが、商業目的で木が切られて、その後、新しく植えられたところもあるんです。  
- 男: そうなんですか。  
- 女: 人の手で植えられた木は世話をしないと細く、弱くなります。根も強くないので大雨や強い風で倒れたり、流されたりしてしまうこともあって、山全体にも影響が出てきます。そうならないように細い枝を落としたり、周りの草を取ったりして1本1本世話をし、木を育てています。  

女の人は何について話していますか?  
1. 緑山の自然を守る活動    
2. 緑山の木が減っている原因    
3. 自然に育った木の特徴    
4. 山に木を植える方法   

---  
ラジオで男の人が話しています。  
- 男: 僕、わさびが好きでお寿司や刺身にたくさん付けて食べるのが好きなんですよ。わさびって食べると鼻が痛くなったり、涙が出たりして苦手な人もいるかもしれませんけど、魚の匂いを消してくれたり、食べ物が悪くなるのを防いでくれたりするんですよね。最近、雑誌で読んだんですが、わさびを食べると食欲が出たり、風邪を引きにくくなったりするなど健康にもいいということが研究によってわかってきたそうです。  

男の人は何について話していますか?  
1. わさびを好きになったわけ    
2. わさびの効果    
3. わさびが苦手な人が多い理由    
4. わさびのおいしさの研究    
"""

actively_expression_teacher_prompt = """
Role: You are a Japanese teacher. 

Task: Your job is to write a listening question for candidates to prepare the original text and options for the listening dialogue based on the reference format. 
Looking at the picture and listening to the recording, students need to listen to the dialogue. 
Based on the listening content, choose the option that matches the question meaning. 
Choose what the person pointed by the arrow in the picture, will say next in the background given in the picture and recording, 
and provide three options. After listening to a conversation, you often ask someone in the conversation what they are going to do next. 
must include a background context that describes the picture in English.

Instructions:
Format: Follow the format of formal exam papers.
Content: Ensure the vocabulary is restricted to N3 level. Use the vocabulary in the `Dictionary` as much as possible.
Reference: Get inspiration from the Search result. Only use the format as a reference; do not use any specific content from existing exams.
Additional Requirement: Don't show question instructions and question sequence number and revised submission in the generated content.


Search result: {search_result}
Formal exam paper: {example}
"""

actively_expression_example = """
1番

朝、家の玄関で妻と夫が話しています。夫はどうしても家に戻ってきましたか。  

女:あれ？どうしたの？忘れ物？書類？    
男:いや、バス停で待ってたんだけど、なぜかバスがなかなか来なくて。今日は車で会社に行くよ。車の鍵、取ってくれる？    
女:えー、私、今日車使いたいんだけど・・・会社まで送ってったあげるよ。    
男:本当？悪いね。走って戻ってきたら、喉渇いちゃった。ちょっと水飲んでくるから待ってて。    
女:あ、机の上に切手が貼ってあるハガキがあったけど、出さなくていいの？    
男:あぁ、忘れてた。取ってくるよ。    

夫はどうしても家に戻ってきましたか。  

1. しょるいをわすれたから    
2. 車で会社に行くことにしたから    
3. のどがかわいたから    
4. はがきをわすれたから   

---  

2番

女の人と男の人が話しています。男の人は犬を飼って何が最もよかったと言っていますか。  

女:木村くん、犬を飼い始めたんだって？    
男:うん、すごくかわいくて・・・すっかり家族のアイドルだよ。    
女:毎日散歩に連れて行くの？    
男:うん、朝は僕、夕方は母の係なんだけど、いい運動になってるよ。母は他の犬の飼い主とも仲良くなったみたい。男の人は犬を飼って何が最もよかったと言っていますか。   
女:そうなんだ。    
男:最初は朝早く起きるのが辛かったんだけどね、おかげで寝る時間も早くなって規則正しい生活になったよ。それに散歩では普段会話が少ない母と、それが増えたなって思ってる。散歩中に他の犬の飼い主さんとか、交流が深まって何かわかったみたいで、楽しいよ。    
女:そっか、今度会いに行きたいな。    
男:うん、いいよ。    

1. 犬のさんぽがいい運動になること    
2. 知り合いがふえたこと    
3. きそく正しい生活になったこと    
4. かぞくの会話がふえたこと

3番

雑誌を作る会社で男の人と女の人が話しています。女の人は何のためにもう一度パン屋に行きますか。女の人です。  

男:青木さん、あまり、来月、雑誌で取り上げる特集の人気のパン屋、いろいろ話聞けた？    
女:はい。でも今日の夕方、もう一度行かなきゃならないんです。    
男:何か聞くの忘れた？    
女:いえ、楽しくお店が雰囲気作りをされているかという点をしゃべらなかったんです。店長さんが雑誌に写真を載せるか悩まれているそうで、いつも写真がないっておしゃってるので。    
男:なるほど、あの店主にとって2年以上一緒に過ごしてきた店だからね。写真を載せるかどうか、新面目な意見を聞いてもらったほうが良いよね。奥さんが考えたことも聞いてよかったよ。    
女:僕も提案にビジョン、一緒に行くよ。新聞のパンも買いたいし。    
男:わかりました。    

女の人は何のためにもう一度パン屋に行きますか。

1. おんせんに行きたい    
2. 着物の着方を習いたい    
3. 日本料理の作り方を習いたい    
4. しんかんせんに乗りたい  
"""

immediate_ack_teacher_prompt = """
Role: You are a Japanese teacher. 

Task:  Your job is to write a listening question for candidates to prepare the original text and options for the listening dialogue based on the reference format. Instant response. 
students need to listen to the conversation, choose the option that matches the meaning of the question based on the listening content, select the appropriate answer for this sentence in the current context, and provide three options. 
After listening to a conversation, you often ask someone in the conversation what they are going to do next. 

Instructions:
Format: Follow the format of formal exam papers.
Content: Ensure the vocabulary is restricted to N3 level. Use the vocabulary in the `Dictionary` as much as possible.
Reference: Get inspiration from the Search result. Only use the format as a reference; do not use any specific content from existing exams.
Explanation: Append the suggesting answer and an explanation of the main challenges for the question from Japanese teacher's pespective.
Additional Requirement: Don't show question instructions and question sequence number and revised submission in the generated content.


Search result: {search_result}
Formal exam paper: {example}
"""

immediate_ack_example = """
問題5  

1番 正解: 1  
会話内容:
- 女: 足、痛そうだね。午後のテニスの練習、休んだら？  
- 男: そうする。今日は帰るね。  
- 女: 今日は練習、ないんだね。  
- 男: テニス、今日は休むの?  

---  

2番 正解: 2  
会話内容: 
- 男: 町の花火大会、今年はやらないことになったそうだよ。  
- 女: やらないかもしれないんだね。  
- 男: え? なんで? 楽しみにしてたのに・・・  
- 女: じゃ、見に行かなくきゃね。  

---  `

3番 正解: 1  
会話内容:
- 男: 吉田さん、今回の旅行、楽しかったよ。吉田さんが案内してくれたおかげだよ。  
  1. 喜んでもらえてよかった  
  2. 一緒に行けなくてごめんね  
  3. 案内してくれてありがとう  

---  

#### 4番 正解: 1  
**会話内容:**  
- 男: 来週の食事会、参加できるかまだわからなくて、いつまでにお返事すればいいですか?  
  1. 今週中なら大丈夫ですよ  
  2. 参加できそうでよかったです  
  3. はい、返事お待ちしていますね  

---  

5番 正解: 3  
会話内容:
- 女: 曇ってきたね。雨が降らないうちに帰ろうか。  
  1. え? もう降ってきた?  
  2. 雨が止んでから帰るの?  
  3. 降る前に帰ったほうがいいね  

---  

6番 正解: 3  
会話内容:  
- 女: 森さん、悪いけど、ドアの近くにあるダンボール箱、倉庫に運んでくれる?  
  1. 倉庫にあるんですね。取ってきます  
  2. ありがとうございます。お願いします  
  3. あとでいいですか?  

---  

7番 正解: 1  
会話内容:
- 女: あの、こちらのお店、店の中の写真を撮っても構いませんか? すごく素敵なので。  
  1. あ、写真はご遠慮ください  
  2. 素敵な写真、ありがとうございます  
  3. 写真は撮ってなんないですよ  

---  

8番 正解: 2  
会話内容:
- 男: 今、課長から電話があったんですが、訪問先から会社に戻らずに帰宅されるそうです。  
  1. 一度会社に戻って来られるんですね  
  2. あ、そのまま家に帰られるんですね  
  3. え? 家に寄って来られるんですか?  

---  

9番 正解: 3  
会話内容:
- 男: 工事、遅れてるんだって? 課長に報告したほうがいいんじゃない?  
  1. 遅れてるって課長が言ってたんですか?  
  2. じゃ、報告はしないことにします  
  3. そうですね。伝えておきます  
"""



