import time
from config import HOST, TEACHER_USERNAME, TEACHER_PASSWORD
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def check_submission(url):
    print(f"Visiting {url}...")
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    browser = webdriver.Chrome(options=options)

    browser.get(HOST + "/login")

    browser.find_element(By.NAME, "username").send_keys(TEACHER_USERNAME)
    browser.find_element(By.NAME, "password").send_keys(TEACHER_PASSWORD)
    browser.find_element(By.NAME, "submit-btn").click()
    
    time.sleep(0.5)
    browser.get(url)
    time.sleep(9.5)

    browser.quit()