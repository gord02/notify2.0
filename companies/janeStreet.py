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
    company =  "Jane Street"
    opts = Options()
    # so that browser instance doesn't pop up
    opts.add_argument("--headless")
    jobs = []

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options = opts)
    try:
        url = "https://www.janestreet.com/join-jane-street/open-roles/?type=internship&location=all-locations"
        driver.get(url)
        content = driver.page_source
        soup = BeautifulSoup(content, "lxml")
        driver.quit()
        
        elements = soup.select("div.position p")
        for element in elements:
            # positions dont have intern in them but they are intern roles
            jobs.append(element.contents[0]+ " Intern")
        
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