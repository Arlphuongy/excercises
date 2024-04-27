import os
import time
import pyautogui as pag
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, TimeoutException

def login(driver, email, password):
    try:
        email_field = driver.find_element(By.NAME, "userLoginId")
        password_field = driver.find_element(By.NAME, "password")
    except NoSuchElementException:
        print("Email or password field not found")
        return False
    except TimeoutException:
        print("Login timed out")
        return False

    email_field.send_keys(email)
    password_field.send_keys(password + Keys.RETURN)
    return True

def click_profile(driver, wait):
    wait.until(EC.url_contains('browse'))
    profile = driver.find_element(By.CSS_SELECTOR, 'a[data-uia="action-select-profile+primary"]')
    profile.click()

def navigate_movie_links(driver, wait, file_path):
    with open(file_path, 'r') as f:
        lines = [line.strip('\n') for line in f.readlines()]

    for i, link in enumerate(lines[:10]):
        driver.get(link)
        wait.until(EC.url_contains('watch'))

        adjust_lang_settings(driver, wait) 
        subtitles = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'lln-sub-text')))
        wait.until(EC.visibility_of(subtitles))
        export(wait)

        time.sleep(5)
        pag.hotkey('ctrl', 'w')

# def save_translation():

def adjust_lang_settings(driver, wait):  
    try:
        settings = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="appMountPoint"]/div/div/div[1]/div/div[1]/div[1]/div[6]')))
        settings.click()

        dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="select2-lln-NSL-dropdown-container"]')))
        dropdown.click()

        time.sleep(1)

        dropdown_input = driver.find_element(By.XPATH, '/html/body/span/span/span[1]/input')
        dropdown_input.send_keys("Vietnamese" + Keys.RETURN)

        time.sleep(1)

        close = driver.find_element(By.XPATH, '//*[@id="lln-options-modal"]/div/div[4]/div')
        close.click()

    except TimeoutException:
        print("Exceeded timeout")
    except NoSuchElementException:
        print("Element not found")
        
def export(wait):
    try: 
        export = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="appMountPoint"]/div/div/div[1]/div/div[1]/div[1]/div[5]')))
        export.click()

        time.sleep(1)

        export_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#llnExportModalExportBtn")))
        export_btn.click()

    except TimeoutException:
        print("Exceeded timeout")
    except NoSuchElementException:
        print("Element not found")


load_dotenv()
email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")

extension_path = './extensions/Language-Reactor.crx'
options = Options()
options.add_extension(extension_path)
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)

driver.get("https://www.netflix.com/login")

wait.until(EC.number_of_windows_to_be(2))

pag.hotkey('ctrl', 'w')

wait.until(EC.url_contains('netflix'))

if login(driver, email, password):
    click_profile(driver, wait)
    time.sleep(2)
    navigate_movie_links(driver, wait, 'ex_4/netflix_links.txt')

