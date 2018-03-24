# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyMtimesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    movie_id=scrapy.Field()
    movie_name_cn = scrapy.Field()
    movie_name_en = scrapy.Field()
    movie_type = scrapy.Field()
    public_time = scrapy.Field()
    public_country = scrapy.Field()
    public_distributor = scrapy.Field()
    director = scrapy.Field()
    screen_writer = scrapy.Field()
    actors = scrapy.Field()
    plot = scrapy.Field()
    box_office = scrapy.Field()
    rating = scrapy.Field()
    hot = scrapy.Field()
