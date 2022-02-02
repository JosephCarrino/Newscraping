#!/usr/bin/env python

from datetime import datetime, timedelta
from os import path
import json
import time
import requests

SCRIPTS_DIR = path.dirname(__file__)
PROJ_DIR = f"{SCRIPTS_DIR}/../"
API_URL = "https://api.nytimes.com/svc/topstories/v2"


def main():
    key = read_key("nyt")

    now = datetime.now()
    now_s = now.strftime("%Y-%m-%dT%H.%M.%S")
    now_epoch = (now - datetime(1970, 1, 1)) / timedelta(seconds=1)

    page_info = {
        "First_Page": f"{API_URL}/home.json?api-key={key}",
        "Abroad": f"{API_URL}/world.json?api-key={key}",
        "Politics": f"{API_URL}/politics.json?api-key={key}",
        "Economics": f"{API_URL}/business.json?api-key={key}",
    }

    for section_name, section_url in page_info.items():
        section_json_raw = requests.get(section_url).text
        obj = json.loads(section_json_raw)
        titles = []
        contents = [] #abstract
        urls = []
        dates = [] #published_date
        placeds = [] #subsections
        ranked = []
        more_info = []
        
        for i, result in enumerate(obj['results']):
            del result['multimedia']
            titles.append(result['title'])
            del result['title']
            contents.append(result['abstract'])
            del result['abstract']
            urls.append(result['url'])
            del result['url']
            dates.append(result['published_date'])
            del result['published_date']
            placeds.append(section_name)
            ranked.append(i)
            more_info.append(result)

        edition = []
        for i, item in enumerate(zip(titles, dates, urls, contents, ranked, placeds, more_info)):
            date = datetime.strptime(item[1][0:10], "%Y-%m-%d")
            date_raw = date.strftime("%B %d, %Y")
            date = date.strftime("%Y-%m-%d")

            scraped_info = {
                'title': item[0],
                'date_raw': date_raw,
                'date': date,
                'url': section_url,
                'news_url': item[2],
                'content': item[3],
                'ranked': item[4],
                'placed': item[5],
                'epoch': time.time(),
                'more_info': item[6]
            }
            if item[5] == "":
                scraped_info['placed'] = "First_Page"

            edition.append(scraped_info)

        base_name = f"{now_s}E{now_epoch}-{section_name.lower()}.json"
        scraped_data_dir = f"{PROJ_DIR}/collectedNews/flow/EN/NYT"
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
