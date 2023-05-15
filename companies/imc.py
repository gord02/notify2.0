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
    company =  "IMC"
    opts = Options()
    # so that browser instance doesn't pop up
    opts.add_argument("--headless")
    jobs = []

    try:
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options = opts)
        url = "https://imc.wd5.myworkdayjobs.com/en-US/invitation/jobs/details/Quant-Trader-Intern---Summer-2023_REQ-01963?workerSubType=71540894c45741dfba126cdff9489e52"
        driver.get(url)
        
        # wait for the specifc component with this class name to rendered before scraping
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "css-129m7dg")))
       
        content = driver.page_source
        soup = BeautifulSoup(content, "lxml")
        driver.quit()
        elements = soup.select("h3 > a")

        i = 0
        while i < len(elements):
            jobs.append(elements[i].contents[0])
            # skip to next job title 
            i = i+ 1
        
    except Exception as e:
        # send email about scrapping error
        error=f"Exception parsing {company}: "+ repr(e)
        print(error)
        notify.parsing_error(error)

    jobs = process.process_job_titles(jobs)
    
    if len(jobs) > 0:
        # update company in database to found
        sqlQueries.update_company(company)
    return jobs
        
# get_data()