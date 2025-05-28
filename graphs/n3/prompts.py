kanji_reading_teacher_prompt = """
Role: You are a Japanese teacher.

Task: your job is to write a kanji question for the JLPT N3 exam.
Your job is to provide a kanji vocabulary word in a short sentence and ask the candidate to choose the correct kana reading. 
The word being tested needs to be underlined with <u></u>, no other tags can appear in the sentence.
give the correct answer number in 1,2,3,4

Instructions:
Format: tightly follow the format of 8 examples in the formal exam paper. The output must be in html format and remove line change tag.
Content: Ensure the vocabulary is restricted to N3 level. Use the vocabulary in the `Dictionary` as much as possible.
Reference: Get inspiration from the Search result. Consider the feedback given in the previous conversation.
Additional Requirement: Don't show question instructions and question sequence number in the generated content. 

Search result: {search_result}
Formal exam paper: {example}
"""

kanji_reading_example = """
    <ul>
        <li>
            山田さんがちらしを<u>配った</u>。
            <ul>
                <li>ひろった</li>
                <li>くばった</li>
                <li>やぶった</li>
                <li>はった</li>
            </ul>
        </li>
        <li>
            私の国は<u>石油</u>を輸入しています。
            <ul>
                <li>いしゅ</li>
                <li>せきう</li>
                <li>せきゆ</li>
                <li>いしう</li>
            </ul>
        </li>
        <li>
            卒業式には生徒の<u>父母</u>もたくさん来ていた。
            <ul>
                <li>ふば</li>
                <li>ふぼ</li>
                <li>ふうぼ</li>
                <li>ふうば</li>
            </ul>
        </li>
        <li>
            この町の<u>主要</u>な産業は何ですか。
            <ul>
                <li>じゅおう</li>
                <li>しゅおう</li>
                <li>じゅうよう</li>
                <li>しゅよう</li>
            </ul>
        </li>
        <li>
            これは<u>加熱</u>して食べてください。
            <ul>
                <li>ねつねつ</li>
                <li>かあつ</li>
                <li>かいねつ</li>
                <li>かねつ</li>
            </ul>
        </li>
        <li>
            川はあの<u>辺り</u>で<u>深く</u>なっている。
            <ul>
                <li>ふかく</li>
                <li>あさく</li>
                <li>ひろく</li>
                <li>せまく</li>
            </ul>
        </li>
        <li>
            文句を言われたので、つい<u>感情的</u>になってしまった。
            <ul>
                <li>がんじょうてき</li>
                <li>かんしょうてき</li>
                <li>かんじょうてき</li>
                <li>がんしょうてき</li>
            </ul>
        </li>
        <li>
            これは<u>残さない</u>でください。
            <ul>
                <li>なくさないで</li>
                <li>よごさないで</li>
                <li>こぼさないで</li>
                <li>のこさないで</li>
            </ul>
        </li>
    </ul>
```
"""

write_chinese_teacher_prompt = """
Role: You are a Japanese teacher. 

Task: Your job is to write a word meaning question for a JLPT N3 level exam paper.
You should write a short sentence and ask candidate to identify the correct kanji writing of a given word in hiragana.
The word being tested needs to be underlined with <u></u>, no other tags can appear in the sentence.
give the correct answer number in 1,2,3,4

Instructions:
Format: tightly follow the format of 6 examples in the formal exam paper. The output must be in html format and remove line change tag.
Content: Ensure the vocabulary is restricted to N3 level. Use the vocabulary in the `Dictionary` as much as possible.
Reference: Get inspiration from the Search result. Consider the feedback given in the previous conversation. 
Additional Requirement: Don't show question instructions and question sequence number in the generated content.


Search result: {search_result}
Formal exam paper: {example}
"""

write_chinese_example = """
<ul>
  <li>ここから<u>じゅんばん</u>に見てください。
    <ul>
      <li>順番</li>
      <li>項番</li>
      <li>順審</li>
      <li>項審</li>
    </ul>
  </li>

  <li>父は銀行に<u>つとめて</u>います。
    <ul>
      <li>勤めて</li>
      <li>働めて</li>
      <li>仕めて</li>
      <li>労めて</li>
    </ul>
  </li>

  <li>ポケットが<u>さゆう</u>にあるんですね。
    <ul>
      <li>裏表</li>
      <li>右左</li>
      <li>表裏</li>
      <li>左右</li>
    </ul>
  </li>

  <li>昨日の試合は<u>まけて</u>しまいました。
    <ul>
      <li>退けて</li>
      <li>負けて</li>
      <li>失けて</li>
      <li>欠けて</li>
    </ul>
  </li>

  <li><u>かこの</u>例も調べてみましょう。
    <ul>
      <li>適去</li>
      <li>過古</li>
      <li>過去</li>
      <li>適古</li>
    </ul>
  </li>

  <li>この資料はページが<u>ぎゃく</u>になっていますよ。
    <ul>
      <li>達</li>
      <li>変</li>
      <li>逆</li>
      <li>別</li>
    </ul>
  </li>
</ul>
"""

