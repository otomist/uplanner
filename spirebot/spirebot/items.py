# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import re
import scrapy
from scrapy.loader import ItemLoader
from scrapy_djangoitem import DjangoItem
from scrapy.loader.processors import TakeFirst, Compose, MapCompose, Join, Identity
from scrapy.utils.markup import (remove_tags, replace_escape_chars)

from schedule.models import Gened
from schedule.models import Department
from schedule.models import Term
from schedule.models import Course
from schedule.models import Section
from schedule.models import Schedule
from schedule.models import ScheduleCourse

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

class GenedItem(DjangoItem):
    django_model = Gened

class DepartmentItem(DjangoItem):
    django_model = Department

class TermItem(DjangoItem):
    django_model = Term
    season = scrapy.Field()
    
class SectionItem(DjangoItem):
    django_model = Section

class ScheduleItem(DjangoItem):
    django_model = Schedule

class ScheduleCourseItem(DjangoItem):
    django_model = ScheduleCourse
    
class ItemLoader(ItemLoader):

    def default_proc(input):
        input = remove_tags(input)
        input = replace_escape_chars(input)
        return input

    def proc_title(input_str):
        title = ''     
        words = input_str.split()
        for word in words[2:]:
            title = title + word + ' '
        return title
    
    def proc_dept(input_str): 
        words = input_str.split()
        return Department.objects.get(code = words[0])

    def proc_number(input_str):
        words = input_str.split()
        return words[1]
    
    def proc_honor(input_str):
        words = input_str.split()
        return '1' if words[1][0] == 'H' else '0'

    def proc_career(input_str):
        career_dict = {
            'Undergraduate' : 'u',
            'Graduate' : 'g',
            'Non-Credit' : 'c',
            'Non_Degree' : 'd',
        }
        return career_dict[input_str]
    
    def proc_session(input_str):
        session_dict = {
            'University' : 'un',
            'University Eligible/CPE' : 'uc',
            'University Non-standard Dates' : 'ud',
            'CPE Summer Session 1' : 'c1',
            'CPE Summer Session 2' : 'c2',
            'CPE Summer Session 3' : 'c3',
        }

        return session_dict[input_str[1:]]
    
    def proc_start_date(input_str):
        date_list = re.split(r'[\s-]+', input_str)
        start_date = date_list[0]
        date_split = start_date.split('/')
        return date_split[2] + '-' + date_split[0] + '-' + date_split[1]
    
    def proc_end_date(input_str):
        date_list = re.split(r'[\s-]+', input_str)
        end_date = date_list[1]
        date_split = end_date.split('/')
        return date_split[2] + '-' + date_split[0] + '-' + date_split[1]

    default_item_class = CourseInfo
    
    default_input_processor = MapCompose(default_proc)
    default_output_processor = TakeFirst()

    title_in = MapCompose(default_proc, proc_title)
    dept_in = MapCompose(default_proc, proc_dept)
    number_in = MapCompose(default_proc, proc_number)
    honors_in = MapCompose(default_proc, proc_honor)
    career_in = MapCompose(default_proc, proc_career)
    session_in = MapCompose(default_proc, proc_session)
    start_date_in = MapCompose(default_proc, proc_start_date)
    end_date_in = MapCompose(default_proc, proc_end_date)

