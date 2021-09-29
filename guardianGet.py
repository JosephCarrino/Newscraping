import json
import urllib.request
from datetime import datetime
import time
import os
import re



#sort i've found o StackOverflow, if I didn't use this I couldn't find the "last saved news" below
#credits to Mark Byers
def sorted_nicely( l ): 
    """ Sort the given iterable in the way that humans expect.""" 
    convert = lambda text: int(text) if text.isdigit() else text 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(l, key = alphanum_key)

f= open("gKey.txt", "r+")
key=f.read()

#Insert here your GuardianAPI key
#key= ""

urls_get= ['https://content.guardianapis.com/search?order-by=relevance&api-key=' + key,
          'https://content.guardianapis.com/search?section=politics&order-by=relevance&api-key=' + key,
          'https://content.guardianapis.com/search?section=world&order-by=relevance&api-key='  + key]

for url_get in urls_get:
    toGet= urllib.request.urlopen(url_get)
    obj = json.loads(toGet.read().decode("utf-8"))['response']
    
    titles= []
    contents= []
    urls= []
    raw_dates= []
    dates= []
    placeds= []
    ranked= []
    
    files= sorted_nicely(os.listdir("guardUK"))
    if len(files) == 0:
        j= 0
    else:
        j= len(files)

    i= 0
    for res in obj['results']:
        titles.append(res['webTitle'])
        contents.append("")
        urls.append(res['webUrl'])
        ddate= datetime.strptime(res['webPublicationDate'][0:10], "%Y-%m-%d")
        raw_dates.append(ddate.strftime("%B %d, %Y"))
        dates.append(ddate.strftime("%Y-%m-%d"))
        placeds.append(res['sectionName'])
        ranked.append(i)
        i+=1
    
    edition= []
    i= 0
    toDump= True
    for item in zip(titles, raw_dates, dates, urls, contents, ranked, placeds):
        scraped_info = {
            'title': item[0],
            'date_raw': item[1],
            'date': item[2],
            'url': item[3],
            'content': item[4],
            'ranked': item[5],
            'placed': item[6],
            'epoch': time.time()
        }
                         
        if i == 0:
            k= 0
            for lastNew in files:
                if lastNew != "":
                    f= open("guardUK/" + lastNew, "r+")
                    searchin= json.load(f)
                    if searchin[0]['url'] == scraped_info['url']:
                        f.close()
                        toDump= False
                        break
                    f.close()
                    k+=1
        i+=1
        edition.append(scraped_info)
    if toDump:
        f= open("guardUK/news" + str(j) + ".json", "w")
        json.dump(edition, f, indent= 4)
        f.close()