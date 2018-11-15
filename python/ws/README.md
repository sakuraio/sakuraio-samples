# 概要

- Python で websocket の連携サービスに接続し、メッセージを受け取り表示するサンプルです。
- python 3.6 以降での動作を確認しています。

# 動作条件

- プロジェクトにモジュールを登録し、モジュールから sakura.io へメッセージを送信してください。
- Websocket の連携サービスを作成し、URL を取得します。
  - 参考リンク: [WebSocket の連携サービス追加](https://sakura.io/docs/pages/guide/tutorial/service/websocket.html#id1)

# 実行方法

- 下記のようにディレクトリを移動し、以下のように実行してください。

```
$ pwd
/path/to/sakuraio-samples/python/ws

$ pip install -r requirements.txt

$ python main.py -u wss://api.sakura.io/ws/v1*****
```

- 成功している場合、下記のように `connection` や `channels` のメッセージが表示されます

```
$ python main.py -u wss://api.sakura.io/ws/v1/***********

start connecting to server
receive...{"module":"test-module","type":"connection","datetime":"2018-10-02T10:01:07.519946727Z","payload":{"is_online":true}}
receive...{"module":"test-module","type":"channels","datetime":"2018-10-02T10:01:07.964050849Z","payload":{"channels":[{"channel":0,"type":"l","value":0,"datetime":"2018-10-02T10:01:07.96405302Z"}]}}
```