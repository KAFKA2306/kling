# 画像→動画 API

`api/image_to_video` は単一画像から動画を生成する Kling AI エンドポイントのクライアント実装です。`KlingClient` から `client.image_to_video` として利用できます。

## 主なファイル
- `image_to_video.py`: `ImageToVideoAPI` クラスを提供し、タスク作成・ステータス確認・一覧取得・完了待ち・動画ダウンロードをサポート。
- `_requests.py`: 生成パラメータ（プロンプト、解像度、再生時間など）を Pydantic で定義。
- `_response.py`: タスク状態や生成結果を表現するレスポンスモデル。
- `_exceptions.py`: API エラーやタスク失敗を表現する例外クラスとハンドラ。

## サポート機能
- `/v1/videos/image2video` 系エンドポイントとの通信。
- タスクが失敗・キャンセルした際の詳細なエラーメッセージ。
- `wait_for_task_completion` によるポーリングとタイムアウト制御。
- 保存用ヘルパー `download_video` による動画ファイルのストリーミング保存。

画像素材を起点に短編動画を生成するワークフローは本モジュールを通じて実行してください。
