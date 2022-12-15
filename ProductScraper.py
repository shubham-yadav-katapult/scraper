from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from lxml import etree
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time
import json

start_links = ['https://www.walmart.com/browse/sports-outdoors/baseball-gear-equipment/4125_4161_4162?povid=HardlinesGlobalNav_DSK_SportsOutdoors_Sports_Baseball']



class Scraper():
    #Initialising Scraper
    def __init__(self, start_link):
        self.start_links = start_links
        self.robot = '//*[contains(text(),"To proceed, please verify that you are not a robot.")]'
        self.master_dict = {'cat':[],'link':[]}
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument("--disable-javascript")
        options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36")
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        #self.driver.execute_cdp_cmd('Network.setUserAgentOverride',
        #{"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})

    
    def clickDepartmentAndShowMore(self):
        self.roboCheck()
        xp_departments_button = '//*[@class="pb6 pr3"]//*[contains(text(),"Departments")]'
        xp_show_more_button = '//*[@class="pb6 pr3"]//*[contains(text(),"Show More")]'
        departments_button = self.driver.find_element(By.XPATH, xp_departments_button)
        departments_button.click()
        time.sleep(1)
        show_more_button = self.driver.find_elements(By.XPATH, xp_show_more_button)
        if len(show_more_button) > 0:
            self.driver.execute_script("arguments[0].scrollIntoView();", show_more_button[0])
            show_more_button[0].click()
        self.roboCheck()

    def roboCheck(self):
        robo_xp = '//*[contains(text(),"Robot or human?")]'
        robo_check_element = self.driver.find_elements(By.XPATH, robo_xp)
        if len(robo_check_element) >0:
            input("Please solve puzzle and press enter to continue")
            try:
                self.clickDepartmentAndShowMore()
            except:
                pass
    
    def run(self):
        for link in self.start_links:
            self.driver.get(link)
            time.sleep(2)
            self.clickDepartmentAndShowMore()
            input("Press Enter to continue")


scraper = Scraper(start_links)
scraper.run()