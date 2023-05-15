
from bs4 import BeautifulSoup
from selenium import webdriver

from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from seleniumwire.utils import decode
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.chrome.service import Service as ChromeService

opts = Options()
opts.add_argument("--headless")
# Create new Driver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options = opts)
# driver = webdriver.Chrome("/Users/gordon/Downloads/chromedriver")

# driver.get('https://www.quora.com/careers/engineering')
# driver.get("https://careers.twosigma.com/careers/SearchJobs/Intern?2047=%5B9813555%5D&2047_format=1532&listFilterMode=1")
# print(driver.title)
# print(driver.requests[0].headers, driver.requests[0].response)
# body = decode(response.body, response.headers.get('Content-Encoding', 'identity'))
# print(driver.requests)
# print("size: ", len(driver.requests))
# print("type of list: ", type(driver.requests))
# print("type of first: ", type(driver.requests[0] ))
# print("header: ", driver.response)
# print("keys: " , driver.requests.__dict__.keys())
url = "https://addepar.com/careers#engineering"
# url = "https://www.adamchoi.co.uk/teamgoals/detailed"
driver.get(url)

content = driver.page_source
# print("content type: ", type(content))
# soup = BeautifulSoup(content, "lxml")
# # print("soup type: ", type(soup))
# print(soup)
# html_source_code = driver.execute_script("return document.body.innerHTML;")
# html_soup: BeautifulSoup = BeautifulSoup(html_source_code, 'html.parser')
# pageB = driver.page_source
# page = driver.execute_script("return document.documentElement.outerHTML")
# soup = BeautifulSoup(page, "lxml")
soup = BeautifulSoup(content, "lxml")

# print(soup)
print(soup)
# print(soupB)

driver.quit()

# =============
# from requests_html import HTMLSession
# session = HTMLSession()
# r = session.get('https://python.org/')
# print("r: type", type(r))
# print(r.html)

from wordScan import wordScan
print(wordScan("Internal squad"))
print(wordScan("Backend Software Engineer"))
print(wordScan("Internal Engineer"))