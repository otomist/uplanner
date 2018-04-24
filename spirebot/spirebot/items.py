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
    #course
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

    def proc_credits(input_str):
        return input_str.replace(' ', '')

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
        end_date = date_list[1]  #"month/day/year"
        date_split = end_date.split('/')  #["month", "day", "year"]
        return date_split[2] + '-' + date_split[0] + '-' + date_split[1]  #"year-month-day"

    #term
    def proc_season(input_str):
        season_dict = {
            'Winter': 'w',
            'Summer' : 't',
            'Spring' : 's',
            'Fall' : 'f',
        }
        return season_dict[input_str.split(' ')[1]]
    
    def proc_year(input_str):
        return input_str.split(' ')[0]
    
    #section
    def proc_days(input_str):
        if ('Mo' not in input_str and 
            'Tu' not in input_str and 
            'We' not in input_str and 
            'Th' not in input_str and 
            'Fr' not in input_str and
            'Sa' not in input_str and
            'Su' not in input_str ):
            return 'TBA'     

        daytime_list = re.split(r'[\s-]+', input_str)
        return daytime_list[0]
    
    def proc_mon(input_str):
        return '1' if 'Mo' in input_str else '0'
    
    def proc_tue(input_str):
        return '1' if 'Tu' in input_str else '0'
    
    def proc_wed(input_str):
        return '1' if 'We' in input_str else '0'

    def proc_thu(input_str):
        return '1' if 'Th' in input_str else '0'
    
    def proc_fri(input_str):
        return '1' if 'Fr' in input_str else '0'
        
    
    def proc_start(input_str):

        start_time = None

        if(input_str == 'TBA'):
            return '00:00:00'
        militarytime = None

        daytime_list = re.split(r'[\s-]+', input_str)

        if 'Mo' not in input_str and 'Tu' not in input_str and 'We' not in input_str and 'Th' not in input_str and 'Fr' not in input_str:
            start_time = daytime_list[0]
        else:
            start_time = daytime_list[1]

        if 'PM' in start_time:
            militarytime = 12
        if 'AM' in start_time:
            militarytime = 0

        time = re.sub(r'[APM]+','', start_time).split(':') #5:15PM becomes ["5","15"]
        militarytime = militarytime + int(time[0])

        return str(militarytime) + ':' + time[1] + ':00'

    def proc_ending(input_str):
        
        end_time = None

        if(input_str == 'TBA'):
            return '00:00:00'

        militarytime = None

        daytime_list = re.split(r'[\s-]+', input_str)

        if 'Mo' not in input_str and 'Tu' not in input_str and 'We' not in input_str and 'Th' not in input_str and 'Fr' not in input_str:
            end_time = daytime_list[0]
        else:
            end_time = daytime_list[2]

        if 'PM' in end_time:
            militarytime = 12
        if 'AM' in end_time:
            militarytime = 0

        time = re.sub(r'[APM]+','', end_time).split(':') #5:15PM becomes ["5","15"]
        militarytime = militarytime + int(time[0])

        return str(militarytime) + ':' + time[1] + ':00'

    def proc_term(input_str):
        season_dict = {
            'Winter': 'w',
            'Summer' : 't',
            'Spring' : 's',
            'Fall' : 'f',
        }
        season = season_dict[input_str.split(' ')[1]]
        year = input_str.split(' ')[0]
        return Term.objects.filter(season = season).get(year = year)
    
    def proc_open(input_str):
        return '1' if input_str == 'Open' else '0'

    def proc_clss(input_str):
        return Course.objects.get(number = input_str.split()[1])
    
    def proc_component(input_str):
        return input_str.split('-')[1][0:3]




    default_item_class = CourseInfo
    
    default_input_processor = MapCompose(default_proc)
    default_output_processor = TakeFirst()

    #course model attributes
    title_in = MapCompose(default_proc, proc_title)
    dept_in = MapCompose(default_proc, proc_dept)
    number_in = MapCompose(default_proc, proc_number)
    honors_in = MapCompose(default_proc, proc_honor)
    credits_in = MapCompose(default_proc, proc_credits)
    career_in = MapCompose(default_proc, proc_career)
    session_in = MapCompose(default_proc, proc_session)
    start_date_in = MapCompose(default_proc, proc_start_date)
    end_date_in = MapCompose(default_proc, proc_end_date)

    #term model attributes
    season_in = MapCompose(default_proc, proc_season)
    year_in = MapCompose(default_proc, proc_year)

    #section model atributes
    days_in = MapCompose(default_proc, proc_days)
    mon_in = MapCompose(default_proc, proc_mon)
    tue_in = MapCompose(default_proc, proc_tue)
    wed_in  = MapCompose(default_proc, proc_wed)
    thu_in = MapCompose(default_proc, proc_thu)
    fri_in = MapCompose(default_proc, proc_fri)
    start_in = MapCompose(default_proc, proc_start)
    ending_in = MapCompose(default_proc, proc_ending)
    term_in = MapCompose(default_proc, proc_term)
    open_in = MapCompose(default_proc, proc_open)
    clss_in = MapCompose(default_proc, proc_clss)
    component_in = MapCompose(default_proc, proc_component)