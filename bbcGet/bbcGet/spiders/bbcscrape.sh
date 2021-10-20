#!/bin/sh
PATH=$PATH:/home/students/giuseppe.carrino2/.local/bin
export PATH
scrapy crawl bbc
git add .
git commit -m "bbc_checkout"
git push origin main
