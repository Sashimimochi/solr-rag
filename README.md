
# はじめに

本記事では、SolrをバックエンドにしてRAGをしてみます。

# RAGとは

再三多くの記事で解説されているので今さら説明するまでもなさそうですが、ユーザからの質問に回答するために必要そうな内容が書かれた文章を検索し、その文章を LLM への入力（プロンプト）に付け加えて入力する手法です。

さまざまな問いかけに答えてくれるChatGPTの能力に驚かされますが、知らない知識に関しては当然のことながら答えられません。
例えば、ChatGPT の無料版である GPT-3.5 については、2021 年 9 月までの Web 上の情報をもとに学習をしているので、それ以後に世に出た情報については知りません。 
また、Web 上に公開されている情報源に関してしか知らないので、自社のサービス固有の情報に関する回答や社外秘情報に関しては当然ながら答えられません。

わからないことについては、一律答えられませんと言ってくれればまだいいのですが、それより厄介なことも起こり得ます。
ハルシネーション（幻覚）と呼ばれる現象で、誤った回答であるにもかかわらず、自信満々に真実であるかのように回答してしまうことがあるのです。
https://xtech.nikkei.com/atcl/nxt/column/18/00692/082900114/

お勉強用途で LLM が返してきたサンプルコードを動かしたらエラーで動かなかった程度で済めばまだいいですが、プロダクトとしてリリースしたものが嘘八百状態では会社の信用問題にかかわるので致命的です。
仮に追加で知識が付与できたとしても、AI はそれが真実であるか否かは関知しないので、ハルシネーションを完全に防止することはできません。

これへの対応策として今一番注目されている手法が、RAG（Retrieval Augmented Generation）と呼ばれる手法です。
https://arxiv.org/abs/2005.11401

RAG は、 プロンプトと呼ばれる LLM への入力情報にモデル外部の情報源からの検索結果を付加して、検索結果に基づいた回答をさせています。
モデルはプロンプトに含まれているリファレンス情報をもとにユーザからの要望に回答すればいいので、知識にないことであっても正確に答えられるようになるのではないかという発想です。

このリファレンス情報の取得のために検索エンジンへのリクエストを投げるステップがあります。

# SolrでRAGをする

Qdrantなどのベクトル検索に特化しているエンジンはもちろん、ElasticsearchについてもLangchainとの連携が公式にサポートされています。
[Qdrant \| 🦜️🔗 Langchain](https://python.langchain.com/docs/integrations/vectorstores/qdrant)
[Elasticsearch \| 🦜️🔗 Langchain](https://python.langchain.com/docs/integrations/vectorstores/elasticsearch)
特にこだわりなければ、すなおにこれらを使うのが開発コストがかからずいいと思います。

そこを本記事ではあえてSolrをバックエンドに使おうと思います。
理由は私がSolrを使っているからです。それだけです。
最近はすっかりElasticsearchに人気を取られがちですが、いろいろなしがらみでSolrを使っている人もいると思いますので、そんな人に届けばいいなと思います。

さて、SolrとLangchainの連携状況ですが、現在issueは出ているもののの公式にはまだサポートされていません。
https://github.com/langchain-ai/langchain/issues/7273

ただ、有志の方が作ったライブラリはありました。
https://github.com/Eurelis/Eurelis-Langchain-SolR-VectorStore



# ここまでのまとめ
# おわりに


Python >= 3.11
eurelis-langchain-solr-vectorstore ライブラリの都合上

langchain からインデックスさせる場合

使用可能な型は限定されている。

```
ValueError: Expected metadata value to be a str, int, float or bool, got None which is a <class 'NoneType'>
```

フィールド名は
`metadata_fieldname_type`
で固定されている
https://github.com/Eurelis/Eurelis-Langchain-SolR-VectorStore/blob/8750c0e53ea03a6a4e2ee8136ebf87fd0b9d3e86/src/eurelis_langchain_solr_vectorstore/solr_core.py#L54-L76

ex.

- `metadata_id_i`
- `metadata_title_s`

uniquekey のフィールド名は id で固定であり、id フィールドが必須
id フィールドは string 型で固定（ハッシュ値のようなものが入る）

embedding model の選定大事
tokenier とか

インデックスデータ/コレクション分け大事
関係ないノイズデータをインデックスさせるておくとベクトル検索でヒットしてしまう
SNS のような短文はノイズになりやすい
キーワードフィルタリングでも防げる

ハイブリット検索大事
特に名詞、固有名詞
送り仮名程度のぶれは fuzzy で吸収する
抽象的な質問ではなく、具体的な質問であれば余計なドキュメントをヒットさせないようキーワードフィルタリングさせるのがよさそう
ランキングの問題ではない
日英表記などの表記ゆれはシノニムで頑張る

要約や抽出（QA）タスクには LLM 強そう

calm2-7b-chat 優秀
rinna に比べて回答の質がいい
持っている知識量も全然違う

低スペック PC の場合、圧縮モデルを使うべし
ものによっては圧縮済みモデルが公開されている
CPU メモリがあれば自分でも圧縮できる

ベクトルデータの保存先として Mongo は良さそう
リスト型のデータをそのまま保存できる
Atlas なら ann 検索も可能
mysql だと一度 string に直して格納し、インデックスさせるときにリストに戻す必要がある

DIH ではベクトルデータが取り込めない
mysql ではリスト型のデータを保存できない
sql で取り出し時にリストにするのも難しい
3rd party 製になったからか transformer script で javascript が正常に動作しない
java で自作プラグインを読み込ませるのも難しい
ドライバーも mariadb のみで mongo などに対応していなさそう

https://python.langchain.com/docs/modules/data_connection/retrievers/vectorstore

```python
docs = retriever.get_relevant_documents("what did he say about ketanji brown jackson")
```

スコアが一定以上のドキュメントだけが欲しい場合
`search_type`の指定が必須

```python
retriever = db.as_retriever(search_type="similarity_score_threshold", search_kwargs={"score_threshold": .5})
```

topK が欲しい場合

```python
retriever = db.as_retriever(search_kwargs={"k": 1})
```
