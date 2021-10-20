#!/bash/sh
PATH=$PATH:/home/students/giuseppe.carrino2/.local/bin
export PATH
scrapy crawl gr1url
scrapy crawl teleGet
scrapy crawl postScrape
