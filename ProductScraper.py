from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from lxml import etree
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time
import json
import pickle

start_links = [
    'https://www.walmart.com/browse/sports-outdoors/baseball-gear-equipment/4125_4161_4162?povid=HardlinesGlobalNav_DSK_SportsOutdoors_Sports_Baseball'
    ]

# import pickle
# import selenium.webdriver

# driver = webdriver.ChromeOptions()

# opts = webdriver.ChromeOptions() 
# opts.add_experimental_option("excludeSwitches", ["enable-automation"])
# opts.add_experimental_option('useAutomationExtension', False)
# opts.add_experimental_option('excludeSwitches', ['enable-logging'])
# opts.add_argument('--disable-blink-features=AutomationControlled')
# opts.add_argument('--ignore-ssl-errors=yes')
# opts.add_argument('--ignore-certificate-errors')
# opts.add_argument("--disable-javascript")
# opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36")

# driver = webdriver.Chrome('./chromedriver',options=opts)
# driver.get("http://www.google.com")
# input("Enter")
# pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))


class Scraper():
    #Initialising Scraper
    def __init__(self, start_link):
        self.start_links = start_links
        self.master_url = self.start_links[0]
        self.robot = '//*[contains(text(),"To proceed, please verify that you are not a robot.")]'
        self.master_dict = {'cat':[],'link':[]}
        self.nth = 0
        opts = webdriver.ChromeOptions()
        opts.add_experimental_option("excludeSwitches", ["enable-automation"])
        opts.add_experimental_option('useAutomationExtension', False)
        opts.add_experimental_option('excludeSwitches', ['enable-logging'])
        opts.add_argument('--disable-blink-features=AutomationControlled')
        opts.add_argument('--ignore-ssl-errors=yes')
        opts.add_argument('--ignore-certificate-errors')
        #opts.add_argument("--disable-javascript")
        opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36")
        self.driver = webdriver.Chrome('./chromedriver',options=opts)
        self.driver.get("http://www.walmart.com")
        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            self.driver.add_cookie(cookie)

    
    def clickDepartmentAndShowMore(self):
        #check robo
        self.roboCheck()
        
        xp_departments_button = '//*[@class="pb6 pr3"]//*[contains(text(),"Departments")]'
        xp_show_more_button = '//*[@class="pb6 pr3"]//*[contains(text(),"Show More")]'
        try:
            self.departments_button = self.driver.find_element(By.XPATH, xp_departments_button)
        except:
            time.sleep(2)
            self.departments_button = self.driver.find_element(By.XPATH, xp_departments_button)
        #click on department button
        self.driver.execute_script("arguments[0].scrollIntoView();", self.departments_button)
        self.departments_button.click()
        time.sleep(1)
        show_more_button = self.driver.find_elements(By.XPATH, xp_show_more_button)
        #click on show more if exists
        if len(show_more_button) > 0:
            self.driver.execute_script("arguments[0].scrollIntoView();", show_more_button[0])
            show_more_button[0].click()
        #check again robo
        self.roboCheck()
        time.sleep(1)
        arrow = self.driver.find_element(By.XPATH,"//*[@class='pb6 pr3']//*[contains(text(),'Departments')]//following-sibling::*")
        if arrow.get_attribute("class") == "ld ld-ChevronUp pa0":
            pass
        elif arrow.get_attribute("class") == "ld ld-ChevronDown pa0":
            self.clickDepartmentAndShowMore()

    def roboCheck(self):
        robo_xp = '//*[contains(text(),"Robot or human?")]'
        robo_check_element = self.driver.find_elements(By.XPATH, robo_xp)
        if len(robo_check_element) >0:
            input("Please solve puzzle and press enter to continue")
            try:
                self.clickDepartmentAndShowMore()
            except:
                pass
    
    def click_nth_radio_button(self):
        radio_b_xp = '//*[@class="pb6 pr3"]//*[contains(text(),"Departments")]//ancestor::*[@class="expand-collapse-section"]//*[@class="ml4"]/div'
        self.driver.execute_script("arguments[0].scrollIntoView();", self.departments_button)
        time.sleep(1)
        radio_bs = self.driver.find_elements(By.XPATH, radio_b_xp )
        self.len_radio_buttons = len(radio_bs)

        self.driver.execute_script("arguments[0].scrollIntoView();", radio_bs[0])
        radio_bs[self.nth].click()
        self.nth = self.nth+1

    
    def check_for_subdepartments(self):
        # { {fn1}
        # if subD exist: fn1 else: append to start urls}
        self.clickDepartmentAndShowMore()
        time.sleep(1)
        radio_b_xp = '//*[@class="pb6 pr3"]//*[contains(text(),"Departments")]//ancestor::*[@class="expand-collapse-section"]//*[@class="ml4"]/div'
        curr_len_radio_bs = len(self.driver.find_elements(By.XPATH, radio_b_xp))
        if curr_len_radio_bs == 0:
            self.get_cat()
        else:
            self.start_links.append(self.driver.current_url)


    def get_cat(self):
        print(self.driver.current_url)
    
    def check_update_master_link(self):
        # master_check  = { keep url as master url untill nth radio button ( if leb(radiobuttons) > n else: master_url = master_urls[]}
        try:
            if self.len_radio_buttons > self.nth:
                pass
            else:
                self.master_url = self.start_links[ self.start_links.index(self.master_url) + 1 ]
        except Exception as e:
            print(e)    
    
    
    
    def run(self):
        while True:
            #open master url
            self.driver.get(self.master_url)
            time.sleep(2)
            #click dep button and show more[if_exist]
            self.clickDepartmentAndShowMore()
            time.sleep(1)
            #click nth radio button
            self.click_nth_radio_button()
            time.sleep(3)
            #check for subD
            self.check_for_subdepartments()
            #master_link check
            self.check_update_master_link()



scraper = Scraper(start_links)
scraper.run()



# master_check  = { keep url as master url untill nth radio button ( if leb(radiobuttons) > n else: master_url = master_urls[]}

#while True:
    #oepn master_url
    #try:
        #fn1 = { click dep button and show more[if_exist] }
        #           
        #           click nth radio button
        #        

        # { {fn1}
        # if subD exist: fn1 else: append to start urls}
        # { master check }
    #except:
        #problamatic url