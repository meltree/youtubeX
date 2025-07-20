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
    params = {
        "part": "snippet",
        "maxResults": 50,
        "q": query,
        "key": API_KEY,
        "type": "video"
    }
    r = requests.get(API_URL, params=params)
    items = r.json().get("items", [])

    html = "<html><body>"
    for item in items:
        video_id = item["id"]["videoId"]
        title = item["snippet"]["title"]
        thumb = item["snippet"]["thumbnails"]["default"]["url"]
        html += f'<a href="/video?id={video_id}"><img src="{thumb}"><div>{title}</div></a><br>'
    html += "</body></html>"
    return html