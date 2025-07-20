from flask import request, Response, send_file
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

def send_video_partial(path):
    file_size = os.path.getsize(path)
    range_header = request.headers.get('Range', None)
    if not range_header:
        return send_file(path, mimetype='video/mp4')

    byte1, byte2 = 0, None
    range_val = range_header.replace('bytes=', '').split('-')

    if len(range_val) == 2:
        if range_val[0]:
            byte1 = int(range_val[0])
        if range_val[1]:
            byte2 = int(range_val[1])

    length = file_size - byte1
    if byte2 is not None:
        length = byte2 - byte1 + 1

    with open(path, 'rb') as f:
        f.seek(byte1)
        data = f.read(length)

    rv = Response(data, 206, mimetype='video/mp4', direct_passthrough=True)
    rv.headers.add('Content-Range', f'bytes {byte1}-{byte1 + length - 1}/{file_size}')
    rv.headers.add('Accept-Ranges', 'bytes')
    rv.headers.add('Content-Length', str(length))
    return rv

@video.route("/video", methods=["GET"])
def video_route():
    video_id = request.args.get("id")
    if not video_id:
        return "Missing 'id' parameter", 400

    url = f"https://www.youtube.com/watch?v={video_id}"
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    CACHE_DIR = os.path.join(BASE_DIR, 'cache')
    os.makedirs(CACHE_DIR, exist_ok=True)
    raw_path = os.path.join(CACHE_DIR, f"{video_id}_raw.mp4")
    final_path = os.path.join(CACHE_DIR, f"{video_id}_ios.mp4")

    if os.path.exists(final_path):
        return send_video_partial(final_path)

    ydl_opts = {
        'format': 'bestvideo[height<=360]+bestaudio/best[height<=360]',
        'progress_hooks': [progress_hook],
        'outtmpl': raw_path,
        'merge_output_format': 'mp4',
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    print("\n🎞 Konvertiere für iPhone 2G ...")
    subprocess.run([
        "ffmpeg", "-i", raw_path,
        "-c:v", "libx264", "-profile:v", "baseline", "-level", "3.0",
        "-c:a", "aac", "-b:a", "128k",
        "-movflags", "faststart",
        "-y", final_path
    ], check=True)

    return send_video_partial(final_path)
