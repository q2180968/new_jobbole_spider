# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join
from datetime import datetime
import re


class JobboleSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ArticleItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


def get_datetime(value):
    value = value.strip().replace('·', '').strip()
    try:
        create_date = datetime.strptime(value, '%Y%M%D').date()
    except Exception as e:
        create_date = datetime.now().date()
    return create_date


def image_filter(value):
    return value


def num_filter(value):
    pattern = r'.*?(\d+).*?'
    match_re = re.match(pattern, value)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0
    return nums


def tag_filter(value):
    if '评论' in value:
        return ''
    else:
        return value


class ArticleItem(scrapy.Item):
    title = scrapy.Field()
    create_date = scrapy.Field(
        input_processor=MapCompose(get_datetime)
    )
    url = scrapy.Field()
    url_obj_id = scrapy.Field()
    front_image_url = scrapy.Field(
        output_processor=MapCompose(image_filter)
    )
    front_image_path = scrapy.Field()
    praise_nums = scrapy.Field(
        input_processor=MapCompose(num_filter)
    )
    comment_nums = scrapy.Field(
        input_processor=MapCompose(num_filter)
    )
    fav_nums = scrapy.Field(
        input_processor=MapCompose(num_filter)
    )
    tags = scrapy.Field(
        input_processor=MapCompose(tag_filter),
        output_processor=Join(',')
    )
    content = scrapy.Field()
