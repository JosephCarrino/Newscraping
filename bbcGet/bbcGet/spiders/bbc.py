#!/usr/bin/env python

import scrapy
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
import time
from os import path
import json
from datetime import datetime, timedelta

#classe per il contenuto eq5iqo00

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
    allowed_domains = ["www.bbc.com"]
    start_urls = ARCH_URLS

    def parse(self, response):
        #using scrapy css selectors to get informations I need"
        titles = response.css(".gs-c-promo-heading__title::text").getall()
        contents = response.css(".gs-c-promo-summary::text").getall()
        urls= response.css(".gs-c-promo-heading::attr(href)").getall()
        dates= response.css("time::attr(datetime)").getall()




        edition= []
        i= 0
        for item in zip(titles,contents,urls,dates):
            i+=1
            yield scrapy.Request("https://www.bbc.com" + item[2], callback=self.getFullContent, meta={'data': item, 'currelem': i, 'edition': edition, 'oldurl': response.url})
            

    def getFullContent(self, response):
        base_url= f"https://{BASE_URL}/"
        fullcont = response.css(".eq5iqo00::text").getall()
        toRet= ""
        for content in fullcont[1:len(fullcont)-1]:
            toRet+= content + ". "
        item = response.meta.get('data')
        date= item[3]
        try:
            date= datetime.strptime(item[3][:len(item[3])-6],"%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d")
        except:
            pass
        scraped_info = {
            'title': item[0],
            'date': date,
            'date_raw': date,
            'url': response.request.url,
            'news_url': "https://www.bbc.com" + item[2],
            'subtitle': item[1],
            'content': toRet,
            'placed': response.meta.get('oldurl').replace(base_url, "").replace("world", "Abroad").replace("politics", "Politics"),
            'epoch': time.time()               
        }
        #I still don't understand why the "replace" function doesn't work if I literally have the same string of "base_url"
        #so this is a raw debug
        if scraped_info['placed'] == base_url[0:len(base_url)-1]:
            scraped_info['placed']= "First_Page"

        response.meta.get('edition').append(scraped_info)
        if response.meta.get('currelem') == len(item):
            now = datetime.now()
            now_s = now.strftime("%Y-%m-%dT%H.%M.%S")
            now_epoch = (now - datetime(1970, 1, 1)) / timedelta(seconds=1)

            base_name = f"{now_s}E{now_epoch}.json"
            scraped_data_dir = f"{PROJ_DIR}/collectedNews/flow/EN/BBC"
            scraped_data_filepath = f"{scraped_data_dir}/{base_name}"
            with open(scraped_data_filepath, "w") as f:
                json.dump(response.meta.get('edition'), f, indent= 4, ensure_ascii=False)
                f.write("\n")
            