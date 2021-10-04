import scrapy


class Gr1urlgetSpider(scrapy.Spider):
    name = 'gr1URLGet'
    allowed_domains = ['www.raiplayradio.it/programmi/archiviogr1/archivio/puntate']
    start_urls = ['https://www.raiplayradio.it/programmi/archiviogr1/archivio/puntate/Agosto-2021-082e428d-6b15-444a-8f82-6ea3c335fb9f/3',
                 'https://www.raiplayradio.it/programmi/archiviogr1/archivio/puntate/Agosto-2021-082e428d-6b15-444a-8f82-6ea3c335fb9f/4',
                 'https://www.raiplayradio.it/programmi/archiviogr1/archivio/puntate/Agosto-2021-082e428d-6b15-444a-8f82-6ea3c335fb9f/5',
                 'https://www.raiplayradio.it/programmi/archiviogr1/archivio/puntate/Agosto-2021-082e428d-6b15-444a-8f82-6ea3c335fb9f/6',
                 'https://www.raiplayradio.it/programmi/archiviogr1/archivio/puntate/Agosto-2021-082e428d-6b15-444a-8f82-6ea3c335fb9f/7']

    def parse(self, response):
        #get the single GR1 edition url and put it in the gr1urls.txt file
        base_url= "https://www.raiplayradio.it"
        content= response.css(".listaAudio")
        headers= content.css("h3")
        toRet= []
        urls= headers.css("a::attr(href)").getall()
        titles= headers.css("a::text").getall()
        for item in zip(titles, urls):
            print(item[0])
            print(" con url: ")
            print(item[1])
            if item[0][8] == "8":
                toRet.append(item[1])
        f= open("gr1urls.txt", "a")
        for turl in toRet:    
            f.write(base_url + turl + "\n")
        f.close()
