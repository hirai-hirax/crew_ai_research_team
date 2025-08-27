# CrewAI Research Team

AI研究チームによる自動リサーチシステム。指定したテーマに対して複数のAIエージェントが協力して調査・分析・報告を行います。

## 概要

このプロジェクトはCrewAIフレームワークを使用し、以下のタスクを実行します：

- **propose**: テーマについて詳細な調査レポートを作成
- **review**: 調査レポートの品質をレビュー・評価
- **finalize**: レビュー結果を反映した最終レポートを作成

## セットアップ

### 必要な環境

- Python 3.12以上
- uv (推奨)

### インストール

```bash
# uvを使用する場合
uv sync

# pipを使用する場合
pip install -e .
```

## 使用方法

### コマンドライン引数での実行

```bash
# uvを使用
uv run main.py --theme "テーマ" --purpose "目的" --client_background "クライアント背景"

# pythonを直接使用
python main.py --theme "テーマ" --purpose "目的" --client_background "クライアント背景"
```

### 引数の説明

- `--theme`: 調査のテーマ（必須ではありません）
- `--purpose`: 調査の目的（必須ではありません）
- `--client_background`: クライアントの背景情報（必須ではありません）

### 実行例

```bash
uv run main.py --theme "AIの未来" --purpose "技術トレンド調査" --client_background "テック企業の戦略企画部門"
```

引数を指定しない場合は、デフォルト値が使用されます。

## 設定

エージェントとタスクの設定は`config/`ディレクトリ内のYAMLファイルで管理されています：

- `config/agents.yaml`: エージェントの設定
- `config/tasks.yaml`: タスクの設定

## プロジェクト構造

```
├── main.py           # メインエントリーポイント
├── crew.py           # CrewAI設定とエージェント定義
├── config/           # 設定ファイル
│   ├── agents.yaml   # エージェント設定
│   └── tasks.yaml    # タスク設定
└── README.md         # このファイル
```