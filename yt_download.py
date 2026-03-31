import yt_dlp
import os
import uuid
def download_youtube(url, audio_only=False, progress_callback=None):
    import yt_dlp
    import os, uuid

    unique_id = str(uuid.uuid4())
    outdir = "downloads"
    os.makedirs(outdir, exist_ok=True)

    output_path = os.path.join(outdir, f"{unique_id}.%(ext)s")

    def hook(d):
        if d['status'] == 'downloading' and progress_callback:
            total = d.get('_total_bytes_str', '')
            downloaded = d.get('_downloaded_bytes_str', '')
            percent = d.get('_percent_str', '')
            speed = d.get('_speed_str', '')
            eta = d.get('eta')
            text = f"📦 Downloading: {percent} ({downloaded}/{total})\n⚡ {speed}, ⏳ ETA: {eta}s"
            progress_callback(text)

    ydl_opts = {
        'format': 'bestaudio/best' if audio_only else 'bestvideo+bestaudio/best',
        'outtmpl': output_path,
        'quiet': True,
        'progress_hooks': [hook],
        'noplaylist': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }] if audio_only else [],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        ext = 'mp3' if audio_only else info.get("ext", "mp4")
        return os.path.join(outdir, f"{unique_id}.{ext}")
