# API クライアント群

`api` ディレクトリは Kling AI 各種エンドポイントへアクセスするための非同期クライアントを集約しています。HTTP 通信は共通で `httpx.AsyncClient` を利用し、例外処理やデータ検証を `_exceptions.py`・`_requests.py`・`_response.py` などのユーティリティモジュールで共有します。

## サブモジュール概要
- `text_to_video/`: テキストから動画を生成するエンドポイントをラップ。
- `image_to_video/` / `multi_image_to_video/`: 1 枚または複数画像から動画を作成。
- `image_generation/`: 静止画生成 API の呼び出しと結果管理。
- `video_extension/` / `video_effects/`: 既存動画の拡張やエフェクト適用を制御。
- `lip_sync/`: 音声に合わせたリップシンク動画の生成。
- `virtual_try_on/`: バーチャル試着（アバター合成）を扱うエンドポイント。
- `account_information_inquiry/`: 利用状況や課金情報の参照 API。
- `callback_protocol/`: 長時間バッチ処理のコールバック受信ワークフロー。

## テスト
各 API モジュールには `_tests` ディレクトリがあり、Pytest を用いたユニットテストで HTTP リクエストの検証や例外ハンドリングを確認しています。

## 拡張方法
新しいエンドポイントを追加する場合は、既存モジュールを参考に以下を実装してください。
1. リクエスト/レスポンス用の Pydantic モデル
2. 例外ハンドラとラッパー
3. クライアントクラス（`KlingClient` から登録）
4. テストケース
