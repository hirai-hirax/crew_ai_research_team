# Weekend Planner

AI エージェントチームによる週末プランニングシステム。指定したエリアと希望に基づいて、複数の AI エージェントが協力してお出かけプランを提案します。

## 概要

このプロジェクトは CrewAI フレームワークを使用し、以下のステップで週末のお出かけプランを作成します：

1. **天気調査**: 指定日の天気予報を Open-Meteo から取得し、屋外/屋内の判断と持ち物を助言
2. **ローカル調査**: エリア内のイベントや施設を Web 検索し、屋内/屋外で分類
3. **推薦作成**: 情報を統合し、本命・気分転換・雨天向けの 3 候補を提示
4. **交通計画**: Google Maps API を使用して本命候補への移動手段・所要時間・概算料金を整理
5. **しおり作成**: タイムライン形式のしおりと持ち物・代替案を出力

各エージェントは `gpt-4o-mini` モデルを使用し、高速な応答を実現しています。

## セットアップ

### 必要な環境

- Python 3.12 以上
- uv (推奨)

### インストール

```bash
# uv を使用する場合
uv sync

# pip を使用する場合
pip install -e .
```

### 環境変数の設定

`.env` ファイルを作成し、以下の API キーを設定してください：

```bash
# Google Maps API (交通手段プランナー用)
GOOGLE_MAPS_API_KEY=your_google_maps_api_key

# Open-Meteo API (天気予報士用) - APIキー不要！

# Web検索用
SERPER_API_KEY=your_serper_api_key

# LLM用
OPENAI_API_KEY=your_openai_api_key
```

詳細は [AGENTS.md](AGENTS.md) を参照してください。

## 使用方法

### 基本的な使い方

```bash
uv run main.py \
  --location "東京23区" \
  --interests "カフェ巡りと美術館" \
  --budget "1人1.5万円" \
  --companions "友人2人" \
  --date "2024年4月20日" \
  --home "東京駅" \
  --departure-time "09:00" \
  --return-time "18:00"
```

### 引数の説明

| 引数 | デフォルト値 | 説明 |
|------|-------------|------|
| `--location` | `東京23区` | 希望エリア（例: 大阪市内、横浜みなとみらい） |
| `--interests` | `カフェ巡りと美術館、夜はライブハウス` | 興味・やりたいこと |
| `--budget` | `1人あたり1.5万円以内` | 予算感 |
| `--companions` | `友人2人` | 同伴者（例: カップル、家族4人） |
| `--date` | *今日の日付* | お出かけ希望日（例: 2024年12月25日） |
| `--home` | `東京駅` | 自宅住所または出発地点 |
| `--departure-time` | `09:00` | 出発希望時間（HH:MM形式） |
| `--return-time` | `18:00` | 帰宅希望時間（HH:MM形式） |

引数を指定しない場合は、デフォルト値が使用されます。

### 実行例

#### 例1: 東京で友人とカフェ巡り

```bash
uv run main.py \
  --location "東京23区" \
  --interests "カフェ巡りとアート" \
  --budget "1人1万円" \
  --companions "友人1人" \
  --date "2024年12月24日" \
  --home "渋谷駅" \
  --departure-time "10:00" \
  --return-time "17:00"
```

#### 例2: 大阪で食べ歩きデート

```bash
uv run main.py \
  --location "大阪市内" \
  --interests "食べ歩きとライブ" \
  --budget "1人1.5万円" \
  --companions "カップル" \
  --date "2024年12月31日" \
  --home "梅田駅" \
  --departure-time "11:00" \
  --return-time "20:00"
```

#### 例3: デフォルト設定で実行

```bash
# すべてデフォルト値を使用
uv run main.py
```

## Google カレンダー連携

Google カレンダー連携を活かす場合は、直近 30 日分の外出イベント（場所・開始/終了時刻・同行者メモ）が取得できるようにしてください。

`calendar_analyst` エージェントがカレンダー情報を分析し、あなたの好みや傾向を反映したプランを提案します。

## 設定

エージェントとタスクの設定は `config/` ディレクトリ内の YAML ファイルで管理されています：

- [config/agents.yaml](config/agents.yaml): エージェント設定（LLM モデル、役割、目標など）
- [config/tasks.yaml](config/tasks.yaml): タスク設定（各エージェントの具体的なタスク内容）

## プロジェクト構造

```
├── main.py                   # メインエントリーポイント
├── crew.py                   # CrewAI 設定とエージェント定義
├── config/                   # 設定ファイル
│   ├── agents.yaml          # エージェント設定
│   └── tasks.yaml           # タスク設定
├── tools/                    # カスタムツール
│   ├── google_maps_tool.py  # Google Maps API ツール
│   └── openweather_tool.py  # Open-Meteo API ツール
├── tests/                    # テストファイル
├── AGENTS.md                 # エージェント詳細ドキュメント
├── README_GOOGLE_MAPS.md     # Google Maps API セットアップガイド
├── README_OPENMETEO.md       # Open-Meteo API セットアップガイド
└── README.md                 # このファイル
```

## トラブルシューティング

### エンコーディングエラー

YAML ファイルは必ず UTF-8 エンコーディングで保存してください。詳細は [AGENTS.md](AGENTS.md) を参照してください。

### API エラー

- Google Maps API のエラーが発生した場合は、API キーが正しく設定されているか確認してください
- 無料枠を超過していないか確認してください

### その他の問題

詳細なセットアップ手順とトラブルシューティングについては、以下のドキュメントを参照してください：

- [AGENTS.md](AGENTS.md) - エージェント実行とAPI設定
- [README_GOOGLE_MAPS.md](README_GOOGLE_MAPS.md) - Google Maps API セットアップ
- [README_OPENMETEO.md](README_OPENMETEO.md) - Open-Meteo API セットアップ
