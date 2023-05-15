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
sys.path.insert(0,'..') #this works relative to where to program was run from 

from logic import process
from logic import notify
from logic import sqlQueries


def get_data(): 
    company =  "Lyft"
    opts = Options()
    # so that browser instance doesn't pop up
    # opts.add_argument("--headless")
    jobs = []
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options = opts)

    try:
        url = "https://www.lyft.com/careers#openings?category=university"
        driver.get(url)
        
        # wait for the specifc component with this class name to rendered before scraping
        # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "sc-973cc4d2-2.jVVOgb")))

        content = driver.page_source
        soup = BeautifulSoup(content, "lxml")
        # print(soup)
        driver.quit()
        
        # elements = soup.select("h3")
        element = soup.select_one("a.sc-973cc4d2-2.jVVOgb")
        print(element)
        # elements = soup.select("p")
        # for element in elements:
        #     print(element.contents[0])
        
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