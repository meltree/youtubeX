from . import main

@main.route('/', methods=['GET'])
def index():
    html = """<html><head><meta name="viewport" content="width=device-width, initial-scale=1.0"><meta charset="UTF-8"><title>YT Suche</title></head><body style="background-color:#ffffff; color:#000000; font-family:sans-serif; font-size:14px;">
<h1 style="text-align:center;">YouTube Suche</h1>
<form action="/search" method="POST" style="text-align:center; margin-bottom:20px;">
  <input name="query" type="text" style="width:200px; padding:4px;">
  <input type="submit" value="Suchen" style="padding:4px;">
</form>
<div style="text-align:center;">"""

    return html + "</div></body></html>"