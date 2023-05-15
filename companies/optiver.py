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
    company =  "Optiver"
    opts = Options()
    # so that browser instance doesn't pop up
    opts.add_argument("--headless")
    jobs = []

    try:
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options = opts)
        url = "https://optiver.com/working-at-optiver/career-opportunities/?_gl=1*14qqpxn*_up*MQ..*_ga*Nzk0MDYzODM5LjE2NzgwNTExMDM.*_ga_YMLN3CLJVE*MTY3ODA1MTEwMS4xLjAuMTY3ODA1MTEwMS4wLjAuMA..&numberposts=10"
        driver.get(url)

        content = driver.page_source
        soup = BeautifulSoup(content, "lxml")
        driver.quit()
        elements = soup.select("h5 > a")
        locations = soup.select("p.text-s")
        for i, element in enumerate (elements):
            jobs.append(element.contents[0] + ": (" + locations[i].contents[2].strip() + ")")

        
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