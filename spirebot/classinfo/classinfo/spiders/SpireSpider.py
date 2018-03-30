from ..items import CourseInfo
from ..items import CourseLoader
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


class SpireSpider(scrapy.Spider):
    name = 'spire'
    login_url = 'https://www.spire.umass.edu/psp/heproda/?cmd=login&languageCd=ENG#'
    start_urls = [login_url]

    def __init__(self):
        self.driver = webdriver.Chrome('C:/Users/Kerry Ngan\Miniconda3/chromedriver.exe')

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

        wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="CLASS_SRCH_WRK2_SSR_PB_CLASS_SRCH"]')))

        #select options for searching
        self.driver.find_element_by_xpath('//*[@id="UM_DERIVED_SA_UM_TERM_DESCR"]/option[3]').click() #spring 2018
        self.driver.find_element_by_xpath('//*[@id="CLASS_SRCH_WRK2_SUBJECT$108$"]/option[35]').click() #computer science
        self.driver.find_element_by_xpath('//*[@id="CLASS_SRCH_WRK2_SESSION_CODE$12$"]/option[2]').click() #university
        self.driver.find_element_by_xpath('//*[@id="CLASS_SRCH_WRK2_SSR_OPEN_ONLY"]').click() #uncheck only open courses
        self.driver.find_element_by_xpath('//*[@id="CLASS_SRCH_WRK2_SSR_PB_CLASS_SRCH"]').click() #start search
        wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="CLASS_SRCH_WRK2_SSR_PB_NEW_SEARCH"]')))
        

        #scrape spire for courses
        driver_selector = Selector(text = self.driver.page_source)

        file = open('C:/Compsci326/scrapespire/test.txt', 'w')

        
        #for selector in driver_selector.css("[id^='DERIVED_CLSRCH_DESCR200'],[id*='win0divDERIVED_CLSRCH_GROUPBOX']"):
        cloader = None
        c = 0
        for selector in driver_selector.xpath("//table[@id = 'ACE_$ICField102$0']/tbody/tr"):
            c=c+1
            file.write(str(c)+"\n")
            if(cloader is None):
                cloader = CourseLoader(item = CourseInfo(), selector = selector)
            else:
                cloader.selector = selector
            file.write("Does cloader exist: "+ str(cloader is not None)+"\n")
            file.write("name element: " +str(selector.css("[id^='DERIVED_CLSRCH_DESCR200']"))+"\n")
            file.write("date element: " +str(selector.css("[id^='MTG_DAYTIME']"))+"\n")
            if selector.css("[id^='DERIVED_CLSRCH_DESCR200']"):
                cloader.add_css('name', "[id^='DERIVED_CLSRCH_DESCR200']")
            if selector.css("[id^='MTG_DAYTIME']"):     
                cloader.add_css('date', "[id^='MTG_DAYTIME']")
            else:
                continue
            if selector.css("[id^='MTG_ROOM']"): 
                cloader.add_css('room', "[id^='MTG_ROOM']")
            if selector.css("[id^='MTG_INSTR']"): 
                cloader.add_css('instructor', "[id^='MTG_INSTR']")
            
            file.write("name value: " +str(cloader.get_output_value('name'))+"\n")
            file.write("date value: " +str(cloader.get_output_value('date'))+"\n")
            
            
            loaded = copy.deepcopy(cloader)
            cloader = None
            yield loaded.load_item()
        file.close
