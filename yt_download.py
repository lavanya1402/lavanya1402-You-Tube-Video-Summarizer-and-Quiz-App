import yt_dlp
import os

def download_youtube_video(url, output_dir="uploads"):
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # ✅ Use safe format (18 = 360p MP4) and custom headers to avoid 403 errors
    ydl_opts = {
        "format": "18",  # Safe format that usually works on most YouTube videos
        "merge_output_format": "mp4",
        "outtmpl": os.path.join(output_dir, "%(title).50s.%(ext)s"),
        "noplaylist": True,
        "quiet": False,  # Set to True to silence logs
        "http_headers": {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "en-US,en;q=0.9",
        },
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get("title", "downloaded_video")
            final_path = os.path.join(output_dir, f"{title[:50]}.mp4")
            print(f"\n✅ Downloaded: {title}")
            print(f"📁 Saved to: {final_path}")
            return final_path

    except Exception as e:
        print(f"\n❌ yt_dlp failed: {e}")
        return None


# ✅ Optional test runner
if __name__ == "__main__":
    test_url = "https://www.youtube.com/watch?v=0R1mA_MVItI"  # Replace with any test video
    downloaded_path = download_youtube_video(test_url)
    print(f"Downloaded Path: {downloaded_path}")
