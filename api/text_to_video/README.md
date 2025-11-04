# テキスト→動画 API

`api/text_to_video` ディレクトリは、テキストプロンプトから動画を生成する Kling AI の代表的なエンドポイントをラップします。

## 主なファイル
- `text_to_video.py`: `TextToVideoAPI` クラスを提供し、タスク作成 (`create`/`create_video`)、ステータス取得 (`get_status`)、非同期クライアント管理を実装。
- `_requests.py`: REST 呼び出し用の HTTP クライアントとリクエストボディの生成を担うヘルパー。
- `_response.py`: タスクステータスや生成結果を Pydantic モデルで表現。
- `_exceptions.py`: タスク失敗や API エラーを捕捉する例外階層とユーティリティ。

## 特徴
- プロンプトとネガティブプロンプト、カメラコントロール、アスペクト比、再生時間など細かなオプションをサポート。
- `wait_for_completion` を利用することで、ポーリングしながら完了を待つ高レベルワークフローを構築可能。
- `KlingClient` からは `client.text_to_video` で利用でき、`KlingConfig` に基づく認証とリトライ機構を共有します。

短尺動画の自動生成を行うマイクロサービスやバッチ処理で、本モジュールがエントリーポイントとなります。
