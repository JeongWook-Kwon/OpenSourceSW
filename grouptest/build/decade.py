# 완료, 데이터 버튼만 추가
# 2번 서치 , 3번 데이터, 5번키워드 그래프

import subprocess
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage
import collections
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from konlpy.tag import Okt
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\odpa0\OneDrive\바탕 화면\오픈소스 기초\grouptest\build\assets\frame0")

okt = Okt()

# 서치 실행
def run_search():
    window.destroy()  # 현재 GUI를 닫습니다.
    subprocess.Popen(['python', OUTPUT_PATH / 'search.py'])

def run_keygraph():
    window.destroy()  # 현재 GUI를 닫습니다.
    subprocess.Popen(['python', OUTPUT_PATH / 'keygraph.py'])

def run_data():  
    subprocess.Popen(['python', OUTPUT_PATH / 'data.py'])


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# 불용어 파일 읽기

def display_wordcloud():
    # 엔트리에서 입력값 가져오기
    with open(r"C:\Users\odpa0\OneDrive\바탕 화면\decadelyrics\stopwords.txt", 'r', encoding='utf-8') as file:
         stopwords = set(file.read().split())
    year = entry_1.get()
    
    if not year:
        print("Please enter a valid year")
        return

    # {year}_lyrics.txt 파일에서 제목과 가사 읽기
    file_path = fr"C:\Users\odpa0\OneDrive\바탕 화면\decadelyrics\{year}_lyrics.txt"
    
    print(f"Looking for file: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            print("File found and read successfully.")
    except FileNotFoundError:
        print(f"No data found for the year {year}")
        return

    # 불용어 파일 읽기


    lyrics_list = []
    title = None
    lyrics = []

    for line in lines:
        line = line.strip()
        if line.startswith("Title:"):
            if title and lyrics:
                # 이전 제목과 가사를 저장
                lyrics_list.append((title, " ".join(lyrics)))
            title = line.replace("Title:", "").strip()
            lyrics = []
        elif line.startswith("Lyrics:"):
            continue
        else:
            lyrics.append(line)

    # 마지막 곡 추가
    if title and lyrics:
        lyrics_list.append((title, " ".join(lyrics)))

    # 노래 제목과 가사에서 가장 많이 나온 키워드 10개를 추출하는 함수
    def extract_top_keywords(lyrics_list):
     word_count = collections.Counter()
     for title, lyrics in lyrics_list:
        # 제목과 가사 합치기
        combined_text = f"{title} {lyrics}"
        # 한글 명사만 추출
        nouns = okt.nouns(combined_text)
        # 중복 제거
        unique_nouns = set(nouns)
        # 불용어 제거 및 한글 필터링
        filtered_nouns = [noun for noun in unique_nouns if noun not in stopwords and re.match(r'^[가-힣]+$', noun)]
        word_count.update(filtered_nouns)

        # 가장 많이 나온 키워드 10개 추출
        top_keywords = word_count.most_common(10)
        return top_keywords

    # 키워드를 사용해 워드 클라우드 생성하는 함수
    def create_word_cloud(top_keywords):
        try:
            wordcloud = WordCloud(font_path='C:\\Users\\odpa0\\AppData\\Local\\Microsoft\\Windows\\Fonts\\BMJUA_ttf.ttf', width=800, height=400, background_color='white').generate_from_frequencies(dict(top_keywords))
        except OSError:
            print("Font file not found. Using default font.")
            wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(dict(top_keywords))
        
        # 워드 클라우드 시각화
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title(f"Top Keywords from {year}", fontsize=15)
        plt.show()

    # 가장 많이 나온 키워드 10개 추출
    top_keywords = extract_top_keywords(lyrics_list)

    # 워드 클라우드 생성 및 시각화
    create_word_cloud(top_keywords)

def generate_wordcloud_from_year():
    """
    주어진 연도의 노래 제목과 가사에서 가장 많이 나온 한글 명사 10개를 추출하고,
    이를 사용해 워드 클라우드를 생성하여 시각화합니다.
    
    Parameters:
    - year (str): 연도를 나타내는 문자열 (e.g., '2010')
    - stopwords_file (str): 불용어 파일 경로
    
    Returns:
    - None (출력만 수행)
    """
    
    year = entry_1.get()

    # 불용어 파일 읽기
    with open(r"C:\Users\odpa0\OneDrive\바탕 화면\decadelyrics\stopwords.txt", 'r', encoding='utf-8') as file:
        stopwords = set(file.read().split())
    
    # {year}_lyrics.txt 파일에서 제목과 가사 읽기
    file_path = fr"C:\Users\odpa0\OneDrive\바탕 화면\decadelyrics\{year}_lyrics.txt"
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    lyrics_list = []
    title = None
    lyrics = []
    
    for line in lines:
        line = line.strip()
        if line.startswith("Title:"):
            if title and lyrics:
                # 이전 제목과 가사를 저장
                lyrics_list.append((title, " ".join(lyrics)))
            title = line.replace("Title:", "").strip()
            lyrics = []
        elif line.startswith("Lyrics:"):
            continue
        else:
            lyrics.append(line)
    
    # 마지막 곡 추가
    if title and lyrics:
        lyrics_list.append((title, " ".join(lyrics)))
    
    # 한글 형태소 분석기 Okt 사용
    okt = Okt()
    
    # 노래 제목과 가사에서 가장 많이 나온 한글 명사 10개를 추출하는 함수
    def extract_top_keywords(lyrics_list):
        word_count = collections.Counter()
        for title, lyrics in lyrics_list:
            # 제목과 가사 합치기
            combined_text = f"{title} {lyrics}"
            # 한글 명사만 추출
            nouns = okt.nouns(combined_text)
            # 중복 제거
            unique_nouns = set(nouns)
            # 불용어 제거 및 한글 필터링
            filtered_nouns = [noun for noun in unique_nouns if noun not in stopwords and re.match(r'^[가-힣]+$', noun)]
            word_count.update(filtered_nouns)
        
        # 가장 많이 나온 한글 명사 10개 추출
        top_keywords = word_count.most_common(10)
        return top_keywords
    
    # 가장 많이 나온 한글 명사 10개 추출
    top_keywords = extract_top_keywords(lyrics_list)
    
    # 워드 클라우드 생성 및 시각화
    def create_word_cloud(top_keywords):
        wordcloud = WordCloud(font_path='C:\\Users\\odpa0\\AppData\\Local\\Microsoft\\Windows\\Fonts\\BMJUA_ttf.ttf', width=800, height=400, background_color='white').generate_from_frequencies(dict(top_keywords))
        
        # 워드 클라우드 시각화
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title(f"Top Keywords from {year}", fontsize=15)
        plt.show()
    
    # 워드 클라우드 생성 및 시각화 함수 호출
    create_word_cloud(top_keywords)


window = Tk()
window.geometry("1400x900")
window.configure(bg = "#FFFFFF")

canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 900,
    width = 1400,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    701.0,
    68.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    700.0,
    596.0,
    image=image_image_2
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    385.0,
    255.5,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=160.0,
    y=225.0,
    width=450.0,
    height=59.0
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    399.0,
    255.0,
    image=image_image_3
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=generate_wordcloud_from_year,  # Changed command to call display_wordcloud
    relief="flat"
)
button_1.place(
    x=733.0,
    y=209.0,
    width=541.0,
    height=88.0
)

canvas.create_text(
    537.0,
    138.0,
    anchor="nw",
    text="Decade Select",
    fill="#000000",
    font=("Inter Bold", 30 * -1)
)


button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: (print("button_2 clicked"), run_search()),
    relief="flat"
)
button_2.place(
    x=401.0,
    y=56.368408203125,
    width=101.55384826660156,
    height=24.63157844543457
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: (print("button_3 clicked"), run_data()),
    relief="flat"
)
button_3.place(
    x=534.83544921875,
    y=56.368408203125,
    width=101.55384826660156,
    height=24.63157844543457
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_4 clicked"),
    relief="flat"
)
button_4.place(
    x=676.0,
    y=56.368408203125,
    width=127.251953125,
    height=24.63157844543457
)

button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: (print("button_5 clicked"), run_keygraph()),
    relief="flat"
)
button_5.place(
    x=835.0,
    y=55.0,
    width=162.0,
    height=24.63157844543457
)

window.resizable(False, False)
window.mainloop()
