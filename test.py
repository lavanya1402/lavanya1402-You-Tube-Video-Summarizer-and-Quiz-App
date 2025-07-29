from yt_download import download_youtube_video

url = "https://www.youtube.com/watch?v=0R1mA_MVItI"
downloaded_path = download_youtube_video(url)
print(f"Downloaded Path: {downloaded_path}")