word_meaning_teacher_prompt = """
Role: You are a Japanese teacher. 

Task: Your job is to write a vocabulary question for candidates to identify the correct kanji writing of a given word in hiragana for a JLPT N3 level exam paper.
Each question presents a word in hiragana within a sentence, and candidates must choose the correct kanji representation from four options. 
The options should include one correct kanji form and three distractors that are plausible but incorrect. The pseudonym of the selected word does not need to be given in the question type. The question type of word meaning selection mainly tests the form of multiple-choice questions, requiring candidates to select the most suitable words from the options based on the context of the sentence or passage. The question type should be left blank in the sentence or dialogue, requiring the selection of semantically and grammatically appropriate words from the options.

Instructions:
Format: Follow the format of formal exam papers.
Content: Ensure the vocabulary is restricted to N3 level. Use the vocabulary in the `Dictionary` as much as possible.
Reference: Get inspiration from the Search result. Only use the format as a reference; do not use any specific content from existing exams.

Additional Requirement: Don't show question instructions and question sequence number in the generated content.


Search result: {search_result}
Formal exam paper: {example}
"""

word_meaning_example = """
大雪で朝から電車が（　）している。
    1.  縮小
    2.  滞在
    3.  延期
    4.  運休

今日は暑かったので、シャツが（　）でぬれてしまった。
    1.  いびき
    2.  あくび
    3.  あせ
    4.  いき

答えさんに声がよく聞こえるように、（　）を使って話してください。
    1.  サイレン
    2.  エンジン
    3.  ノック
    4.  マイク

昨日は早く寝たが、夜中に大きな音がして目が（　）しまった。
    1.  嫌がって
    2.  覚めて
    3.  驚いて
    4.  怖がって

林さんはいつも冗談ばかり言うので、その話も本当かどうか（　）。
    1.  あやしい
    2.  おそろしい
    3.  にくらしい
    4.  まずしい

本日の面接の結果は、1 週間以内にメールで（　）します。
    1.  広告
    2.  合図
    3.  通知
    4.  伝言

兄はいつも（　）シャツを着ているので、遠くにいてもすぐに見つかる。
    1.  派手な
    2.  盛んな
    3.  わがままな
    4.  身近な

ここに車を止めることは規則で（　）されていますから、すぐに移動してください。
    1.  支配
    2.  英殺
    3.  禁止
    4.  批判

このコートは古いがまだ着られるので、捨ててしまうのは（　）。
    1.  もったいない
    2.  しかたない
    3.  かわいらしい
    4.  こいかない

弟への誕生日プレゼントは、誕生日まで弟に見つからないように、たんすの奥に（　）。
    1.  包んだ
    2.  隠した
    3.  囲んだ
    4.  閉じた

山口さんは今度のパーティーには来られないかもしれないが、（　）誘うつもりだ。
    1.  十分
    2.  一応
    3.  けっこう
    4.  たいてい
"""

synonym_substitution_teacher_prompt = """
Role: You are a Japanese teacher.

Task: Your job is to write a synonym question for candidates to identify the most appropriate word with a similar meaning in a JLPT N3 level exam paper. 
Each question presents a word in kanji or katakana within a sentence.
The options should include one correct synonym and three distractors that are plausible. The synonyms that need to be replaced should be indicated with underscores.

Instructions:
Format: Follow the format of formal exam papers.
Content: Ensure the vocabulary is restricted to N3 level. Use the vocabulary in the `Dictionary` as much as possible.
Reference: Get inspiration from the Search result. Only use the format as a reference; do not use any specific content from existing exams.

Additional Requirement: Don't show question instructions and question sequence number in the generated content.


Search result: {search_result}
Formal exam paper: {example}
"""

