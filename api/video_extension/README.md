# 動画拡張 API

`api/video_extension` は既存動画を入力としてシーン延長やエフェクト付与を行う Kling AI Video Extension サービスのクライアント実装です。

## 主なファイル
- `video_extension.py`: `VideoExtensionAPI` クラスを提供し、タスク作成・ステータス取得・リトライ制御を実装。`tenacity` を使ったレートリミット再試行やレスポンスのバリデーションを行います。
- `_requests.py`: タスク作成・一覧のクエリパラメータを Pydantic モデルで定義。
- `_responses.py`: タスク状態 (`TaskStatusResponse` / `TaskStatusData`) やエラーメッセージを構造化。
- `_exceptions.py`: レート制限・サーバエラー・タイムアウトなどを細分化した例外とハンドラをまとめる。

## 機能
- `/v1/videos/video-extend` エンドポイントに対して POST/GET を発行。
- バリデーションエラー時には `VideoExtensionValidationError` を発生させ、レスポンス形式が想定外の場合にも安全に失敗。
- タスク終端状態（成功/失敗）でログにトレースを残すため、運用監視に統合しやすい設計。

動画の延長編集や再生成を自動化するマイクロサービスで活用してください。
