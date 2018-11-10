import scrapy
import re, os, time, shutil
from scrapy.linkextractor import LinkExtractor
from scrapy.selector import Selector
from imagecrawler.items import ImagecrawlerItem

class PexelsScraper(scrapy.Spider):
    name = "pexels"
    src_extractor = re.compile('src="([^"]*)"')
    tags_extractor = re.compile('alt="([^"]*)"')

    # Define the regex we'll need to filter the returned links
    url_matcher = re.compile('^https:\/\/www\.pexels\.com\/photo\/')
    
    # Create a set that'll keep track of ids we've crawled
    crawled_ids = set()

    
    def start_requests(self):
        url = "https://www.pexels.com/search/selfie"
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
	    body = Selector(text=response.body)
	    images = body.css('img.image-section__image').extract()
	    result = body.css('img.image-section__image ::attr(src)').extract_first()


	    #yield {'img_url': result}
	    yield ImagecrawlerItem(file_urls=[result])
	    
	    if len(os.listdir('/work/imagecrawler/output/full')) > 0:
	    	for name in os.listdir('/work/imagecrawler/output/full'):
	    		temp = name.find('?')
	    		new_name = name[:temp]
	    		shutil.copy('/work/imagecrawler/output/full/' + name, '/work/imagecrawler/output/result/' + new_name)


	    # body.css().extract() returns a list which might be empty
	    #for image in images:
	        #img_url = PexelsScraper.src_extractor.findall(image)[0]
	        #tags = [tag.replace(',', '').lower() for tag in PexelsScraper.tags_extractor.findall(image)[0].split(' ')]   
	        #yield {'img_url': img_url}
	        #yield {'img_tags': tags}



	    link_extractor = LinkExtractor(allow=PexelsScraper.url_matcher)
	    next_links = [link.url for link in link_extractor.extract_links(response) if not self.is_extracted(link.url)]
	    #yield {'next_links': next_links}
	    for link in next_links:
	        yield scrapy.Request(link, self.parse)


	    
	    # Crawl the filtered links
    def is_extracted(self, url):
        # Image urls are of type: https://www.pexels.com/photo/asphalt-blur-clouds-dawn-392010/
        id = url.split('/')[-2].split('-')[-1]
        if id not in PexelsScraper.crawled_ids:
            PexelsScraper.crawled_ids.add(id)
            return False
        return True
        