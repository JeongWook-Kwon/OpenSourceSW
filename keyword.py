import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter

# Step 1: Fetch song list from Melon
def get_song_list(chart_date):
    url = f"https://www.melon.com/chart/age/index.htm?chartType=AG&chartGenre=KPOP&chartDate={chart_date}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    songs = []
    for tr in soup.select('tr[data-song-no]'):
        song_no = tr['data-song-no']
        title = tr.select_one('div.ellipsis.rank01 a').text.strip()
        artist = tr.select_one('div.ellipsis.rank02 a').text.strip()
        songs.append({'song_no': song_no, 'title': title, 'artist': artist})
    return songs

# Step 2: Fetch lyrics for a song
def get_lyrics(song_no):
    url = f"https://www.melon.com/song/detail.htm?songId={song_no}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    lyrics = soup.select_one('div#d_video_summary')
    return lyrics.text.strip() if lyrics else ""

# Step 3: Find songs containing the keyword
def keyword_frequency(chart_date, keyword):
    songs = get_song_list(chart_date)
    keyword_songs = []
    for song in songs:
        try:
            lyrics = get_lyrics(song['song_no'])
            if keyword in lyrics:
                keyword_songs.append(song)
        except Exception as e:
            print(f"Error fetching lyrics for {song['title']}: {e}")
    return keyword_songs

# Step 4: Plot keyword frequency over years
def plot_keyword_frequency(years, keyword):
    frequencies = []
    for year in years:
        chart_date = f"{year}0101"
        keyword_songs = keyword_frequency(chart_date, keyword)
        frequencies.append(len(keyword_songs))
    
    plt.figure(figsize=(10, 5))
    plt.bar(years, frequencies, color='skyblue')
    plt.xlabel('Year')
    plt.ylabel('Number of Songs')
    plt.title(f"Number of Songs Containing the Keyword '{keyword}' Over Years")
    plt.show()

# Example usage
years = range(2010, 2021)  # Analyze from 2010 to 2020
keyword = 'love'
plot_keyword_frequency(years, keyword)
