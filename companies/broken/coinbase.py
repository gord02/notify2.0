from bs4 import BeautifulSoup
from selenium import webdriver
# from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# options = webdriver.ChromeOptions() 
# driver.get('https://bet365.com')

opts = Options()
# so that browser instance doesn't pop up
# opts.add_argument("--headless")
# opts.add_argument("start-maximized")


driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options = opts)
driver.implicitly_wait(10)

url = "https://www.coinbase.com/careers/positions?department=Internships%2520%2526%2520University%2520Grad%2520Positions"
driver.get(url)

# wait for the specifc component with this class name to rendered before scraping
# WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "Department__Job-sc-1n8uxi6-4")))

content = driver.page_source
soup = BeautifulSoup(content, "lxml")
driver.quit()
jobs = set()
# print(soup)
# elements = soup.select("div.Department__Job-sc-1n8uxi6-4")
elements = soup.select("a")
for element in elements:
    print(element.contents[0])
    # jobs.add(element.contents)

for title in jobs:
    print(title)