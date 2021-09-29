import os
import time
from datetime import datetime

while True:
    os.chdir("bbcGet/bbcGet/spiders")
    os.chdir("../../../bbcGet/bbcGet/spiders")
    os.system("scrapy crawl bbc")
    os.chdir("../../../scrapyGetters/scrapyGetters/spiders")
    os.system("scrapy crawl 20Get")
    os.system("scrapy crawl teleGet")
    hour= datetime.today().strftime("%H")
    if int(hour) >= 20:
        os.system("scrapy crawl zdfGet")
    os.chdir("../../../")
    os.system("python nytimesGet.py")
    os.system("python zeitGet.py")
    os.system("python guardianGet.py")
    time.sleep(180)