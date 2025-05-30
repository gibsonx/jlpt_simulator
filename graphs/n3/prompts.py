kanji_reading_teacher_prompt = """
Role: You are a Japanese teacher.

Task: your job is to write a kanji question for the JLPT N3 exam. 
Your job is to provide a kanji vocabulary word and ask the candidate to choose the correct kana reading. The word being tested needs to be underlined.

Instructions:
Format: Follow the format of formal exam papers.
Content: Ensure the vocabulary is restricted to N3 level. Use the vocabulary in the `Dictionary` as much as possible.
Reference: Get inspiration from the Search result. Only use the format as a reference; do not use any specific content from existing exams.
Explanation: Append the correct answer and an explanation of the main challenges for the question from Japanese teacher's pespective.
Additional Requirement: Don't show question requirement and question sequence in the generated content.


Search result: {search_result}
Formal exam paper: {example}
"""

kanji_reading_example = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>日本語 読み方テスト</title>
</head>
<body>
    <h2>問題１　<u>のことばの読み方</u>として最もよいものを、１・２・３・４から一つえらびなさい。</h2>

    <ol>
        <li>
            山田さんがちらしを<u>配った</u>。
            <ol type="1">
                <li>ひろった</li>
                <li>くばった</li>
                <li>やぶった</li>
                <li>はった</li>
            </ol>
        </li>
        <li>
            私の国は<u>石油</u>を輸入しています。
            <ol type="1">
                <li>いしゅ</li>
                <li>せきう</li>
                <li>せきゆ</li>
                <li>いしう</li>
            </ol>
        </li>
        <li>
            卒業式には生徒の<u>父母</u>もたくさん来ていた。
            <ol type="1">
                <li>ふば</li>
                <li>ふぼ</li>
                <li>ふうぼ</li>
                <li>ふうば</li>
            </ol>
        </li>
        <li>
            この町の<u>主要</u>な産業は何ですか。
            <ol type="1">
                <li>じゅおう</li>
                <li>しゅおう</li>
                <li>じゅうよう</li>
                <li>しゅよう</li>
            </ol>
        </li>
        <li>
            これは<u>加熱</u>して食べてください。
            <ol type="1">
                <li>ねつねつ</li>
                <li>かあつ</li>
                <li>かいねつ</li>
                <li>かねつ</li>
            </ol>
        </li>
        <li>
            川はあの<u>辺り</u>で<u>深く</u>なっている。
            <ol type="1">
                <li>ふかく</li>
                <li>あさく</li>
                <li>ひろく</li>
                <li>せまく</li>
            </ol>
        </li>
        <li>
            文句を言われたので、つい<u>感情的</u>になってしまった。
            <ol type="1">
                <li>がんじょうてき</li>
                <li>かんしょうてき</li>
                <li>かんじょうてき</li>
                <li>がんしょうてき</li>
            </ol>
        </li>
        <li>
            これは<u>残さない</u>でください。
            <ol type="1">
                <li>なくさないで</li>
                <li>よごさないで</li>
                <li>こぼさないで</li>
                <li>のこさないで</li>
            </ol>
        </li>
    </ol>
</body>
</html>

