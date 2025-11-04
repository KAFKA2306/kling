# バーチャル試着 API

`api/virtual_try_on` は人物画像と衣服画像を合成し、バーチャル試着結果を生成する Kling AI のエンドポイントを扱うクライアントです。

## 主なファイル
- `virtual_try_on.py`: `VirtualTryOnAPI` クラスを提供し、タスク作成・ステータス確認・一覧取得を実装。API 応答コードを精査してエラーを投げ直します。
- `_requests.py`: 人物画像・衣服画像・モデル名などの入力を Pydantic モデル化。
- `_responses.py`: タスク生成応答 (`VirtualTryOnTaskResponse`) やステータス (`TaskResponse`) を定義。
- `_exceptions.py`: 認証、レート制限、タイムアウト、API エラーを区別する例外群。
- `_tests/`: FastAPI/HTTPX モックを使って動作確認するテストスイート。
- `__init__.py`: 公開 API を整理したエクスポートハブ。

## 機能
- `/v1/images/kolors-virtual-try-on` エンドポイントへの POST/GET。
- Base64/URL 形式の画像入力に対応し、コールバック URL の設定が可能。
- 失敗時には `APIError` や `TaskFailedError` を発生させ、`request_id` を保持。

アパレル EC やアバター生成など、衣服のバーチャルフィッティングを提供する機能で活用してください。
