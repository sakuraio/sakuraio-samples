# ファイルアップロードのサンプル実装

sakura.ioモジュールを使ってファイルを送信し、WebSocketサービス連携で接続した受信ソフトウエアでファイルを受信して保存するサンプル実装です。

## 送信側 (sakura.ioモジュール利用)

### Arduino

プログラムに埋め込まれた画像ファイルを起動時に一度送信する

### Raspberry Pi

#### sakuraio-upload.py

引数で指定されたファイルを送信する

```bash
python3 sakuraio-upload.py /tmp/photo.jpg
```

#### send-cam.sh

Raspberry Piのカメラで撮影した写真を送信する

```bash
bash send-cam.sh
```

## 受信側 (WebSocketサービス連携を利用)

モジュールから送信されたファイルをWebSocket経由で受信し、 `モジュールID-時刻.bin` としてカレントディレクトリに保存するサンプルです。

### Linux

```bash
./server/build/server_linux_amd64 wss://api.sakura.io/ws/v1/3c7ee813-8d5b-4a11-9b22-xxxxxxxxxxxx
```

### macOS

```bash
./server/build/server_darwin_amd64 wss://api.sakura.io/ws/v1/3c7ee813-8d5b-4a11-9b22-xxxxxxxxxxxx
```

### Windows

```bash
.\server\build\server_windows_amd64.exe wss://api.sakura.io/ws/v1/3c7ee813-8d5b-4a11-9b22-xxxxxxxxxxxx
```
