import secretes
from requests import get
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc

# def ytm_video_id_extractor(artist, title):
#   # 브라우저 꺼짐 방지 옵션
#   chrome_options = uc.ChromeOptions()
#   chrome_options.add_experimental_option("detach", True)

#   base_url = "https://music.youtube.com/search?q="
#   driver = uc.Chrome(options=chrome_options)

#   # 요소 보일 때까지 대기 
#   driver.implicitly_wait(5)
#   driver.get(f"{base_url}{artist}{title}")
  
#   # 로그인, 나중에 따로 빼기
#   driver.find_element(By.XPATH, '//*[@id="buttons"]/ytd-button-renderer/yt-button-shape').click()
#   driver.execute_script(f'document.getElementById("identifierId").value = "{secretes.YT_ID}"')
#   driver.find_element(By.XPATH, '//*[@id="identifierNext"]/div/button').click()
  
