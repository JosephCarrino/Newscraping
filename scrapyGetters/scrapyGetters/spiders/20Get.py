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


class A20getSpider(scrapy.Spider):
    name = '20Get'
    allowed_domains = ['www.tagesschau.de/multimedia/video/videoarchiv2.html']
    start_urls = ['https://www.tagesschau.de/multimedia/video/videoarchiv2.html']

    def parse(self, response):
        base_url="https://www.tagesschau.de"
        boxes = response.css(".viewB")
        toRet= []
        for box in boxes:
            box= box.css(".teaser")
            if box.css(".headline").css("a::text").get() == "tagesschau " or box.css(".headline").css("a::text").get() == "tagesschau":
                if box.css(".dachzeile::text").get()[11:16] == "20:00":
                    toRet.append(box)   
        
        #lastNew = ""
        #files= sorted_nicely(os.listdir("../../../DE"))
        #if len(files) == 0:
            #j= 0
        #else:
            #lastNew= files[len(files)-1]
            #j= len(files)
        
                             
        
        for box in toRet:
            toDump= True
            findTitle= box.css(".teasertext")
            titles= findTitle.css('a::text').get().split(",")
            contents= ""
            findUrl= box.css(".headline")
            urls= base_url + findUrl.xpath('.//a').css('::attr(href)').get()
            findDate= str(box.css("p::text").get())[0:10]
            dates= datetime.strptime(findDate, "%d.%m.%Y").strftime("%B %d, %Y")
            edition= []
            i= 0
            for title in titles:
                scraped_info = {
                    'title': title,
                    'date_raw': dates,
                    'date': datetime.strptime(dates, "%B %d, %Y").strftime("%Y-%m-%d"),
                    'url': response.request.url,
                    'url_news': urls,
                    'content': contents,
                    'ranked': str(i),
                    'epoch': time.time()
                }
                #if i == 0:
                    #if lastNew != "":
                        #f= open("../../../DE/" + lastNew, "r+")
                        #searchin= json.load(f)
                        #if searchin[0]['date'] >= scraped_info['date']:
                            #f.close()
                            #toDump= False
                            #break
                #else:
                    #scraped_info['title']= title[1:len(title)]
                i+=1
                edition.append(scraped_info)
            print(edition)
            if toDump:
                f= open("../../../collectedNews/DE/Tagesschau/" + str(scraped_info['date']) + ".json", "w")
                json.dump(edition, f, indent= 4, ensure_ascii=False)
                f.close()
                #j+=1
                
            
            