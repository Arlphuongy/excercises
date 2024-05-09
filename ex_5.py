import os
import time
import argparse
from dotenv import load_dotenv
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
)  # , StaleElementReferenceException, NoSuchWindowException, UnexpectedAlertPresentException


def login(email, password):
    try:
        time.sleep(1)
        email_field = driver.find_element(By.NAME, "userLoginId")
        password_field = driver.find_element(By.NAME, "password")

        email_field.send_keys(email)
        password_field.send_keys(password + Keys.RETURN)

        wait.until(EC.url_contains("browse"))
        profile = wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, 'a[data-uia="action-select-profile+primary"]')
            )
        )
        profile.click()
        return True

    except (TimeoutException, NoSuchElementException) as e:
        print(f"Login failed: {e}")
        return False


def navigate_movie_links(links_file, start, end, en_file, zh_file, folder_path):
    with open(links_file, "r", encoding="utf-8") as f:
        lines = [line.strip("\n") for line in f.readlines()]

    for i in range(start, end + 1):
        link = lines[i]
        start_time = time.time()

        try:
            driver.get(link)
            wait.until(EC.url_contains("watch"))

            if adjust_lang_settings(i, link, folder_path):
                export()
                savetranslation(en_file, zh_file)
                end_time = time.time()
                run_time = end_time - start_time
                print(f"Saved {link} at index {i}, took {run_time} to complete")

        except Exception:
            print(f"Failed to process link {link} at index {i}")
            with open(f"{folder_path}failed_links.txt", "a", encoding="utf-8") as f:
                f.write(link + "\n")


def savetranslation(en_file, zh_file):
    tabs = driver.window_handles
    driver.switch_to.window(tabs[1])
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "tbody")))

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    trs = soup.find_all("tr")
    tran_subs = []
    ori_subs = []

    for tr in trs[2:-2]:
        second_td = tr.find_all("td")[1]
        third_td = tr.find_all("td")[2]

        character_spans = [
            span.get_text()
            for span in second_td.find_all("span")
            if span.parent.name != "div"
        ]

        tran_text = " ".join(character_spans)  # second_td.get_text()
        tran_lines = [line.strip() for line in tran_text.split("\n") if line.strip()]
        tran_text = "\n".join(tran_lines)

        ori_text = third_td.get_text().replace("\n", " ")
        ori_lines = [line.strip() for line in ori_text.split("\n") if line.strip()]
        ori_text = "\n".join(ori_lines)

        tran_subs.append(tran_text)
        ori_subs.append(ori_text)

    with open(zh_file, "a", encoding="utf-8") as f:
        for text in tran_subs:
            f.write(text + "\n")

    with open(en_file, "a", encoding="utf-8") as f:
        for text in ori_subs:
            f.write(text + "\n")

    driver.close()
    driver.switch_to.window(tabs[0])


def adjust_lang_settings(i, link, folder_path):
    try:
        settings = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    '//*[@id="appMountPoint"]/div/div/div[1]/div/div[1]/div[1]/div[6]',
                )
            )
        )
        settings.click()

        dropdown = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    '//*[@id="lln-options-modal"]/div/div[3]/div/div[2]/div[5]/label/span[3]/span[1]/span[1]/span',
                )
            )
        )
        dropdown.click()

        dropdown_input = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "/html/body/span/span/span[1]/input")
            )
        )
        dropdown_input.send_keys("Simplified Chinese")

        WebDriverWait(driver, 6).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//span[contains(text(), 'Simplified Chinese')]")
            )
        )

        dropdown_input.send_keys(Keys.RETURN)

    except Exception as e:
        print(f"Failed to translate link {link} at index {i} with error {e}")
        with open(f"{folder_path}no_translation.txt", "a", encoding="utf-8") as f:
            f.write(link + "\n")

    else:
        close = driver.find_element(
            By.XPATH, '//*[@id="lln-options-modal"]/div/div[4]/div'
        )
        close.click()
        return True


def export():
    subtitles = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "lln-sub-text"))
    )
    wait.until(EC.visibility_of(subtitles))

    export = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                '//*[@id="appMountPoint"]/div/div/div[1]/div/div[1]/div[1]/div[5]',
            )
        )
    )
    export.click()

    export_btn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#llnExportModalExportBtn"))
    )
    export_btn.click()

    wait.until(EC.number_of_windows_to_be(2))


load_dotenv()
email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")

extension_path = "src/extensions/Language-Reactor.crx"
options = Options()
options.add_extension(extension_path)
options.add_argument("--mute-audio")  # giỏi hihi
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)

driver.get("https://www.netflix.com/login")
wait.until(EC.number_of_windows_to_be(2))
tabs = driver.window_handles
driver.switch_to.window(tabs[0])
driver.close()
driver.switch_to.window(tabs[1])
wait.until(EC.url_contains("netflix"))


def main():
    parser = argparse.ArgumentParser(
        description="extracting subtitle pairs from netflix"
    )

    parser.add_argument(
        "--start",
        type=int,
        required=True,
        help="starting index of links in file",
    )

    parser.add_argument(
        "--end",
        type=int,
        required=True,
        help="ending index of links in file",
    )

    args = parser.parse_args()

    folder_path = "src/netflix/zh/"
    en_file = f"{folder_path}en_{args.start}-{args.end}.txt"
    zh_file = f"{folder_path}zh_{args.start}-{args.end}.txt"

    links_file = "src/netflix_film_links_c.txt"
    login(email, password)
    navigate_movie_links(
        links_file, args.start, args.end, en_file, zh_file, folder_path
    )
    driver.quit()


if __name__ == "__main__":
    main()

    # py ex_4/extract_subtitles.py --start "0" --end "250"
    # py ex_4/extract_subtitles.py --start "251" --end "500"
    # py ex_4/extract_subtitles.py --start "501" --end "750"
    # py ex_4/extract_subtitles.py --start "751" --end "1000"
    # py ex_4/extract_subtitles.py --start "1001" --end "1250"
    # py ex_4/extract_subtitles.py --start "1251" --end "1500"

    # python ex_4/extract_subtitles.py --start "4001" --end "4100"
    # python ex_4/extract_subtitles.py --start "4101" --end "4200"
    # python ex_4/extract_subtitles.py --start "4201" --end "4201"
