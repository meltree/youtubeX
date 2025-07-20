from flask import request
from . import search
import requests
import json


# enter your config file name here if different from "config.json"
config_name = "myconfig.json"

API_URL = "https://www.googleapis.com/youtube/v3/search"
API_KEY = json.load(open(config_name))["API_KEY"]

@search.route("/search", methods=["POST"])
def search():
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

    html = """<html><head><title>YT Suche</title></head><body style="background-color:#000; color:#fff; font-family:sans-serif; font-size:14px;">
<h1 style="text-align:center;">YouTube Suche</h1>
<form action="/search" method="POST" style="text-align:center; margin-bottom:20px;">
  <input name="query" type="text" style="width:200px; padding:4px;">
  <input type="submit" value="Suchen" style="padding:4px;">
</form>
<div style="text-align:center;">"""

    for item in items:
        video_id = item["id"]["videoId"]
        title = item["snippet"]["title"]
        thumb = item["snippet"]["thumbnails"]["default"]["url"]
        html += f"""
        <div style="margin-bottom:10px;">
            <a href="/video?id={video_id}" style="color:white; text-decoration:none;">
                <img src="{thumb}" style="width:120px; height:auto; border:1px solid #555;"><br>
                <div style="margin-top:4px;">{title}</div>
            </a>
        </div>"""

    html += "</div></body></html>"
    return html