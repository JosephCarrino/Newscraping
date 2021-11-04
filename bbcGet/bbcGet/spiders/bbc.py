import scrapy
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
import time
import json
import os
import re 
from datetime import datetime


#sort i've found o StackOverflow, if I didn't use this I couldn't find the "last saved news" below
#credits to Mark Byers
def sorted_nicely( l ): 
    """ Sort the given iterable in the way that humans expect.""" 
    convert = lambda text: int(text) if text.isdigit() else text 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(l, key = alphanum_key)


class BbcSpider(scrapy.Spider):
    name = 'bbc'
    allowed_domains = ['www.bbc.com/news/world']
    start_urls = ['https://www.bbc.com/news/world/',
                 'https://www.bbc.com/news',
                 'https://www.bbc.com/news/politics']

    def parse(self, response):
        #using scrapy css selectors to get informations I need
        base_url= 'https://www.bbc.com/news/'
        titles = response.css(".gs-c-promo-heading__title::text").getall()
        contents = response.css(".gs-c-promo-summary::text").getall()
        urls= response.css(".gs-c-promo-heading::attr(href)").getall()
        dates= response.css("time::attr(datetime)").getall()

        #knowing my last saved news index, in order to not overwrite anything
        #files= sorted_nicely(os.listdir("../../../UK"))
        #if len(files) == 0:
            #j= 0
        #else:
            #lastNew= files[len(files)-1]
            #lastNew= lastNew.replace("news", "").replace(".json", "")
            #j= int(lastNew)+1
        
        #array of news-titles, I will use this to notice if I have already saved a news
        #searchin= []
        #files= os.listdir("../../../collectedNews/UK/BBC")
        #for index in range(0, j):
            #try:
                #f= open("../../../collectedNews/UK/BBC/" + str(index) + ".json", "r+")
                #data = json.load(f)
                #searchin.append(data['title'])
            #maybe some news have been deleted so I just skip the numbers I can't find in the directory
            #except:
                #pass
        
        edition= []
        for item in zip(titles,contents,urls,dates):
            toSave= True
            date= item[3][0:len(item[3])-5]
            try:
                date= datetime.strptime(date,"%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d")
            except:
                pass
            scraped_info = {
                'title': item[0],
                'date': date,
                'date_raw': date,
                #'date': datetime.strptime(date, "%B %d, %Y").strftime("%Y-%m-%d"),
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
            
            #looking if I already saved the news
            #for i in searchin:
                #if i == scraped_info['title']:
                    #toSave = False
                    #break
            edition.append(scraped_info)
            
        now = datetime.now().strftime("%Y-%m-%dT%H.%M.%S")
        if toSave:
            f= open("../../../collectedNews/flow/EN/BBC/" + str(now) + "E" + str(time.time())  + ".json", "w")
            json.dump(edition, f, indent= 4, ensure_ascii=False)
            f.close()
            f= open("../../../collectedNews/flow/EN/BBC/" + str(now) + "E" + str(time.time())  + ".json", "a")
            f.write("\n")
            f.close()
            #j+=1
