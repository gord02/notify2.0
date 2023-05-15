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
    company =  "Coursera"
    opts = Options()
    # so that browser instance doesn't pop up
    opts.add_argument("--headless")
    jobs = []

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options = opts)
    try:
        url = "https://about.coursera.org/careers/jobs/"
        driver.get(url)
        
                # wait for the specifc component with this class name to rendered before scraping
        # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "opening")))
        content = driver.page_source
        soup = BeautifulSoup(content, "lxml")
        driver.quit()
        # print(soup)
        
        
        # Not reliable scrap since we cannot navigate through linkedin page results but the filters for above 
        # link(posted in last 24 hours) will help keep results limited to one page
        elements = soup.select("div.opening > a")
        locations = soup.select("span.location")
        print("elements.size: ", len(elements))
        print("locations.size: ", len(locations))
        
        for i, element in enumerate (elements):     
            print(element.contents)
            print(locations[i].contents)
            # jobs.append(element.contents[0].strip())
            # print(element.contents[0].strip())
        
        jobs = process.process_job_titles(jobs)
        if len(jobs) > 0:
            # update company in database to found
            sqlQueries.update_company(company)
        return jobs
    
    except Exception as e:
        # send email about scrapping error
        error=f"Exception parsing {company} "+ repr(e)
        print(error)
        # notify.parsing_error(error)
        return jobs
    
get_data()