synonym_substitution_example = """
さん、避難してください。
    1.  ならんで
    2.  入って
    3.  にげて
    4.  急いで

来週、ここで企業の説明会があります。
    1.  旅行
    2.  会社
    3.  大学
    4.  建物

ちょっとバックしてください。
    1.  前に進んで
    2.  後ろに下がって
    3.  横に動いて
    4.  そこで止まって

このやり方がベストだ。
    1.  最もよい
    2.  最もよくない
    3.  最も難しい
    4.  最も難しくない

田中さんがようやく来てくれました。
    1.  笑に
    2.  すぐに
    3.  やっと
    4.  初めて
"""

word_usage_teacher_prompt = """
Role: You are a Japanese teacher. 

Task: Your job is to write a word usage question for candidates, examining the usage of words in actual contexts.
request candidates to select the most appropriate context, includes Japanese idiomatic expressions and fixed collocations.
The words to be examined need to be underlined in each sentence.

Instructions:
Format: Follow the format of formal exam papers.
Content: Ensure the vocabulary is restricted to N3 level. Use the vocabulary in the `Dictionary` as much as possible.
Reference: Get inspiration from the Search result. Only use the format as a reference; do not use any specific content from existing exams.

Additional Requirement: Don't show question instructions and question sequence number in the generated content.


Search result: {search_result}
Formal exam paper: {example}
"""

word_usage_example = """
内容
    1.  修理のため、エアコンの内容を一度取り出します
    2.  鍋の中にカレーの内容を入れて、1時間くらい煮てください
    3.  古い財布から新しい財布へ内容を移しました
    4.  この手紙の内容は、ほかの人には秘密にしてください

活動
    1.  彼は有名なロック歌手だったが、今は活動していない
    2.  山に登ると、新鮮な空気が活動していて気持ちがいい
    3.  さっきまで活動していたパソコンが、急に動かなくなった
    4.  駅前のコンビニは24時間活動しているので便利だ

落ち着く
    1.  この辺りは、冬になると雪が落ち着いて、春になるまで溶けません
    2.  シャツにしみが落ち着いてしまって、洗ってもきれいになりません
    3.  あそこの木の上に美しい鳥が落ち着いています
    4.  大好きなこの曲を聞くと、いつも気持ちが落ち着きます

ぐっすり
    1.  遠慮しないで、ぐっすり食べてください
    2.  優勝できたのは、毎日ぐっすり練習したからだと思う
    3.  今日は疲れているので、朝までぐっすり眠れそうだ
    4.  古い友人と久しぶりに会って、ぐっすりおしゃべりした

性格
    1.  日本の古い性格に興味があるので、神社やお寺によく行きます
    2.  森さんはおとなしい性格で、自分の意見はあまり言いません
    3.  値段が高くても、塗装で性格のいい車を買うつもりです
    4.  音楽の性格を伸ばすために、5歳から専門家の指導を受けました
"""

sentence_grammar_teacher_prompt = """
Role: You are a Japanese teacher. 

Task: Your job is to provide a sentence with a blank space and ask the candidate to fill in the most appropriate grammatical structure.

Instructions:
Format: Follow the format of formal exam papers.
Content: Ensure the vocabulary is restricted to N3 level. Use the vocabulary in the `Dictionary` as much as possible.
Reference: Get inspiration from the Search result. Only use the format as a reference; do not use any specific content from existing exams.

Additional Requirement: Don't show question instructions and question sequence number in the generated content.


Search result: {search_result}
Formal exam paper: {example}
"""

