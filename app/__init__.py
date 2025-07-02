import os
from flask import Flask
from dotenv import load_dotenv

def create_app():
    app = Flask(__name__)
    load_dotenv()

    app.secret_key = os.getenv("FLASK_SECRET_KEY", "fallback-dev-key")

    # Register blueprint
    from app.routes import main
    app.register_blueprint(main)

    return app
