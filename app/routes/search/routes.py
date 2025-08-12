from flask import request, send_file, abort
from io import BytesIO
import os
from . import search
import requests
import json


# enter your config file name here if different from "config.json"
config_name = "myconfig.json"

API_URL = "https://www.googleapis.com/youtube/v3/search"
API_VIDEO_URL = "https://www.googleapis.com/youtube/v3/videos"
API_KEY = json.load(open(config_name))["API_KEY"]

@search.route("/search", methods=["POST"])
def search_r():
    query = request.form.get("query")
    print(f"Search query: {query}")
    params = {
        "part": "snippet",
        "maxResults": 50,
        "q": query,
        "key": API_KEY,
        "type": "video"
    }
    r = requests.get(API_URL, params=params)
    items = r.json().get("items", [])
    print(f"Search results: {len(items)} items found")

    html = """<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>YT Suche</title></head><body style="background-color:#ffffff; color:#000000; font-family:sans-serif; font-size:14px;">
<h1 style="text-align:center;">YouTube Suche</h1>
<form action="/search" method="POST" style="text-align:center; margin-bottom:20px;">
  <input name="query" type="text" style="width:200px; padding:4px;">
  <input type="submit" value="Suchen" style="padding:4px;">
</form>
<div style="text-align:left;">"""

    for item in items:
        video_id = item["id"]["videoId"]
        thumb = item["snippet"]["thumbnails"]["default"]["url"]
        thumb = f"/img_proxy?url={thumb}"
        title = item["snippet"]["title"]
        description = item["snippet"]["description"]
        params = {"part": "contentDetails", "id": video_id, "key": API_KEY}
        r_video = requests.get(API_VIDEO_URL, params=params)
        duration = r_video.json()['items'][0]['contentDetails']['duration']
        print(f"Video duration: {duration}")
#         html += f"""
#         <div style="margin-bottom:10px; max-width:320px; overflow: hidden;">
#   <a href="/video?id={video_id}" style="color:black; text-decoration:none; display:block;">
#     <img src="{thumb}" style="width:120px; height:auto; float:left; margin-right:10px; border:1px solid #555;">
#     <div style="overflow: hidden; word-wrap: break-word; margin-top: 4px;">
#       {title}
#     </div>
#   </a>
# </div>

# """
        html += f"""
        <div style="margin-bottom:10px; max-width:320px; overflow: hidden;">
  <a href="/video?id={video_id}" style="color:black; text-decoration:none; display:block;">
    <img src="{thumb}" style="width:120px; height:auto; float:left; margin-right:10px; border:1px solid #555;">
    <div style="overflow: hidden; word-wrap: break-word; margin-top: 4px;">
      {title}
    </div>
    <div style="color:#666; font-size:12px; margin-top:4px; overflow: hidden; white-space: nowrap; text-overflow: ellipsis;">
      {description}...
    </div>
    <div style="color:#999; font-size:11px; margin-top:2px;">
      {duration}
    </div>
  </a>
</div>
"""

    html += "</div></body></html>"
    return html

@search.route("/img_proxy", methods=["GET"])
def img_proxy_r():
    url = request.args.get("url")
    print(url)
    try:
        response = requests.get(url)
        if response.status_code != 200:
            abort(404)
        return send_file(BytesIO(response.content), mimetype='image/jpeg')
    except Exception:
        abort(500)