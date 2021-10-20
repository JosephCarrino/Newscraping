import scrapy
from scrapy.http import HtmlResponse
from scrapy import Selector
from datetime import datetime
import time
import os
import json
import re

class PbsgetSpider(scrapy.Spider):
    name = 'pbsGet'
    toD= datetime.today()
    url= toD.strftime("%B-%#d-%Y")
    isWeek= toD.weekday()
    #different urls for weekdays and weekends
    if isWeek < 5:
        searchurl = "https://www.pbs.org/newshour/show/" + str(url) + "-pbs-newshour-full-episode"
    else:
        searchurl = "https://www.pbs.org/newshour/show/" + str(url) + "-pbs-newshour-weekend-full-episode"
    #for i in range (1, 31):
        #if i < 10:
        #   ddate= datetime.strptime("0" + str(i) + "/09/2021", "%d/%m/%Y")
        #   isWeek= ddate.weekday()
        #else:
        #   ddate= datetime.strptime(str(i) + "/09/2021", "%d/%m/%Y")
        #    isWeek= ddate.weekday()
        #if isWeek < 5:
        #    urls.append("https://www.pbs.org/newshour/show/september-" + str(i) + "-2021-pbs-newshour-full-episode")
        #else:
        #    urls.append("https://www.pbs.org/newshour/show/september-" + str(i) + "-2021-pbs-newshour-weekend-full-episode")
    
    allowed_domains = ['www.pbs.org']
    start_urls = [searchurl.lower()]
    #start_urls = ["https://www.pbs.org/newshour/show/october-19-2021-pbs-newshour-full-episode"]

    def parse(self, response):
        ddate= datetime.strptime(response.css(".video-single__title--large").css("span::text").get(), "%B %d, %Y")
        date_raw= ddate.strftime("%B %d, %Y")
        date= ddate.strftime("%Y-%m-%d")
        content= response.css(".playlist").css("li")
        titles= []
        durations= []
        urls= []
        rankeds= []
        i= 0
        for new in content:
            titles.append(new.css(".playlist__title::text").get())
            durations.append(new.css(".playlist__duration::text").get())
            urls.append(new.css("a::attr(href)").get())
            rankeds.append(i)
            i+=1
        
        edition= []
        for item in zip(titles, urls, durations, rankeds):
            scraped_info = {
                'title': item[0],
                'date_raw': date_raw,
                'date': date,
                'url': item[1],
                'duration': item[2],
                'ranked': item[3],
                'epoch': time.time()
            }
            edition.append(scraped_info)
            
        f= open("../../../collectedNews/US/PBS/" + str(date) + ".json", "w")
        json.dump(edition, f, indent= 4, ensure_ascii=False)
        f.close()
            
