import json
import urllib.request
from datetime import datetime
import time
import os
import re
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def sorted_nicely( l ): 
    """ Sort the given iterable in the way that humans expect.""" 
    convert = lambda text: int(text) if text.isdigit() else text 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(l, key = alphanum_key)

f= open("zeitKey.txt", "r+")
key=f.read()

#Insert here your ZeitAPI key
#key= ""

url= "https://api.zeit.de/content?fields=title+subtitle+href+release_date+&limit=50"
hdr= { 'X-Authorization' : key }

req = urllib.request.Request(url, headers=hdr)
toGet = urllib.request.urlopen(req)
objs= json.loads(toGet.read().decode("utf-8"))
news= objs['matches']

#files= sorted_nicely(os.listdir("zeitDE"))
#if len(files) == 0:
    #j= 0
#else:
    #j= len(files)

titles= []
raw_dates= []
dates= []
urls= []
contents= []

top= True
for new in news: 
    titles.append(new['title'])
    ddate= datetime.strptime(new['release_date'][0:10], "%Y-%m-%d")
    raw_dates.append(ddate.strftime("%B %d, %Y"))
    dates.append(ddate.strftime("%Y-%m-%d"))
    urls.append(new['href'])
    contents.append(new['subtitle'])

i= 0
toDump= True
edition= []
for item in zip(titles, raw_dates, dates, urls, contents):
    scraped_info = {
        'title': item[0],
        'date_raw': item[1],
        'date': item[2],
        'url': item[3],
        'content': item[4],
        'ranked': i,
        'epoch': time.time()
    }
    #for lastNew in files:
        #if lastNew != "":
            #f= open("zeitDE/" + lastNew, "r+")
            #searchin= json.load(f)
            #if searchin['url'] == scraped_info['url']:
                #f.close()
                #toDump= False
    i+=1
    if(i <= 20):
        edition.append(scraped_info)
now = datetime.now().strftime("%Y-%m-%dT%H.%M.%S")
if toDump:
    f= open("collectedNews/DE/Zeit/" + str(now) + "E" + str(time.time()) + ".json", "w")
    json.dump(edition, f, indent= 4)
    f.close()
    i+=1
    #j+=1
                     
