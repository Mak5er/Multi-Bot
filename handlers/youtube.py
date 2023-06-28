from pytube import YouTube

# ссылка на загружаемое видео
link = "https://www.youtube.com/watch?v=J0Aq44Pze-w"
yt = YouTube(link)
print(yt.streams)
