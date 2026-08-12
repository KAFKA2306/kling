# Kling AI Python SDK

Kling AI API と連携するための型安全な Python SDK です。動画生成からアカウント管理まで、すべてのエンドポイントを 1 つのクライアントから呼び出せます。

## ✨ Features
- Text-to-Video / Image-to-Video / Multi-Image / Video Extension など主要生成機能をカバー
- httpx ベースの非同期クライアントと Pydantic v2 による型安全なリクエスト・レスポンス
- `KlingClient` シングルトンとサブクライアントのモジュール化で拡張が容易
- provider-neutral な `VideoStoryboard` を Kling request plan へ決定論的に compile

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

## 🎞️ Storyboard IR

`models/storyboard.py` は provider 固有の prompt や endpoint ではなく、時間軸・Shot・構図・動き・文字演出・参照素材・禁止事項を正準データとして保持します。

```text
Evidence / Script
  → VideoStoryboard
  → Shot
  → KlingStoryboardCompiler
  → Kling request plan
  → KlingClient
  → task / generated artifact
```

`usecases/storyboard.py` は現行 SDK の request model で保持できる内容だけを compile します。

- 参照素材なし → `/v1/videos/text2video`
- first frame + optional last frame → `/v1/videos/image2video`
- reference image 1〜4枚 → `/v1/videos/multi-image-to-video`
- duration は 5 秒または 10 秒を厳密に要求し、別の長さを自動丸めしない
- aspect ratio は現行 request model と一致する `16:9` / `9:16` / `1:1` のみ
- 現行 Storyboard adapter が lossless に表現できない reference video/audio は fail closed

compile 自体はネットワークを使用しません。実送信する場合だけ `KlingStoryboardAdapter.submit()` が既存 `KlingClient.post()` を利用します。

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

`pytest-asyncio` と `httpx.AsyncClient` のモックを利用し、レート制限・タイムアウトなどの経路をカバーしてください。Storyboard のテストは request plan の compile と fake client 送信までで停止し、実APIは呼びません。

## 📁 Repository Map
- `client.py` / `config.py` : SDK エントリーポイント
- `api/` : ドメイン別 API 実装（例: `api/text_to_video`）
- `models/` : 共通 Pydantic モデル群。`models/storyboard.py` が provider-neutral IR
- `_docs/` : ユーザーガイドおよび法的情報
- `usecases/` : 実運用を想定したオーケストレーション例。`usecases/storyboard.py` が Kling adapter
- `tests/` : 共通テストユーティリティ、各 API のテストは `api/<feature>/_tests`

## 📚 Additional Resources
- API リファレンスとガイド: `_docs/`
- 拡張シナリオのサンプルコード: `usecases/`
- 既知の制限やリリースノート: `AGENTS.md`, `CLAUDE.md`

バージョンアップ時は `_docs/` に移行手順を追記し、`config.py` のデフォルト値変更は PR 説明に根拠を明記してください。
