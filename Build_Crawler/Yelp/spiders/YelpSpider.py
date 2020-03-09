import scrapy
from Yelp.items import YelpItem


class YelpSpider(scrapy.Spider):
    name = "YelpScraper"

    def start_requests(self):
        url = 'https://www.yelp.com/search?'
        search = getattr(self, 'search', 'restaurants')
        location = getattr(self, 'location', 'San Francisco, CA')
        url = url + 'find_desc=' + search + '&find_loc=' + location
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        res = scrapy.Selector(response)
        place_urls = res.xpath("//h4/span[text()[contains(., '.')]]/a/@href").extract()
        for place_url in place_urls:
            url = "https://www.yelp.com" + place_url
            yield scrapy.Request(url, self.parse2)

        try:
            next_link = res.xpath("//a[contains(@class, 'next-link')]/@href").extract_first()
            next_url = "https://www.yelp.com" + next_link
            yield scrapy.Request(next_url, self.parse)
        except TypeError:
            pass

    def parse2(self, response):
        place = scrapy.Selector(response)
        item = YelpItem()
        item["Name"] = place.xpath("//div[@class = 'hidden']/div/meta[@itemprop = 'name']/@content").extract_first()\
            .replace("’", "'")
        item["Rating"] = place.xpath("//div[@class = 'hidden']/div/div[@itemprop='aggregateRating']/meta/@content")\
            .extract_first()
        item["Reviews"] = place.xpath("//div[@class = 'hidden']/div/div[@itemprop='aggregateRating']/span/text()")\
            .extract_first()
        item["Price"] = place.xpath("//div[@class = 'hidden']/div/meta[@itemprop = 'priceRange']/@content")\
            .extract_first()
        item["Category"] = place.xpath("//h1/../../span[2]/span/a/text()").extract()
        item["Address"] = place.xpath("//div[@class = 'hidden']/div/address/span/text()").extract()
        item["Phone"] = place.xpath("//div[@class = 'hidden']/div/span[@itemprop = 'telephone']/text()").extract_first()\
            .strip()
        yield item

        # item["Name"] = place.xpath("//h1/text()").extract_first()
        # item["Rating"] = place.xpath("//div[contains(@class, 'stars')]/@aria-label").extract_first() \
        #     .replace(" star rating", "")
        # item["Reviews"] = place.xpath("//h1/../../div[2]/div[2]/p/text()").extract_first().replace(" reviews", "")
        # item["Price"] = place.xpath("//h1/../../span[1]/span/text()").extract_first()
        # item["Category"] = place.xpath("//h1/../../span[2]/span/a/text()").extract()