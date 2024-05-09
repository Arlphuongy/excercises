"""
This module provides utility functions for interacting with a Netflix account.
It includes functionality to log in, select a profile, fetch and clean film links.
"""

import os
import time
import re
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException


def login(cur_driver, email, password):
    """Attempt to log in to a web page using specified credentials."""
    try:
        email_field = cur_driver.find_element(By.NAME, "userLoginId")
        password_field = cur_driver.find_element(By.NAME, "password")
    except NoSuchElementException:
        print("Email or password field not found")
        return False
    except TimeoutException:
        print("Login timed out")
        return False

    email_field.send_keys(email)
    password_field.send_keys(password + Keys.RETURN)
    return True


def click_profile(cur_driver, cur_wait):
    """Click on the user profile after successful login."""
    cur_wait.until(EC.url_contains("browse"))

    profile = cur_driver.find_element(
        By.CSS_SELECTOR, 'a[data-uia="action-select-profile+primary"]'
    )
    profile.click()


def clean_netflix_links(input_file, output_file):
    """Clean and sort Netflix movie links extracted from the web."""
    cleaned_links = []

    # Open the input file containing raw links for reading
    with open(input_file, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()  # Remove leading/trailing whitespace
            # Check if the line is a valid Netflix watch URL
            if line.startswith("https://www.netflix.com/watch/"):
                # Extract the numeric movie ID from the URL
                movie_id = re.split(r"[^0-9]", line.split("/")[-1])[0]
                cleaned_link = f"https://www.netflix.com/watch/{movie_id}"
                cleaned_links.append(cleaned_link)

    # Remove duplicates and sort the links by their numeric movie IDs
    unique_sorted_links = sorted(
        set(cleaned_links), key=lambda x: int(x.split("/")[-1])
    )

    # Write the cleaned and sorted links to the output file
    with open(output_file, "w", encoding="utf-8") as file:
        for link in unique_sorted_links:
            file.write(link + "\n")


def fetch_netflix_movie_links(cur_driver, cur_wait):
    """Fetch and store Netflix movie links from a specific genre."""
    # Navigate to a specific genre page on Netflix
    cur_driver.get("https://www.netflix.com/browse/genre/34399?so=yr")

    # Wait for the genre page to fully load
    cur_wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "rowContainer_title_card"))
    )

    # Initialize the last_height for the scroll operation
    last_height = cur_driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll to the bottom of the page
        cur_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Pause to allow new content to load
        new_height = cur_driver.execute_script("return document.body.scrollHeight")
        # If the scroll height hasn't changed, we are at the bottom of the page
        if new_height == last_height:
            break
        last_height = new_height

    # Collect all visible movie links on the genre page
    movie_links = cur_driver.find_elements(
        By.CSS_SELECTOR, ".rowContainer_title_card .slider-refocus"
    )
    movie_urls = [link.get_attribute("href") for link in movie_links]

    # Write the fetched movie URLs to a file
    with open("src/netflix_film_links.txt", "a", encoding="utf-8") as f:
        for url in movie_urls:
            f.write(url + "\n")

    # Call the clean_netflix_links function to process the collected URLs
    clean_netflix_links("src/netflix_film_links.txt", "src/netflix_film_links_c.txt")


# Load environment variables from .env file
load_dotenv()

# Access variables securely
email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")

options = webdriver.ChromeOptions()
# options.add_extension("../Language-Reactor.crx")qq
options.add_argument("--ignore-certificate-errors")
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)

driver.get("https://www.netflix.com/login")

if login(driver, email, password):
    # click_profile(driver, wait)
    time.sleep(2)
    fetch_netflix_movie_links(driver, wait)

driver.quit()
