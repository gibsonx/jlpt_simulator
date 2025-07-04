kanji_reading_teacher_prompt = """
Role: You are a Japanese teacher writing an exam paper for the JLPT N3 level.

Task: your job is to write a kanji question for a JLPT N3 level exam paper.
Your must provide a kanji word in a short sentence and ask the candidate to choose the correct kana words
The word being tested needs to be underlined with <u></u>, like <u>主要</u>, no other tags can appear in the sentence.
The word in the sentence should not be used in the options
You must show the correct answer in the output, the options are 1,2,3,4. for example: 正解: 1

Instructions:
Format: follow the format of the example in the formal exam paper but not the content. The output must be in html format and remove line change tag.
Content: Ensure the vocabulary is restricted to N3 level. 
Reference: Get inspiration from the Search result. Consider the feedback given in the previous conversation.
Additional Requirement: Don't show question instructions and sequence number in the generated content. 

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
Role: You are a Japanese teacher writing an exam paper for the JLPT N3 level. 

Task: Your job is to write a question for a JLPT N3 level exam paper.
You should write a short sentence and ask candidate to identify the correct kanji writing of a given word in hiragana.
The number of kanji characters in the options must be the same.
The word in hiragana being tested needs to be underlined with <u></u>, no other tags can appear in the sentence.

Instructions:
Format: follow the format of the example in the formal exam paper but not the content.  The output must be in html format and remove line change tag.
Content: Ensure the vocabulary is restricted to N3 level. 
Reference: Get inspiration from the Search result. Consider the feedback given in the previous conversation. 
Additional Requirement: 
- Don't show question instructions and sequence number in the generated content. 
- The word in the sentence can neither be used in the question nor options.
- You must show the correct answer in the output, the options are 1,2,3,4. for example: 正解: 1

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
Role: You are a Japanese teacher writing an exam paper for the JLPT N3 level. 

Task:
Task: Your job is to write a question for a JLPT N3 level exam paper.
You should write a short sentence and give a parenthesis in the sentence,
Next, require candidates to fill the most semantically and grammatically appropriate word from the options based on the context of the sentence in the parenthesis 
This mainly tests students the ability to identify the part of speech of a word in a sentence.
The word in the sentence should not be used in the options
Options are written either entirely in kanji or entirely in kana.


Instructions:
Format: follow the format of the 2 examples in the formal exam paper but not the content. The output must be in html format and remove line change tag.
Content: Ensure the vocabulary is restricted to N3 level. 
Reference: Get inspiration from the Search result. Consider the feedback given in the previous conversation. 
Additional Requirement: 
- Don't show question instructions and sequence number in the generated content. 
- The word in the sentence can neither be used in the question nor options.
- You must show the correct answer in the output, the options are 1,2,3,4. for example: 正解: 1

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
Role: You are a Japanese teacher writing an exam paper for the JLPT N3 level. 

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
Content: Ensure the vocabulary is restricted to N3 level. 
Reference: Get inspiration from the Search result. Consider the feedback given in the previous conversation. 
Additional Requirement: 
- Don't show question instructions and sequence number in the generated content. 
- The word in the sentence can neither be used in the question nor options.
- You must show the correct answer in the output, the options are 1,2,3,4. for example: 正解: 1

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

<a>来週、ここで<u>企業</u>の説明会があります。
<ul class='options'>
  <li>旅行</li>
  <li>会社</li>
  <li>大学</li>
  <li>建物</li>
</ul>
"""

