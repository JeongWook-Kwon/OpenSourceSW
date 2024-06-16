import tkinter as tk
from tkinter import ttk
import pandas as pd

def load_and_sort_csv(file_path):
    """
    주어진 CSV 파일을 로드하고, Likes 기준으로 내림차순 정렬하여 상위 100개를 출력합니다.
    
    Parameters:
    - file_path (str): CSV 파일 경로
    
    Returns:
    - pandas DataFrame: 상위 100개 곡의 제목, 가수, 좋아요 수를 포함한 데이터프레임
    """
    # CSV 파일 로드
    data = pd.read_csv(file_path)
    
    # Artist 컬럼에서 쉼표 제거
    data['Artist'] = data['Artist'].str.replace(',', '', regex=False)
    
    # Likes 기준으로 내림차순 정렬
    sorted_data = data.sort_values(by='Likes', ascending=False)
    
    # 제목, 가수, 좋아요 수 컬럼만 선택
    sorted_titles_artists_likes = sorted_data[['Title', 'Artist', 'Likes']]
    
    # 인덱스 재설정
    sorted_titles_artists_likes.reset_index(drop=True, inplace=True)
    
    # 상위 100개 데이터 반환
    return sorted_titles_artists_likes.head(100)

def count_songs_per_artist_from_csv(file_path):
    """
    Given a CSV file containing song data, this function counts the number of songs per artist
    and returns the result as a pandas Series.
    
    Parameters:
    - file_path (str): Path to the CSV file containing song data
    
    Returns:
    - pandas Series: Series with artist names as index and song counts as values
    """
    # CSV 파일 로드
    data = pd.read_csv(file_path)
    
    # 가수 이름에서 ','를 제거
    data['Artist'] = data['Artist'].str.replace(',', '', regex=False)
    
    # 각 가수별 곡 수를 계산하여 Series 반환
    return data['Artist'].value_counts()

def show_results():
    # CSV 파일 경로
    file_path = 'melon_top_100(add LIKES).csv'
    
    # 결과 데이터 가져오기
    top_100_songs = load_and_sort_csv(file_path)
    artist_song_counts = count_songs_per_artist_from_csv(file_path)
    
    # Top 100 곡을 표시할 새 창 생성
    top100_window = tk.Toplevel(root)
    top100_window.title('Top 100 Songs by Likes')
    
    # Top 100 곡 데이터를 표시할 Treeview 생성
    treeview_top100 = ttk.Treeview(top100_window, columns=('Title', 'Artist', 'Likes'), show='headings')
    treeview_top100.heading('Title', text='Title')
    treeview_top100.heading('Artist', text='Artist')
    treeview_top100.heading('Likes', text='Likes')
    
    # 데이터 삽입
    for index, row in top_100_songs.iterrows():
        treeview_top100.insert('', 'end', values=(row['Title'], row['Artist'], row['Likes']))
    
    treeview_top100.pack(padx=10, pady=10)
    
    # 가수별 곡 수를 표시할 새 창 생성
    artist_counts_window = tk.Toplevel(root)
    artist_counts_window.title('Song Counts per Artist')
    
    # 가수별 곡 수를 표시할 Treeview 생성
    treeview_artist_counts = ttk.Treeview(artist_counts_window, columns=('Artist', 'Count'), show='headings')
    treeview_artist_counts.heading('Artist', text='Artist')
    treeview_artist_counts.heading('Count', text='Count')
    
    # 데이터 삽입
    for artist, count in artist_song_counts.items():
        treeview_artist_counts.insert('', 'end', values=(artist, count))
    
    treeview_artist_counts.pack(padx=10, pady=10)

# tkinter 초기화
root = tk.Tk()
root.title('Song Data Visualizer')

# 버튼 생성
button_show_results = tk.Button(root, text='데이터 확인하기', command=show_results)
button_show_results.pack(padx=20, pady=20)

# GUI 시작
root.mainloop()
