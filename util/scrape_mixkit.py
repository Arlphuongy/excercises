import os
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

service = Service(executable_path="C:\Program Files (x86)\chromedriver.exe")
driver = webdriver.Chrome(service=service)
wait = WebDriverWait(driver, 10)

def download(soup, index):
    elements = soup.find_all('div', class_='item-grid__item')

    for element in elements:
        video = element.find('video', class_='item-grid-video-player__video')
        if video:
            video_url = video['src']
            
            video_response = requests.get(video_url)
            
            video_path = os.path.join(videos_folder_path, f'video_{index}.mp4')
            with open(video_path, 'wb') as file:
                file.write(video_response.content)
            
            print(f"Saved video to {video_path}")
        
        thumbnail = element.find('img', class_='item-grid-video-player__thumb')
        if thumbnail:
            thumbnail_url = thumbnail['src']
            title = thumbnail.get('alt')
            
            thumbnail_response = requests.get(thumbnail_url)
            
            thumbnail_path = os.path.join(thumbnails_folder_path, f'thumbnail_{index}.jpg')
            with open(thumbnail_path, 'wb') as file:
                file.write(thumbnail_response.content)
            
            print(f"Saved thumbnail to {thumbnail_path}")
            
            description = ""
            description_tag = element.find('p', class_='item-grid-card__description')
            if description_tag:
                description = "|" + description_tag.text.strip()
            
            with open(titles_file_path, 'a', encoding='utf-8') as titles_file:
                titles_file.write(f'{title}{description}\n')  
            print(f"Saved title {title} and maybe description to {titles_file_path}")
        
        index += 1


videos_folder_path = 'mixkit/videos'
thumbnails_folder_path = 'mixkit/thumbnails' 
titles_folder_path = 'mixkit/titles'
os.makedirs(videos_folder_path, exist_ok=True)
os.makedirs(thumbnails_folder_path, exist_ok=True)
os.makedirs(titles_folder_path, exist_ok=True)

titles_file_path = os.path.join(titles_folder_path, 'titles.txt')

# driver.get('https://mixkit.co/free-stock-video/animal/')
# wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[4]/h2')))
driver.get('https://mixkit.co/free-stock-video/cats/')
wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div/h1')))

start_time = time.time()

index = 0
while True:
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    
    download(soup, index)

    try:
        next_page = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'pagination__link--next')))
        next_page.click()

        time.sleep(3.5)

        index += len(soup.find_all('div', class_='item-grid__item'))
    except Exception as e:
        print("No more pages or failed to move onto the next page")
        break


end_time = time.time()
run_time = end_time - start_time
print(f"Process took {run_time} to complete")

driver.quit()
