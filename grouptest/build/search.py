#완
# 데이터 가는 버튼만 추가하면 됨

import pandas as pd
import os
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, Toplevel, Listbox, Scrollbar
import subprocess
from pathlib import Path
from PIL import ImageTk, Image

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\odpa0\OneDrive\바탕 화면\오픈소스 기초\grouptest\build\assets\frame1")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def run_decade():
    window.destroy()  # 현재 GUI를 닫습니다.
    subprocess.Popen(['python', OUTPUT_PATH / 'decade.py'])

def run_keygraph():
    window.destroy()  # 현재 GUI를 닫습니다.
    subprocess.Popen(['python', OUTPUT_PATH / 'keygraph.py'])

def run_data():  
    subprocess.Popen(['python', OUTPUT_PATH / 'data.py'])


def search_songs_by_keyword_and_year(directory, keyword, year):
    """
    주어진 디렉토리에서 특정 연도의 CSV 파일을 읽어와서
    주어진 키워드를 포함하는 노래를 검색하고 출력합니다.

    Parameters:
    - directory: CSV 파일들이 저장된 디렉토리 경로
    - keyword: 검색할 키워드
    - year: 검색할 연도
    """
    # 연도에 해당하는 파일 이름 생성
    csv_file = os.path.join(directory, f"melon_chart_{year}.csv")
    
    # 파일이 존재하는지 확인
    if not os.path.exists(csv_file):
        print(f"No data available for the year {year}.")
        return []

    # CSV 파일을 DataFrame으로 읽기
    df = pd.read_csv(csv_file)
    
    # 주어진 키워드를 포함하는 노래 필터링
    filtered_df = df[df['lyric'].str.contains(keyword, case=False, na=False)]
    
    # 결과 반환
    if not filtered_df.empty:
        return filtered_df[['title', 'singer']].values.tolist()
    else:
        return []

def display_results(results):
    result_window = Toplevel(window)
    result_window.title("Search Results")
    result_window.geometry("600x400")

    scrollbar = Scrollbar(result_window)
    scrollbar.pack(side="right", fill="y")

    listbox = Listbox(result_window, yscrollcommand=scrollbar.set)
    listbox.pack(side="left", fill="both", expand=True)

    for title, singer in results:
        listbox.insert("end", f"Title: {title}, Artist: {singer}")

    scrollbar.config(command=listbox.yview)

def on_search():
    keyword = entry_1.get()
    year = entry_2.get()
    
    if not year.isdigit():
        print("Please enter a valid year.")
        return

    results = search_songs_by_keyword_and_year(directory, keyword, int(year))
    
    if results:
        display_results(results)
    else:
        print(f"No songs from {year} contain the keyword '{keyword}'.")

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
canvas.create_rectangle(
    740.0,
    40.0,
    1360.0,
    860.0,
    fill="#E2F8F9",
    outline="")

canvas.create_rectangle(
    740.0,
    40.0,
    1360.0,
    860.0,
    fill="#E2F8F9",
    outline="")

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    325.5,
    349.5,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=116.0,
    y=326.0,
    width=419.0,
    height=45.0
)

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    355.0,
    469.0,
    image=image_image_1
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    325.5,
    469.5,
    image=entry_image_2
)
entry_2 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_2.place(
    x=116.0,
    y=445.0,
    width=419.0,
    height=47.0
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    355.0,
    348.0,
    image=image_image_2
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=on_search,
    relief="flat"
)
button_1.place(
    x=85.0,
    y=628.0,
    width=541.0,
    height=88.0
)

canvas.create_text(
    183.0,
    155.0,
    anchor="nw",
    text="Searching Tab",
    fill="#000000",
    font=("Inter Bold", 30 * -1)
)

image_path = relative_to_assets("wordcloud.png")
wordcloud_image = Image.open(image_path)
wordcloud_image = wordcloud_image.resize((600, 800))  # Resize the image to desired dimensions
wordcloud_photo = ImageTk.PhotoImage(wordcloud_image)

wordcloud_canvas = canvas.create_image(
    1050.0,
    450.0,
    image=wordcloud_photo
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    364.0,
    62.0,
    image=image_image_3
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=43.0,
    y=48.0,
    width=140.0,
    height=29.0
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
    x=172.0,
    y=48.0,
    width=140.0,
    height=29.0
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: (print("button_4 clicked"), run_decade()),
    relief="flat"
)
button_4.place(
    x=332.0,
    y=48.0,
    width=140.0,
    height=29.0
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
    x=514.0,
    y=48.0,
    width=161.0,
    height=29.0
)

directory = './melon_charts'  # CSV 파일들이 저장된 디렉토리

window.resizable(False, False)
window.mainloop()
