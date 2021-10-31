import scrapy
from scrapy.http import HtmlResponse
from scrapy import Selector
from datetime import datetime
from datetime import date
import time
import os
import json
import re

class FrgetSpider(scrapy.Spider):
    name = 'frGet'
    urls= []
    tod= date.today().strftime("%d")
    #for i in range(1, 31):
    urls.append("https://www.france24.com/en/archives/2021/10/" + str(tod) + "-October-2021")
    allowed_domains = ['https://www.france24.com/en']
    start_urls = urls

    def parse(self, response):
        news= response.css(".o-archive-day__list").css("li")
        titles= []
        urls= []
        raw_dates= []
        dates= []
        rankeds= []
        act_date= datetime.strptime(response.url[45:], "%d-%B-%Y")
        i= 0
        for new in news:
            titles.append(new.css("a::text").get())
            urls.append("https://www.france24.com" + new.css("a::attr(href)").get())
            raw_dates.append(act_date.strftime("%B %d, %Y"))
            dates.append(act_date.strftime("%Y-%m-%d"))
            rankeds.append(i)
            i+=1
        
        edition= []
        for item in zip(titles, raw_dates, dates, urls, rankeds):
            scraped_info = {
                'title': item[0],
                'date_raw': item[1],
                'date': item[2],
                'url': response.request.url,
                'news_url': item[3],
                'content': "",
                'ranked': item[4],
                'placed': "First_Page",
                'epoch': time.time()                
            }
            edition.append(scraped_info)
            
        f= open("../../../collectedNews/edtion/EN/France24/" + str(edition[0]['date']) + ".json", "w")
        json.dump(edition, f, indent= 4, ensure_ascii=False)
        f.close()
        
