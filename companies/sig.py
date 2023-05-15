from bs4 import BeautifulSoup
from selenium import webdriver
# from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import sys
import time
sys.path.insert(0,'..') #this works relative to where to program was run from 

from logic import process
from logic import notify
from logic import sqlQueries

def get_data(): 
    company =  "SIG"
    opts = Options()
    # so that browser instance doesn't pop up
    opts.add_argument("--headless")
    jobs = []

    try:
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options = opts)
        url = "https://careers.sig.com/search-results?keywords=intern&ref=levels.fyi"
        driver.get(url)

        content = driver.page_source
        soup = BeautifulSoup(content, "lxml")
        driver.quit()
        elements = soup.select("div.job-title > span")
        next = soup.select_one("a.next-btn")
        for element in elements:
            jobs.append(element.contents[0])
        
        while(True):
            # if(next != None and 'href' not in next.attrs):
            # print(next)
            # print("next: ", next.attrs )
            # print("next: ", next.contents )
            if('href' not in next.attrs):
                print("not found")
                break
            
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options = opts)
            driver.get(next['href'])   
            content = driver.page_source
            soup = BeautifulSoup(content, "lxml")
            driver.quit()
            elements = soup.select("div.job-title > span")
            for element in elements:
                jobs.append(element.contents[0])
                
            next = soup.select_one("a.next-btn")
            
        
    except Exception as e:
        # send email about scrapping error
        error=f"Exception parsing {company} "+ repr(e)
        print(error)
        notify.parsing_error(error)
        
    jobs = process.process_job_titles(jobs)
    
    if len(jobs) > 0:
        # update company in database to found
        sqlQueries.update_company(company)
    return jobs
        
# get_data()