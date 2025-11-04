# アカウント情報照会 API

`api/account_information_inquiry` ディレクトリは、Kling AI アカウントの利用状況や課金情報を取得するためのラッパーを提供します。

## 主な構成
- `account_infomration_inquiry.py`: リソースパックの利用量を取得する非同期ユーティリティ関数 `get_account_costs` を提供。
- `_requests.py`: クエリパラメータを Pydantic モデルで表現。
- `_responses.py`: API 応答を型安全にパースするレスポンスモデル。
- `_tests/`: QPS 制限や期間フィルタが正しく反映されるかを確認するテスト。

## 利用シナリオ
- 指定期間内のリソース消費量の把握
- プリペイドパックの残量をダッシュボードで可視化
- 請求オートメーションのバックエンド処理

`get_account_costs` は `datetime` もしくはミリ秒単位の Unix タイムスタンプを受け取り、必要に応じて変換を行います。レート制限 (QPS <= 1) を厳守した上でご利用ください。
