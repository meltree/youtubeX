from flask import Flask


def create_app():
    app = Flask(__name__)

    from app.routes.main import main
    from app.routes.search import search
    from app.routes.video import video

    app.register_blueprint(main)
    app.register_blueprint(search)
    app.register_blueprint(video)

    return app