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
