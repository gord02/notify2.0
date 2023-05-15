from bs4 import BeautifulSoup
from selenium import webdriver
# from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService

import sys
sys.path.insert(0,'..') #this works relative to where to program was run from 

from logic import process
from logic import notify
from logic import sqlQueries


def get_data(): 
    company =  "Stripe"
    opts = Options()
    # so that browser instance doesn't pop up
    opts.add_argument("--headless")
    jobs = []
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options = opts)

    try:
        # more specific link
        # https://stripe.com/jobs/search?teams=University&office_locations=North+America--Chicago&office_locations=North+America--Mexico+City&office_locations=North+America--New+York&office_locations=North+America--Seattle&office_locations=North+America--South+San+Francisco&office_locations=North+America--Toronto
        url = "https://stripe.com/jobs/search"
        driver.get(url)
        content = driver.page_source
        soup = BeautifulSoup(content, "lxml")
        driver.quit()
    
        elements = soup.select("a.JobsListings__link")
        for element in elements:
            jobs.append(element.contents[0])
        
    
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
        
