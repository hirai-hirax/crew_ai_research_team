# CrewAI Research Team

AI研究チームによる自動リサーチシステム。指定したテーマに対して複数のAIエージェントが協力して調査・分析・報告を行います。

## 概要

このプロジェクトはCrewAIフレームワークを使用し、以下のタスクを実行します：

- **propose**: テーマについて詳細な調査レポートを作成
- **review**: 調査レポートの品質をレビュー・評価
- **finalize**: レビュー結果を反映した最終レポートを作成
- **weekend_recommendation**: 週末の予定をユーザーの希望に合わせて提案

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
# 既存のリサーチタスクを実行
uv run main.py --mode research --theme "テーマ" --purpose "目的" --client_background "クライアント背景"

# 週末プランニングエージェントを実行
uv run main.py --mode weekend \
  --location "東京23区" \
  --interests "カフェ巡りと美術館" \
  --budget "1人1.5万円" \
  --companions "友人2人" \
  --weather "晴れ時々曇り"
```

### 引数の説明

- `--mode`: 実行するクルーを選択（`research` または `weekend`）
- `--theme`: 調査のテーマ（researchのみ）
- `--purpose`: 調査の目的（researchのみ）
- `--client_background`: クライアントの背景情報（researchのみ）
- `--location`: 希望エリア（weekendのみ）
- `--interests`: 興味・やりたいこと（weekendのみ）
- `--budget`: 予算感（weekendのみ）
- `--companions`: 同伴者（weekendのみ）
- `--weather`: 天気の概要（weekendのみ）

### 実行例

```bash
uv run main.py --mode research --theme "AIの未来" --purpose "技術トレンド調査" --client_background "テック企業の戦略企画部門"

uv run main.py --mode weekend --location "大阪市内" --interests "食べ歩きとライブ" --budget "1人1万円" --companions "カップル" --weather "曇り一時雨"
```

引数を指定しない場合は、デフォルト値が使用されます。

## 設定

エージェントとタスクの設定は`config/`ディレクトリ内のYAMLファイルで管理されています：

- `config/agents.yaml`: エージェント設定
- `config/tasks.yaml`: タスク設定

## プロジェクト構造

```
├── main.py           # メインエントリーポイント
├── crew.py           # CrewAI設定とエージェント定義
├── config/           # 設定ファイル
│   ├── agents.yaml   # エージェント設定
│   └── tasks.yaml    # タスク設定
└── README.md         # このファイル
```
