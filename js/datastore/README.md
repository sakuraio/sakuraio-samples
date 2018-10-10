# sakura.io DataStore取得サンプル

JavaScriptを使用して、sakura.ioのDataStore連携サービスに接続し、メッセージを取得するサンプルです。


## 動作条件

- [sakura.io](https://sakura.io/) にモジュールを登録している
- [DataStore 連携サービス](https://sakura.io/docs/pages/spec/platform/data-integration/datastore.html) のトークンを取得している
  - トークンは `ecc3daf5-acd3-0a9c-90d1-fefeae194cc1` のような形式です
- Chrome, Firefox, Edge等のウェブブラウザを導入している


## 実行方法


- [index.html](https://sakuraio.github.io/sakuraio-samples/js/datastore/index.html) をブラウザで開く
- 取得したトークン等のパラメータを埋める
- 取得ボタンを押す

取得したJSON文字列が表示されれば成功です。