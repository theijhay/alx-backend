#!/usr/bin/env python3
"""
Basic Flask app with Babel support and parametrized templates
"""
from flask import Flask, render_template, request
from flask_babel import Babel

class Config(object):
    """
    Configuration class for Babel
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"

app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)

@babel.locale_selector
def get_locale():
    """
    Determine the best match for the app's supported languages
    based on the request's Accept-Language header.
    """
    return request.accept_languages.best_match(app.config['LANGUAGES'])

@app.route('/', strict_slashes=False)
def index():
    """
    Render the index template
    """
    return render_template('3-index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