sentence_grammar_example = """
私は、自分の作ったパンを多くたくさんの人（　）食べてほしいと思って、パン屋を始めた。
    1.  は
    2.  に
    3.  まで
    4.  なら

---
（学校にて）

学生：「先生、今、よろしいですか。英語の発表（　）、ちょっと相談したいのですが。」
先生：「ええ、いいですよ。」
    1.  にとって
    2.  によると
    3.  のことで
    4.  のは

---

いつもは勉強を2時間以上かかるが、今日は1時間（　）終わりそうだ。
    1.  くらい
    2.  ころで
    3.  ぐらい
    4.  ぐらいで

---

母：「えっ、（　）ご飯食べたばかりなのに、もうおなかすいたの？」
    1.  そろそろ
    2.  だんだん
    3.  さっき
    4.  ずっと

---

大事なレシートをズボンのポケットに（　）洗濯してしまった。
    1.  入れたまま
    2.  入ったまま
    3.  入れている間
    4.  入っている間

---
（駅のホームにて）

「急げ、9時の特急に間に合うかもしれないし、走ろうか。」
「いや、（　）もう間に合わないと思う。次の電車にしよう。」
    1.  走ってて
    2.  走ってるよ
    3.  走らさきゃ
    4.  走っちゃって

---

私はよくインターネットで物を買い替えるが、掃除機は壊れたら、実際に（　）買いたいものだ。
    1.  見てないと
    2.  見ておきたくなった
    3.  見てから
    4.  見ておいて

---
（料亭にて）

（体を丸めてお辞儀をして）「おいしそうな料理ですね。」
店員：「どうぞたくさん（　）ください。」
    1.  召し上がって
    2.  おっしゃって
    3.  なおって
    4.  いらっし

---

A：「最近、寒くなって（　）ね。」
B：「ええ、今日は特に冷えますね。」
    1.  いました
    2.  ありました
    3.  いきました
    4.  きました

---
（大学にて）

A：「日曜日の留学生交流会、どうだった？」
B：「楽しかったよ。初めてだったからちょっと緊張したけど、新しい友達もできたし。」
    1.  行ってよかったよ
    2.  行こうかと思うよ
    3.  行きたかったなあ
    4.  行けたらいいなあ

---
（大学の事務所で）

学生：「すみません、ペンを（　）。」
事務所の人：「あ、はい、これを使ってください。」
    1.  お貸しできますか
    2.  お貸しいたしますか
    3.  貸したらいかがですか
    4.  貸していただけませんか

---
（家にて）

娘：「ちょっと駅前の本屋に行ってくるね。」
父：「雨が降っているし、車で（　）？」
娘：「いいの？ありがとう。」
    1.  送っててない
    2.  送ってこようか
    3.  送ってあげない
    4.  送ってあげようか

---
（会社にて）

「中山さん、今、ちょっといいですか。」
中山：「あ、ごめんなさい、これからABC銀行に（　）、戻ってきてからでもいいですか。」
    1.  行くところだからです
    2.  行くとこなんです
    3.  行っているところだからです
    4.  行っているところなんです
"""

sentence_sort_teacher_prompt = """
Role: You are a Japanese teacher. 

Task: Your job is to provide a sentence sorting question that requires selecting the correct arrangement order.
Ask candidate to choose the correct option from the following 4 options.

Instructions:
Format: Follow the format of formal exam papers.
Content: Ensure the vocabulary is restricted to N3 level. Use the vocabulary in the `Dictionary` as much as possible.
Reference: Get inspiration from the Search result. Only use the format as a reference; do not use any specific content from existing exams.
Explanation: Append the correct answer and an explanation of the main challengesfor the question from Japanese teacher's pespective.
Additional Requirement: Don't show question instructions and question sequence number in the generated content.


Search result: {search_result}
Formal exam paper: {example}
"""

sentence_sort_example = """
山川大学では、__★_ 新入生がにアンケート調査を行っている。
    1.  大学生活
    2.  持っている
    3.  に対して
    4.  イメージ

来週の夫の誕生日には、__★_ つもりだ。
    1.  最近
    2.  プレゼントする
    3.  かばんを
    4.  欲しがっている

私は、健康の__★_。
    1.  している
    2.  ために
    3.  毎日8時間以上寝る
    4.  ように

部長が__★_ クッキーがとてもおいしいので、私も東京に行くことがあったら、買おうと思う。
    1.  たびに
    2.  ために
    3.  お土産の
    4.  ように

私はこの図書館が好きだ。広くて本の数が多い __★_ いい。
    1.  景色を楽しみながら
    2.  大きな窓から街が見えて
    3.  だけでなく
    4.  読書ができるのも
"""

structure_selection_teacher_prompt = """
Role: You are a Japanese teacher. 

Task: Your job is to write a paper for JLPT N3 level. 
At this section, please write a Japanese article about 300-400 words with 4-5 lines written with markdown. 
After that, you should give 4 related questions from the content of the article. 
The purpose is to also test candidate the ability to identify Japanese sentence structure. 
Candidate should fill in the gaps in the article by choosing the grammar structure that best fits the context from the following 4 options, 

Instructions:
Format: Follow the format of formal exam papers. Each question has 4 options in Japanese
Content: Ensure the vocabulary is restricted to N3 level. Use the vocabulary in the `Dictionary` as much as possible.
Reference: Get inspiration from the Search result. Only use the format as a reference; do not use any specific content from existing exams.
Explanation: give the correct answer and an explanation of the main challenges for the question from Japanese teacher's pespective.
Additional Requirement: Don't show question instructions and question sequence number and revised submission in the generated content.


Search result: {search_result}
Formal exam paper: {example}
"""

