import pandas as pd
import requests
import numpy as np
from bs4 import BeautifulSoup
import re
from selenium import webdriver
import time
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Edge("C:\Program Files\msedgedriver.exe")
url = 'https://www.nfl.com/games/dolphins-at-bills-2023-reg-4?active-tab=watch'
options = Options()
options.headless = True

driver.get(url)
driver.maximize_window()

drives_element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "all-drives-panel"))
)
drives_html = drives_element.get_attribute('innerHTML')
print(drives_html)
driver.quit()