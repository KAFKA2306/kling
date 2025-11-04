# Kling AI Python SDK

Kling AI API と連携するための最新かつ型安全な Python SDK です。動画生成、画像処理、アカウント管理を含むすべての Kling AI サービスに、直感的でわかりやすいインターフェースを提供します。

## ✨ 特長

- **完全な API カバレッジ**: すべての Kling AI エンドポイントをサポート
- **型安全性**: 実行時型チェックのために Pydantic v2 を採用
- **Async/Await 対応**: HTTPX によるネイティブな非同期サポート

## 🚀 インストール

```bash
uv sync install kling-ai-sdk
```

## 📚 クイックスタート

### 基本的な使用例

```python
from kling.client import KlingClient
from kling.api.text_to_video import TextToVideoRequest

async def main():
    # API キーでクライアントを初期化
    client = KlingClient(api_key="your-api-key")

    # テキストから動画を生成するリクエストを作成
    request = TextToVideoRequest(
        prompt="A beautiful sunset over mountains",
        duration=5.0,
        resolution="1920x1080"
    )

    # リクエストを送信
    response = await client.text_to_video(request)
    print(f"Video generation started with ID: {response.task_id}")

# 非同期関数を実行
import asyncio
asyncio.run(main())
```

## 📦 API モジュール

### アカウント情報
- リソースパッケージと利用状況の確認
- アカウントの制限やクォータの確認

```python
from kling.api.account_information_inquiry import get_account_costs

async def check_usage():
    client = KlingClient(api_key="your-api-key")
    response = await get_account_costs(
        client=client,
        start_time=start_timestamp,
        end_time=end_timestamp
    )
    return response
```

### コールバックプロトコル
- 長時間タスクの非同期コールバック処理
- タスク更新と完了のハンドリング

```python
from kling.api.callback_protocol import CallbackRequest, register_callback_handler

@register_callback_handler
def handle_callback(callback: CallbackRequest):
    print(f"Received callback for task {callback.task_id}")
    print(f"Status: {callback.task_status}")
    if callback.task_result:
        print(f"Result URL: {callback.task_result.video_url}")
```

### メディア生成
- テキストから動画を生成
- 画像から動画へ変換
- 複数画像からの動画生成
- 動画エフェクトと後処理
- バーチャル試着機能

```python
# テキストから動画
from kling.api.text_to_video import TextToVideoRequest

# 画像から動画
from kling.api.image_to_video import ImageToVideoRequest

# 動画エフェクト
from kling.api.video_effects import apply_effect
```

## 🔧 設定

環境変数またはコード上でクライアントを設定できます。

```python
from kling.client import KlingClient

# カスタム設定で初期化
client = KlingClient(
    api_key="your-api-key",
    base_url="https://api.kling.ai/v1",
    timeout=30.0,
    max_retries=3
)
```

### 環境変数

```bash
export KLING_API_KEY="your-api-key"
export KLING_BASE_URL="https://api.kling.ai/v1"
export KLING_TIMEOUT=30
```
