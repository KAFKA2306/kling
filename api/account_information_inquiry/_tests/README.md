# テスト: アカウント情報照会

`api/account_information_inquiry/_tests` では Pytest を用いて課金情報 API ラッパーの動作を検証します。

## テスト内容
- `test_client.py`: HTTP クライアントのモックを通じて、エンドポイント `/account/costs` へのリクエストが正しく組み立てられるかを確認。
- `test_models.py`: `_requests.py` と `_responses.py` の Pydantic モデルが期待通りにバリデーションを行うかを検証。

## 実行方法
プロジェクトルートで `pytest api/account_information_inquiry/_tests` を実行すると、本ディレクトリのテストが走ります。非同期関数については `pytest-asyncio` を利用しています。
