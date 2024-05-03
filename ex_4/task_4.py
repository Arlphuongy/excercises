import os
import time
import pyautogui as pag
from dotenv import load_dotenv
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException, NoSuchWindowException

def login(driver, wait, email, password):
    try:
        email_field = driver.find_element(By.NAME, "userLoginId")
        password_field = driver.find_element(By.NAME, "password")

        email_field.send_keys(email)
        password_field.send_keys(password + Keys.RETURN)

        #click profile
        wait.until(EC.url_contains('browse'))
        profile = driver.find_element(By.CSS_SELECTOR, 'a[data-uia="action-select-profile+primary"]')
        profile.click()
        return True 

    except (TimeoutException, NoSuchElementException) as e:
        print(f"Login failed: {e}")
        return False
    

def navigate_movie_links(driver, wait, links_file, index, attempts):
    with open(links_file, 'r') as f:
        lines = [line.strip('\n') for line in f.readlines()]

    for i, link in enumerate(lines[index:100]):
        driver.get(link)
        wait.until(EC.url_contains('watch'))

        try: 
            adjust_lang_settings(driver, wait)
            export(wait)        
            tabs = driver.window_handles
            driver.switch_to.window(tabs[1])
            wait.until(EC.presence_of_element_located((By.TAG_NAME, 'tbody')))
            if savetranslation(driver):
                print("Saved translation and original subtitles into files")    
                continue
            #not finisheddddddddddd

        except (TimeoutException, NoSuchElementException, StaleElementReferenceException, NoSuchWindowException):

            if attempts > 0:
                print(f"Failed to process link {link} at index {i}. Retrying...")
                navigate_movie_links(driver, wait, links_file, i, attempts - 1)
            else:
                print(f"Failed to process link {link} at index {i} after 2 attempts")
                driver.quit()    

        else:
            pag.hotkey('ctrl', 'w') 




def savetranslation(driver):
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    trs = soup.find_all('tr')

    tran_subs = []
    ori_subs = []

    folder_path = 'ex_4/files/'

    try: 
        for tr in trs:
            second_td = tr.find_all('td')[1]
            third_td = tr.find_all('td')[2]

            tran_text = second_td.get_text()
            ori_text = third_td.get_text()

            tran_subs.append(tran_text)
            ori_subs.append(ori_text)

    except NoSuchWindowException:
        print("something happened trying to save subtitles")
        return False
    
    else:
        with open(f'{folder_path}tran_subs.txt', 'w', encoding='utf-8') as f:
            for text in tran_subs:
                f.write(text + '\n')

        with open(f'{folder_path}ori_subs.txt', 'w', encoding='utf-8') as f:
            for text in ori_subs:
                f.write(text + '\n')
                
        return True

def adjust_lang_settings(driver, wait):  
    settings = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="appMountPoint"]/div/div/div[1]/div/div[1]/div[1]/div[6]')))
    settings.click()

    dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="select2-lln-NSL-dropdown-container"]')))
    dropdown.click()

    dropdown_input = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/span/span/span[1]/input')))
    # dropdown_input = driver.find_element(By.XPATH, '/html/body/span/span/span[1]/input')
    dropdown_input.send_keys("Vietnamese" + Keys.RETURN)

    close = driver.find_element(By.XPATH, '//*[@id="lln-options-modal"]/div/div[4]/div')
    close.click()


def export(wait):
    subtitles = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'lln-sub-text')))
    wait.until(EC.visibility_of(subtitles))

    export = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="appMountPoint"]/div/div/div[1]/div/div[1]/div[1]/div[5]')))
    export.click()

    time.sleep(1)

    export_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#llnExportModalExportBtn")))
    export_btn.click()


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

def main():
    links_file = 'ex_4/netflix_links.txt'
    navigate_movie_links(driver, wait, links_file, 0, 2)

if login(driver, wait, email, password):
    main()
