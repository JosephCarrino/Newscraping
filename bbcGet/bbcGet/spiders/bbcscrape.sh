#!/bin/sh
PATH=$PATH:/home/joseph/.local/bin
export PATH
scrapy crawl bbc
cd ../../..
git add .
git commit -m "bbc_checkout"
git push origin main
