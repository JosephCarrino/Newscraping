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


#QUESTO SCRIPT VA USATO SOLO DOPO (CIRCA) LE 20, PRIMA L'EDIZIONE NON VIENE TROVATA NEL SITO CAUSANDO UN CRASH (nello script "letsScrape" è tutto controllato)

class ZdfgetSpider(scrapy.Spider):
    name = 'zdfGet'
    today= datetime.today().strftime("%y%m%d")
    myurl= "https://www.zdf.de/nachrichten/heute-19-uhr/" + today + "-heute-sendung-19-uhr-100.html"
    allowed_domains = ['www.zdf.de/nachrichten/heute-19-uhr/']
    start_urls = [myurl]

    def parse(self, response):
        box = response.css(".details")
        box_titles= box.css(".item-description::text").get()
        titles= box_titles.split(";")
        
        box_dates= box.css(".teaser-info::text").getall()
        print(box_dates)
        date= box_dates[1]
        
        url= response.url
        
        ranks= []
        contents= []
        for i in range(0, len(titles)):
            returning= ""
            tcont= titles[i].split("-")
            if len(tcont) > 1:
                tcont= tcont[1:len(tcont)]
                for cont in tcont:
                    returning+= cont + ""
            contents.append(returning)
            ranks.append(i)
        
        #lastNew = ""
        #files= sorted_nicely(os.listdir("../../../zdfDE"))
        #if len(files) == 0:
            #j= 0
        #else:
            #lastNew= files[len(files)-1]
            #j= len(files)
          
        
        edition= []
        toDump= True
        for item in zip(titles, contents, ranks):
            scraped_info = {
                'title': item[0].replace("\n","").strip(),
                'date_raw': datetime.strptime(date, "%d.%m.%Y").strftime("%B %d, %Y"),
                'date': datetime.strptime(date, "%d.%m.%Y").strftime("%Y-%m-%d"),
                'url': response.request.url,
                'news_url': url,
                'content': item[1],
                'ranked': item[2],
                'placed': "First_Page",
                'epoch': time.time()
            }
            #if lastNew != "" and len(edition) == 0:
                #f= open("../../../zdfDE/" + lastNew, "r+")
                #searchin= json.load(f)
                #if searchin[0]['date'] >= scraped_info['date']:
                    #f.close()
                    #toDump= False
                    #break
            edition.append(scraped_info)
        if toDump:
            f= open("../../../collectedNews/edition/DE/Zdf/" + str(scraped_info['date']) + ".json", "w")
            json.dump(edition, f, indent= 4, ensure_ascii=False)
            f.close()
            #j+=1
            f= open("../../../collectedNews/edition/DE/Zdf/" + str(scraped_info['date']) + ".json", "a")
            f.write("\n")
            f.close()
                
         
