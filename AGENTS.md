# Repository Guidelines

## Authentication
Kling AI API は JWT (JSON Web Token) ベースの認証を使用します。`KlingConfig` は Access Key と Secret Key を受け取り、`generate_jwt_token()` メソッドで HS256 署名付き JWT を生成します。トークンは 30 分間有効で、`iss` (issuer) に Access Key、`exp` (expiration) と `nbf` (not before) を含みます。各 API リクエストでは `_get_headers()` が最新の JWT を生成し、`Authorization: Bearer {token}` ヘッダーとして送信します。

## Error Handling
Kling AI API は HTTP ステータスコードに加えて、レスポンスボディに `code` フィールドを含むエラーを返します。特に重要なエラーコード：
- **1102**: アカウント残高不足（HTTP 429 + `InsufficientBalanceError`）
- HTTP 429 はレート制限と残高不足の両方で使用されるため、`code` フィールドで判別が必要です
- `api/text_to_video/_requests.py:222-236` で `code: 1102` を検出し、適切な例外を raise します

## Project Structure & Module Organization
SDK のエントリーポイントは `client.py` と `config.py` で、`httpx` ベースのクライアント生成と JWT 認証を担います。ドメインごとの API 実装は `api/` 直下にあり、各フォルダは `_requests.py`, `_responses.py`,  `<feature>.py` で構成される。共通データモデルは `models/` に集約し、生成系・拡張系・課金系モデルを横断的に再利用します。ドキュメントは `_docs/` にまとめ、ユーザー向けガイドと法的情報を分類しています。`usecases/` では実運用を想定した高レベルオーケストレーション例を提供し、サンプルコードからクライアント統合のベストプラクティスを学べます。テストはモジュール単位で `_tests/` フォルダに分散しており、例えば `api/virtual_try_on/_tests` が該当 API の検証を担当します。

## Build, Test, and Development Commands
依存関係の解決は `uv` の利用を推奨しています。初回は次を実行し、仮想環境と依存性を同期させてください。
```
uv sync install kling-ai-sdk
```
開発時は `uv run python -m pytest` で全テストを走らせ、対象 API のみ検証する際は `pytest api/image_to_video/_tests -k create_task` のようにパスやキーワードで絞り込みます。実装中のファイルだけ動作確認したい場合は `uv run python -m pytest --maxfail=1 path/to/tests` を活用します。非同期コードの再現確認には `uv run python -m asyncio` を利用すると、イベントループと整合した実行が可能です。Markdown ドキュメントはローカルエディタでプレビューし、更新後は PR 説明に差分の意図を記載してください。

## Coding Style & Naming Conventions
コメント禁止。エラーハンドリング禁止。例外禁止。th二重実装禁止。ハードコーディング禁止。DRYの原則必須。二重実装禁止。常に最小コードで機能を実現するようにスリム化する。
Python 3.11 互換、4 スペースインデント、型ヒント必須が基本方針です。Pydantic モデルには `Field(..., description=...)` を付与し、公開 API は `__all__` で明示的に制御してください。例外クラスは `<Feature>Error` の命名、HTTP クライアントは `<Feature>API` のクラス名で統一します。Docstring は一行サマリ＋詳細記述形式を採用し、Markdown でのコード例と整合するように保守します。ロガーは `logging.getLogger(__name__)` を使用し、通信層ではシリアライズ前後で機密情報を記録しないよう注意してください。

## Testing Guidelines
適切なディレクトリで実施。最小のコードになるように常に削減。フレームワークは Pytest を標準とし、`pytest-asyncio` で非同期タスクを検証します。テストファイル名は `test_<subject>.py` とし、正常系に加えてリトライや例外経路をカバーしてください。最低限、導入前に `pytest --maxfail=1 --disable-warnings` が成功することを確認し、CI での実行を想定した決 deterministic なテストを維持します。負荷試験や大容量レスポンスの検証では `_tests` 内にサンプルペイロードを追加し、`pytest --durations=10` で遅延を監視します。

## Commit & Pull Request Guidelines
コミットメッセージは命令形の 1 行目（72 文字以内）を基本とし、必要に応じて `feat:`, `fix:`, `docs:`, `test:` のような接頭辞を使用します。複数ファイルに跨る変更は論理的な単位で分割し、ビルドやテストに影響のある変更は同じコミットで検証結果を得てください。PR は「目的」「主要変更点」「テスト結果」「ロールバック手順」を箇条書きで記述し、影響するモジュール（例: `api/video_effects`, `models/video_extension.py`）を明記してください。スクリーンショットが不要なコード変更でも、ログやサンプルレスポンスなど確認に役立つ補足情報を添えます。レビュー前に `git status -sb` で不要ファイルが紛れ込んでいないか確認することも推奨します。

## Security & Configuration Tips
API キーやシークレットは `.env` に保存して動的に読み込み、`.gitignore` で除外状態を維持してください。`api/callback_protocol` を利用する場合は署名検証を必ず有効化し、テスト環境でもフェイルクローズ戦略を保ちます。タイムアウトやリトライ回数を変更する際は `config.py` のデフォルト値を根拠付きで見直し、PR 説明に設定差分を記録することで将来的なトラブルシューティングを容易にします。顧客データや生成結果の URL をログに出力する際はマスキングを行い、保存先の権限管理を徹底してください。
