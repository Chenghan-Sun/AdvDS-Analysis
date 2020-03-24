import scrapy
import re
from Yelp.items import YelpItem, ReviewItem


class YelpSpider(scrapy.Spider):
    name = "YelpScraper"
    scrap_reviews = True

    def start_requests(self):
        """
        choose the urls to start from
        """
        cities = []
        with open("cities_of_CA.csv", "r") as f:
            for line in f:
                cities.append(line.strip())
        url_start = 'https://www.yelp.com/search?'
        # crawling the TOP 12 cities in California
        for city in cities[:12]:  # choose crawling cities
            search = 'restaurants'
            location = city + ', ' + 'CA'
            url = url_start + 'find_desc=' + search + '&find_loc=' + location
            yield scrapy.Request(url, meta={"city": city, "first_page": True}, callback=self.parse)

    def parse(self, response, scrap_reviews=scrap_reviews):
        """
        parse the search pages, crawl all of the urls of restaurants
        """
        city = response.meta["city"]
        if response.meta["first_page"]:
            # yield the item to create table in the database
            item = YelpItem()
            item["City"] = city
            item["Name"] = "table_start"
            yield item

            if scrap_reviews:
                item = ReviewItem()
                item["City"] = city
                item["Restaurant"] = "table_start"
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

    def parse2(self, response, scrap_reviews=scrap_reviews):
        """
        parse the restaurant pages, download the required information
        """
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
                                             .format(i + 1)).extract())

        pattern = re.compile(
            '"providerUrl":.*?,"label":"(.*?)","attributionText":.*?,"icon":.*?,"title":"(.*?)"')
        amenities = re.findall(pattern, place.xpath("//script[@type = 'application/json']/text()")[2].extract())
        for amenity in amenities:
            name = amenity[1].replace(" ", "_").replace("-", "_")
            amen_list = ["Delivery", "Wi_Fi", "Takes_Reservations", "Parking", "Vegetarian_Options",
                         "Accepts_Credit_Cards", "Accepts_Apple_Pay", "Accepts_Google_Pay", "Take_out"]
            if name in amen_list:
                item[name] = amenity[0]
        yield item

        if scrap_reviews:
            yield scrapy.Request(response.url,
                                 meta={"city": item["City"],
                                       "restaurant": item["Name"],
                                       "avg_rate": item["Rating"]},
                                 callback=self.parse3, dont_filter=True)

    def parse3(self, response):
        """
        parse every review page of the restaurant, download all of the reviews
        """
        item = ReviewItem()
        item["City"] = response.meta["city"]
        item["Restaurant"] = response.meta["restaurant"]
        item["Avg_rate"] = response.meta["avg_rate"]
        place = scrapy.Selector(response)
        pattern_str1 = (
            '"comment":{"text":"((?:.(?!"comment":))*?)","language"(?:.(?!"comment":))*?'
            '"rating":((?:.(?!"comment":))*?),"photosUrl"(?:.(?!"comment":))*?"funny":((?:.(?!"comment":))*?),'
            '"useful":((?:.(?!"comment":))*?),"cool":((?:.(?!"comment":))*?)},"userFeedback"(?:.(?!"comment":))*?'
            '"businessOwnerReplies".*?"reviewCount":(.*?),"altText".*?"friendCount":(.*?),"displayLocation":"(.*?)",'
            '"markupDisplayName":"(.*?)","userUrl".*?"photoCount":(.*?),"link".*?"localizedDate":"(.*?)"}'
        )
        pattern_str2 = (
            '"comment":{"text":"((?:.(?!"text":))*?)","language"(?:.(?!"text":))*?'
            '"rating":((?:.(?!"text":))*?),"photosUrl"(?:.(?!"text":))*?"funny":((?:.(?!"text":))*?),'
            '"useful":((?:.(?!"text":))*?),"cool":((?:.(?!"text":))*?)},"userFeedback"(?:.(?!"text":))*?'
            '"previousReviews":\\[.*?"isUpdated":true.*?"reviewCount":(.*?),"altText".*?"friendCount":(.*?),'
            '"displayLocation":"(.*?)","markupDisplayName":"(.*?)","userUrl".*?"photoCount":(.*?),'
            '"link".*?"localizedDate":"(.*?)"}'
        )
        pattern1 = re.compile(pattern_str1)
        pattern2 = re.compile(pattern_str2)
        html_str = place.xpath("//script[@type = 'application/json']/text()")[2].extract()
        reviews = re.findall(pattern1, html_str) + re.findall(pattern2, html_str)
        for review in reviews:
            item["Content"] = review[0]
            item["Review_rate"] = review[1]
            item["Funny"] = review[2]
            item["Useful"] = review[3]
            item["Cool"] = review[4]
            item["Review_Count"] = review[5]
            item["Friend_Count"] = review[6]
            item["Location"] = review[7]
            item["User_name"] = review[8]
            item["Total_photos"] = review[9]
            item["Review_time"] = review[10]
            yield item

        try:
            next_url = place.xpath("//link[@rel = 'next']/@href").extract_first()
            yield scrapy.Request(next_url,
                                 meta={"city": item["City"],
                                       "restaurant": item["Restaurant"],
                                       "avg_rate": item["Avg_rate"]},
                                 callback=self.parse3)
        except TypeError:
            pass

