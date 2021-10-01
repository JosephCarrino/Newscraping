import scrapy


class RtsurlgetSpider(scrapy.Spider):
    name = 'rtsURLGet'
    urls= []
    for i in range(1, 50):
        urls.append("https://www.rts.ch/hbv7/ajax/emissions/25000623/audios?offset=" + str(i))
        i+=6
    allowed_domains = ['www.rts.ch/audio-podcast/emissions/2021/emission/le-12h30-25000623.html']
    start_urls = "https://www.rts.ch/hbv7/ajax/emissions/25000623/audios?offset=1"

    def parse(self, response):
        contents= response.css(".list-item")
        urls= []
        for content in contents[0:len(contents)-1]:
            urls.append(content.css("a::attr(href)").get())
        f= open("rtsurls.txt", "a")
        for url in urls:
            f.write(url + "\n")
        f.close()
