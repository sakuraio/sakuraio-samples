using System;
using System.Net.Http;
using System.Threading.Tasks;

namespace datastore
{
    class Program
    {
        static async Task Main(string[] args)
        {
            var client = new HttpClient();
            Console.Write("トークンを入力 > ");
            var token = Console.ReadLine();
            var url = "https://api.sakura.io/datastore/v1/messages?token=" + token;
            var result = await client.GetStringAsync(url);
            Console.WriteLine(result);
        }
    }
}
