#!/usr/bin/env python

import scrapy
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
import time
from os import path
import json
from datetime import datetime, timedelta

SCRIPTS_DIR = path.dirname(__file__)
PROJ_DIR = f"{SCRIPTS_DIR}/../../../"
BASE_URL = f"www.bbc.com/news"
ARCH_URLS = [
    f"https://{BASE_URL}",
    f"https://{BASE_URL}/world/",
    f"https://{BASE_URL}/politics"
]

class BbcSpider(scrapy.Spider):
    name = 'bbc'
    allowed_domains = [BASE_URL]
    start_urls = ARCH_URLS

    def parse(self, response):
        #using scrapy css selectors to get informations I need
        base_url= f"https://{BASE_URL}/"
        titles = response.css(".gs-c-promo-heading__title::text").getall()
        contents = response.css(".gs-c-promo-summary::text").getall()
        urls= response.css(".gs-c-promo-heading::attr(href)").getall()
        dates= response.css("time::attr(datetime)").getall()

        now = datetime.now()
        now_s = now.strftime("%Y-%m-%dT%H.%M.%S")
        now_epoch = (now - datetime(1970, 1, 1)) / timedelta(seconds=1)


        edition= []
        for item in zip(titles,contents,urls,dates):
            date= item[3][0:len(item[3])-5]
            try:
                date= datetime.strptime(date,"%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d")
            except:
                pass
            scraped_info = {
                'title': item[0],
                'date': date,
                'date_raw': date,
                'url': response.request.url,
                'news_url': "https://www.bbc.com" + item[2],
                'content': item[1],
                'placed': response.url.replace(base_url, "").replace("world", "Abroad").replace("politics", "Politics"),
                'epoch': time.time()               
            }
            #I still don't understand why the "replace" function doesn't work if I literally have the same string of "base_url"
            #so this is a raw debug
            if scraped_info['placed'] == base_url[0:len(base_url)-1]:
                scraped_info['placed']= "First_Page"
            
            edition.append(scraped_info)
            
        base_name = f"{now_s}E{now_epoch}.json"
        scraped_data_dir = f"{PROJ_DIR}/collectedNews/flow/EN/BBC"
        scraped_data_filepath = f"{scraped_data_dir}/{base_name}"
        with open(scraped_data_filepath, "w") as f:
            json.dump(edition, f, indent= 4, ensure_ascii=False)
            f.write("\n")