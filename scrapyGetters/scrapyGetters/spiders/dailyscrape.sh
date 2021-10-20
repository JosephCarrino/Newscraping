#!/bash/sh
PATH=$PATH:/home/students/giuseppe.carrino2/.local/bin
export PATH
scrapy crawl zdfGet
scrapy crawl rtsURLGet
scrapy crawl rtsGet
scrapy crawl pbsGet
scrapy crawl frGet
scrapy crawl 20Get