```

Each `<u>` tag wraps the kanji or phrase that is underlined in the image. Let me know if you’d like the correct answers marked or the text translated.

"""

write_chinese_teacher_prompt = """
Role: You are a Japanese teacher. 

Task: Your job is to write a word meaning question for a JLPT N3 level exam paper, asking candidate to identify the correct kanji writing of a given word in hiragana.
Each question contains a word in hiragana in a sentence, and candidates must choose the correct option from 4 options. 
The options should include one correct kanji form and three distractors that are plausible. The word being tested needs to be underlined.

Instructions:
Format: Follow the format of formal exam papers.
Content: Ensure the vocabulary is restricted to N3 level. Use the vocabulary in the `Dictionary` as much as possible.
Reference: Get inspiration from the Search result. Only use the format as a reference; do not use any specific content from existing exams.
Explanation: Append the correct answer and an explanation of the main challenges for the question from Japanese teacher's pespective.
Additional Requirement: Don't show question requirement and question sequence in the generated content.


Search result: {search_result}
Formal exam paper: {example}
"""

write_chinese_example = """
<h2>問題２</h2>
<p>このことばを漢字で書くとき、最もよいものを、１・２・３・４から一つえらびなさい。</p>

<ol start="9">
  <li>ここから<u>じゅんばん</u>に見てください。
    <ol type="1">
      <li>順番</li>
      <li>項番</li>
      <li>順審</li>
      <li>項審</li>
    </ol>
  </li>

  <li>父は銀行に<u>つとめて</u>います。
    <ol type="1">
      <li>勤めて</li>
      <li>働めて</li>
      <li>仕めて</li>
      <li>労めて</li>
    </ol>
  </li>

  <li>ポケットが<u>さゆう</u>にあるんですね。
    <ol type="1">
      <li>裏表</li>
      <li>右左</li>
      <li>表裏</li>
      <li>左右</li>
    </ol>
  </li>

  <li>昨日の試合は<u>まけて</u>しまいました。
    <ol type="1">
      <li>退けて</li>
      <li>負けて</li>
      <li>失けて</li>
      <li>欠けて</li>
    </ol>
  </li>

  <li><u>かこの</u>例も調べてみましょう。
    <ol type="1">
      <li>適去</li>
      <li>過古</li>
      <li>過去</li>
      <li>適古</li>
    </ol>
  </li>

  <li>この資料はページが<u>ぎゃく</u>になっていますよ。
    <ol type="1">
      <li>達</li>
      <li>変</li>
      <li>逆</li>
      <li>別</li>
    </ol>
  </li>
</ol>
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
Explanation: Append the correct answer and an explanation of the main challenges for the question from Japanese teacher's pespective.
Additional Requirement: Don't show question requirement and question sequence in the generated content.


Search result: {search_result}
Formal exam paper: {example}
"""

word_meaning_example = """
<h2>問題３</h2>
<p>（　　　）に入れるのに最もよいものを、１・２・３・４から一つえらびなさい。</p>

<ol start="15">
  <li>大雪で朝から電車が（　）している。
    <ol type="1">
      <li>縮小</li>
      <li>滞在</li>
      <li>延期</li>
      <li>運休</li>
    </ol>
  </li>

  <li>今日は暑かったので、シャツが（　）でぬれてしまった。
    <ol type="1">
      <li>いびき</li>
      <li>あくび</li>
      <li>あせ</li>
      <li>いき</li>
    </ol>
  </li>

  <li>澤さんに声がよく聞こえるように、（　）を使って話してください。
    <ol type="1">
      <li>サイレン</li>
      <li>エンジン</li>
      <li>ノック</li>
      <li>マイク</li>
    </ol>
  </li>

  <li>昨日は早く寝たが、夜中に大きな音で目が（　）しまった。
    <ol type="1">
      <li>嫌がって</li>
      <li>覚めて</li>
      <li>驚いて</li>
      <li>怖がって</li>
    </ol>
  </li>

  <li>林さんはいつも元気ばかり言うので、その話も本当かどうか（　）。
    <ol type="1">
      <li>あやしい</li>
      <li>おそろしい</li>
      <li>にくらしい</li>
      <li>まずい</li>
    </ol>
  </li>

  <li>本日の面接の結果は、1週間以内にメールで（　）します。
    <ol type="1">
      <li>広告</li>
      <li>合図</li>
      <li>通知</li>
      <li>伝言</li>
    </ol>
  </li>

  <li>兄はいつも（　）シャツを着ているので、遠くにいてもすぐに見つかる。
    <ol type="1">
      <li>派手な</li>
      <li>盛んな</li>
      <li>わがままな</li>
      <li>身近な</li>
    </ol>
  </li>

  <li>ここに車を止めることは規則で（　）されていますから、すぐに移動してください。
    <ol type="1">
      <li>支配</li>
      <li>英殺</li>
      <li>禁止</li>
      <li>批判</li>
    </ol>
  </li>

  <li>このコートは古いがまだ着られるので、捨ててしまうのは（　）。
    <ol type="1">
      <li>もったいない</li>
      <li>しかたない</li>
      <li>かわいらしい</li>
      <li>こいしかない</li>
    </ol>
  </li>

  <li>弟への誕生日プレゼントは、誕生日まで弟に見つからないように、たなの奥に（　）。
    <ol type="1">
      <li>包んだ</li>
      <li>隠した</li>
      <li>閉んだ</li>
      <li>開した</li>
    </ol>
  </li>
</ol>
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
Explanation: Append the correct answer and an explanation of the main challenges for the question from Japanese teacher's pespective.
Additional Requirement: Don't show question requirement and question sequence in the generated content.


Search result: {search_result}
Formal exam paper: {example}
"""

synonym_substitution_example = """
<h2>問題４</h2>
<p>に意味が最も近いものを、１・２・３・４から一つえらびなさい。</p>

<ol start="26">
  <li>さん、<u>避難</u>してください。
    <ol type="1">
      <li>ならんで</li>
      <li>入って</li>
      <li>にげて</li>
      <li>急いで</li>
    </ol>
  </li>

  <li>来週、ここで<u>企業</u>の説明会があります。
    <ol type="1">
      <li>旅行</li>
      <li>会社</li>
      <li>大学</li>
      <li>建物</li>
    </ol>
  </li>

  <li>ちょっと<u>バックして</u>ください。
    <ol type="1">
      <li>前に進んで</li>
      <li>後ろに下がって</li>
      <li>横に動いて</li>
      <li>そこで止まって</li>
    </ol>
  </li>

  <li>このやり方が<u>ベスト</u>だ。
    <ol type="1">
      <li>最もよい</li>
      <li>最もよくない</li>
      <li>最も難しい</li>
      <li>最も難しくない</li>
    </ol>
  </li>

  <li>田中さんが<u>ようやく</u>来てくれました。
    <ol type="1">
      <li>楽に</li>
      <li>すぐに</li>
      <li>やっと</li>
      <li>初めて</li>
    </ol>
  </li>
</ol>
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
Explanation: Append the correct answer and an explanation of the main challenges for the question from Japanese teacher's pespective.
Additional Requirement: Don't show question requirement and question sequence in the generated content.


Search result: {search_result}
Formal exam paper: {example}
"""

word_usage_example = """
<h2>問題５</h2>
<p>つぎのことばの使い方として最もよいものを、２・３・４から一つえらびなさい。</p>

<h3>31. 内容</h3>
<ol type="1">
  <li>修理のため、エアコンの<u>内容</u>を一度取り出します</li>
  <li>鍋の中にカレーの<u>内容</u>を入れて、１時間くらい煮てください</li>
  <li>古い財布から新しい財布へ<u>内容</u>を移しました</li>
  <li>この手紙の<u>内容</u>は、ほかの人には秘密にしてください</li>
</ol>

<h3>32. 活動</h3>
<ol type="1">
  <li>彼は有名なロック歌手だったが、今は<u>活動</u>していない</li>
  <li>山に登ると、新鮮な空気が<u>活動</u>していて気持ちがよい</li>
  <li>さっきまで<u>活動</u>していたパソコンが、急に動かなくなった</li>
  <li>駅前のコンビニは24時間<u>活動</u>しているので便利だ</li>
</ol>

<h3>33. 落ち着く</h3>
<ol type="1">
  <li>この辺りは、冬になると雪が<u>落ち着いて</u>、春になるまで溶けません</li>
  <li>シャツにしみが<u>落ち着いて</u>しまって、洗ってもきれいになりません</li>
  <li>あそこの木の上に美しい鳥が<u>落ち着いて</u>います</li>
  <li>大好きなこの曲を聞くと、いつも気持ちが<u>落ち着き</u>ます</li>
</ol>
"""

sentence_grammar_teacher_prompt = """
Role: You are a Japanese teacher. 

Task: Your job is to provide a sentence with a blank space and ask the candidate to fill in the most appropriate grammatical structure.

Instructions:
Format: Follow the format of formal exam papers.
Content: Ensure the vocabulary is restricted to N3 level. Use the vocabulary in the `Dictionary` as much as possible.
Reference: Get inspiration from the Search result. Only use the format as a reference; do not use any specific content from existing exams.
Explanation: Append the correct answer and an explanation of the main challenges for the question from Japanese teacher's pespective.
Additional Requirement: Don't show question requirement and question sequence in the generated content.


Search result: {search_result}
Formal exam paper: {example}
"""

sentence_grammar_example = """
<h2>問題１</h2>
<p>つぎの文の（　　　）に入れるのに最もよいものを、１・２・３・４から一つえらびなさい。</p>

<ol>
  <li>
    私は、自分の作ったパンをたくさんの人（　　　）食べてほしいと思って、パン屋を始めた。
    <ol type="1">
      <li>は</li>
      <li>に</li>
      <li>まで</li>
      <li>なら</li>
    </ol>
  </li>

  <li>
    （研究室で）<br>
    学生「先生、今、よろしいですか。来週の発表（　　　）、ちょっとご相談したいのですが。」<br>
    先生「ええ、いいですよ。」
    <ol type="1">
      <li>にとって</li>
      <li>によると</li>
      <li>のことで</li>
      <li>のほか</li>
    </ol>
  </li>

  <li>
    いつもは宿題に２時間以上かかるが、今日は１時間（　　　）終わりそうだ。
    <ol type="1">
      <li>ごろに</li>
      <li>ごろで</li>
      <li>ぐらいに</li>
      <li>ぐらいで</li>
    </ol>
  </li>

  <li>
    兄「ねえ、お母さん、おなかすいた。」<br>
    母「えっ、（　　　）ご飯食べたばかりなのに、もうおなかすいたの？」
    <ol type="1">
      <li>そろそろ</li>
      <li>だんだん</li>
      <li>さっき</li>
      <li>ずっと</li>
    </ol>
  </li>

  <li>
    大事なレシートをズボンのポケットに（　　　）洗濯してしまった。
    <ol type="1">
      <li>入れたまま</li>
      <li>入ったまま</li>
      <li>入れている間</li>
      <li>入っている間</li>
    </ol>
  </li>

  <li>
    （駅の近くで）A「急げば、９時の電車に間に合うかもしれないよ。走ろうか。」<br>
    B「いや、（　　　）もう間に合わないと思うよ。次の電車にしよう。」
    <ol type="1">
      <li>走ってて</li>
      <li>走ったって</li>
      <li>走らなきゃ</li>
      <li>走っちゃって</li>
    </ol>
  </li>

  <li>
    私はよくインターネットで買い物をするが、洋服は買わない。実際に（　　　）買いたいからだ。
    <ol type="1">
      <li>着てみないと</li>
      <li>着ておかないと</li>
      <li>着てみてから</li>
      <li>着ておいて</li>
    </ol>
  </li>
</ol>
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
Additional Requirement: Don't show question requirement and question sequence in the generated content.


Search result: {search_result}
Formal exam paper: {example}
"""

sentence_sort_example = """
<h2>問題２</h2>
<p>つぎの文の ★ に入る最もよいものを、１・２・３・４から一つえらびなさい。</p>
<ol start="14">
  <li>
    山川大学では、<u>＿＿</u> <u>＿＿</u> ★ <u>＿＿</u> <u>＿＿</u> 新入生がにアンケート調査を行っている。
    <ol type="1">
      <li>大学生活</li>
      <li>持っている</li>
      <li>に対して</li>
      <li>イメージ</li>
    </ol>
  </li>

  <li>
    来週の夫の誕生日には、<u>＿＿</u> <u>＿＿</u> ★ <u>＿＿</u> <u>＿＿</u> つもりだ。
    <ol type="1">
      <li>最近</li>
      <li>プレゼントする</li>
      <li>かばんを</li>
      <li>欲しがっている</li>
    </ol>
  </li>

  <li>
    私は、健康の<u>＿＿</u> <u>＿＿</u> ★ <u>＿＿</u> <u>＿＿</u>。
    <ol type="1">
      <li>している</li>
      <li>ために</li>
      <li>毎日８時間以上寝る</li>
      <li>ように</li>
    </ol>
  </li>
</ol>
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
Additional Requirement: Don't show question requirement and question sequence and revised submission in the generated content.


Search result: {search_result}
Formal exam paper: {example}
"""

structure_selection_example = """
<h2>問題３</h2>
<p>
つぎの文章を読んで、文章全体の内容を考えて、
文中の <strong>19</strong> から <strong>22</strong> の中に入る最もよいものを、
１・２・３・４から一つえらびなさい。
</p>

<hr>

<p>以下は、留学生の作文である。</p>

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

<!DOCTYPE html>  
<html lang="en">  
<head>  
    <meta charset="UTF-8">  
    <meta name="viewport" content="width=device-width, initial-scale=1.0">  
    <title>Questions</title>  
</head>  
<body>  
    <h1>Questions</h1>  
  
    <h2>19.</h2>  
    <ol>  
        <li>招待してくれたのです</li>  
        <li>招待してくれたはずです</li>  
        <li>招待してくれたばかりです</li>  
        <li>招待してくれたそうです</li>  
    </ol>  
  
    <h2>20.</h2>  
    <ol>  
        <li>それで</li>  
        <li>でも</li>  
        <li>実は</li>  
        <li>また</li>  
    </ol>  
  
    <h2>21.</h2>  
    <ol>  
        <li>は</li>  
        <li>などを</li>  
        <li>しか</li>  
        <li>だけ</li>  
    </ol>  
  
    <h2>22.</h2>  
    <ol>  
        <li>育ててみてほしいです</li>  
        <li>育ててみてもいいです</li>  
        <li>育ててみようとしました</li>  
        <li>育ててみることにしました</li>  
    </ol>  
</body>  
</html>  
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
Additional Requirement: Don't show question requirement and question sequence and revised submission in the generated content.


Search result: {search_result}
Formal exam paper: {example}
"""

short_reading_example = """
<!DOCTYPE html>  
<html lang="ja">  
<head>  
    <meta charset="UTF-8">  
    <meta name="viewport" content="width=device-width, initial-scale=1.0">  
    <title>問題4</title>  
</head>  
<body>  
    <h1>問題4</h1>  
    <p>つぎの(1)から(4)の文章を読んで、質問に答えなさい。答えは、1・2・3・4から最もよいものを一つえらびなさい。</p>  
  
    <h2>(1)</h2>  
    <p>これは、今川さんが後のミゲルさんに書いたメールである。</p>  
      
    <p><strong>ミゲルさん</strong></p>  
    <p>メールをありがとう。</p>  
    <p>同じ会社で働くことになって、うれしいです。</p>  
    <p>住む所についてアドバイスをくださいと書いてあったので、お答えします。</p>  
    <p>会社まで歩いて行きたいと書いてありましたが、会社のりはオフィスばかりで、アパートはほとんどありません。電車通勤になりますが、私が以前住んでいた緑野という町はいいですよ。</p>  
    <p>緑野駅から会社のある北駅まで電車で15分だし、いろいろなお店があって便利です。</p>  
    <p>いい所が見つかるといいですね。会えるのを楽しみにしています。</p>  
  
    <p>今川</p>  
</body>  
</html>  

<!DOCTYPE html>  
<html lang="ja">  
<head>  
    <meta charset="UTF-8">  
    <meta name="viewport" content="width=device-width, initial-scale=1.0">  
    <title>問題23</title>  
</head>  
<body>  
    <h1>問題23</h1>  
    <p>まで電車で15分で行けるし、店も多いので、緑野にしたらどうか。</p>  
    <ol>    
        <li>いろいろな店があって便利なので、北駅駅の近くにしたらどうか</li>  
        <li>北駅まで電車で15分で行けるし、店も多いので、緑野にしたらどうか</li>  
        <li>いろいろな店があって便利なので、北駅駅の近くにしたらどうか</li>  
    </ol>  
</body>  
</html>  

<!DOCTYPE html>  
<html lang="ja">  
<head>  
    <meta charset="UTF-8">  
    <meta name="viewport" content="width=device-width, initial-scale=1.0">  
    <title>問題24</title>  
</head>  
<body>  
    <h1>(2)</h1>  
    <p>友達のマキは、いいことがあったという話をよくする。だから私は、マキは運がいいのだと思っていた。しかし、最近、そうではないと気づいた。</p>  
    <p>先日二人で出かけたとき、事故で電車が止まっていて、何キロも歩いて帰ることになった。嫌だなと思っている私に、マキは「知らない町を歩けるね。」とうれしそうに言った。こんなことでも、マキは楽しめてしまうのだ。今まで私が聞いた話も、マキだから「いいこと」だと感じたのだろうと思う。</p>  
  
    <h2>24. 最近、「私」はマキのことをどのような人だと思うようになったか。</h2>  
    <ol>  
        <li>「いいこと」ばかりが起きる。運がいい人</li>  
        <li>「私」と一緒に経験したことは、何でも「いいこと」だと思える人</li>  
        <li>ほかの人に起こった「いいこと」を一緒に喜んであげられる人</li>  
        <li>ほかの人が「いいこと」だと思わないことも「いいこと」だと思える人</li>  
    </ol>  
</body>  
</html>  

<!DOCTYPE html>  
<html lang="ja">  
<head>  
    <meta charset="UTF-8">  
    <meta name="viewport" content="width=device-width, initial-scale=1.0">  
    <title>(3)</title>  
</head>  
<body>  
    <h1>(3)</h1>  
    <p><strong>(会社で)</strong></p>  
    <p>ミンさんが席に戻ると、机の上に、原口課長からのメモが置いてあった。</p>  
  
    <p><strong>ミンさん</strong></p>  
    <p>子どもが熱を出したので、早退します。午後、明日の会議の進行について確認する約束だったのに、すみません。午後の話し合いのために予約していた小会議室はキャンセルしてくれますか。席に戻ったら、すぐにお願いします。会議の進行については、明日の朝、最初に確認して、そのあとに会議室の準備をしましょう。</p>  
    <p>それから、ミンさんの作った資料ですが、問題ないので、今日中に8人分印刷しておいてください。</p>  
    <p>よろしくお願いします。</p>  
    <p>9月8日 12:10</p>  
    <p>原口</p>  
  
    <h2>25. このメモを読んで、ミンさんはまず何をしなければならないか。</h2>  
    <ol>  
        <li>会議の進行について口課長と確認する</li>  
        <li>小会議室をキャンセルする</li>  
        <li>会議室の準備をする</li>  
        <li>会議の資料を8人分印刷する</li>  
    </ol>  
</body>  
</html>  

<!DOCTYPE html>  
<html lang="ja">  
<head>  
    <meta charset="UTF-8">  
    <meta name="viewport" content="width=device-width, initial-scale=1.0">  
    <title>(4)</title>  
</head>  
<body>  
    <h1>(4)</h1>  
    <p>日本のファミリーレストランは、店の壁やソファーなどに、赤やオレンジ色のような暖かさを感じさせる色、つまり、暖色を使うことが多い。</p>  
    <p>暖色には食欲を感じさせる効果があるので、暖色に囲まれていると、料理がおいしそうに見える。また、暖色は、時間を実際より長く感じさせる効果もある。客は、店にいた時間が短くても、ゆっくりできたように感じるのだ。</p>  
  
    <h2>26.</h2>  
    <p>店の暖房にあまりお金がかからないようにするため</p>  
    <ol>  
        <li>客に、店の料理と店で過ごす時間にいい印象を持ってもらうため</li>  
        <li>店をおしゃれに見せて、客に店に入りたいと思ってもらうため</li>  
        <li>客に長く店にいてもらって、料理をたくさん注文してもらうため</li>  
    </ol>  
</body>  
</html>      
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
Explanation: Append the correct answer and an explanation of the main challenges for the question from Japanese teacher's pespective.
Additional Requirement: Don't show question requirement and question sequence and revised submission in the generated content.


Search result: {search_result}
Formal exam paper: {example}
"""

midsize_reading_example = """
<!DOCTYPE html>  
<html lang="ja">  
<head>  
    <meta charset="UTF-8">  
    <meta name="viewport" content="width=device-width, initial-scale=1.0">  
    <title>問題5</title>  
</head>  
<body>  
    <h1>問題5</h1>  
    <p>つぎの(1)と(2)の文章を読んで、質問に答えなさい。答えは、1・2・3・4から最もよいものを一つえらびなさい。</p>  
  
    <h2>(1)</h2>  
    <p>日本に留学に来る前、母が持っていきなさいと言って、私の国でよく売っている粉の香辛料をくれました。私が普段あまり使わないものでしたが、役に立つかもしれないと母が言うので、荷物に入れました。最近、それが本当に役に立ちました。</p>  
    <p>先月、<u>①ちょっと困ったことがありました</u>。ある留学生交流会に、国の料理を何か作ってさし出してと言われたのです。私にも得意な料理はあるのですが、日本では買えない材料を使うので作れません。そのとき、私はあの香辛料を思い出したのです。</p>  
    <p>私は、肉と卵を使ってチャーハンを作り、香辛料をかけてみました。すると、日本によくある普通のチャーハンが、私の国らしい味と香りの<u>②特別なチャーハン</u>になったのです。交流会でも、みんな、おいしいおいしいと言って食べてくれて、安心しました。</p>  
    <p>あのとき、母はこういうことを予想していたのでしょうか。明日電話するので、<u>③母に聞いてみようと思います</u>。</p>  
  
    <h2>27. <u>①ちょっと困ったことがありました</u>とあるが、「私」が困ったのはなぜか。</h2>  
    <ol>  
        <li>母に、普段あまり使わない香辛料を持っていくように言われたから</li>  
        <li>得意な料理がないのに、国の料理を作ってきてほしいと言われたから</li>  
        <li>国の料理を作ってきてほしいと言われたが、日本では得意な料理が作れないから</li>  
        <li>チャーハンが作れないのに、チャーハンを作ってきてほしいと言われたから</li>  
    </ol>  
</body>  
</html>  

<!DOCTYPE html>  
<html lang="ja">  
<head>  
    <meta charset="UTF-8">  
    <meta name="viewport" content="width=device-width, initial-scale=1.0">  
    <title>問題28・29</title>  
</head>  
<body>  
    <h2>28. <u>②特別なチャーハン</u>とは、どのようなチャーハンか。</h2>  
    <ol>  
        <li>日本で売っている材料でチャーハンを作って、国の香辛料をかけたもの</li>  
        <li>日本で売っている材料でチャーハンを作って、日本の香辛料をかけたもの</li>  
        <li>国から持ってきた材料でチャーハンを作って、国の香辛料をかけたもの</li>  
        <li>国から持ってきた材料でチャーハンを作って、日本の香辛料をかけたもの</li>  
    </ol>  
  
    <h2>29. <u>③母に聞いてみようと思います</u>とあるが、「私」はどのようなことを聞くと考えられるか。</h2>  
    <ol>  
        <li>国の香辛料がどうして日本で役に立つと思ったのか</li>  
        <li>どんな料理を作るときに国の香辛料を使えばいいのか</li>  
        <li>「私」が日本に留学することを予想していたかどうか</li>  
        <li>次の留学生交流会に、どんな料理を持っていけばいいと思うか</li>  
    </ol>  
</body>  
</html>  

<!DOCTYPE html>  
<html lang="ja">  
<head>  
    <meta charset="UTF-8">  
    <meta name="viewport" content="width=device-width, initial-scale=1.0">  
    <title>(2)</title>  
</head>  
<body>  
    <h1>(2)</h1>  
    <p>重大な影響が出ている。このような問題に関心を持つ企業や消費者は、日本でも海外でも増えている。</p>  
    <p>服や靴を作っている、ある海外のファッションの会社が始めた活動がある。まず、漁師たち、つまり魚をとって生活している人たちに組んで、魚をとるときに絡むごみを、港に持ち帰ってもらう。そして、会社がそのごみを回収、分類し、その中のプラスチックを繊維に変え、服や靴にして売るというリサイクル活動である。</p>  
    <p>実は、以前、漁師たちはごみがとれても海に戻していた。漁に持ち帰ると捨てるのにお金がかかるからだ。この活動は、漁師にとっても、自分のお金を使わずに海をきれいにできる良さがあるのだ。</p>  
    <p>これらの服や靴は、最近日本でも売られ始めた。デザインも悪くない。消費者の意識が変化している今、日本でもきっと受け入れられるだろう。</p>  
  
    <h2>30. 「海外のファッションの会社」がしていることとして、合っているのはどれか。</h2>  
    <ol>  
        <li>漁師たちと一緒に、海にごみをとりに行っている</li>  
        <li>漁師たちから捨てごみを受け取って、他に持ち帰っている</li>  
        <li>漁師たちがプラスチックごみから服や靴を作るのを助けて、それを売っている</li>  
        <li>漁師たちが持ってきたプラスチックごみを利用して、服や靴を作っている</li>  
    </ol>  
</body>  
</html>  

<!DOCTYPE html>  
<html lang="ja">  
<head>  
    <meta charset="UTF-8">  
    <meta name="viewport" content="width=device-width, initial-scale=1.0">  
    <title>問題31・32</title>  
</head>  
<body>  
    <h2>31. 漁師たちは、なぜ「海外のファッションの会社」が始めた活動に参加するのか。</h2>  
    <ol>  
        <li>ほかの漁師たちとの協力関係ができるから</li>  
        <li>自分たちのお金をかけずに、海のごみを減らすことができるから</li>  
        <li>魚をとるためにかかっていたお金を減らすことができるから</li>  
        <li>自分たちが少しお金を出すだけで、海をきれいにしてもらえるから</li>  
    </ol>  
  
    <h2>32. この文章を書いた人は、日本で売られ始めた「海外のファッションの会社」の服や靴について、どのように考えているか。</h2>  
    <ol>  
        <li>海外のファッションに関心を持つ人が増えているので、売れるだろう</li>  
        <li>環境問題に関心を持つ人が増えているし、デザインも悪くないので、売れるだろう</li>  
        <li>デザインの良さで製品を選ぶ人が増えているので、値段が高くても売れるだろう</li>  
        <li>製品のデザインが日本の消費者には合わないので、あまり売れないだろう</li>  
    </ol>  
</body>  
</html>  
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
Explanation: Append the correct answer and an explanation of the main challenges for the question from Japanese teacher's pespective.
Additional Requirement: Don't show question requirement and question sequence and revised submission in the generated content.


Search result: {search_result}
Formal exam paper: {example}
"""

long_reading_example = """
<!DOCTYPE html>  
<html lang="ja">  
<head>  
    <meta charset="UTF-8">  
    <meta name="viewport" content="width=device-width, initial-scale=1.0">  
    <title>問題6</title>  
</head>  
<body>  
    <h1>問題6</h1>  
    <p>つぎの文章を読んで、質問に答えなさい。答えは、1・2・3・4から最もよいものを一つえらびなさい。</p>  
  
    <p>分が住むために直し始めた。日本の古民家には、丈夫で立派な木の材料が使われている。それを利用して直せば、長く住めるいい家になると考えたのだ。</p>  
      
    <p>Kさんの直し方はこうだ。まず、家を一度バラバラにする。そして、材料の悪くなっている部分は取り替えるが、そのまま使える材料はできるだけ使って、前と同じように組み立てる。直しながら壁の色を変えたり、最新の暖房を入れたりもする。この方法なら、古民家が時代に合った住みやすい家になるのだ。</p>  
      
    <p>Kさんは、家を直して住み始めたあと、下村にあるほかの古民家もそのままにしておくのはもったいないと思い、友人にお金を借りて直し始めた。自分のように古民家を直した家の良さがわかり、買ってくれる人がいるはずだと信じていたのだ。実際、すぐにそのような人は見つかった。そして、その後、直した古民家を見学しに全国各地の人が下村に来るようになった。</p>  
      
    <p>日本では、古い家を直すより新しい家を建てたほうがいいという考えが、まだまだ強い。Kさんの行動は、日本人に（　　　）を教えてくれているのだと思う。</p>  
  
    <h2>33. Kさんが住む前の下村は、どのような状態だったか。</h2>  
    <ol>  
        <li>ほとんど壊れていないのに、誰も住んでいない古民家がたくさんあった</li>  
        <li>住みやすいように直されているのに、誰も住んでいない古家がたくさんあった</li>  
        <li>壊れたまま直さず人が住んでいる古民家がたくさんあった</li>  
        <li>誰も住んでいない壊れた古民家がたくさんあった</li>  
    </ol>  
</body>  
</html>  

<!DOCTYPE html>  
<html lang="ja">  
<head>  
    <meta charset="UTF-8">  
    <meta name="viewport" content="width=device-width, initial-scale=1.0">  
    <title>問題34・35・36</title>  
</head>  
<body>  
    <h2>34. Kさんの方法で直した古民家は、どのような家になるか。</h2>  
    <ol>  
        <li>新しい材料をできるだけ使っていて、壁の色や暖房も新しく変えた家</li>  
        <li>新しい材料をできるだけ使っているが、壁の色や暖房は昔と変わらない家</li>  
        <li>古い材料をできるだけ使っていて、朝の色や暖房も昔と変わらない家</li>  
        <li>古い材料をできるだけ使っているが、駅の色や暖房は新しく変えた家</li>  
    </ol>  
  
    <h2>35. そのような人とはあるが、どのような人か。</h2>  
    <ol>  
        <li>Kさんが直して住み始めた古民家を買ってくれる人</li>  
        <li>下村の古民家を直そうとするKさんに、お金を貸してくれる人</li>  
        <li>下村にある壊れた古民家を買って、Kさんに直してもらおうとする人</li>  
        <li>古民家を直した家の良さがKさんのように分かって、買ってくれる人</li>  
    </ol>  
  
    <h2>36. （　）に入れるのに最もよいものはどれか。</h2>  
    <ol>  
        <li>古い家を自分で直すことの面白さ</li>  
        <li>古い家にはない、新しい家の素晴らしさ</li>  
        <li>古い家を利用し、直して使っていくことの良さ</li>  
        <li>古い家を変えずに、そのまま残していくことの価値</li>  
    </ol>  
</body>  
</html>   
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
Explanation: Append the correct answer and an explanation of the main challenges for the question from Japanese teacher's pespective.
Additional Requirement: Don't show question requirement and question sequence and revised submission in the generated content.


Search result: {search_result}
Formal exam paper: {example}
"""

information_retrieval_example = """
<!DOCTYPE html>  
<html lang="ja">  
<head>  
    <meta charset="UTF-8">  
    <meta name="viewport" content="width=device-width, initial-scale=1.0">  
    <title>問題7</title>  
</head>  
<body>  
    <h1>問題7</h1>  
    <p>右のページは、あるスキー場のホームページに載っているスキー教室の案内である。これを読んで、下の質問に答えなさい。答えは、1・2・3・4から最もよいものを一つえらびなさい。</p>  
  
    <h2>37.</h2>  
    <ol>  
        <li>①</li>  
        <li>②</li>  
        <li>③</li>  
        <li>④</li>  
    </ol>  
  
    <h2>38. 園内活動の協力者になりたいと思っている人が、気をつけなければならないことはどれか。</h2>  
    <ol>  
        <li>複数の活動に応募することはできない</li>  
        <li>説明会は、AとBの両方に参加しなければならない</li>  
        <li>説明会に参加するために、参加希望日の前日までに電話で連絡しなければならない</li>  
        <li>応募用紙は、必要な情報を書いて、事務所に持参しなければならない</li>  
    </ol>  
</body>  
</html>  

<!DOCTYPE html>  
<html lang="ja">  
<head>  
    <meta charset="UTF-8">  
    <meta name="viewport" content="width=device-width, initial-scale=1.0">  
    <title>園内活動の協力者募集</title>  
</head>  
<body>  
    <h1>園内活動の協力者を募集します</h1>  
    <p>東山公園内の活動に、4月から新しく協力してくださる方を募集します。※一緒に公園で活動しませんか。</p>  
  
    <table border="1" cellpadding="5">  
        <thead>  
            <tr>  
                <th>活動の種類</th>  
                <th>活動日、時間</th>  
                <th>活動場所、内容</th>  
            </tr>  
        </thead>  
        <tbody>  
            <tr>  
                <td>① 花や木の世話</td>  
                <td>毎週火曜日 9時～11時</td>  
                <td>公園内で、花や木の世話をします。花の世話が初めての方も歓迎します。</td>  
            </tr>  
            <tr>  
                <td>② ホームページ作り</td>  
                <td>毎週火曜日 9時～11時</td>  
                <td>公園の事務所で、ホームページの記事を書く活動です。※パソコンが扱える方にお願いします。</td>  
            </tr>  
            <tr>  
                <td>③ 公園の掃除</td>  
                <td>毎週木曜日 14時～16時</td>  
                <td>園内で、ごみ拾いなどをします。多くの方の協力が必要な活動です。</td>  
            </tr>  
            <tr>  
                <td>④ 公園の案内</td>  
                <td>毎月第2日曜日 9時～11時</td>  
                <td>園内を歩いて、公園を案内します。</td>  
            </tr>  
        </tbody>  
    </table>  
  
    <h2>応募できる方</h2>  
    <p>東山市に住んでいる18歳以上の方で、説明会に参加できる方※④の活動に分けて募集していますが、複数の活動への応募も可能です。</p>  
  
    <h2>説明会</h2>  
    <p>以下のAかBのどちらかに参加してください（AとBの内容は同じです）。参加希望日の前日までに、事務所へ電話で連絡してください。</p>  
  
    <table border="1" cellpadding="5">  
        <thead>  
            <tr>  
                <th>日時</th>  
                <th>場所</th>  
            </tr>  
        </thead>  
        <tbody>  
            <tr>  
                <td>A 3月19日(土) 14時（約30分）</td>  
                <td>東山文化センター 2階会議室</td>  
            </tr>  
            <tr>  
                <td>B 3月19日(土) 14時（約30分）</td>  
                <td>東山文化センター 2階会議室</td>  
            </tr>  
        </tbody>  
    </table>  

<!DOCTYPE html>  
<html lang="ja">  
<head>  
    <meta charset="UTF-8">  
    <meta name="viewport" content="width=device-width, initial-scale=1.0">  
    <title>応募方法</title>  
</head>  
<body>  
    <h2>応募方法</h2>  
    <p>説明会でお渡しする応募用紙に必要な情報を書いて、事務所へ持参、または郵送してください。</p>  
  
    <h2>応募の前に活動に参加してみたい方</h2>  
    <p>①～③の活動に参加してみたい方は、それぞれの活動日・時間に事務所に来てください。特に連絡は必要ありません。</p>  
  
    <p><strong>東山公園 事務所</strong></p>  
    <p>〒166-0113 東山市花田町 13-5<br>電話: 0685-65-9877 (9:00～17:00)</p>  
</body>  
</html>  
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
Explanation: Append the correct answer and an explanation of the main challenges for the question from Japanese teacher's pespective.
Additional Requirement: Don't show question requirement and question sequence and revised submission in the generated content.


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
Explanation: Append the correct answer and an explanation of the main challenges for the question from Japanese teacher's pespective.
Additional Requirement: Don't show question requirement and question sequence and revised submission in the generated content.


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
Explanation: Append the correct answer and an explanation of the main challenges for the question from Japanese teacher's pespective.
Additional Requirement: Don't show question requirement and question sequence and revised submission in the generated content.


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
Explanation: Append the correct answer and an explanation of the main challenges for the question from Japanese teacher's pespective.
Additional Requirement: Don't show question requirement and question sequence and revised submission in the generated content.


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
Additional Requirement: Don't show question requirement and question sequence and revised submission in the generated content.


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



