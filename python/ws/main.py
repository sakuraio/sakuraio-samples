import sys
from optparse import OptionParser
from websocket import create_connection

parser = OptionParser()
parser.add_option("-u", "--url", dest="url", help="set url from each project, ex) python main.py -u wss://api.sakura.io/ws/v1/******")
(options, args)= parser.parse_args()
url = options.url
if url is None:
    print("plese set url, ex) python main.py -u wss://api.sakura.io/ws/v1/****** ")
    print("program exit")
    sys.exit(0)
if not url.startswith("wss"):
    print("invalid url")
    sys.exit(0)

ws = create_connection(url)

print("start connecting to server")

while True:
    message = ws.recv()
    print(f"receive...{message}")

ws.close()