import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
    wait.until(
        EC.url_contains('browse')
    )

    profile = driver.find_element(By.CSS_SELECTOR, 'a[data-uia="action-select-profile+primary"]')
    profile.click()

def click_film_choose_genre(driver, wait):
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".main-header"))
    )

    film_link = driver.find_element(By.XPATH, "//a[@href='/browse/genre/34399']")
    film_link.click()

    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".subgenres"))
    )

    genre_button = driver.find_element(By.CSS_SELECTOR, ".subgenres")
    genre_button.click()

    genre_link = driver.find_element(By.XPATH, "//a[@href='/browse/genre/1365?bc=34399']")
    genre_link.click()

    toggle = driver.find_element(By.CLASS_NAME, "aro-grid")
    toggle.click()

    time.sleep(15)

def extract_links(driver, wait):
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".slider-item"))
    )

    elements = driver.find_elements(By.CSS_SELECTOR, ".slider-item .title-card-container a")
    links = [element.get_attribute("href") for element in elements if element.get_attribute("href")]
    base_url = "https://www.netflix.com"
    base_links = [base_url + link if link.startswith('/watch') else link for link in links] 
    formatted_links = []
    for link in base_links:
        if '?' in link:
            index = link.index('?')
            formatted_links.append(link[:index])
        else:
            formatted_links.append(link)
    return formatted_links

service = Service(executable_path="C:\Program Files (x86)\chromedriver.exe")
driver = webdriver.Chrome(service=service)
wait = WebDriverWait(driver, 10)
driver.get("https://www.netflix.com/login")

if login(driver, "lehongthai2000@gmail.com", "Netfl1x13122000@@&&"):
    click_profile(driver, wait)
    click_film_choose_genre(driver, wait)
    formatted_links = extract_links(driver, wait)
    with open('ex_4/netflix_links.txt', 'w') as f:
        for link in formatted_links:
            f.write(link + '\n')

driver.quit


