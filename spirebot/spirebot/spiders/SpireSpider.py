from ..items import CourseItem, GenedItem, DepartmentItem, TermItem, SectionItem, ScheduleItem, ScheduleCourseItem
from ..items import ItemLoader
import logging
import copy
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import scrapy
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from scrapy.http import Request
from scrapy.shell import inspect_response

from schedule.models import Term, Department, Course



class SpireSpider(scrapy.Spider):
    name = 'spire'
    login_url = 'https://www.spire.umass.edu/psp/heproda/?cmd=login&languageCd=ENG#'
    start_urls = [login_url]

    def __init__(self):
        self.driver = webdriver.Chrome('C:/Users/Kerry Ngan\Miniconda3/chromedriver.exe')
    
    def load_termitem(self, page_selector, index):
        term_loader = ItemLoader(item = TermItem(), selector = page_selector)
        course_loader.add_xpath('season', '//*[@id="UM_DERIVED_SA_UM_TERM_DESCR"]/option['+ str(course_index) +']')
        course_loader.add_xpath('year', '//*[@id="UM_DERIVED_SA_UM_TERM_DESCR"]/option['+ str(course_index) +']')
    
    #creates an item for each section and passes it into a pipeline
    def load_courseitem(self, page1_selector, page2_selector, index):  
        course_loader = ItemLoader(item = CourseItem(), selector = page1_selector)

        course_loader.add_css('title', "[id^='DERIVED_CLSRCH_DESCR200$" + str(index) + "']")
        course_loader.add_css('dept', "[id^='DERIVED_CLSRCH_DESCR200$" + str(index) + "']")
        course_loader.add_css('number', "[id^='DERIVED_CLSRCH_DESCR200$" + str(index) + "']")
        course_loader.add_css('honors', "[id^='DERIVED_CLSRCH_DESCR200$" + str(index) + "']")

        course_loader.selector = page2_selector

        if page2_selector.css("[id^='win0divDERIVED_CLSRCH_DESCRLONG']"):
            course_loader.add_css('description', "[id^='win0divDERIVED_CLSRCH_DESCRLONG']")
        else: 
            course_loader.add_value('description', "Not available at this time")

        if page2_selector.css("#SSR_CLS_DTL_WRK_SSR_REQUISITE_LONG"):
            course_loader.add_css('reqs', "#SSR_CLS_DTL_WRK_SSR_REQUISITE_LONG")
        else: 
            course_loader.add_value('reqs', "Not available at this time")

        course_loader.add_css('credits', "[id^='SSR_CLS_DTL_WRK_UNITS_RANGE']")
        course_loader.add_css('career', "[id^='PSXLATITEM_XLATLONGNAME$33$']")
        
        course_loader.add_css('session', "[id='PSXLATITEM_XLATLONGNAME']")
        #course_loader.add_value('gened', 'social behavior')MTG_DATE$0
        course_loader.add_css('start_date', "[id^='MTG_DATE']")
        course_loader.add_css('end_date', "[id^='MTG_DATE']") 

        return course_loader.load_item()

    def load_sectionitem(self, page1_selector, page2_selector, index): 
        section_loader = ItemLoader(item = SectionItem(), selector = page1_selector)
        #SSR_CLS_DTL_WRK_CLASS_NBR

        course_loader.add_css('id', "[id^='SSR_CLS_DTL_WRK_CLASS_NBR']")
        course_loader.add_css('days', "[id^='MTG_SCHED$0']")
        course_loader.add_css('start', "[id^='MTG_SCHED$0']")
        course_loader.add_css('end', "[id^='MTG_SCHED$0']")
        course_loader.add_css('term', "[id^='MTG_SCHED$0']") #foriegn key


    def parse(self, response):
        wait = WebDriverWait(self.driver,10)

        #login to spire
        self.driver.get(response.url)
        username = self.driver.find_element_by_id('userid')
        password = self.driver.find_element_by_id('pwd')
        with open('C:/Users/Kerry Ngan/Documents/login_info.txt') as f:
            line = f.read()
        f.close()
        login_info = line.split()
        username.send_keys(login_info[0])
        password.send_keys(login_info[1])
        self.driver.find_element_by_name('Submit').submit()

        #move to student center
        wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="ptifrmtgtframe"]')))
        student_center_url =self.driver.find_element_by_xpath('//*[@id="ptifrmtgtframe"]').get_attribute('src')
        self.driver.get(student_center_url)

        #click on class search button
        class_search = self.driver.find_element_by_xpath('//*[@id="DERIVED_SSS_SCL_SSS_GO_4$83$"]') 
        class_search.click()

        wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="CLASS_SRCH_WRK2_SSR_PB_CLASS_SRCH$29$"]')))

        #select options for searching
        option_selector = Selector(text = self.driver.page_source)
        term_index = 3
        self.load_termitem(option_selector, term_index)
        
        self.driver.find_element_by_xpath('//*[@id="UM_DERIVED_SA_UM_TERM_DESCR"]/option['+ str(course_index) +']').click() #spring 2018
        self.driver.find_element_by_xpath('//*[@id="CLASS_SRCH_WRK2_SUBJECT$108$"]/option[35]').click() #computer science
        self.driver.find_element_by_xpath('//*[@id="CLASS_SRCH_WRK2_SESSION_CODE$12$"]/option[2]').click() #university
        self.driver.find_element_by_xpath('//*[@id="CLASS_SRCH_WRK2_SSR_OPEN_ONLY"]').click() #uncheck only open courses
        self.driver.find_element_by_xpath('//*[@id="CLASS_SRCH_WRK2_SSR_PB_CLASS_SRCH"]').click() #start search
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"[id^='DERIVED_CLSRCH_SSR_CLASSNAME_LONG$']")))
        

        #start scraping spire for course information
        page1_selector = Selector(text = self.driver.page_source)
        course_index = 0
        selector_index = 0 #count of the links on the page

        while self.driver.find_elements_by_css_selector("[id^='ACE_$ICField106$" + str(course_index) + "']"):
            is_course = False
            while  self.driver.find_element_by_css_selector("[id^='ACE_$ICField106$" + str(course_index) + "']").find_elements_by_css_selector("[id^='DERIVED_CLSRCH_SSR_CLASSNAME_LONG$" + str(selector_index) + "']"): 
                
                search_result = self.driver.find_element_by_css_selector("[id^='DERIVED_CLSRCH_SSR_CLASSNAME_LONG$" + str(selector_index) + "']") #finds the first section for a course
                search_result.click() #clicks on the section
                wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="CLASS_SRCH_WRK2_SSR_PB_BACK"]'))) #wait for page to load
                page2_selector = Selector(text = self.driver.page_source)#update the driver selector2 with the current page source
                
                if(not is_course):
                    yield self.load_courseitem(page1_selector, page2_selector, course_index)
                    is_course = True

                #webelement2_list.append(driver_selector.xpath("//div[@id = 'win0divPSPAGECONTAINER']/table/tbody/tr")) #splits the page source into elements for each row 
                #yield self.load_sectionitem(page1_selector,page2_selector,selector_index)

                self.driver.find_element_by_css_selector("[id^='CLASS_SRCH_WRK2_SSR_PB_BACK']").click() #clicks on view search results to go back
                wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"[id^='DERIVED_CLSRCH_SSR_CLASSNAME_LONG$" + str(selector_index) + "']")))#wait for page to load
                selector_index = selector_index + 1

            course_index = course_index + 1
    
        self.driver.quit()
            

