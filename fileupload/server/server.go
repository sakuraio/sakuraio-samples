package main

import (
	"encoding/hex"
	"encoding/json"
	"os"
	"time"

	"github.com/sirupsen/logrus"
	"github.com/urfave/cli"
	"golang.org/x/net/websocket"
)

type FileBuffer struct {
	Module   string
	Size     int
	Sequence int
	Data     []byte
	Logger   *logrus.Entry
}

type Channel struct {
	Type    string           `json:"type"`
	Channel int              `json:"channel"`
	Value   *json.RawMessage `json:"value"`
}

type ChannelPayload struct {
	Channels []Channel `json:"channels"`
}

type ChannelMessage struct {
	Type    string         `json:"type"`
	Module  string         `json:"module"`
	Payload ChannelPayload `json:"payload"`
}

var (
	log     = logrus.New()
	origin  = "https://api.sakura.io/"
	buffers = map[string]*FileBuffer{}
)

func main() {
	logrus.SetLevel(logrus.DebugLevel)

	app := cli.NewApp()

	app.Name = "sakuraio upload sample"
	app.Usage = "connect to websocket and receive uploaded file"
	app.Version = "0.0.1"

	app.Action = func(context *cli.Context) error {
		url := context.Args().Get(0)
		ws, err := websocket.Dial(url, "", origin)
		if err != nil {
			log.Fatal(err)
		}
		log.Infof("Connected to %s", url)
		return receiveLoop(ws)
	}

	app.Run(os.Args)
}

func receiveLoop(ws *websocket.Conn) error {
	for {
		var channelMessage ChannelMessage
		err := websocket.JSON.Receive(ws, &channelMessage)
		if err != nil {
			log.Errorf("Connection closed %s", err)
			return err
		}

		if channelMessage.Type != "channels" {
			continue
		}

		switch channelMessage.Payload.Channels[0].Channel {
		case 1:
			// Start
			var size int
			json.Unmarshal(*channelMessage.Payload.Channels[0].Value, &size)
			startUpload(channelMessage.Module, size)

		case 2:
			// Chunk
			var sequence int
			json.Unmarshal(*channelMessage.Payload.Channels[0].Value, &sequence)

			data := make([]byte, 0)
			for _, c := range channelMessage.Payload.Channels[1:] {
				var hexstring string
				json.Unmarshal(*c.Value, &hexstring)
				d, _ := hex.DecodeString(hexstring)
				data = append(data, d...)
			}

			receiveChunk(channelMessage.Module, sequence, data)

		case 3:
			// Finish
			finishUpload(channelMessage.Module)

		default:
			log.Warnf("Invalid Channel ID %d", channelMessage.Payload.Channels[0].Channel)
		}
	}
	return nil
}

func NewFileBuffer(module string, size int) *FileBuffer {
	return &FileBuffer{
		Module:   module,
		Size:     size,
		Sequence: -1,
		Data:     []byte{},
		Logger:   logrus.WithField("module", module),
	}
}

func startUpload(module string, size int) {
	f := NewFileBuffer(module, size)
	buffers[module] = f
	f.Logger.Infof("Start download size=%d", size)
}

func receiveChunk(module string, sequence int, data []byte) {
	fileBuffer, ok := buffers[module]
	if !ok {
		log.Warnf("Invalid module %s", module)
		return
	}

	if sequence != fileBuffer.Sequence+1 {
		fileBuffer.Logger.Warnf("Invalid Sequence %d", sequence)
		return
	}
	fileBuffer.Logger.Debugf("Chunk sequence=%d", sequence)
	fileBuffer.Data = append(fileBuffer.Data, data...)
	fileBuffer.Sequence = sequence
}

func finishUpload(module string) {
	fileBuffer, ok := buffers[module]
	if !ok {
		log.Warnf("Invalid module %s", module)
		return
	}
	defer func() {
		delete(buffers, module)
	}()

	filename := module + "-" + time.Now().Format("20060102_150405") + ".bin"
	fileBuffer.Logger.Infof("finishUpload save to %s", filename)

	file, err := os.Create(filename)
	if err != nil {
		fileBuffer.Logger.Errorf("open file error %s", err)
		return
	}
	defer file.Close()

	if len(fileBuffer.Data) < fileBuffer.Size {
		fileBuffer.Logger.Warnf("Invalid data size %d", len(fileBuffer.Data))
	}

	_, err = file.Write(fileBuffer.Data[:fileBuffer.Size])
	if err != nil {
		fileBuffer.Logger.Errorf("write file error %s", err)
	}
}
