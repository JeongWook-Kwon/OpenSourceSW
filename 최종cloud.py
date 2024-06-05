import collections
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 불용어 파일 읽기
with open(r"C:\Users\박주현\Desktop\opensource\stopwords.txt", 'r', encoding='utf-8') as file:
    stopwords = set(file.read().split())

# 사용자가 입력한 연도 받기
year = input("Please enter the year you want to check the chart for (e.g., 2010): ")

# {year}_lyrics.txt 파일에서 제목과 가사 읽기
file_path = fr"C:\Users\박주현\Desktop\opensource\연대별 Top 50 제목 및 가사\{year}_lyrics.txt"
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

# 노래 제목과 가사에서 가장 많이 나온 키워드 10개를 추출하는 함수
def extract_top_keywords(lyrics_list):
    word_count = collections.Counter()
    for title, lyrics in lyrics_list:
        # 제목과 가사 합치기
        combined_text = f"{title} {lyrics}"
        # 특수 문자 제거 및 소문자 변환
        combined_text = re.sub(r'[^\w\s]', '', combined_text).lower()
        # 단어 리스트로 변환 및 중복 제거
        words = set(combined_text.split())
        # 불용어 제거
        words = [word for word in words if word not in stopwords]
        word_count.update(words)
    
    # 가장 많이 나온 키워드 10개 추출
    top_keywords = word_count.most_common(10)
    return top_keywords

# 키워드를 사용해 워드 클라우드 생성하는 함수
def create_word_cloud(top_keywords):
    wordcloud = WordCloud(font_path='C:\\Windows\\Fonts\\H2GTRM.TTF', width=800, height=400, background_color='white').generate_from_frequencies(dict(top_keywords))
    
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
