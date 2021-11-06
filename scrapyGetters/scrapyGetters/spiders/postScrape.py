import scrapy
from scrapy.http import HtmlResponse
from scrapy import Selector
from datetime import datetime
import time
import os
import json
import re


#sort i've found o StackOverflow, if I didn't use this I couldn't find the "last saved news" below
#credits to Mark Byers
def sorted_nicely( l ): 
    """ Sort the given iterable in the way that humans expect.""" 
    convert = lambda text: int(text) if text.isdigit() else text 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(l, key = alphanum_key)



place_dict= {'https://www.ilpost.it/': "First_Page",
            'https://www.ilpost.it/mondo/': "Abroad",
            'https://www.ilpost.it/politica/': "Politics",
            'https://www.ilpost.it/economia/': "Economics"}


class PostscrapeSpider(scrapy.Spider):
    name = 'postScrape'
    allowed_domains = ['www.ilpost.it']
    start_urls = ['http://www.ilpost.it',
                 'https://www.ilpost.it/mondo/',
                 'https://www.ilpost.it/politica/',
                 'https://www.ilpost.it/economia/']

    def parse(self, response):
        articles= response.css("#content").css("article")
        titles= []
        dates_raw= []
        dates= []
        urls= []
        contents= []
        placeds=[]
        rankeds= []
        
        i= 0
        for article in articles:
            tourl= article.css("header").css("figure").css("a::attr(href)").get()
            urls.append(tourl)
            try:
                todate=datetime.strptime(tourl[22:32], "%Y/%m/%d")
            except:
                todate= datetime.now()
            dates.append(todate.strftime("%Y-%m-%d"))
            dates_raw.append(todate.strftime("%B %d, %Y"))
            info= article.css(".entry-content")
            titles.append(info.css("h2").css("a::text").get())
            contents.append(info.css("p").css("a::text").get())
            placeds.append(place_dict[response.url])
            rankeds.append(i)
            i+=1
         
        edition= []
        toDump= True
        for item in zip(titles, dates_raw, dates, urls, contents, rankeds, placeds):
            scraped_info= {
                'title': item[0],
                'date_raw': item[1],
                'date': item[2],
                'url': response.request.url,
                'news_url': item[3],
                'content': item[4],
                'ranked': item[5],
                'placed': item[6],
                'epoch': time.time()
            }
            edition.append(scraped_info)
            
        now = datetime.now().strftime("%Y-%m-%dT%H.%M.%S")    
        if toDump:
            my_f = str(now) + "E" + str(time.time())
            f= open("../../../collectedNews/flow/IT/ilPost/" + my_f + ".json", "w")
            json.dump(edition, f, indent= 4, ensure_ascii=False)
            f.close()
            f= open("../../../collectedNews/flow/IT/ilPost/" + my_f + ".json", "a")
            f.write("\n")
            f.close()
