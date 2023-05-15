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
    company =  "Addepar"
    opts = Options()
    # so that browser instance doesn't pop up
    opts.add_argument("--headless")
    jobs = []

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options = opts)
    try:
        url = "https://addepar.com/careers#engineering"
        driver.get(url)
        content = driver.page_source
        soup = BeautifulSoup(content, "lxml")
        driver.quit()

        titles = set()
        
        elements = soup.select("p.f4")
        for element in elements:
            titles.add(element.contents[0])
        
       
    except Exception as e:
        # send email about scrapping error
        error=f"Exception parsing {company} "+ repr(e)
        print(error)
        notify.parsing_error(error)
        
    jobs = process.process_job_titles(titles)
    if len(jobs) > 0:
        # update company in database to found
        sqlQueries.update_company(company)
        
    return jobs
    
get_data()