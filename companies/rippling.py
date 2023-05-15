from bs4 import BeautifulSoup
from selenium import webdriver

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
    company =  "Rippling"
    
    opts = Options()
    opts.add_argument("--headless")
    # so that browser instance doesn't pop up
    
    opts.add_argument("--window-size=1920,1080")
    
    user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36" 
    opts.add_argument("user-agent=%s" % user_agent) 

    # ---

    jobs = []

    try:
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options = opts)
        url = "https://www.rippling.com/careers/open-roles"
        driver.get(url)
        
        # wait for the specifc component with this class name to rendered before scraping
        # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "s-careers-usa")))
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, "w-22")))
        # WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, "s-careers-usa")))
        
        content = driver.page_source
        soup = BeautifulSoup(content, "lxml")
        driver.quit()
        # print(soup)
        elements = soup.select("a > p")
        locations = soup.select("div.md\:pl-16 > p.pl-8") 
        
        i = 0
        pl = 0
        # print(len(elements))
        # print(len(locations))
        while i < len(elements):
            # print(elements[i].contents[0] + " (" + locations[pl].contents[0] + ")")
            jobs.append(elements[i].contents[0] + " (" + locations[pl].contents[0] + ")")
            # skip to next job title 
            i = i+ 2
            pl += 1
            
        
    except Exception as e:
        # send email about scrapping error
        error=f"Exception parsing: {company} "+ repr(e)
        print(error)
        # exc_type, exc_tb = sys.exc_info()
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print("exception type: ", exc_type, " excpetion line number", exc_tb )
        # notify.parsing_error(error)
        jobs = process.process_job_titles(jobs)

    jobs = process.process_job_titles(jobs)
    
    if len(jobs) > 0:
        # update company in database to found
        sqlQueries.update_company(company)
    return jobs
        
# get_data()


