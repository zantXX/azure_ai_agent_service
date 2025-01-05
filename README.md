# Azure AI Agent Service - gradio

> [!CAUTION]
> NOW IN PROGRESS、現在作成途中です。動作しません。作成完了予定もありません。

Azure AI Agent ServiceをGUIで扱えるためのツールにする予定

## 利用の仕方

uvを利用しています。uvの環境構築等は、公式サイト等を参照してください。
以下を実行する

```bash
uv sync
uv run gradio_ui.py
```

## task

1. パッケージの整理
    - [公式関数](https://learn.microsoft.com/ja-jp/python/api/azure-ai-projects/azure.ai.projects?view=azure-python-preview)から関数を引っ張ってきて追加する。
    - gradio接続用の関数を作っていく(gradio_functions)
        - create agentするときの動作
        - fileをアップロードするときの動作-ログ表示
        - agentの更新、選択時の操作
        - new chatの動作
        - chatの更新
        - azure ai searchの動作
        - 実行手順をリスト表示
1. gradio
    - web uiの更新
        - agentとthreadの削除ボタンの追加
        - azure ai searchの動作
        - ファイル選択フィールドの追加
            - ツールに登録する
            - チャットに一時的に追加する
        - 動作確認
        - 実行手順をリスト表示
