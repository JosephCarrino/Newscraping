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

def main():

    f= open("nytKey.txt", "r+")
    key=f.read()

    #Insert here your NewYorkTimesAPI key
    #key= ""


    conv_dic= {'https://api.nytimes.com/svc/topstories/v2/home.json?api-key='+key: "First_Page",
            'https://api.nytimes.com/svc/topstories/v2/world.json?api-key='+key: "Abroad",
            'https://api.nytimes.com/svc/topstories/v2/politics.json?api-key='+key: "Politics",
            'https://api.nytimes.com/svc/topstories/v2/business.json?api-key='+key: "Economics"}

    urls_get= ['https://api.nytimes.com/svc/topstories/v2/home.json?api-key=' + key,
        'https://api.nytimes.com/svc/topstories/v2/world.json?api-key=' + key,
        'https://api.nytimes.com/svc/topstories/v2/politics.json?api-key=' + key,
        'https://api.nytimes.com/svc/topstories/v2/business.json?api-key=' + key]

    for url_get in urls_get:
        toGet= urllib.request.urlopen(url_get)
        obj = json.loads(toGet.read().decode("utf-8"))
        titles= []
        contents= [] #abstract
        urls= []
        dates= [] #published_date
        placeds= [] #subsections
        ranked= []
        more_info= []
        
        #files= sorted_nicely(os.listdir("US"))
        #if len(files) == 0:
            #j= 0
        #else:
            #j= len(files)
            
        i= 0        
        for result in obj['results']:   
            del result['multimedia']
            titles.append(result['title'])
            del result['title']
            contents.append(result['abstract'])
            del result['abstract']
            urls.append(result['url'])
            del result['url']
            dates.append(result['published_date'])
            del result['published_date']
            placeds.append(conv_dic[url_get])
            ranked.append(i)
            more_info.append(result)
            i+= 1
        
        edition= []
        i= 0
        toDump= True
        for item in zip(titles, dates, urls, contents, ranked, placeds, more_info):
            date= datetime.strptime(item[1][0:10], "%Y-%m-%d")
            date_raw= date.strftime("%B %d, %Y")
            date= date.strftime("%Y-%m-%d")
            scraped_info = {
                'title': item[0],
                'date_raw': date_raw,
                'date': date,
                'url': url_get,
                'news_url': item[2],
                'content': item[3],
                'ranked': item[4],
                'placed': item[5],
                'epoch': time.time(),
                'more_info': item[6]
            }
            if item[5] == "":
                scraped_info['placed']= "First_Page"
            #if i == 0:
                #for lastNew in files:
                    #if lastNew != "":
                        #f= open("US/" + lastNew, "r+")
                        #searchin= json.load(f)
                        #if searchin[0]['url'] == scraped_info['url']:
                            #f.close()
                            #toDump= False
                            #break
                        #f.close()
            i+=1
            edition.append(scraped_info)
        now = datetime.now().strftime("%Y-%m-%dT%H.%M.%S")
        if toDump:
            my_f = str(now) + "E" + str(time.time())
            f= open("collectedNews/flow/EN/NYT/" + my_f + ".json", "w")
            json.dump(edition, f, indent= 4)
            f.close()
            f= open("collectedNews/flow/EN/NYT/" + my_f + ".json", "a")
            f.write("\n")
            f.close()
            
if __name__ == "__main__":
    main()