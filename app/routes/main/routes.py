from . import main

@main.route('/', methods=['GET'])
def index():
    html = """<html><head><title>YT Suche</title></head><body style="background-color:#000; color:#fff; font-family:sans-serif; font-size:14px;">
<h1 style="text-align:center;">YouTube Suche</h1>
<form action="/search" method="POST" style="text-align:center; margin-bottom:20px;">
  <input name="query" type="text" style="width:200px; padding:4px;">
  <input type="submit" value="Suchen" style="padding:4px;">
</form>
<div style="text-align:center;">"""

    return html + "</div></body></html>"