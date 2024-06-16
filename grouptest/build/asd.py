import pandas as pd
from konlpy.tag import Okt
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud

def generate_wordcloud_from_lyrics(csv_file, stopwords_file, font_path):
    # 데이터 로드
    df = pd.read_csv(csv_file)

    # 불용어 리스트 로드
    with open(stopwords_file, 'r', encoding='utf-8') as file:
        stopwords = set(file.read().splitlines())

    # 한글 형태소 분석기 Okt 사용
    okt = Okt()

    # 각 곡의 가사에서 중복된 명사를 제거하고 빈도수 카운트
    count = Counter()
    for lyrics in df['Lyrics'].dropna():
        lyrics_nouns = okt.nouns(lyrics)  # 가사에서 명사 추출
        unique_nouns = set(lyrics_nouns)  # 중복 제거
        filtered_nouns = [noun for noun in unique_nouns if noun not in stopwords]  # 불용어 제거
        count.update(filtered_nouns)  # 명사 카운트

    # 많이 사용된 단어 추출 (상위 10개)
    most_common_nouns = dict(count.most_common(20))
    print(most_common_nouns)

    # 워드클라우드 생성
    wordcloud = WordCloud(font_path=font_path, width=800, height=800, background_color='white').generate_from_frequencies(most_common_nouns)

    # 워드클라우드 시각화
    plt.figure(figsize=(10, 10))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

# 함수 호출 예시
if __name__ == "__main__":
    csv_file = 'melon_top_100.csv'
    stopwords_file = r"C:\Users\odpa0\OneDrive\바탕 화면\decadelyrics\stopwords.txt"
    font_path = r'C:\Users\odpa0\AppData\Local\Microsoft\Windows\Fonts\BMJUA_ttf.ttf'
    
    generate_wordcloud_from_lyrics(csv_file, stopwords_file, font_path)
