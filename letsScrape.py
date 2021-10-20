import os
import time
from datetime import datetime

notToday= True

while True:
    os.chdir("bbcGet/bbcGet/spiders")
    os.chdir("../../../bbcGet/bbcGet/spiders")
    os.system("scrapy crawl bbc")
    os.chdir("../../../scrapyGetters/scrapyGetters/spiders")
    os.system("scrapy crawl teleGet")
    #Per usare lo script di GR1 bisogna prima impostare in gr1URLGet i link per l'archivio di Settembre, quando uscirà
    #os.system("scrapy crawl gr1URLGet")
    #os.system("scrapy crawl gr1Get")
    os.system("scrapy crawl postScrape")
    hour= datetime.today().strftime("%H")
    #if int(hour) < 20 and not notToday:
        #notToday= True
    #if int(hour) >= 20 and notToday:
    os.system("scrapy crawl zdfGet")
    os.system("scrapy crawl rtsURLGet")
    os.system("scrapy crawl rtsGet")
    os.system("scrapy crawl pbsGet")
    os.system("scrapy crawl frGet")
    os.system("scrapy crawl 20Get")
    #notToday= False 
    os.chdir("../../../")
    os.system("python3 nytimesGet.py")
    os.system("python3 zeitGet.py")
    #Guardian manda notizie molto vecchie
    #os.system("python guardianGet.py")
    time.sleep(180)