word_usage_teacher_prompt = """
Role: You are a Japanese teacher writing an exam paper for the JLPT N3 level. 

Task: Your job is to write a kanji for examining the usage of words in actual contexts for a JLPT N3 level exam paper.
Ask the student to choose the sentence that best matches the true meaning or usage of the word from 4 options,
which exam student the knowledge of Japanese idiomatic expressions and fixed collocations.
The words to be examined need to be underlined in each sentence. the question must be written in kanji, like <a>内容</a> <a>落ち着く</a>
Make only one option correct (the one using the word naturally), and ensure the other 3 sound plausible but are semantically incorrect.

Instructions:
Format: follow the format of the example in the formal exam paper but not the content. The output must be in html format and remove line change tag.
Content: Ensure the vocabulary is restricted to N3 level. 
Reference: Get inspiration from the Search result. Consider the feedback given in the previous conversation. 
Additional Requirement: Don't show question instructions and sequence number in the generated content.
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
Role: You are a Japanese teacher writing an exam paper for the JLPT N3 level. 

Task: Your job is to write a sentence grammar question for examining the usage of words in actual contexts for a JLPT N3 level exam paper.
You should write a short sentence (reference: example 1) or a conversation with 2 sentences (reference: example 2) around 40-60 words and give a parenthesis in the sentence.
the content is ranging from everyday situations, dialogues, to short explanatory contexts.

Next, require candidates to fill the most semantically and grammatically appropriate word from the options based on the context of the sentence in the parenthesis 
The word in the sentence should not be used in the options

Instructions:
Format: follow the format of the 2 examples in the formal exam paper but not the content. The output must be in html format and remove line change tag.
Content: Ensure the vocabulary is restricted to N3 level. 
Reference: Get inspiration from the Search result. Consider the feedback given in the previous conversation. 
Additional Requirement: 
- Don't show question instructions and sequence number in the generated content. 
- The word in the sentence can neither be used in the question nor options.
- You must show the correct answer in the output, the options are 1,2,3,4. for example: 正解: 1

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

Task: You should write a sentence around 40-60 words and cut a sequential 4 words as options. 
4 words must be fixed grammatical expression whose word order and structure cannot be reversed or altered 
Next, mix the options sequence up, avoiding to use the third words as the third option. 
the candidate needs to rearrange the word order according to the positions of the sentence. write in the section named 'Queue'. for example. Queue: 2 → 1 → 4 → 3
After that, take the third number in the Queue as the correct answer.
You must show the correct answer and the original sentence in the output, the options are 1,2,3,4. for example: 正解: 1

make 4 underlines to replace cut words and the third underline is marked by a ★ symbol. don't make it twice.  
The full expression of this in html is: <u>＿＿</u> <u>＿＿</u> <u>&nbsp; &nbsp;★</u><u>&nbsp; &nbsp;</u> <u>＿＿</u>   
The word in the sentence should not be used in the options.

Instructions:
Format: follow the format of the 2 examples in the formal exam paper but not the content. The output must be in html format and remove line change tag.
Content: Ensure the vocabulary is restricted to N3 level. 
Reference: Get inspiration from the Search result. Consider the feedback given in the previous conversation. 
Additional Requirement: 
- Don't show question instructions and sequence number in the generated content. 
- The word in the sentence can neither be used in the question nor options.
- You must show the correct answer in the output, the options are 1,2,3,4. for example: 正解: 1


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
Role: You are a Japanese teacher writing an exam paper for the JLPT N3 level. 

Task: Your job is to write a paper for JLPT N3 level. 
At this section, please write a Japanese article about 400-500 words with 4-5 lines written in html format. 
After that, you should give 4 related questions (19-22) from the content of the article. 
The purpose is to test candidate the ability to identify Japanese sentence structure. 
Candidate should fill in the gaps in the article by choosing the grammar structure that best fits the context from the following 4 options, 


Instructions:
Format: follow the format of the example in the formal exam paper but not the content. The output must be in html format and remove line change tag.
Content: Ensure the vocabulary is restricted to N3 level. 
Reference: Get inspiration from the Search result. Consider the feedback given in the previous conversation. 
Additional Requirement: 
- Don't show question instructions and sequence number in the generated content. 
- The word in the sentence can neither be used in the question nor options.
- You must show the correct answer in the output, the options are 1,2,3,4. for example: 正解: 1


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
Role: You are a Japanese teacher writing an exam paper for the JLPT N3 level. 

Task: Your job is to write a reading question for JLPT N3 level exam. 
First you need to write a short article around 250 words for student to read. 
Then, you give a question by the related content in the article.
The purpose is to ensure the students are able to understand the meaning of the article.

Instructions:
Format: follow the format of the 2 examples in the formal exam paper but not the content. The output must be in html format and remove line change tag.
Content: Ensure the vocabulary is restricted to N3 level. 
Reference: Get inspiration from the Search result. Consider the feedback given in the previous conversation. 
Additional Requirement: 
- Don't show question instructions and sequence number in the generated content. 
- The word in the sentence can neither be used in the question nor options.
- You must show the correct answer in the output, the options are 1,2,3,4. for example: 正解: 1

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
Role: You are a Japanese teacher writing an exam paper for the JLPT N3 level. 

Task: Your job is to write a reading question for a JLPT N3 level exam.
First you need to write a mid-size article around 400 words for student to read. 
The keypoints being tested in each question needs to be underlined with <u></u>
Then, you give 3 questions by the related content in the article. the meaning of keypoint cannot be found in the article.
instead, students needs to find the answer by understanding the context in the article. 


Instructions:
Format: follow the format of the 2 examples in the formal exam paper but not the content. The output must be in html format and remove line change tag.
Content: Ensure the vocabulary is restricted to N3 level. 
Reference: Get inspiration from the Search result. Consider the feedback given in the previous conversation. 
Additional Requirement: 
- Don't show question instructions and sequence number in the generated content. 
- The word in the sentence can neither be used in the question nor options.
- You must show the correct answer in the output, the options are 1,2,3,4. for example: 正解: 1


Search result: {search_result}
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
Role: You are a Japanese teacher writing an exam paper for the JLPT N3 level.

Task: Task: Your job is to write a reading question for a JLPT N3 level exam. 
First you need to write a long article around 400 words for student to read. 
Then, you give 4 questions by the related content in the article.
The purpose is to ensure the students are able to understand the meaning of the article.


Instructions:
Format: follow the format of the example in the formal exam paper but not the content. The output must be in html format and remove line change tag.
Content: Ensure the vocabulary is restricted to N3 level. 
Reference: Get inspiration from the Search result. Consider the feedback given in the previous conversation. 
Additional Requirement: 
- Don't show question instructions and sequence number in the generated content. 
- The word in the sentence can neither be used in the question nor options.
- You must show the correct answer in the output, the options are 1,2,3,4. for example: 正解: 1


Search result: {search_result}
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
Role: You are a Japanese teacher writing an exam paper for the JLPT N3 level. 

Task: You are a Japanese teacher writing an exam paper for the JLPT N3 level. Your job is to write a Japanese article for candidate to retrieve information. 
you must provide a html format table and clues related to the table. The content and clues must be complex enough for JLPT n3 level.
After the article, asking candidate to answer 2 questions from the related content of the article. 
The questions should require reasoning beyond direct lookup; 
the true answer must be inferred through understanding the context and meaning of the key points, rather than being easily found in the article.
 
This section is designed to simulate real-life scenarios where students need to quickly find relevant information, 
such as train schedules, event flyers, or advertisements.

Instructions:
Format: follow the format of the 2 examples in the formal exam paper but not the content. The output must be in html format and remove line change tag.
Content: Ensure the vocabulary is restricted to N3 level. 
Reference: Get inspiration from the Search result. Consider the feedback given in the previous conversation. 
Additional Requirement: 
- Don't show question instructions and sequence number in the generated content. 
- The word in the sentence can neither be used in the question nor options.
- You must show the correct answer in the output, the options are 1,2,3,4. for example: 正解: 1


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
Role: You are a Japanese teacher writing an exam paper for the JLPT N3 level. 

Task: Your job is to write a natural-sounding conversation between a man and a woman.
The dialogue should consist of 6–7 exchanges (back-and-forth turns). The total length should be approximately 200–300 words.
The topic should be appropriate for language learners and reflect everyday situations.
Next, provide multiple-choice options based on the listening content. These options should test comprehension of the conversation’s meaning.
After the conversation, ask a follow-up question related to the conversation and focusing on the man or woman's next action.

Instructions:
Format: follow the format of the 2 examples in the formal exam paper but not the content.
Content: Ensure the vocabulary is restricted to N3 level. 
Reference: Get inspiration from the Search result. Consider the feedback given in the previous conversation. 
Additional Requirement: 
- Don't show question instructions and sequence number in the generated content. 
- The word in the sentence can neither be used in the question nor options.
- You must show the correct answer in the output, the options are 1,2,3,4. for example: 正解: 1


Search result: {search_result}
Formal exam paper: {example}
"""

