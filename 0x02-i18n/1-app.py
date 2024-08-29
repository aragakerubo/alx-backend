#!/usr/bin/env python3
"""
Basic Flask app, Basic Babel setup
"""

from flask import Flask, render_template
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


@app.route("/")
def index() -> str:
    """Return index page"""
    return render_template("1-index.html")


if __name__ == "__main__":
    """ Main Function running in debug mode"""
    app.run(debug=True)
