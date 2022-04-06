#!/bash/sh
PATH=$PATH:/home/students/giuseppe.carrino2/.local/bin
export PATH
scrapy crawl teleGet
scrapy crawl postScrape
scrapy crawl dwGet
scrapy crawl abcGet
scrapy crawl cnnGEt
scrapy crawl fr24rssGet
cd ../../..
git add .
git commit -m "checkout"
git push origin main
