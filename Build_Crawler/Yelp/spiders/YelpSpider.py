import scrapy
import re
from Yelp.items import YelpItem


class YelpSpider(scrapy.Spider):
    name = "YelpScraper"

    def start_requests(self):
        cities = []
        with open("cities_of_CA.csv", "r") as f:
            for line in f:
                cities.append(line.strip())
        url_start = 'https://www.yelp.com/search?'
        for city in cities[:2]:
            search = 'restaurants'
            location = city + ', ' + 'CA'
            url = url_start + 'find_desc=' + search + '&find_loc=' + location
            yield scrapy.Request(url, meta={"city": city, "first_page": True}, callback=self.parse)

    def parse(self, response):
        city = response.meta["city"]
        if response.meta["first_page"]:
            item = YelpItem()
            item["City"] = city
            item["Name"] = "table_start"
            yield item
        res = scrapy.Selector(response)
        place_urls = res.xpath("//h4/span[text()[contains(., '.')]]/a/@href").extract()
        for place_url in place_urls:
            url = "https://www.yelp.com" + place_url
            yield scrapy.Request(url, meta={"city": city}, callback=self.parse2)

        try:
            next_link = res.xpath("//a[contains(@class, 'next-link')]/@href").extract_first()
            next_url = "https://www.yelp.com" + next_link
            yield scrapy.Request(next_url, meta={"city": city, "first_page": False}, callback=self.parse)
        except TypeError:
            pass

    def parse2(self, response):
        place = scrapy.Selector(response)
        item = YelpItem()
        item["City"] = response.meta["city"]
        item["Name"] = place.xpath("//div[@class = 'hidden']/div/meta[@itemprop = 'name']/@content").extract_first() \
            .replace("’", "'")
        item["Rating"] = place.xpath("//div[@class = 'hidden']/div/div[@itemprop='aggregateRating']/meta/@content") \
            .extract_first()
        item["Reviews"] = place.xpath("//div[@class = 'hidden']/div/div[@itemprop='aggregateRating']/span/text()") \
            .extract_first()
        item["Price"] = place.xpath("//div[@class = 'hidden']/div/meta[@itemprop = 'priceRange']/@content") \
            .extract_first()
        item["Category"] = ",".join(place.xpath("//h1/../../span[2]/span/a/text()").extract())
        item["Address"] = ",".join(place.xpath("//div[@class = 'hidden']/div/address/span/text()").extract())

        for i, day in enumerate(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]):
            item[day] = ",".join(place.xpath("//table[contains(@class, 'hours-table')]//tr[{}]/td[1]//p/text()"
                                             .format(i+1)).extract())

        pattern = re.compile(
            '"providerUrl":.*?,"label":"(.*?)","attributionText":.*?,"icon":.*?,"title":"(.*?)"')
        amenities = re.findall(pattern, place.xpath("//script[@type = 'application/json']/text()")[2].extract())
        for amenity in amenities:
            name = amenity[1].replace(" ", "_").replace("-", "_")
            if name in ["Health_Score", "Wi_Fi", "Smoking", "Delivery", "Take_out"]:
                item[name] = amenity[0]
        yield item

        # item["Phone"] = place.xpath("//div[@class = 'hidden']/div/span[@itemprop = 'telephone']/text()").extract_first() \
        #     .strip()
        # item["Highlights"] = place.xpath("//span[contains(@class, 'business-highlight')]/text()").extract()
        # item["Name"] = place.xpath("//h1/text()").extract_first()
        # item["Rating"] = place.xpath("//div[contains(@class, 'stars')]/@aria-label").extract_first() \
        #     .replace(" star rating", "")
        # item["Reviews"] = place.xpath("//h1/../../div[2]/div[2]/p/text()").extract_first().replace(" reviews", "")
        # item["Price"] = place.xpath("//h1/../../span[1]/span/text()").extract_first()
        # item["Category"] = place.xpath("//h1/../../span[2]/span/a/text()").extract()
