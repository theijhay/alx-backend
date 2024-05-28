#!/usr/bin/env python3
"""Flask application with Babel for i18n"""

from flask import Flask, render_template, request
from flask_babel import Babel, _

class Config:
    """Configuration class for Flask app"""
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'

app = Flask(__name__)
app.config.from_object(Config)

babel = Babel(app)

@babel.localeselector
def get_locale():
    """
    Determine the best match for supported languages.
    If 'locale' parameter is present in the request and its value is a supported locale,
    return it. Otherwise, use the default locale.
    Returns:
        str: Best match locale string.
    """
    locale = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])

@app.route('/')
def index():
    """
    Render the main index page.
    Returns:
        str: Rendered HTML template.
    """
    return render_template('4-index.html', home_title=_("home_title"), home_header=_("home_header"))

if __name__ == '__main__':
    app.run(debug=True)
