#!/usr/bin/env python

import scrapy
import json
from os import path
from datetime import datetime, timedelta
from datetime import date
import time
import urllib.request

SCRIPTS_DIR = path.dirname(__file__)
PROJ_DIR = f"{SCRIPTS_DIR}/../../../"
BASE_URL = f"www.servizitelevideo.rai.it/televideo/pub"
CATE_URL = f"http://www.servizitelevideo.rai.it/televideo/pub/solotesto.jsp?categoria="
ARCH_URLS = [
    f"{CATE_URL}Prima&pagina=103",
    f"{CATE_URL}Politica&pagina=120",
    f"{CATE_URL}Politica&pagina=130",
    f"{CATE_URL}Dal%20Mondo&pagina=150"
]

class TelegetSpider(scrapy.Spider):
    
    cate_conv= {'0': "First_Page",
                '1': "Undefinied",
                '2': "Politics",
                '3': "Economics",
                '4': "Italy",
                '5': "Abroad",
                '6': "Cultures"}
    
    base_url= "https://www.servizitelevideo.rai.it/televideo/pub/solotesto.jsp?pagina="
    
    name = 'teleGet'
    allowed_domains = [BASE_URL]
    start_urls = ARCH_URLS
    
    def stringFormat(self, s):
        return s.replace('\n', ' ').replace('\\', '').replace('  ', ' ').strip()

    def parse(self, response):
        content= response.css("pre")
        titleString= content.css("::text").getall()
        titleString= titleString[0:len(titleString)-1]
        titles= []
        urls= []
        contents= []
        placed= []
        ranked= []
        
        now = datetime.now()
        now_s = now.strftime("%Y-%m-%dT%H.%M.%S")
        now_epoch = (now - datetime(1970, 1, 1)) / timedelta(seconds=1)
       
        edition= []
        i= 0
        for info in titleString:
            if i%2 == 0:
                titles.append(self.stringFormat(info))
                ranked.append(int(i/2))
            else:
                url= self.base_url + info
                urls.append(url)
                contents.append("")
                if url[len(url)-1] == "0":
                    placed.append("First_Page")
                else:
                    placed.append(self.cate_conv[url[len(url)-2]])
            i+= 1
        i= 0

        for item in zip(titles, urls, contents, ranked, placed):
            scraped_info = {
                'title': item[0],
                'date_raw': date.today().strftime("%B %d, %Y"),
                'date': date.today().strftime("%Y-%m-%d"),
                'url': response.request.url,
                'news_url': item[1],
                'content': item[2],
                'ranked': item[3],
                'placed': item[4],
                'epoch': time.time()
            }
            i+=1
            edition.append(scraped_info)
        
        base_name = f"{now_s}E{now_epoch}.json"
        scraped_data_dir = f"{PROJ_DIR}/collectedNews/flow/IT/Televideo"
        scraped_data_filepath = f"{scraped_data_dir}/{base_name}"
        with open(scraped_data_filepath, "w") as f:
            json.dump(edition, f, indent= 4, ensure_ascii=False)
            f.write("\n")

