#!/usr/bin/env python3
"""Flask application with Babel for i18n"""

from flask import Flask, render_template, request, g
from flask_babel import Babel, _

app = Flask(__name__)


class Config:
    """Config class for Flask app"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)


babel = Babel(app)


@babel.localeselector
def get_locale():
    """Determine the best match for supported languages."""
    # Locale from URL parameters
    locale = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale

    # Locale from user settings
    user = g.get('user', None)
    if user and user.get('locale') in app.config['LANGUAGES']:
        return user['locale']

    # Locale from request headers
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def home():

    """Render the home page"""
    return render_template("3-index.html")


# Register `get_locale` as a template global
app.jinja_env.globals.update(get_locale=get_locale)

if __name__ == "__main__":
    app.run(debug=True)
