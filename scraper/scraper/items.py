# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    category = scrapy.Field()
    isbn13 = scrapy.Field()
    isbn10 = scrapy.Field()
    publisher = scrapy.Field()
    binding = scrapy.Field()
    height = scrapy.Field()
    noOfPages  = scrapy.Field()
    publisherDate = scrapy.Field()
    language = scrapy.Field()
    width = scrapy.Field()
    subTitle = scrapy.Field()
    weight = scrapy.Field()
    depth = scrapy.Field()
    returnable = scrapy.Field()
    price = scrapy.Field()
