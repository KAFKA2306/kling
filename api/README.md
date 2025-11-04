# API クライアント群

`api` ディレクトリは Kling AI 各種エンドポイントへアクセスするための非同期クライアントを集約しています。HTTP 通信は共通で `httpx.AsyncClient` を利用し、例外処理やデータ検証を `_exceptions.py`・`_requests.py`・`_response.py` などのユーティリティモジュールで共有します。

## API 一覧

### 1. account_information_inquiry
アカウント情報・リソースパッケージ照会（クレジット消費なし）

**エンドポイント:** `/account/costs`

**関数:**
- `get_account_costs(client, start_time, end_time, resource_pack_name=None)` - リソースパッケージ一覧と残量取得

**戻り値:** `AccountCostsResponse` - リソースパッケージ情報リスト

---

### 2. callback_protocol
非同期タスク完了通知受信（FastAPI ルーター）

**エンドポイント:** `/callbacks/kling` (受信側)

**関数:**
- `register_callback_handler(handler)` - コールバックハンドラーを登録
- `verify_callback_signature(request, secret, header_name="X-Kling-Signature")` - 署名検証
- `handle_kling_callback(request, callback_data)` - Kling AI からのコールバック受信

**戻り値:** `CallbackAckResponse` - 受信確認応答

---

### 3. image_generation
テキストプロンプトから画像生成

**エンドポイント:** `/v1/images/generations`

**クラス:** `KlingImageGenerator` (alias: `ImageGenerationClient`)

**メソッド:**
- `create_task(prompt, model_name="kling-1", negative_prompt=None, image=None, image_reference=None, image_fidelity=0.3, human_fidelity=None, n=1, aspect_ratio="1:1", callback_url=None)` - 画像生成タスク作成
- `get_task(task_id)` - タスクステータス取得
- `list_tasks(status=None, limit=10, offset=0)` - タスク一覧取得（ページネーション）
- `wait_for_task_completion(task_id, poll_interval=2, timeout=300)` - タスク完了まで待機

**戻り値:** `TaskResponse`, `TaskListResponse`

---

### 4. image_to_video
単一画像から動画生成

**エンドポイント:** `/v1/videos/image2video`

**クラス:** `ImageToVideoAPI`

**メソッド:**
- `create_task(request)` - 画像→動画生成タスク作成（`ImageToVideoRequest` 必須）
- `get_task_status(task_id)` - タスクステータス取得
- `list_tasks(limit=10, offset=0, status=None)` - タスク一覧取得
- `wait_for_task_completion(task_id, poll_interval=5.0, timeout=300.0)` - タスク完了まで待機
- `download_video(video_url, output_path, chunk_size=8192)` - 動画ダウンロード

**戻り値:** `VideoGenerationResponse`, `TaskListResponse`

---

### 5. lip_sync
音声に合わせたリップシンク動画生成

**エンドポイント:** `/v1/lip-sync`

**クラス:** `LipSyncAPI`

**メソッド:**
- `create_task(request)` - リップシンクタスク作成（`LipSyncRequest` または dict）
- `get_task(task_id)` - タスクステータス取得
- `list_tasks(query_params=None, status=None)` - タスク一覧取得
- `cancel_task(task_id)` - タスクキャンセル

**戻り値:** `LipSyncResponse`, `TaskData`, `TaskListResponse`

---

### 6. multi_image_to_video
複数画像から動画生成

**エンドポイント:** `/v1/videos/multi-image-to-video`

**クラス:** `MultiImageToVideoAPI`

**メソッド:**
- `create_video(request)` - 複数画像→動画生成タスク作成（`MultiImageToVideoRequest` 必須）
- `get_status(task_id)` - タスクステータス取得
- `wait_for_completion(task_id, poll_interval=5.0, timeout=300.0)` - タスク完了まで待機

**便利関数:**
- `generate_multi_image_video(image_list, api_key, prompt=None, negative_prompt=None, model_name="kling-v1-6", mode="std", duration=5, aspect_ratio="16:9", wait=True, poll_interval=5.0, timeout=300.0)` - 完全ワークフロー

