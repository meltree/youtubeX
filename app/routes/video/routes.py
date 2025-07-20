from flask import request, send_file
from . import video
import os
import yt_dlp
import subprocess

def progress_hook(d):
    if d['status'] == 'downloading':
        percent = d.get('_percent_str', '').strip()
        speed = d.get('_speed_str', '').strip()
        eta = d.get('_eta_str', '').strip()
        print(f"\r⏬ {percent} @ {speed} | ETA: {eta}", end='', flush=True)
    elif d['status'] == 'finished':
        print("\n✅ Download abgeschlossen!")

@video.route("/video", methods=["GET"])
def video_route():
    video_id = request.args.get("id")
    url = f"https://www.youtube.com/watch?v={video_id}"
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    CACHE_DIR = os.path.join(BASE_DIR, 'cache')
    os.makedirs(CACHE_DIR, exist_ok=True)
    raw_path = os.path.join(CACHE_DIR, f"{video_id}_raw.mp4")
    final_path = os.path.join(CACHE_DIR, f"{video_id}_ios.mp4")

    # Wenn finale Datei schon existiert, direkt senden
    if os.path.exists(final_path):
        return send_file(final_path, mimetype="video/mp4")

    # Video mit yt-dlp herunterladen (rohes Format)
    ydl_opts = {
        'format': 'bestvideo[height<=360]+bestaudio/best[height<=360]',
        'progress_hooks': [progress_hook],
        'outtmpl': raw_path,
        'merge_output_format': 'mp4',
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    # Konvertiere mit ffmpeg in iOS 1.0.0-kompatibles Format
    print("\n🎞 Konvertiere für iPhone 2G ...")
    subprocess.run([
        "ffmpeg", "-i", raw_path,
        "-c:v", "libx264", "-profile:v", "baseline", "-level", "3.0",
        "-c:a", "aac", "-b:a", "128k",
        "-movflags", "faststart",
        "-y", final_path
    ], check=True)

    return send_file(final_path, mimetype="video/mp4")
