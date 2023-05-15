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
    company = "Jump Trading"
    opts = Options()
    # so that browser instance doesn't pop up
    opts.add_argument("--headless")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options = opts)

    url = "https://www.jumptrading.com/careers/?locations=Chicago+New-York&titleSearch=campus+intern"
    jobs = []

    try:
        driver.get(url)
        content = driver.page_source
        soup = BeautifulSoup(content, "lxml")
        driver.quit()
        elements = soup.select("a > div > div > p")

        # for i, element in enumerate(elements):
        i=0
        # each p tag is the job name and the following p tag is the location 
        while i+1 < len(elements):
            jobs.append(elements[i].contents[0] + ": " + elements[i+1].contents[0])
            # skips to the next job title
            i = i + 2
    
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