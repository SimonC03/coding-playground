from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()

url = r'https://www.avanza.se/aktier/lista.html'
fn = 'avanza.html'
driver.get(url)

time.sleep(1)

button = driver.find_element(By.CLASS_NAME, 'cookie-consent-necessary-btn')
button.click()

time.sleep(1)

button = driver.find_element(By.CLASS_NAME, 'fetchMoreButton')
button.click()

time.sleep(1)

with open(fn,'w') as f:
   f.write(driver.page_source)
