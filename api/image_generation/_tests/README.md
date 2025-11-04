# テスト: 画像生成 API

`api/image_generation/_tests` には画像生成クライアントのユニットテストが配置されています。HTTP 通信をモックしながら、Pydantic モデルの妥当性とタスク操作の制御フローを検証します。

## 主なテスト
- `test_client.py`: `create_task`・`get_task`・`list_tasks`・`wait_for_task_completion` が期待通りのエンドポイントを呼び出すか、およびタイムアウト処理が適切かを確認。

## 実行方法
ルートディレクトリから `pytest api/image_generation/_tests` を実行してください。非同期テストには `pytest-asyncio` を利用しています。
