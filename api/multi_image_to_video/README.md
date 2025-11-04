# 複数画像→動画 API

`api/multi_image_to_video` は複数の画像シーケンスから動画を生成する Kling AI エンドポイント向けのクライアントです。トランジション制御やアスペクト比の調整など、連続したフレーム生成に特化した機能を備えています。

## 主な構成
- `multi_image_to_video.py`: `MultiImageToVideoAPI` クラスと高レベルヘルパー `generate_multi_image_video` を提供。タスク作成・進捗監視・完了待機を実装。
- `_requests.py`: 画像リストやプロンプト、モード設定を Pydantic モデルで定義。
- `_response.py`: タスク結果とステータスを表現するレスポンスモデル。
- `_exceptions.py`: 失敗時に詳細情報を保持する独自例外とハンドラ。

## 主な機能
- `/v1/videos/multi-image-to-video` エンドポイントへのアクセス。
- タスクが失敗した際に `MultiImageToVideoTaskError` を発生させ、詳細メッセージを添付。
- コンビニエンス関数により、API キーのみで生成→完了待ち→動画取得までを一括実行。

スライドショーやアニメーションなど、複数の静止画を連結して動画化するユースケースで利用してください。
