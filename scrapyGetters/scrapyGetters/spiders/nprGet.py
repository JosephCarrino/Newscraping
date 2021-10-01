import scrapy
from datetime import datetime
import time
import re
import os

#sort i've found o StackOverflow, if I didn't use this I couldn't find the "last saved news" below
#credits to Mark Byers
def sorted_nicely( l ): 
    """ Sort the given iterable in the way that humans expect.""" 
    convert = lambda text: int(text) if text.isdigit() else text 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(l, key = alphanum_key)



class NprgetSpider(scrapy.Spider):
    name = 'nprGet'
    allowed_domains = ['www.npr.org']
    start_urls = ['https://www.npr.org/programs/morning-edition/archive/']
    handle_httpstatus_list = [500, 503, 504, 400, 408, 307, 403]
    def start_requests(self):
        yield scrapy.Request('https://www.npr.org/programs/morning-edition/archive', cookies ={ 'cookie': 'choiceVersion=1; trackingChoice=true; _fbp=fb.1.1632333351192.251011065; _cb_ls=1; _cb=DjJVkFCyo-A_gctIT; __stripe_mid=39c14551-299d-4bea-b43b-07c8d8ede32314a29f; _admrla=2.0-62b25eeb-80b7-02cf-f713-776dd6711cb3; dateOfChoice=1632334920282; ak_bmsc=8230CD100B46B7A79E0A27FB59D3A621~000000000000000000000000000000~YAAQBItIF9kiEqp6AQAAmeXDFg0+QVlPQQ7gVEOMr9RqtF9yvRls137MMVMzHuhNCBxhzC4Yi+tM4skOtuWNGWzaHEBKaguRMyQHxOvpspte1WRIpjVyZXK6+Ips2nWygJvRPj9PEqZa341JsR3+3eKQiNkMZwQ4/YxmYu1rKxJQHgCD9lPx3BOG7+gbwui0a3sj8Ltky17UIiOb93g5RqyGkSy7gAnQ1bZ1PYrbpjDJmEw6iO+Jy/k5O6GQzVibmFHGahTYMUoweztb8Tmuy9DjWFWcMTK5mPrxqQfoEdPeYmxY/LI2sIxO38eyYfFzFPEyR55XwKwdcYZ/t7z9d4nguPuQW43mOpB8FZV0IJomXwiQLf98/wNoF5POMnzY9wb4pvfbm4zb90I23hjDThF0Mg7ffIQCs7VYhaki; _gid=GA1.2.1359020403.1632469512; _gat=1; _cb_svref=null; __stripe_sid=e2708446-2bff-435b-9f74-7b19aa7cce18f2d6b0; _awl=2.1632472552.0.4-8ecbdfe1-62b25eeb80b702cff713776dd6711cb3-6763652d6575726f70652d7765737431-614d8de8-0; bm_sv=0F46C039908ACD5CB16B5A74D20AD429~GuuStFCbTl1JQXMfR8HjS4dNP1UvfT5h6D85ZjC/qezTh5+Y/8Yqms/EKHUR51BK9xMS5f+XlMafjS0171GMnV636bc+rM+yp24z9EOW75bN6qUR6Em+ZDm0WSkp5d26cBQCJUt5o+rHE5WAF5zeDQ==; _chartbeat2=.1632333352390.1632472562801.111.WV3IEfhUSRBRv5B3CqpaKXDJe5v9.2; _ga_XK44GJHVBE=GS1.1.1632472550.4.1.1632472562.0; _ga=GA1.1.1424869441.1632333352'})
    
    def parse(self, response):
        print(response.status)
        content= response.css(".program-show")
        #print(content)
        #print(response.css("body").get())
        lastNew = ""
        files= sorted_nicely(os.listdir("../../../collectedNews/US/NPR"))
        if len(files) == 0:
            j= 0
        else:
            lastNew= files[len(files)-1]
            j= len(files)
        
        for article in content:
            i= 0
            date_raw = article.css("h2::text").get().replace("Morning Edition for ", "")
            date = datetime.strptime(date_raw, "%B %d, %Y").strftime("%Y-%m-%d")
            news= article.css("section").css("article")
            if lastNew != "":
                f= open("../../../US/" + lastNew, "r+")
                searchin= json.load(f)
                if searchin[0]['date'] >= date:
                    f.close()
                    continue
            urls= []
            titles= []
            ranks= []
            for new in news:
                print("a new")
                header= new.css("div").css("h3").css("a")
                urls.append(header.css("::attr(href)").get())
                titles.append(header.css("a::text").get())
                ranks.append(str(i))
                i+=1
            edition= []
            for item in zip(titles, urls, ranks):
                scraped_info = {
                    'title': item[0],
                    'date_raw': date_raw,
                    'date': date,
                    'url': item[1],
                    'content': "",
                    'ranked': item[2],
                    'epoch': time.time()                   
                }
                edition.append(scraped_info)
            f= open("../../../collectedNews/US/NPR/news" + str(j) + ".json", "w")
            json.dump(edition, f, indent= 4, ensure_ascii=False)
            f.close()
            j+=1
                
