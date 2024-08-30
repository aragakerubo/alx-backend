#!/usr/bin/env python3
"""
Basic Flask app, Basic Babel setup, Get locale from request,
Parameterize templates, Force locale with URL parameter,
Mock logging in, Use user locale, Infer appropriate time zone
"""

from flask import Flask, render_template, request, g
from flask_babel import Babel, _
from typing import List
import pytz


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
    """Get locale by priority:
    1) URL parameter
    2) User locale from user settings
    3) User locale from request header
    4) Default
    """
    # Priority 1: URL parameter
    url_locale = request.args.get("locale")
    if url_locale and url_locale in Config.LANGUAGES:
        return url_locale

    # Priority 2: User locale from user settings
    user = getattr(g, "user", None)
    if user:
        user_locale = user.get("locale")
        if user_locale and user_locale in Config.LANGUAGES:
            return user_locale

    # Priority 3: User locale from request header
    header_locale = request.accept_languages.best_match(Config.LANGUAGES)
    if header_locale:
        return header_locale

    # Priority 4: Default
    return Config.BABEL_DEFAULT_LOCALE


@babel.timezoneselector
def get_timezone() -> str:
    """Get timezone by priority:
    1) URL parameter
    2) User timezone from user settings
    3) Default
    """
    # Priority 1: URL parameter
    url_timezone = request.args.get("timezone")
    if url_timezone:
        try:
            return pytz.timezone(url_timezone)
        except pytz.exceptions.UnknownTimeZoneError:
            pass

    # Priority 2: User timezone from user settings
    user = getattr(g, "user", None)
    if user:
        user_timezone = user.get("timezone")
        if user_timezone:
            try:
                return pytz.timezone(user_timezone)
            except pytz.exceptions.UnknownTimeZoneError:
                pass

    # Priority 3: Default
    return Config.BABEL_DEFAULT_TIMEZONE


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
    return render_template("7-index.html", get_locale=get_locale)


if __name__ == "__main__":
    """ Main Function running in debug mode"""
    app.run(debug=True)
