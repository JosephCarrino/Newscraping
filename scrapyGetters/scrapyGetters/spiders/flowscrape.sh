#!/bash/sh
PATH=$PATH:/home/students/giuseppe.carrino2/.local/bin
export PATH
scrapy crawl teleGet
scrapy crawl postScrape
git add .
git commit -m "checkout"
git push origin main