topic_understanding_example = """
--- example 1 ---
<p class='background'>会社で課長と男の人が話しています。男の人は出張レポートのことを国きなればなみませんか。</p>

<div class='conversation'>
女：田中さん。初めての出張、お疲れ様でした、この出張のレポート詳みました。
男：はい。
女：出張の目的と訪問した会社で誰に会ったのかはこれています。ただ、話し合いについては最終的にどうなったのかがわかりくいています。そこを直してください。
男：はい、わかりました。
女：次の訪問日は3ヶ月後になつたんですね。
男：はい。
</div>

<a class='follow-up'>男の人は出張レポートのことを直きなければなりませんか。</a>
<ul class='options'>
    <li>しゅっちょうの　もくてき</li>
    <li>会った人のじょうほう</li>  
    <li>話し合いのけっか</li>  
    <li>つぎのほうもん日/li> 
</ul>  

--- example 2 ---
<p class='background'>図書館で男の学生と受付の人が話しています。男の学生は本の子をずるためにこの後、何をしますか。</p>

<div class='conversation'>
男：すみません。昔れたし本があるんですが、図書館のパソコンで調べたら貸し出し中になっていて、子でっていう件があきけと押せんいんです。
女：すみません。その本の名前は今、問題があって使えないてなっています。あの、図書館の利用カードは持っていますか。
男：はい。
女：それではうちの図書館に貸して出してしたければ予约できますよ。
男：あ、そうですか。わかりました。
女：あ、ただ、借りているつしゃの本の中に貸し出し期限を過ぎた本があると予約できるって子的できるが…。
男：それは大丈夫です。ありがとうごさいます。
</div>

<a class='follow-up'>男の学生は本の予約をするためにこの後、何をしますか。</a>
<ul class='options'>
    <li>パソコンでもうしこむ</li>  
    <li>利用カードを作る</li> 
    <li>もうしこみ用紙に書いて出す</li>   
    <li>かりている本をかえす</li> 
</ul>
"""

