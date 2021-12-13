from datetime import datetime
import json
import time
import urllib.request


def main():
    f = open("keys/nytKey.txt", "r+")
    key = f.read()

    conv_dic = {'https://api.nytimes.com/svc/topstories/v2/home.json?api-key='+key: "First_Page",
            'https://api.nytimes.com/svc/topstories/v2/world.json?api-key='+key: "Abroad",
            'https://api.nytimes.com/svc/topstories/v2/politics.json?api-key='+key: "Politics",
            'https://api.nytimes.com/svc/topstories/v2/business.json?api-key='+key: "Economics"}

    urls_get = ['https://api.nytimes.com/svc/topstories/v2/home.json?api-key=' + key,
        'https://api.nytimes.com/svc/topstories/v2/world.json?api-key=' + key,
        'https://api.nytimes.com/svc/topstories/v2/politics.json?api-key=' + key,
        'https://api.nytimes.com/svc/topstories/v2/business.json?api-key=' + key]

    for url_get in urls_get:
        to_get = urllib.request.urlopen(url_get)
        obj = json.loads(to_get.read().decode("utf-8"))
        titles = []
        contents = [] #abstract
        urls = []
        dates = [] #published_date
        placeds = [] #subsections
        ranked = []
        more_info = []
        
        i = 0
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
            i += 1
        
        edition = []
        i = 0
        to_dump = True
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
                scraped_info['placed'] = "First_Page"

            i += 1
            edition.append(scraped_info)
        now = datetime.now().strftime("%Y-%m-%dT%H.%M.%S")
        if to_dump:
            my_f = str(now) + "E" + str(time.time())
            f = open("collectedNews/flow/EN/NYT/" + my_f + ".json", "w")
            json.dump(edition, f, indent= 4)
            f.close()
            f = open("collectedNews/flow/EN/NYT/" + my_f + ".json", "a")
            f.write("\n")
            f.close()


if __name__ == "__main__":
    main()
