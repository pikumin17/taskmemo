# taskmemo

Python 標準ライブラリだけで作る、小さなコマンドライン TODO アプリです。
GitHub Issue ごとに add / list / done の機能を実装していきます。

## 使い方

`add` にタスクの内容を渡して追加します。空白を含む内容は引用符で囲みます。

```sh
python3 taskmemo.py add "買い物に行く"
python3 taskmemo.py add "メールを返信する"
python3 taskmemo.py list
```

`list` は、1 から始まる整数 ID とタスクの内容を表示します。

```text
1: 買い物に行く
2: メールを返信する
```

タスクはコマンドを実行したディレクトリの `tasks.json` に保存されます。ファイルがなければ、`list` は空の一覧として扱います。
