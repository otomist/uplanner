# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from schedule.models import Term, Department, Course, Section, Gened

class spirebotPipeline(object):

    def process_item(self, item, spider):
        if ('code' in item.fields and 'code' in item and Department.objects.filter(code = item['code']).exists()):
            if(item['code'] == Department.object.get(code = item['code']).code):
                return

        if ('number' in item.fields and 
            'number' in item and
            'title' in item and
            'session' in item and 
            'dept' in item and 
            Course.objects.filter(title = item['title'], session = item['session'], dept = item['dept'], number = item['number']).exists()):
            if(item['number'] == Course.objects.filter(title = item['title'], session = item['session'], dept = item['dept']).get(number = item['number']).number):
                return
        
        if ('sid' in item.fields and 'sid' in item and Section.objects.filter(sid = item['sid']).exists()):
            if(item['sid'] == str(Section.objects.get(sid = item['sid']).sid)):
                return
        
        if ('season' in item.fields and
            'year' in item.fields and
            'season' in item and 
            'year' in item and
            Term.objects.filter(season = item['season'], year = item['year']).exists()):

            if(item['season'] == Term.objects.filter(season = item['season']).get(year = item['year']).season):
                return
        
        if ('all_gened' in item.fields and 'all_gened' in item and item['all_gened'] != 'None' and 'number' in item):
            gened_dict = {
                'CW' : 'College Writing',
                'R1' : 'Basic Math Skills',
                'R2' : 'Analytical Reasoning',
                'BS' : 'Biological Science',
                'PS' : 'Physical Science',
                'AL' : 'Literature',
                'AT' : 'Arts',
                'HS' : 'Historical Study',
                'SB' : 'Social and Behavioral Sciences',
                'U' : 'United States',
                'DU' : 'Diversity in the United States',
                'G' : 'Global',
                'DG' : 'Diversity in the Globe',
                'I' : 'Interdisciplinary',
                'SI' : 'Science Interdisciplinary',
            }

            item.save()
            course_object = Course.objects.filter(title = item['title']).filter(session = item['session']).get(number = item['number'])

            for gened_attr in item['all_gened'].split(' '):
                if not Gened.objects.filter(code = gened_attr).exists():
                    Gened(name = gened_dict[gened_attr], code = gened_attr).save()

                course_object.gened.add(Gened.objects.get(code = gened_attr))

            return item
        
        item.save() #save scraped attributes to django database 
        return item
        
        
        