from urlparse import urljoin
from scrapy import Spider, Request
from pycon_speakers.loaders import SpeakerLoader


class EuroPython(Spider):
    name = 'europython.eu'
    years = '2006,2008,2009,2010,2011,2012,2013,2014'

    def start_requests(self):
        years = [int(x) for x in self.years.split(',')]
        for year in years:
            url = 'http://lanyrd.com/{0}/europython/speakers/'
            callback = self.parse
            if year >= 2011:
                url = 'https://ep2013.europython.eu/ep{0}'
                callback = self.parse_new
            yield Request(url.format(year), callback, meta={'cookiejar': year})

    def parse(self, response):
        for speaker in response.css('div.mini-profile'):
            il = SpeakerLoader(selector=speaker)
            il.add_css('name', ".name > a::text")
            il.add_css('image_urls', "img::attr(src)")
            il.add_value('year', str(response.meta['cookiejar']))
            yield il.load_item()
        # pagination
        pages = response.css('.pagination a::attr(href)').extract()
        for page in pages:
            yield Request(urljoin(response.url, page), meta=response.meta)

    def parse_new(self, response):
        for speaker in response.css('.archive .talk .speakers > .speaker'):
            il = SpeakerLoader(selector=speaker)
            il.add_css('name', "span::text")
            il.add_css('image_urls', "a > img::attr(src)", lambda x:
                        [urljoin(response.url, y) for y in x])
            il.add_value('year', str(response.meta['cookiejar']))
            yield il.load_item()

