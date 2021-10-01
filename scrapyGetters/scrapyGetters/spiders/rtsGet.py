import scrapy
from scrapy.http import HtmlResponse
from scrapy import Selector
from datetime import datetime
import time
import os
import json
import re
import dateparser

#sort i've found o StackOverflow, if I didn't use this I couldn't find the "last saved news" below
#credits to Mark Byers
def sorted_nicely( l ): 
    """ Sort the given iterable in the way that humans expect.""" 
    convert = lambda text: int(text) if text.isdigit() else text 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(l, key = alphanum_key)



class RtsgetSpider(scrapy.Spider):
    name = 'rtsGet'
    f=open("rtsurls.txt", "r+")
    toGetUrls= f.read()
    #print(toGetUrls)
    toGetUrls = toGetUrls.split("\n")
    toGetUrls = list(dict.fromkeys(toGetUrls))
    allowed_domains = ['https://www.rts.ch/audio-podcast/2021/audio']
    start_urls = toGetUrls

    def parse(self, response):
        print(response.url)
        chapters= response.css(".audio-chapter-list").css("ul").css("li")
        todate= response.css(".timeframe").css("span")
        todate= dateparser.parse(todate[1].css("::text").get()[3:]).date()
        chapters= chapters[1:len(chapters)]
        titles= []
        dates_raw= []
        dates= []
        urls= []
        rankeds= []
        durations= []
        i= 0
        for chapter in chapters:
            urls.append(chapter.css("a::attr(href)").get())
            titles.append(chapter.css(".title::text").get())
            durations.append(chapter.css(".duration::text").get())
            dates_raw.append(todate.strftime("%B %d, %Y"))
            dates.append(todate.strftime("%Y-%m-%d"))
            rankeds.append(i)
            i+=1
        
        edition= []
        for item in zip(titles, dates_raw, dates, urls, durations, rankeds):
            scraped_info = {
                'title': item[0],
                'date_raw': item[1],
                'date': item[2],
                'url': item[3],
                'duration': item[4],
                'ranked': item[5],
                'epoch': time.time()
            }
            edition.append(scraped_info)
        
        f= open("../../../collectedNews/CH/RTS/" + str(edition[0]['date']) + ".json", "w")
        json.dump(edition, f, indent= 4, ensure_ascii=False)
        f.close()
    