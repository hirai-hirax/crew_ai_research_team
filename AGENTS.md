# Agent Documentation

## Execution

This project uses `uv` for dependency management and execution.

To run the agent or tests, please use `uv run`.

### Running Tests

```bash
uv run python -m unittest discover tests
```

### Running the Agent

```bash
uv run python main.py
```

## Environment Setup

### Required API Keys

このプロジェクトでは以下のAPIキーが必要です。`.env` ファイルに設定してください。

#### 1. Google Maps API Key (必須 - transport_planner用)

交通手段プランナーが正確な移動時間を取得するために使用します。

**取得手順:**

1. [Google Cloud Platform Console](https://console.cloud.google.com/) にアクセス
2. 新しいプロジェクトを作成（または既存のプロジェクトを選択）
3. APIライブラリから以下のAPIを有効化:
   - **Directions API**
   - **Distance Matrix API**
4. 認証情報ページでAPIキーを作成
5. APIキーの制限を設定（推奨）:
   - アプリケーションの制限: なし（開発用）または IPアドレス制限
   - APIの制限: Directions API と Distance Matrix API のみ

**`.env` への設定:**

```
GOOGLE_MAPS_API_KEY=your_api_key_here
```

**料金について:**
- 月間40,000リクエストまで無料
- 超過時: $0.005/リクエスト
- 個人使用では通常無料枠内に収まります

**参考リンク:**
- [Google Maps Platform 料金](https://developers.google.com/maps/billing-and-pricing/pricing)
- [APIキーのベストプラクティス](https://developers.google.com/maps/api-security-best-practices)

#### 2. その他のAPI Keys

天気情報には**Open-Meteo API**を使用します（APIキー不要・完全無料）。

```
SERPER_API_KEY=your_serper_key_here
OPENAI_API_KEY=your_openai_key_here
```

### Full .env Template

```bash
# Google Maps API (交通手段プランナー用)
GOOGLE_MAPS_API_KEY=your_google_maps_api_key

# Open-Meteo API (天気予報士用) - APIキー不要！

# Web検索用
SERPER_API_KEY=your_serper_api_key

# LLM用
OPENAI_API_KEY=your_openai_api_key
```

## ⚠️ 重要: ファイルエンコーディングのベストプラクティス

### 🔴 エンコーディングエラーを防ぐために

YAMLファイル（`config/agents.yaml`, `config/tasks.yaml`）は**必ずUTF-8エンコーディング**で保存してください。

#### ❌ やってはいけないこと

1. **PowerShellのリダイレクトを使用した一括置換**
   ```powershell
   # ❌ これを実行するとエンコーディングが壊れる可能性があります
   (Get-Content file.yaml) -replace 'old', 'new' | Set-Content file.yaml
   ```
   
2. **エンコーディングを指定しないファイル操作**
   - PowerShellのデフォルトエンコーディングはUTF-8ではない場合があります

#### ✅ 推奨される方法

1. **VSCodeなどのエディタで手動編集**
   - VSCodeは自動的にUTF-8を使用します
   - ステータスバーでエンコーディングを確認/変更できます

2. **PowerShellで置換する場合は明示的にUTF-8を指定**
   ```powershell
   # ✅ UTF-8を明示的に指定
   $content = Get-Content 'file.yaml' -Encoding UTF8
   $content -replace 'old', 'new' | Set-Content 'file.yaml' -Encoding UTF8
   ```

3. **Pythonスクリプトを使用**
   ```python
   # ✅ Pythonはデフォルトでutf-8を使用
   with open('file.yaml', 'r', encoding='utf-8') as f:
       content = f.read()
   content = content.replace('old', 'new')
   with open('file.yaml', 'w', encoding='utf-8') as f:
       f.write(content)
   ```

#### 🔧 エンコーディングエラーが発生した場合

**症状:**
```
UnicodeDecodeError: 'utf-8' codec can't decode bytes
```

**対処法:**
1. バックアップから復元（Git使用の場合）
   ```bash
   git checkout config/agents.yaml
   ```

2. ファイルを手動で修正し、UTF-8で保存し直す

3. エディタでエンコーディングを確認
   - VSCode: ステータスバー右下
   - 「UTF-8」になっているか確認

### 教訓

> **日本語を含むYAMLファイルは、必ずUTF-8エンコーディングで保存すること。**
> **PowerShellで一括置換する場合は、必ず`-Encoding UTF8`を指定すること。**
