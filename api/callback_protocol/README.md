# コールバックプロトコル

`api/callback_protocol` は Kling AI の非同期タスクが完了した際に送られてくるコールバックを受信・検証するための FastAPI ルーターを提供します。

## 主な構成
- `callback_protocol.py`: 署名検証・バリデーション・ハンドラ登録を行うエントリーポイント。`register_callback_handler` でアプリ固有の処理を差し込めます。
- `_requests.py` / `_responses.py`: コールバックボディおよび ACK 応答を Pydantic モデルで定義。
- `_exceptions.py`: バリデーションエラーやセキュリティエラーを表現する独自例外。
- `_utils.py`: HMAC 署名検証などのユーティリティ。
- `_tests/`: FastAPI テストクライアントを使ったルート検証。

## 想定ワークフロー
1. `verify_callback_signature` でヘッダーの署名を検証。
2. `CallbackRequest` モデルでペイロードを構造化。
3. `register_callback_handler` で設定した非同期処理に渡して、動画 URL などの成果物を保存。

Kling AI の非同期ジョブ（動画生成など）を本番運用に組み込む際の入口となるモジュールです。
