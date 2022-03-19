#!/usr/bin/env python

import json
import urllib.request
from datetime import datetime, timedelta
import time
from os import path
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

SCRIPTS_DIR = path.dirname(__file__)
PROJ_DIR = f"{SCRIPTS_DIR}/../"


def main():
    key = read_key("zeit")

    now = datetime.now()
    now_s = now.strftime("%Y-%m-%dT%H.%M.%S")
    now_epoch = (now - datetime(1970, 1, 1)) / timedelta(seconds=1)

    url= "https://api.zeit.de/content?fields=title+subtitle+href+release_date+&limit=50"
    hdr= { 'X-Authorization' : key }

    req = urllib.request.Request(url, headers=hdr)
    toGet = urllib.request.urlopen(req)
    objs= json.loads(toGet.read().decode("utf-8"))
    news= objs['matches']

    titles= []
    raw_dates= []
    dates= []
    urls= []
    contents= []

    for new in news:
        titles.append(new['title'])
        ddate= datetime.strptime(new['release_date'][0:10], "%Y-%m-%d")
        raw_dates.append(ddate.strftime("%B %d, %Y"))
        dates.append(ddate.strftime("%Y-%m-%d"))
        urls.append(new['href'])
        contents.append(new['subtitle'])

    i= 0
    edition= []
    for item in zip(titles, raw_dates, dates, urls, contents):
        scraped_info = {
            'title': item[0],
            'date_raw': item[1],
            'date': item[2],
            'url': url,
            'news_url': item[3],
            'content': item[4],
            'ranked': i,
            'epoch': time.time(),
            'language': "DE"
        }
        i+=1
        if(i <= 20):
            edition.append(scraped_info)

    base_name = f"{now_s}E{now_epoch}.json"
    scraped_data_dir = f"{PROJ_DIR}/collectedNews/flow/DE/Zeit"
    scraped_data_filepath = f"{scraped_data_dir}/{base_name}"
    with open(scraped_data_filepath, "w") as f:
        json.dump(edition, f, indent=4, ensure_ascii=False)
        f.write("\n")


def read_key(key_name: str) -> str:
    key_dir = f"{PROJ_DIR}/keys"

    with open(f"{key_dir}/{key_name}Key.txt", "r") as f:
        key = f.read()
    key = key.strip()

    return key


if __name__ == "__main__":
    main()          
