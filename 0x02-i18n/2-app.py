#!/usr/bin/env python3
"""
Basic Flask app, Basic Babel setup, Get locale from request
"""

from flask import Flask, render_template, request
from flask_babel import Babel
from typing import List


class Config:
    """Config app class"""

    LANGUAGES: List[str] = ["en", "fr"]
    BABEL_DEFAULT_LOCALE: str = "en"
    BABEL_DEFAULT_TIMEZONE: str = "UTC"


app = Flask(__name__)
babel = Babel(app)
app.config.from_object(Config)


@babel.localeselector
def get_locale() -> str:
    """Get locale from request"""
    return request.accept_languages.best_match(app.config["LANGUAGES"])


@app.route("/")
def index() -> str:
    """Return index page"""
    return render_template("2-index.html")


if __name__ == "__main__":
    """ Main Function running in debug mode"""
    app.run(debug=True)
