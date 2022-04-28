#!/usr/bin/env python

import scrapy
from scrapy.http import HtmlResponse
from scrapy import Selector
from datetime import datetime, timedelta
import time
from os import path
import json

SCRIPTS_DIR = path.dirname(__file__)
PROJ_DIR = f"{SCRIPTS_DIR}/../../../"
BASE_URL = f"www.agi.it"
RSS_URL = f"https://www.agi.it/estero/rss"


class AgigetSpider(scrapy.Spider):
    name = 'agiGet'
    allowed_domains = [BASE_URL]
    start_urls = [RSS_URL]

    def dateFormatter(self, dates_raw):
        dates= []
        for raw_date in dates_raw:
            if raw_date == "":
                dates.append(datetime.now().strftime("%Y-%m-%d"))
            else:
                raw_date = raw_date[5:16]
                todate = datetime.strptime(raw_date, "%d %b %Y")
                dates.append(todate.strftime("%Y-%m-%d"))
        return dates

    def parse(self, response):
        articles = response.css("item")

        titles= []
        dates_raw= []
        urls= []
        contents= []

        for article in articles:
            titles.append(article.css("title::text").get())
            contents.append(article.css("description::text").get().replace("<p>", "").replace("<strong>", "").replace("</p>", "").replace("</strong", ""))
            dates_raw.append(article.css("pubDate::text").get())
            urls.append(article.css("link::text").get())

        dates= self.dateFormatter(dates_raw)

        edition= []
        i= 0
        for item in zip(titles, dates_raw, dates, urls, contents):
            i+=1
            scraped_info = {
                'title': item[0],
                'date_raw': item[1],
                'date': item[2],
                'url': response.request.url,
                'news_url': item[3],
                'subtitle': "",
                "content": item[4],
                'ranked': i,
                'placed': "Abroad",
                'epoch': time.time(),
                'language': 'IT',
                'source': "AGI"
            }
            edition.append(scraped_info)
        
        now = datetime.now()
        now_s = now.strftime("%Y-%m-%dT%H.%M.%S")
        now_epoch = (now - datetime(1970, 1, 1)) / timedelta(seconds=1)

        base_name = f"{now_s}E{now_epoch}.json"
        scraped_data_dir = f"{PROJ_DIR}/collectedNews/flow/IT/AGI"
        scraped_data_filepath = f"{scraped_data_dir}/{base_name}"
        with open(scraped_data_filepath, "w") as f:
            json.dump(edition, f, indent= 4, ensure_ascii=False)
            f.write("\n")

        pass
