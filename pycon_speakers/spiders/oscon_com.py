from scrapy import Spider, Request
from pycon_speakers.loaders import SpeakerLoader

class OsConSpider(Spider):
    name = 'oscon.com'
    years = '2013,2012,2011,2010,2009,2008,2007'
    base_url = 'http://www.oscon.com/oscon{year}/public/schedule/speakers'

    def start_requests(self):
        years = [int(x) for x in self.years.split(',')]
        for year in years:
            meta = {'year': year}
            url = self.base_url.format(year=year)
            yield Request(url, meta=meta)

    def parse(self, response):
        for speaker in response.xpath('//span[@class="en_speaker_name"]').extract():
            il = SpeakerLoader()
            il.add_value('name', speaker)
            il.add_value('year', str(response.meta['year']))
            yield il.load_item()
