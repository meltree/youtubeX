from flask import request, send_file
from . import video
import os
import yt_dlp


@video.route("/video", methods=["GET"])
def video():
    video_id = request.args.get("id")
    url = f"https://www.youtube.com/watch?v={video_id}"
    path = f"/tmp/{video_id}.mp4"

    if not os.path.exists(path):
        ydl_opts = {
            'format': '360p',
            'outtmpl': path,
            'quiet': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    return send_file(path, mimetype="video/mp4")