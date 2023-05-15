


from bs4 import BeautifulSoup
from selenium import webdriver
from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time
import sys
# allows for getting files up a level when trying to run this file directly
sys.path.insert(0,'..') #this works relative to where to program was run from 

from logic import process
from logic import notify
from logic import sqlQueries

def get_data():  
    try:
        company =  "Block"
        opts = Options()
        # so that browser instance doesn't pop up
        opts.add_argument("--headless")

        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options = opts)
        url = "https://block.xyz/careers?types=Intern"
        jobs = []

        driver.get(url)
        content = driver.page_source
        soup = BeautifulSoup(content, "lxml")
        driver.quit()

        elements = soup.select("div.JobList_titleColumn__3oZrC")
        
        for x in elements:
            # print(x.contents[0])
            jobs.append(x.contents[0])

    except Exception as e:
        # send email about scrapping error
        error=f"Exception parsing {company} "+ repr(e)
        print(error)
        notify.parsing_error(error)

    jobs = process.process_job_titles(jobs)
    # print(jobs)
    if len(jobs) > 0:
        # update company in database to found
        sqlQueries.update_company(company)
            
    return jobs
        

# get_data()