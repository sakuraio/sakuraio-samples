# sakura.io WebSocket接続サンプル

C#を使用して、sakura.ioのWebSocket連携サービスに接続し、メッセージを受信するサンプルです。


## 動作条件

- [sakura.io](https://sakura.io/) にモジュールを登録している
- [WebSocket 連携サービス](https://sakura.io/docs/pages/spec/platform/data-integration/websocket.html) のトークンを取得している
  - トークンは `ecc3daf5-acd3-0a9c-90d1-fefeae194cc1` のような形式です
- [.NET Core 2.1](https://www.microsoft.com/net/download) 以上を導入している


## 実行方法


- `appsettings.sample.json` を `appsettings.json` にリネームします
- `appsettings.json` を編集し、上で取得したトークンを入力します

```
> dotnet restore   # 依存パッケージのインストールを行います
> dotnet run       # 実際のアプリケーションの実行を行います
```

受信したJSON文字列がリアルタイムに表示されれば成功です。
終了はCtrl+Cで行えます。
