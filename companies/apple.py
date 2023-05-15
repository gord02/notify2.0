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
    company =  "Apple"
    opts = Options()
    # so that browser instance doesn't pop up
    opts.add_argument("--headless")
    # access will be blocked without this user agent
    user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36" 
    opts.add_argument("user-agent=%s" % user_agent) 

    jobs = []

    try:
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options = opts)
        
        url = "https://jobs.apple.com/en-us/search?location=united-states-USA+canada-CANC&team=internships-STDNT-INTRN"
        driver.get(url)
        content = driver.page_source
        soup = BeautifulSoup(content, "lxml")
        driver.quit()

        # allows us to traverse pages 
        page = soup.find(id="page-number")
        page1 =  (int)(page['value'])
        pages = soup.select("span.pageNumber")
        endPage = (int)(pages[1].contents[0])
        pageNum = "&page="
        
        while page1 <= endPage:
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options = opts)
            newUrl = url + pageNum + str(page1)
            driver.get(newUrl)
            content = driver.page_source
            soup = BeautifulSoup(content, "lxml")
            elements = soup.select("a.table--advanced-search__title")
            for element in elements:
                jobs.append(element.contents[0])
            page1+=1   
                
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