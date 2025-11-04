# 動画エフェクト API

`api/video_effects` には既存動画へスタイル変換や効果適用を行う Kling AI Video Effects サービスのクライアントが収められています。

## 主なファイル
- `video_effects.py`: `VideoEffectsAPI` クラスを提供し、タスク作成・取得・一覧・キャンセルを実装。HTTP リトライや詳細な例外マッピングを内蔵。
- `_requests.py`: エフェクト種別やスタイル参照 URL などを含むリクエストモデルと、タスクリストのクエリパラメータを定義。
- `_responses.py`: タスク作成 (`CreateTaskResponse`)、ステータス取得 (`GetTaskResponse`)、一覧 (`ListTasksResponse`) などのレスポンスモデルを保持。
- `_exceptions.py`: 認証エラー、レート制限、サーバエラーなどを区別する例外クラスとハンドリング関数。
- `_tests/`: タスク操作が期待通りの HTTP メソッド・エンドポイントで行われるかを検証するテスト。
- `__init__.py`: パッケージ外からインポートしやすいように公開 API を再エクスポート。

## 特徴
- ベース URL やタイムアウト、最大リトライ回数を柔軟に設定可能。
- レスポンスコードに応じて `VideoEffectsRateLimitError` や `VideoEffectsUnauthorizedError` など適切な例外を送出。
- `204 No Content` に対応し、削除系操作のハンドリングも容易。

ポストプロダクションやコンテンツ加工を自動化するワークフローで活用してください。
