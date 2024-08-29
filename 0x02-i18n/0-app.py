#!/usr/bin/env python3
"""
Basic Flask app
"""

from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index() -> str:
    """Return index page"""
    return render_template("0-index.html")


if __name__ == "__main__":
    """ Main Function running in debug mode"""
    app.run(debug=True)
