using System;
using System.Collections.Generic;
using System.Net.WebSockets;
using System.Threading;
using System.Threading.Tasks;
using System.Linq;
using System.Text;
using Microsoft.Extensions.Configuration;
using System.IO;

namespace csharp_websocket
{
    class Program
    {
        static async Task Main(string[] args)
        {
            // appsettings.jsonから設定の取得
            var config = new ConfigurationBuilder()
                .SetBasePath(Directory.GetCurrentDirectory())
                .AddJsonFile("appsettings.json")
                .Build();
            var endpoint = config["endpoint"];
            var token = config["token"];

            // WebSocketの接続先URIの設定
            var strUri = endpoint + token;
            Console.WriteLine("connection uri: " + strUri);

            // WebSocketコネクションの生成
            var ws = new ClientWebSocket();
            await ws.ConnectAsync(new Uri(strUri), CancellationToken.None);
            Console.WriteLine("started");
            
            var receiveBuffer = new ArraySegment<byte>(new byte[4096]);
            while (ws.State == WebSocketState.Open) {
                // 1行受信する毎にループが回る
                var result = await ws.ReceiveAsync(receiveBuffer, CancellationToken.None);
                
                if (result.MessageType == WebSocketMessageType.Text) {
                    var bytes = receiveBuffer.Take(result.Count).ToArray();
                    var text = Encoding.UTF8.GetString(bytes);

                    Console.WriteLine("Receive: " + text);
                }
            }
            Console.WriteLine("closed");
        }
    }
}
