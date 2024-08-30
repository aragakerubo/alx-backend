#!/usr/bin/env python3
"""
Basic Flask app, Basic Babel setup, Get locale from request,
Parameterize templates, Force locale with URL parameter,
Mock logging in
"""

from flask import Flask, render_template, request, g
from flask_babel import Babel, _
from typing import List


class Config:
    """Config app class"""

    LANGUAGES: List[str] = ["en", "fr"]
    BABEL_DEFAULT_LOCALE: str = "en"
    BABEL_DEFAULT_TIMEZONE: str = "UTC"


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}

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


def get_user() -> dict:
    """Get user"""
    login_as = request.args.get("login_as")
    if login_as:
        user_id = int(login_as)
        return users.get(user_id)
    return None


@app.before_request
def before_request() -> None:
    """Get user"""
    g.user = get_user()


@app.route("/")
def index() -> str:
    """Return index page"""
    return render_template("5-index.html", get_locale=get_locale)


if __name__ == "__main__":
    """ Main Function running in debug mode"""
    app.run(debug=True)
