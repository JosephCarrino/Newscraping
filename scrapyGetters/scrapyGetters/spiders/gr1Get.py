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



class Gr1getSpider(scrapy.Spider):
    f=open("gr1urls.txt", "r+")
    toGetUrls= f.read()
    #print(toGetUrls)
    toGetUrls = toGetUrls.split("\n")
    name = 'gr1Get'
    allowed_domains = ['www.raiplayradio.it']
    start_urls = toGetUrls

    def parse(self, response):
        box= response.css(".descriptionProgramma")
        timebox= box.css("ul").css("li").css("span::text").get()
        date= datetime.strptime(timebox, "%d/%m/%Y")
        d_raw= date.strftime("%B %d, %Y")
        d_real= date.strftime("%Y-%m-%d")
        url= response.url
        titles= box.css(".aodHtmlDescription::text").getall()
        while True:
            try:
                titles.remove("\n")
            except:
                break
        titles= titles[0:len(titles)-1]
        
        contents= []
        for i in range(0, len(titles)):
            toApp= ""
            con= titles[i].split(".")
            titles[i]= con[0] + "."
            con= con[1:len(con)]
            for c in con:
                toApp+= c + ". "
            contents.append(toApp)
        
        #lastNew = ""
        #files= sorted_nicely(os.listdir("../../../gr1IT"))
        #if len(files) == 0:
            #j= 0
        #else:
            #lastNew= files[len(files)-1]
            #j= len(files)
                  
        i= 0
        edition= []
        toDump= True
        for item in zip(titles, contents):
            if item[0].replace("\r", "").replace("\n", "").replace("\t", "").strip() == ".":
                continue
            scraped_info = {
                'title': item[0].replace("\r", "").replace("\n", "").replace("\t", "").strip(),
                'date_raw': d_raw,
                'date': d_real,
                'url': response.request.url,
                'news_url': url,
                'content': item[1],
                'ranked': i,
                'placed': "First_Page",
                'epoch': time.time()
            }
            #if lastNew != "" and len(edition) == 0:
                #f= open("../../../gr1IT/" + lastNew, "r+")
                #searchin= json.load(f)
                #if searchin[0]['date'] >= scraped_info['date']:
                    #f.close()
                    #toDump= False
                    #break
            edition.append(scraped_info)
            i+=1

        if toDump:
            f= open("../../../collectedNews/edition/IT/GR1/" + str(edition[0]['date']) + ".json", "w")
            json.dump(edition, f, indent= 4, ensure_ascii=False)
            f.close()
            f= open("../../../collectedNews/edition/IT/GR1/" + str(edition[0]['date']) + ".json", "a")
            f.write("\n")
            f.close()
            #j+=1