keypoint_understanding_teacher_prompt = """
Role: You are a Japanese teacher writing an exam paper for the JLPT N3 level. 

Task: Your job is to write a natural-sounding conversation between a man and a woman.
The dialogue should consist of 6–7 exchanges (back-and-forth turns). The total length should be approximately 200–300 words.
The topic should be appropriate for language learners and reflect everyday situations.
Next, provide multiple-choice options based on the listening content. These options should test comprehension of the conversation’s meaning.
After the conversation, ask a follow-up question focusing on why the man or woman does it, 
encouraging deeper understanding of the motivation or reasoning behind it.
The question should prompt students to choose the best option that matches the overall message or key point of the dialogue.


Instructions:
Format: follow the format of the 2 examples in the formal exam paper but not the content.
Content: Ensure the vocabulary is restricted to N3 level. 
Reference: Get inspiration from the Search result. Consider the feedback given in the previous conversation. 
Additional Requirement: 
- Don't show question instructions and sequence number in the generated content. 
- The word in the sentence can neither be used in the question nor options.
- You must show the correct answer in the output, the options are 1,2,3,4. for example: 正解: 1


Search result: {search_result}
Formal exam paper: {example}
"""

keypoint_understanding_example = """
--- example 1 ---
<p class='background'>朝、家の玄関で妻と夫が話しています。夫はどうしても家に戻ってきましたか。</p>

<div class='conversation'>
女:あれ？どうしたの？忘れ物？書類？    
男:いや、バス停で待ってたんだけど、なぜかバスがなかなか来なくて。今日は車で会社に行くよ。車の鍵、取ってくれる？    
女:えー、私、今日車使いたいんだけど・・・会社まで送ってったあげるよ。    
男:本当？悪いね。走って戻ってきたら、喉渇いちゃった。ちょっと水飲んでくるから待ってて。    
女:あ、机の上に切手が貼ってあるハガキがあったけど、出さなくていいの？    
男:あぁ、忘れてた。取ってくるよ。    
</div>

<a class='follow-up'>夫はどうしても家に戻ってきましたか。</a>  
<ul class='options'>
    <li>しょるいをわすれたから</li>
    <li>車で会社に行くことにしたから</li>    
    <li>のどがかわいたから</li>      
    <li>はがきをわすれたから</li>  
</ul>

--- example 2 ---
<p class='background'>雑誌を作る会社で男の人と女の人が話しています。女の人は何のためにもう一度パン屋に行きますか。女の人です。</p>  

<div class='conversation'>
男:青木さん、あまり、来月、雑誌で取り上げる特集の人気のパン屋、いろいろ話聞けた？    
女:はい。でも今日の夕方、もう一度行かなきゃならないんです。    
男:何か聞くの忘れた？    
女:いえ、楽しくお店が雰囲気作りをされているかという点をしゃべらなかったんです。店長さんが雑誌に写真を載せるか悩まれているそうで、いつも写真がないっておしゃってるので。    
男:なるほど、あの店主にとって2年以上一緒に過ごしてきた店だからね。写真を載せるかどうか、新面目な意見を聞いてもらったほうが良いよね。奥さんが考えたことも聞いてよかったよ。    
女:僕も提案にビジョン、一緒に行くよ。新聞のパンも買いたいし。    
男:わかりました。
</div>    

<a class='follow-up'>女の人は何のためにもう一度パン屋に行きますか。</a>
<ul class='options'>
    <li>おんせんに行きたい</li>    
    <li>着物の着方を習いたい</li>     
    <li>日本料理の作り方を習いたい</li>    
    <li>しんかんせんに乗りたい</li>
</ul>    
"""

