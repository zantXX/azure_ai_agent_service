# Azure AI Agent Service - gradio

> [!CAUTION]
> NOW IN PROGRESS、現在作成途中です。動作しません。作成完了予定もありません。

Azure AI Agent ServiceをGUIで扱えるためのツールにする予定。

## 利用の仕方

uvを利用しています。uvの環境構築等は、公式サイト等を参照してください。
`.env.example` を参考に、Azureやデフォルト設定を`.env`に記述・作成してください。
以下を実行して、動作予定です。

```bash
uv sync
uv run gradio_ui.py
```

## task

1. パッケージの整理
    - [公式関数](https://learn.microsoft.com/ja-jp/python/api/azure-ai-projects/azure.ai.projects?view=azure-python-preview)から関数を引っ張ってきて追加する。
    - gradio接続用の関数を作っていく(`utils/gradio_functions.py`)
        - chatの動作についって
        - azure ai searchの動作
        - 実行手順をリスト表示
        - fileをアップロードするときの動作を最適化(ファイルの更新差分のみをアップロード)
1. gradio
    - web uiの更新(`gradio_ui.py`)
        - azure ai searchの動作
        - ファイル選択フィールドの追加
            - ツールに登録する
            - チャットに一時的に追加する
        - 動作確認
        - 実行手順をリスト表示

## ファイル構造

- downloads
  - エージェントで作成されたファイルを保存予定
- files
  - OpenAPI, FuctionCalling, ファイル検索に用いるファイルを格納予定
- utils
  - gradioの動作で必要な関数をまとめて格納。`agent.py`, `thread.py`, `tools.py`, `messsage.py`と大まかな箱ごとにファイルを作成済み。
  - `gradio_functions.py`では、上記の関数とgradioをつなぐ関数を作成予定。
