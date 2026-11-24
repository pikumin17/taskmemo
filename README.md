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

`done` に `list` で表示される ID を渡すと、そのタスクを完了にします。

```sh
python3 taskmemo.py done 1
python3 taskmemo.py list
```

完了したタスクには `[完了]` が付きます。

```text
1: [完了] 買い物に行く
2: メールを返信する
```

存在しない ID を指定すると、エラーメッセージを表示して終了します（終了コードは 0 以外）。

タスクはコマンドを実行したディレクトリの `tasks.json` に保存されます。ファイルがなければ、`list` は空の一覧として扱います。