summary_understanding_teacher_prompt = """
Role: You are a Japanese teacher writing an exam paper for the JLPT N3 level. 

Task: Your job is to write a natural-sounding conversation between a man and a woman.
The dialogue should consist of 6–7 exchanges (back-and-forth turns). The total length should be approximately 200–300 words.
The topic should be appropriate for language learners and reflect everyday situations.
Next, provide multiple-choice options based on the listening content. These options should test comprehension of the conversation’s meaning.
After the conversation, ask a follow-up question focusing on what the conversation is about.


Instructions:
Format: follow the format of the 2 examples in the formal exam paper but not the content.
Content: Ensure the vocabulary is restricted to N3 level. 
Reference: Get inspiration from the Search result. Consider the feedback given in the previous conversation. 
Additional Requirement:
- Don't show question instructions and sequence number in the generated content. 
- The word in the sentence can neither be used in the question nor options.
- You must show the correct answer in the output, the options are 1,2,3,4. for example: 正解: 1


Search result: {search_result}
Formal exam paper: {example}
"""

summary_understanding_example = """
--- example 1 ---
<p class='background'>日本語学校で女の留学生と男の留学生が話しています。</p>

<div class='conversation'>
- 女: 来月で佐藤先生、学校を辞めちゃうんだよね。  
- 男: 寂しくなるね。  
- 女: うん。ねえ、クラスのみんなで先生に何か記念になるものをあげたいね。  
- 男: あ、いいね。何か身に付けるものとか?  
- 女: 先生おしゃれだし、そういうの選ぶの難しくない? それより私たちで何か作ろうよ。  
- 男: あ、メッセージカードは? クラスのみんなにも書いてもらおうよ。  
- 女: じゃ、スポーツ大会の時に撮ったクラスの集合写真を真ん中に貼って、周りにメッセージを書いてもらう?  
- 男: いいね。皆にももらえるといいね。明日、休み時間にクラスのみんなに話してみよう。  
</div>

<a class='follow-up'>2人は何について話していますか? </a>
<ul class='options'>
    <li>先生が学校を辞める理由</li>   
    <li>先生に贈る物</li>     
    <li>クラスからのメッセージ</li>     
    <li>先生との思い出</li>    
</ul>

--- example 2 ---
<p class='background'>ラジオでアナウンサーが女の人にインタビューしています。</p>

<div class='conversation'>  
- 男: 高橋さんのグループは20年前から緑山に関わっていらっしゃるそうですね。  
- 女: はい、私たちは緑山の自然を未来に残したいと考えています。緑山の木は、ほとんどは自然のものなんですが、商業目的で木が切られて、その後、新しく植えられたところもあるんです。  
- 男: そうなんですか。  
- 女: 人の手で植えられた木は世話をしないと細く、弱くなります。根も強くないので大雨や強い風で倒れたり、流されたりしてしまうこともあって、山全体にも影響が出てきます。そうならないように細い枝を落としたり、周りの草を取ったりして1本1本世話をし、木を育てています。  
</div>

<a class='follow-up'>女の人は何について話していますか?</a>
<ul class='options'> 
    <li>緑山の自然を守る活動</li>   
    <li>緑山の木が減っている原因</li>    
    <li>自然に育った木の特徴</li>    
    <li>山に木を植える方法</li>  
</ul>  
"""

