# 概要

- データストアのメッセージを csv に書き込みます。

# 動作条件

- Python 3.6 で動作確認を行っています。

# 使い方

- `sakuraio-samples/python/datastore/` に行き、`main.py` を実行してください。

```
$ pwd

/path/to/sakuraio-samples/python/datastore/
```

- `-r` をつけることで全件取得して書き込みます。

```
$ python main.py -t <連携サービスのトークン> -r
```