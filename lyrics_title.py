import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import concurrent.futures

headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"}

# ChromeDriver 경로 설정
service = Service(r"C:\Users\박주현\Desktop\opensource\chromedriver.exe")
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # 브라우저를 숨긴 상태로 실행

# Chrome 웹 드라이버 시작
driver = webdriver.Chrome(service=service, options=options)

# 사용자가 입력한 연도 받기
year = input("Please enter the year you want to check the chart for (e.g., 2010): ")

# 멜론 차트 URL 설정
chart_url = f'https://www.melon.com/chart/age/index.htm?chartType=AG&chartGenre=KPOP&chartDate={year}'

# URL로 이동
driver.get(chart_url)
time.sleep(3)  # 페이지 로딩을 위해 잠시 대기

# 노래 제목 가져오기
titles_elements = driver.find_elements(By.CSS_SELECTOR, ".ellipsis.rank01 a")

# 처음 50개의 노래 제목만 처리
titles_elements = titles_elements[:50]

# 제목 리스트에 텍스트만 저장
titles = [title.text for title in titles_elements]

# 페이지의 전체 HTML 소스 가져오기
html_source = driver.page_source

# BeautifulSoup 객체 생성
soup = BeautifulSoup(html_source, 'html.parser')

# 'href' 속성이 'javascript:melon.play.playSong'을 포함하는 모든 <a> 태그 찾기
song_links = soup.find_all('a', href=lambda href: href and 'melon.play.playSong' in href)

# 각 링크에서 songId 추출
song_ids = []
for link in song_links[:50]:  # 처음 50개의 곡에 대해서만 처리
    href = link['href']
    song_id = href.split("'")[3]  # songId는 작은따옴표로 둘러싸여 있는 세 번째 요소
    song_ids.append(song_id)

# 웹 드라이버 종료
driver.quit()

def fetch_lyrics(idx, song_id):
    song_url = f"https://www.melon.com/song/detail.htm?songId={song_id}"
    
    # requests를 사용하여 페이지 가져오기
    response = requests.get(song_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    try:
        # 가사를 포함하는 태그 찾기
        lyrics_div = soup.find('div', class_='lyric')
        if lyrics_div:
            # HTML 태그를 제거하고 텍스트만 추출, 원치 않는 주석 부분 제거
            lyrics = lyrics_div.get_text(separator="\n").replace("<!-- height:auto; 로 변경시, 확장됨 -->", "").strip()
            return (titles[idx], lyrics)  # 노래 제목과 가사를 튜플로 반환
        else:
            print(f"Lyrics not found for songId: {song_id}")
            return (titles[idx], "Lyrics not found")
    except Exception as e:
        print(f"Error retrieving lyrics for songId: {song_id} - {str(e)}")
        return (titles[idx], "Error retrieving lyrics")

# 병렬 처리를 위해 ThreadPoolExecutor 사용
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(fetch_lyrics, idx, song_id) for idx, song_id in enumerate(song_ids)]
    lyrics_list = [future.result() for future in concurrent.futures.as_completed(futures)]

with open(f"{year}_lyrics.txt", "w", encoding="utf-8") as file:
    for title, lyrics in lyrics_list:
        file.write(f"Title: {title}\nLyrics:\n{lyrics}\n\n")