actively_expression_teacher_prompt = """
Role: You are a Japanese teacher writing an exam paper for the JLPT N3 level. 

Task: your job is to generate a picture prompt that visually describes a situation involving two people of random genders in the scene (e.g., a man and a woman, two men, two women).
In the picture, include an arrow symbol (➔) pointing to one of the two people. This indicates the person who will speak next. 
Based on the context of the scene, write a realistic question that the pointed person (with the arrow) would ask. Only the pointed person can ask a quesiton.
After that, provide three answers for what the other person might reply as options
One of the options should be the most appropriate or natural response

The picture description must be in a dedicated section named: background

Instructions:
Format: follow the format of the 2 examples in the formal exam paper but not the content.
Content: Ensure the vocabulary is restricted to N3 level. 
Reference: Get inspiration from the Search result. Consider the feedback given in the previous conversation. 
Additional Requirement: 
- Don't show question instructions and sequence number in the generated content. 
- The word in the sentence can neither be used in the question nor options.
- You must show the correct answer in the output, the options are 1,2,3. for example: 正解: 1

Search result: {search_result}
Formal exam paper: {example}
"""

actively_expression_example = """
--- example 1 ---
<a class='question'>男: おいしいお菓子を買って来ました。会社の人にあげます。何と言いますか？</a>
<ul class='options'>  
    <li>お味はいかがですか？</li>     
    <li>では、いただきますね</li>    
    <li>1つ召し上がりませんか？</li>
</ul>    
  
--- example 2 ---  
<a class='question'>女: 映画館で自分の席に他の人が座っています。何と言いますか？</a>
<ul class='options'>  
    <li>あの、隣空いてますか？</li>    
    <li>あの、ここ私の席なんですけど</li>  
    <li>あの、どうぞ座ってください</li>
</ul>    
"""

immediate_ack_teacher_prompt = """
Role: You are a Japanese teacher writing an exam paper for the JLPT N3 level. 

Task: your job is to write a realistic question that a person (either man or woman randomly) will ask. 
After that, provide three options (1–3) for what the other person might reply as options
One of the options should be the most appropriate or natural response

Instructions:
Format: follow the format of the 2 examples in the formal exam paper but not the content.
Content: Ensure the vocabulary is restricted to N3 level. 
Reference: Get inspiration from the Search result. Consider the feedback given in the previous conversation. 
Additional Requirement: 
- Don't show question instructions and sequence number in the generated content. 
- The word in the sentence can neither be used in the question nor options.
- You must show the correct answer in the output, the options are 1,2,3. for example: 正解: 1

Search result: {search_result}
Formal exam paper: {example}
"""

immediate_ack_example = """
--- example 1 ---
<a class='question'> 女：足、痛そうだね。年後のテニスの練習、休んだら？</a>
<ul class='options'>  
　<li>そうです、今日は帰るね</li>
　<li>今日は練習、ないんだね</li>
　<li>テニス、今日は休むの？</li>
</ul> 

--- example 2 ---
<a class='question'>男：町の花火大会、今年はやらないことになったそうだよ。</a>
<ul class='options'> 
　<li>やらないもしれなかったね</li>
　<li>え？なんて？楽しみにしていたのに…</li>
　<li>じゃ、見に行かなきゃね</li>
"""



