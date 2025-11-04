# Kling AI Python SDK

Kling AI API と連携するための型安全な Python SDK です。動画生成からアカウント管理まで、すべてのエンドポイントを 1 つのクライアントから呼び出せます。

## ✨ Features
- Text-to-Video / Image-to-Video / Multi-Image / Video Extension など主要生成機能をカバー
- httpx ベースの非同期クライアントと Pydantic v2 による型安全なリクエスト・レスポンス
- `KlingClient` シングルトンとサブクライアントのモジュール化で拡張が容易

## 🚀 Installation
```bash
uv sync install kling-ai-sdk
```

## 🔑 Configuration
SDK は `KlingConfig` を通じて Access Key と Secret Key を受け取り、JWT トークンを生成して認証します。

```python
from config import KlingConfig

config = KlingConfig(
    api_key="YOUR_ACCESS_KEY",
    secret_key="YOUR_SECRET_KEY"
)
```

開発環境では `.env` に設定：
```
KLING_ACCESS_KEY="your_access_key"
KLING_SECRET_KEY="your_secret_key"
```

**重要**: Kling AI API を使用するには、アカウントにクレジット残高が必要です。残高不足の場合は `InsufficientBalanceError` (code: 1102) が発生します。

## 📦 Core APIs
- `client.text_to_video` : テキストから動画タスクの作成とポーリング
- `client.image_to_video` : 静止画を動画へ変換
- `client.multi_image_to_video` : 複数画像からのストーリー生成
- `client.video_extension` : 既存動画の延長やエフェクト適用
- `api/account_information_inquiry` : 利用状況・コストの取得
- `api/callback_protocol` : 非同期タスクのコールバック登録

各 API フォルダには `_requests.py`（入力バリデーション）、`_response.py`（レスポンス構造）、`<feature>.py`（ビジネスロジック）が配置されています。

## 🧪 Testing
```bash
uv run python -m pytest --maxfail=1 --disable-warnings
uv run python -m pytest api/image_to_video/_tests -k create_task
uv run python -m pytest --durations=10
```

`pytest-asyncio` と `httpx.AsyncClient` のモックを利用し、レート制限・タイムアウトなどの経路をカバーしてください。

## 📁 Repository Map
- `client.py` / `config.py` : SDK エントリーポイント
- `api/` : ドメイン別 API 実装（例: `api/text_to_video`）
- `models/` : 共通 Pydantic モデル群
- `_docs/` : ユーザーガイドおよび法的情報
- `usecases/` : 実運用を想定したオーケストレーション例
- `tests/` : 共通テストユーティリティ、各 API のテストは `api/<feature>/_tests`

## 📚 Additional Resources
- API リファレンスとガイド: `_docs/`
- 拡張シナリオのサンプルコード: `usecases/`
- 既知の制限やリリースノート: `AGENTS.md`, `CLAUDE.md`

バージョンアップ時は `_docs/` に移行手順を追記し、`config.py` のデフォルト値変更は PR 説明に根拠を明記してください。
