#!/usr/bin/env python3
"""
Basic Flask app, Basic Babel setup, Get locale from request,
Parameterize templates, Force locale with URL parameter
"""

from flask import Flask, render_template, request
from flask_babel import Babel, _
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
    locale = request.args.get("locale")
    if locale and locale in app.config["LANGUAGES"]:
        return locale
    return request.accept_languages.best_match(app.config["LANGUAGES"]) or "en"


@app.route("/")
def index() -> str:
    """Return index page"""
    return render_template("4-index.html", get_locale=get_locale)


if __name__ == "__main__":
    """ Main Function running in debug mode"""
    app.run(debug=True)
