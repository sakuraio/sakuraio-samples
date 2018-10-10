# sakura.io DataStore取得サンプル

C#を使用して、sakura.ioのDataStore連携サービスに接続し、メッセージを取得するサンプルです。


## 動作条件

- [sakura.io](https://sakura.io/) にモジュールを登録している
- [DataStore 連携サービス](https://sakura.io/docs/pages/spec/platform/data-integration/datastore.html) のトークンを取得している
  - トークンは `ecc3daf5-acd3-0a9c-90d1-fefeae194cc1` のような形式です
- [.NET Core 2.1](https://www.microsoft.com/net/download) 以上を導入している


## 実行方法

```
> dotnet run       # 実際のアプリケーションの実行を行います

トークンを入力 >    # 取得したトークン文字列を入力もしくは貼り付けを行う
```

受信したJSON文字列が表示されれば成功です。
