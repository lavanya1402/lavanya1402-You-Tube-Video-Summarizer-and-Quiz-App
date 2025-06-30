import yt_dlp
import os

def download_youtube_video(url, output_dir="uploads"):
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Setup yt-dlp options
    ydl_opts = {
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4",
        "merge_output_format": "mp4",
        "outtmpl": os.path.join(output_dir, "%(title).50s.%(ext)s"),
        "noplaylist": True,
        "http_headers": {  # Bypass 403 by simulating a real browser
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        },
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get('title', 'downloaded_video')
            final_path = os.path.join(output_dir, f"{title[:50]}.mp4")
            print(f"\n✅ Downloaded: {title}")
            print(f"📁 Saved to: {final_path}")
            return final_path

    except Exception as e:
        print(f"\n❌ Error downloading video: {e}")
        return None


if __name__ == "__main__":
    # You can change this URL to any public YouTube video
    url = "https://www.youtube.com/watch?v=bf7pCxj6mEg"
    download_youtube_video(url)
