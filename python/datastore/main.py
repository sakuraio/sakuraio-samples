import csv
import json
from urllib import request
from urllib.error import HTTPError
from urllib.parse import urljoin, urlparse
from optparse import OptionParser

HEADER = ["id", "module", "channel", "type", "value", "datetime"]

def parse_options():
    parser = OptionParser()
    parser.add_option("-H", "--host")
    parser.add_option("-t", "--token")
    parser.add_option("-r", "--recursive", action="store_true", default=False)
    return parser.parse_args()

def write_csv(url, recursive=False, writer=None, token=""):
    try:
        response = fetch(url)
    except HTTPError as error:
        print(error)
    if recursive:
        write_rows(writer, response)
        cursor = next_cursor(response)
        if cursor is not None:
            print(f"next cursor exists...{cursor}")
            ret = urlparse(url)
            next_url = f"{ret.scheme}://{ret.netloc}{ret.path}?cursor={cursor}&token={token}"
            write_csv(next_url, recursive=True, writer=writer, token=token)
    else:
        write_rows(writer, response)

def fetch(url):
    print(f"url...{url}\n")
    urlData = request.urlopen(url)
    data = urlData.read()
    encoding = urlData.info().get_content_charset("utf-8")
    return json.loads(data.decode(encoding))

def write_rows(writer, response):
    for msg in response["results"]:
        values = [msg[k] for k in HEADER]
        writer.writerow(values)

def next_cursor(response):
    return response["meta"]["cursor"]

if __name__ == "__main__":
    opt, args = parse_options()
    if opt.host is not None:
        url = urljoin(f"https://{opt.host}",
            f"datastore/v1/channels?token={opt.token}")
    else:
        url = f"https://api.sakura.io/datastore/v1/channels?token={opt.token}"
    f = open('./datastore.csv', 'w')

    writer = csv.writer(f, lineterminator="\n")
    # write header
    writer.writerow(HEADER)
    write_csv(url, writer=writer, recursive=opt.recursive, token=opt.token)
    f.close()