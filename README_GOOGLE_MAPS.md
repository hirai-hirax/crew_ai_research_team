# Google Maps API 連携ガイド

このドキュメントでは、交通手段プランナー(transport_planner)で使用されるGoogle Maps API連携について説明します。

## 概要

交通手段プランナーは、Google Maps APIを使用して以下の機能を提供します:

- **正確な移動時間の取得**: リアルタイムの交通状況を考慮した所要時間
- **複数の移動手段の比較**: 自動車、公共交通機関、徒歩を一度に比較
- **詳細な経路情報**: 乗り換え情報、運賃、具体的な路線名など
- **渋滞情報の考慮**: 自動車の場合、通常時と渋滞時の所要時間を提示

## 使用されるツール

### 1. Google Maps経路検索ツール (GoogleMapsDirectionsTool)

指定された出発地から目的地までの詳細な経路情報を取得します。

**取得できる情報:**
- 所要時間
- 距離
- 詳細な経路案内
- 公共交通機関の場合:
  - 乗り換え情報(路線名、停車駅数)
  - 運賃
  - 乗車駅・下車駅
- 自動車の場合:
  - 渋滞を考慮した所要時間

**対応する移動手段:**
- `driving`: 自動車
- `transit`: 公共交通機関(電車・バス)
- `walking`: 徒歩
- `bicycling`: 自転車

### 2. Google Maps複数手段比較ツール (GoogleMapsDistanceMatrixTool)

複数の移動手段の所要時間と距離を一度に比較します。

**用途:**
- 最適な移動手段の選択
- 複数の選択肢の迅速な比較

## API設定

### 1. Google Cloud Platformでの設定

#### プロジェクトの作成

1. [Google Cloud Console](https://console.cloud.google.com/) にアクセス
2. 画面上部の「プロジェクトを選択」をクリック
3. 「新しいプロジェクト」をクリック
4. プロジェクト名を入力(例: "weekend-planner")
5. 「作成」をクリック

#### APIの有効化

1. 左側メニューから「APIとサービス」→「ライブラリ」を選択
2. 以下のAPIを検索して有効化:
   - **Directions API**
   - **Distance Matrix API**

各APIの「有効にする」ボタンをクリックします。

#### APIキーの作成

1. 左側メニューから「APIとサービス」→「認証情報」を選択
2. 「認証情報を作成」→「APIキー」をクリック
3. APIキーが生成されます(後で使用するのでコピーしておく)

#### APIキーの制限設定(推奨)

セキュリティのため、APIキーに制限を設定することを推奨します:

1. 生成されたAPIキーの「編集」をクリック
2. **アプリケーションの制限**:
   - 開発環境: 「なし」
   - 本番環境: 「IPアドレス」を選択し、サーバーのIPを追加
3. **APIの制限**:
   - 「キーを制限」を選択
   - 以下のAPIのみ許可:
     - Directions API
     - Distance Matrix API
4. 「保存」をクリック

### 2. 環境変数への設定

プロジェクトルートの `.env` ファイルに以下を追加:

```bash
GOOGLE_MAPS_API_KEY=your_actual_api_key_here
```

**注意:** 
- `.env` ファイルは `.gitignore` に含まれているため、Gitにコミットされません
- APIキーは絶対に公開リポジトリにコミットしないでください

## 料金について

### 無料枠

Google Maps APIには無料枠があります(2025年11月現在):

- **Directions API**: 月間 40,000 リクエストまで無料
- **Distance Matrix API**: 月間 40,000 要素まで無料

### 超過時の料金

無料枠を超えた場合:

- **Directions API**: $0.005/リクエスト
- **Distance Matrix API**: $0.005/要素

### 使用量の目安

週末プランナーの1回の実行で:
- 複数手段比較ツール: 1回 (3要素 = 自動車、公共交通、徒歩)
- 経路検索ツール: 1-2回 (主要な移動手段の詳細)

**月間使用例:**
- 週4回使用: 約16-20リクエスト/月
- 毎日使用: 約90-180リクエスト/月

通常の個人使用では、無料枠(40,000リクエスト)を超えることはほぼありません。

### 使用量の確認

Google Cloud Consoleで使用量をモニタリングできます:

1. [Google Cloud Console](https://console.cloud.google.com/)
2. 「APIとサービス」→「ダッシュボード」
3. 各APIの使用状況グラフを確認

### 予算アラートの設定(推奨)

万が一の超過に備えて、予算アラートを設定することを推奨します:

1. Google Cloud Consoleで「お支払い」→「予算とアラート」
2. 「予算を作成」をクリック
3. 例: 月額$1のアラートを設定

## トラブルシューティング

### エラー: "GOOGLE_MAPS_API_KEY環境変数が設定されていません"

**原因:** `.env` ファイルにAPIキーが設定されていない

**解決方法:**
1. プロジェクトルートに `.env` ファイルがあるか確認
2. `GOOGLE_MAPS_API_KEY=your_key` の形式で記載されているか確認
3. アプリケーションを再起動

### エラー: "Google Maps APIエラー: REQUEST_DENIED"

**原因:** APIが有効化されていない、またはAPIキーが無効

**解決方法:**
1. Google Cloud Consoleで以下を確認:
   - Directions API が有効化されているか
   - Distance Matrix API が有効化されているか
2. APIキーが正しくコピーされているか確認
3. APIキーに不要な制限がかかっていないか確認

### エラー: "経路が見つかりませんでした"

**原因:** 入力された住所が不正確、または経路が存在しない

**解決方法:**
1. 出発地・目的地の住所を正確に入力
2. 有名なランドマーク名(駅名など)を使用
3. 移動手段を変更してみる(例: transitからdrivingへ)

### APIレスポンスが遅い

**原因:** Google Maps APIサーバーの一時的な遅延

**解決方法:**
- 通常は一時的な問題なので、数分後に再試行
- [Google Maps Platform Status](https://status.cloud.google.com/)でサービス状態を確認

## 使用例

### 基本的な使用法

週末プランナーを実行すると、transport_plannerが自動的にGoogle Maps APIツールを使用します:

```bash
uv run python main.py --date 2025-11-23
```

### 期待される出力例

```
交通手段の比較:

| 移動手段 | 所要時間 | 距離 | 備考 |
|---------|---------|------|------|
| 自動車 | 45分 | 32.5km | 渋滞時: 1時間15分 |
| 公共交通機関 | 1時間5分 | - | - |
| 徒歩 | 6時間30分 | 25.8km | - |

# 東京駅 → 横浜駅 の経路情報

**移動手段**: 公共交通機関
**出発時刻**: 2025年11月23日 09:00

## ルート 1

- **所要時間**: 28分
- **距離**: 31.2km

### 乗り換え詳細

1. **電車** (JR東海道本線)
   - 乗車: 東京
   - 下車: 横浜
   - 停車駅数: 5駅
   - 運賃: 480円

**合計運賃**: 約480円
```

## 参考リンク

- [Google Maps Platform ドキュメント](https://developers.google.com/maps/documentation)
- [Directions API リファレンス](https://developers.google.com/maps/documentation/directions/overview)
- [Distance Matrix API リファレンス](https://developers.google.com/maps/documentation/distance-matrix/overview)
- [料金計算ツール](https://developers.google.com/maps/billing-and-pricing/pricing)
- [APIキーのベストプラクティス](https://developers.google.com/maps/api-security-best-practices)

## サポート

問題が解決しない場合:
- [Google Maps Platform サポート](https://developers.google.com/maps/support)
- [Stack Overflow - google-maps](https://stackoverflow.com/questions/tagged/google-maps)
