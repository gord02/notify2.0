from bs4 import BeautifulSoup
from selenium import webdriver
# from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By

import sys
sys.path.insert(0,'..') #this works relative to where to program was run from 

from logic import process
from logic import notify
from logic import sqlQueries


def get_data(): 
    company =  "Uber"
    opts = Options()
    # so that browser instance doesn't pop up
    opts.add_argument("--headless")
    jobs = []
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options = opts)

    try:
        url = "https://www.uber.com/ca/en/careers/list/?department=University&team=University&team=Engineering"
        # https://www.uber.com/ca/en/careers/list/?location=CAN-Ontario-Toronto&location=USA-Illinois-Chicago&location=USA-California-San%20Fransisco&location=USA-New%20York-New%20York%20City&department=University&team=University&team=Engineering
        driver.get(url)
        content = driver.page_source
        soup = BeautifulSoup(content, "lxml")
        driver.quit()
        
        
        elements = soup.select("a.css-bNzNOn")
        # locations = soup.select("div > div > div > span.css-dCwqLp")
       
        for element in elements:
            jobs.append(element.contents[0])
        
        # for loc in locations:
        #     print(loc.contents[0])
        
    
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