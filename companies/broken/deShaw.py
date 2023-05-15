from bs4 import BeautifulSoup
from selenium import webdriver
from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService

import sys
sys.path.insert(0,'..') #this works relative to where to program was run from 

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
    # try:
    url = "https://www.deshaw.com/careers/internships"
    
    driver.implicitly_wait(10)
    # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "waitCreate")))
    driver.set_page_load_timeout(30)
    driver.implicitly_wait(3)
    driver.get(url)
    content = driver.page_source
    soup = BeautifulSoup(content, "lxml")
    driver.quit()
    print(soup)
    
    # elements = soup.select("p > span")
    # # print("----------")
    # for element in elements:
    #     print(element)
    #     # positions dont have intern in them but they are intern roles
    #     jobs.append(element.contents[0]+ " Intern")
    
    # jobs = process.process_job_titles(jobs)
    # if len(jobs) > 0:
    #     # update company in database to found
    #     sqlQueries.update_company(company)

    # except:
    #     # send email about scrapping error
    #     notify.parsing_error(company)
    #     return jobs
        
    return jobs
    
    
get_data()