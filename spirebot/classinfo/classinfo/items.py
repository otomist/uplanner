# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import re
import scrapy
from scrapy.loader import ItemLoader
from scrapy.contrib.djangoitem import DjangoItem
from scrapy.loader.processors import TakeFirst, MapCompose, Join
from scrapy.loader.processors import Identity
from scrapy.utils.markup import (remove_tags, replace_escape_chars)

from schedule.models import Course

class CourseInfo(scrapy.Item):
    name = scrapy.Field()
    status = scrapy.Field()
    class_number = scrapy.Field()
    session = scrapy.Field()
    units = scrapy.Field()
    class_component = scrapy.Field()
    career = scrapy.Field()
    grading = scrapy.Field()
    gened = scrapy.Field()
    rap_tap_hlc = scrapy.Field()
    topic = scrapy.Field()
    date = scrapy.Field()
    room = scrapy.Field()
    instructor = scrapy.Field()
    meet_dates = scrapy.Field()
    add_consent = scrapy.Field()
    enrollement_req = scrapy.Field()
    description = scrapy.Field()
    textbook = scrapy.Field()
    class_overview = scrapy.Field()

class CourseItem(DjangoItem):
    django_model = Course

    
class CourseLoader(ItemLoader):
    default_item_class = CourseInfo
    default_input_processor = MapCompose(remove_tags, replace_escape_chars)
    default_output_processor = TakeFirst()

    date_out = Join()
