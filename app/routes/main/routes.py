from . import main

@main.route('/', methods=['GET'])
def index():
    return """
    <html><body>
        <form action="/search" method="POST">
            <input name="query" type="text">
            <input type="submit" value="Search">
        </form>
    </body></html>
    """