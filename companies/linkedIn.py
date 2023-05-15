from bs4 import BeautifulSoup
from selenium import webdriver
from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService

from logic import process
from logic import notify
from logic import sqlQueries

def get_data(): 
    company =  "LinkedIn"
    opts = Options()
    # so that browser instance doesn't pop up
    opts.add_argument("--headless")
    jobs = []

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options = opts)
    try:
        url = "https://www.linkedin.com/jobs/search/?currentJobId=3502921259&f_C=1337&f_TPR=r86400&geoId=92000000"
        driver.get(url)
        content = driver.page_source
        soup = BeautifulSoup(content, "lxml")
        driver.quit()
        
        # Not reliable scrap since we cannot navigate through linkedin page results but the filters for above 
        # link(posted in last 24 hours) will help keep results limited to one page
        elements = soup.select("a span")
        
        for element in elements:
            jobs.append(element.contents[0].strip())
            # print(element.contents[0].strip())
    
    except Exception as e:
        jobs = process.process_job_titles(jobs)
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