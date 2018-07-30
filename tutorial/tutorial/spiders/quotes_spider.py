import scrapy
 
 
class QuotesSpider(scrapy.Spider):
    name = "quotes"
 
    def start_requests(self):
        urls = [
            'https://search.jd.com/Search?keyword=%E7%89%9B%E4%BB%94%E8%A3%A4%E7%94%B7&enc=utf-8&qrst=1&rt=1&stop=1&vt=1&page=61&s=1824&click=0',
            'https://search.jd.com/Search?keyword=%E7%89%9B%E4%BB%94%E8%A3%A4%E7%94%B7&enc=utf-8&qrst=1&rt=1&stop=1&vt=1&page=63&s=1824&click=0',
	    'https://search.jd.com/Search?keyword=%E7%89%9B%E4%BB%94%E8%A3%A4%E7%94%B7&enc=utf-8&qrst=1&rt=1&stop=1&vt=1&page=65&s=1824&click=0',
	    'https://search.jd.com/Search?keyword=%E7%89%9B%E4%BB%94%E8%A3%A4%E7%94%B7&enc=utf-8&qrst=1&rt=1&stop=1&vt=1&page=67&s=1824&click=0',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
 
    def parse(self, response):
	parameters = response.url.split("&")
	for p_str in parameters:
            print(len(parameters))
            print(p_str)
        page = response.url.split("&")[-3]
        filename = 'jdquotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
