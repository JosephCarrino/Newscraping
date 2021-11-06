import scrapy
import json
import re
import os
from datetime import datetime
from datetime import date
import time
import urllib.request

#sort i've found o StackOverflow, if I didn't use this I couldn't find the "last saved news" below
#credits to Mark Byers
def sorted_nicely( l ): 
    """ Sort the given iterable in the way that humans expect.""" 
    convert = lambda text: int(text) if text.isdigit() else text 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(l, key = alphanum_key)


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
    allowed_domains = ['www.servizitelevideo.rai.it/televideo/pub']
    start_urls = ['http://www.servizitelevideo.rai.it/televideo/pub/solotesto.jsp?categoria=Prima&pagina=103',
                 'https://www.servizitelevideo.rai.it/televideo/pub/solotesto.jsp?categoria=Politica&pagina=120',
                 'https://www.servizitelevideo.rai.it/televideo/pub/solotesto.jsp?categoria=Politica&pagina=130',
                 'https://www.servizitelevideo.rai.it/televideo/pub/solotesto.jsp?categoria=Dal%20Mondo&pagina=150'
                 ]
    
    def stringFormat(self, s):
        return s.replace('\n', ' ').replace('\\', '').replace('  ', ' ').strip()
    
    #Per ora non usato, ma vorrei riuscire a sistemare il problema delle librerie che sovrascrivono urlopen
    def deepParse(toParse, subPage= 2):
        toGet= urllib.request.urlopen(toParse)
        newData= toGet.read().decode("utf8")
        #cerco l'inizio
        start= newData.find("<pre")
        start= newData.find(">", start)
        end=newData.find("<", start)
        #lo formatto decentemente
        toRet= stringFormat(newData[start+1:end])
        try:
            #se mi accorgo che ci sono più pagine, ottengo anche queste
            if toRet[1] == "/":
                page= toParse[len(toParse)-4:len(toParse)]
                newPage = "https://www.servizitelevideo.rai.it/televideo/pub/solotesto.jsp?regione=&pagina" + page + "&sottopagina=0" + str(subPage)
                toRet += deepParse(newPage, subPage+1)
        except:
            pass
        return toRet
    
    def parse(self, response):
        content= response.css("pre")
        titleString= content.css("::text").getall()
        titleString= titleString[0:len(titleString)-1]
        titles= []
        urls= []
        contents= []
        placed= []
        ranked= []
        
        #lastNew = ""
        #files= sorted_nicely(os.listdir("../../../collectedNews/IT/Televideo"))
        #if len(files) == 0:
            #j= 0
        #else:
           # lastNew= files[len(files)-1]
            #j= len(files)
        
       
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
        toDump= True
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
            #if i == 0:
                #for lastNew in files:
                    #if lastNew != "":
                        #f= open("../../../collectedNews/IT/Televideo/" + lastNew, "r+")
                        #searchin= json.load(f)
                        #if searchin[0]['url'] == scraped_info['url']:
                            #f.close()
                            #toDump= False
                            #break
            i+=1
            edition.append(scraped_info)
        now = datetime.now().strftime("%Y-%m-%dT%H.%M.%S")
        if toDump:
            my_f = str(now) + "E" + str(time.time())
            f= open("../../../collectedNews/flow/IT/Televideo/" + my_f + ".json", "w")
            json.dump(edition, f, indent= 4, ensure_ascii=False)
            f.close()
            f= open("../../../collectedNews/flow/IT/Televideo/" + my_f + ".json", "a")
            f.write("\n")
            f.close()