**戻り値:** `MultiImageToVideoTask`, `TaskResponse`

---

### 7. text_to_video
テキストプロンプトから動画生成

**エンドポイント:** `/v1/videos/text2video`

**クラス:** `TextToVideoAPI`

**メソッド:**
- `create(prompt, negative_prompt=None, model_name="kling-v1", cfg_scale=0.5, mode="standard", camera_control=None, aspect_ratio="16:9", duration=5, callback_url=None, external_task_id=None)` - テキスト→動画生成タスク作成
- `get_status(task_id)` - タスクステータス取得
- `wait_for_completion(task_id, poll_interval=5.0, timeout=300.0)` - タスク完了まで待機
- `download_video(url)` - 動画ダウンロード
- `list_tasks(page=1, page_size=30)` - タスク一覧取得
- `generate(prompt, negative_prompt=None, model_name="kling-v1", cfg_scale=0.5, mode="standard", camera_control=None, aspect_ratio="16:9", duration=5, wait=True, poll_interval=5.0, timeout=300.0)` - 作成＋待機統合

**便利関数:**
- `generate_text_to_video(prompt, api_key, negative_prompt=None, model_name="kling-v1", cfg_scale=0.5, mode="standard", camera_control=None, aspect_ratio="16:9", duration=5, wait=True, poll_interval=5.0, timeout=300.0)` - スタンドアロン関数

**戻り値:** `TaskResponse`, bytes (動画データ)

---

### 8. video_effects
既存動画へのエフェクト適用

**エンドポイント:** `/v1/video-effects`

**クラス:** `VideoEffectsAPI`

**メソッド:**
- `create_task(**kwargs)` - ビデオエフェクトタスク作成（`CreateVideoEffectRequest` パラメータ）
- `get_task(task_id)` - タスクステータス取得
- `list_tasks(status=None, limit=10, cursor=None)` - タスク一覧取得（カーソルページネーション）
- `cancel_task(task_id)` - タスクキャンセル

**戻り値:** `CreateTaskResponse`, `GetTaskResponse`, `ListTasksResponse`, `CancelTaskResponse`

---

### 9. video_extension
既存動画の拡張（時間延長）

**エンドポイント:** `/v1/videos/video-extend`

**クラス:** `VideoExtensionAPI`

**メソッド:**
- `create_task(request, **kwargs)` - ビデオ拡張タスク作成（`VideoExtensionRequest` 必須）
- `get_task(task_id, **kwargs)` - タスクステータス取得
- `list_tasks(page_num=1, page_size=30, **kwargs)` - タスク一覧取得

**戻り値:** `VideoExtensionResponse`, `TaskStatusResponse`, `list[TaskStatusData]`

---

### 10. virtual_try_on
バーチャル試着（人物＋衣服画像合成）

**エンドポイント:** `/v1/images/kolors-virtual-try-on`

**クラス:** `VirtualTryOnAPI` (alias: `VirtualTryOnClient`)

**メソッド:**
- `create_task(human_image, cloth_image=None, model_name="kolors-virtual-try-on-v1-5", callback_url=None, **kwargs)` - 試着タスク作成
- `get_task_status(task_id)` - タスクステータス取得
- `list_tasks(page_num=1, page_size=30)` - タスク一覧取得
- `wait_for_completion(task_id, poll_interval=5.0, timeout=300.0)` - タスク完了まで待機

**戻り値:** `VirtualTryOnTaskResponse`, `TaskResponse`, `TaskListResponse`

---

## テスト
各 API モジュールには `_tests` ディレクトリがあり、Pytest を用いたユニットテストで HTTP リクエストの検証や例外ハンドリングを確認しています。

## 拡張方法
新しいエンドポイントを追加する場合は、既存モジュールを参考に以下を実装してください。
1. リクエスト/レスポンス用の Pydantic モデル
2. 例外ハンドラとラッパー
3. クライアントクラス（`KlingClient` から登録）
4. テストケース