structure_selection_example = """
夏休みの思い出  

お母さん、中学生の妹さんと住んでいます。[19] 日本人の家に泊まるのは初めてだったので、行く前は少し不安な気持ちもありました。[20] 行ってみたらとても楽しかったです。  

印象に残っているのは、巡りの畑で育てた野菜を使って、みんなで料理を作ったことです。友達のお母さんは、畑でいろいろな野菜を育てていました。私たちは、その野菜を使ってみんなで料理をしました。私は、お店に売られている野菜 [21] 食べたことがありませんでした。家で育てた野菜を食べたのは初めてでしたが、とてもおいしかったです。特に「私も野菜を育ててみたい」と、胸がいっぱ言う行ってらない。」と言ったら、それを聞いていたお母さんが、家の中でも育てることができる野菜について教えてくれました。  

お母さんに教えてもらったやり方で、私も野菜を [22]。今、２種類の野菜を育てています。  

野菜の世話をしながら、楽しかった夏休みのことをいつも思い出しています。  

--- 

1. 招待してくれたのです    
2. 招待してくれたはずです    
3. 招待してくれたばかりです    
4. 招待してくれたそうです    

1. それで    
2. でも    
3. 実は    
4. また    

1. は    
2. などを    
3. しか    
4. だけ    

1. 育ててみてほしいです    
2. 育ててみてもいいです    
3. 育ててみようとしました    
4. 育ててみることにしました     
"""

short_reading_teacher_prompt = """
Role: You are a Japanese teacher. 

Task: Your job is to write a question for candidate to read a short article around 200 words.
The article is composed as 5-6 lines, you must split lines. Then, you give a question from the related content of the article.
The content is specific for emails Notification and letter articles.

Instructions:
Format: Follow the format of formal exam papers. Don't show sequence number of the questions.
Content: Ensure the vocabulary is restricted to N3 level. Use the vocabulary in the `Dictionary` as much as possible.
Reference: Get inspiration from the Search result. Only use the format as a reference; do not use any specific content from existing exams.
Explanation: Append the correct answer and an explanation of the main challengesfor the question from Japanese teacher's pespective.
Additional Requirement: Don't show question instructions and question sequence number and revised submission in the generated content.


Search result: {search_result}
Formal exam paper: {example}
"""

short_reading_example = """
---

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

25. このメモを読んで、ミンさんはまず何をしなければならないか。
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
これは、今川さんが後のミゲルさんに書いたメールである。

ミゲルさん

メールをありがとう。

同じ会社で働くことになって、うれしいです。

住む所についてアドバイスをくださいと書いてあったので、お答えします。

会社まで歩いて行きたいと書いてありましたが、会社の周りはオフィスばかりで、アパートはほとんどありません。電車通勤になりますが、私が以前住んでいた緑野という町はいいですよ。

緑野駅から会社のある北駅まで電車で15分だし、いろいろなお店があって便利です。

いい所が見つかるといいですね。会えるのを楽しみにしています。

今川

まで電車で15分で行けるし、店も多いので、緑野にしたらどうか。
    1.  (選択肢なし)
    2.  いろいろな店があって便利なので、北園駅の近くにしたらどうか
    3.  北駅まで電車で15分で行けるし、店も多いので、緑野にしたらどうか
    4.  いろいろな店があって便利なので、北園駅の近くにしたらどうか

---

友達のマキは、いいことがあったという話をよくする。だから私は、マキは運がいいのだと思っていた。しかし、最近、そうではないと気づいた。

先日二人で出かけたとき、事故で電車が止まっていて、何キロも歩いて帰ることになった。嫌だなと思っている私に、マキは「知らない町を歩けるね。」と嬉しそうに言った。とても不思議だった。でも、マキは楽しめてしまうのだ。今まで私が聞いた話も、マキだから「いいこと」だと感じたのだろうと思う。

最近、「私」はマキのことをどのような人だと思うようになったか。
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

information_retrieval_teacher_prompt = """
Role: You are a Japanese teacher. 

Task: You are a japanese teacher. Your job is to write a Japanese article for candidate to retrieve information. 
you must provide a markdown format table and clues related to the table. The content cannot be same as the Formal exam paper
The content includes searching for advertisements, notifications, schedules.
After the article, asking candidate to answer 2 questions from the related content of the article. 

Instructions:
Format: Follow the format of formal exam papers. Each question has 4 options in Japanese
Content: Ensure the vocabulary is restricted to N3 level. Use the vocabulary in the `Dictionary` as much as possible.
Reference: Get inspiration from the Search result. Only use the format as a reference; do not use any specific content from existing exams.

Additional Requirement: Don't show question instructions and question sequence number and revised submission in the generated content.


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



