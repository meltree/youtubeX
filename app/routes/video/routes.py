from flask import request, send_file
from . import video
import os
import yt_dlp

def progress_hook(d):
    if d['status'] == 'downloading':
        percent = d.get('_percent_str', '').strip()
        speed = d.get('_speed_str', '').strip()
        eta = d.get('_eta_str', '').strip()
        print(f"\r⏬ {percent} @ {speed} | ETA: {eta}", end='', flush=True)
    elif d['status'] == 'finished':
        print("\n✅ Download abgeschlossen!")


@video.route("/video", methods=["GET"])
def video():
    video_id = request.args.get("id")
    url = f"https://www.youtube.com/watch?v={video_id}"
    path = f"/tmp/{video_id}.mp4"

    if not os.path.exists(path):
        ydl_opts = {
            'format': 'best[height<=360]',
            'progress_hooks': [progress_hook],
            'outtmpl': path,
            'quiet': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    return send_file(path, mimetype="video/mp4")