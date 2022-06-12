# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.exceptions import CloseSpider
import downFiles
from downFiles.items import DownfilesItem

class Crawler(CrawlSpider):
    name = 'Scrapy_Crawler'
    allowed_domains = ['www.nirsoft.net'] # Here put desired domain restriction
    start_urls = ['http://www.nirsoft.net/'] # Here put desired url
  
    Max_Pages = 1000 # Here change how many maximum pages you would like.
    Max_Depth = 1 # Here change desired maximum depth
    
    
    count = 0 # The count starts at zero.
    
    custom_settings = {
        'DEPTH_LIMIT': str(Max_Depth),
    }  
  
    rules = (
        Rule(LinkExtractor(allow=''),
         callback='parse_item', follow = True),
    )
  
    def parse_item(self, response):
            # Return if more than N
        if self.count >= self.Max_Pages:
            raise CloseSpider(f"Scraped {self.N} items. Eject!")
        # Increment to count by one:
        self.count += 1
        
        file_url = response.css('.downloadline::attr(href)').get()
        file_url = response.urljoin(file_url)
        file_extension = file_url.split('.')[-1]
        if file_extension not in ('html'):
            return
        item = DownfilesItem()
        item['file_urls'] = [file_url]
        item['original_file_name'] = file_url.split('/')[-1]
        yield item