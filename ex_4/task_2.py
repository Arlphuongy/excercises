from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# options = webdriver.ChromeOptions()
# options.add_experimental_option('detach', True)

driver = webdriver.Chrome()
driver.get("https://www.netflix.com/login")

email = driver.find_element(By.NAME, "userLoginId")
password = driver.find_element(By.NAME, "password")

email.send_keys("lehongthai2000@gmail.com")
password.send_keys("Netfl1x13122000@@&&")

password.send_keys(Keys.RETURN)

