#!/usr/bin/env python3
"""Flask application with Babel for i18n and mock user login"""

from flask import Flask, render_template, request, g
from flask_babel import Babel, _

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}

class Config:
    """Configuration class for Flask app"""
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'

app = Flask(__name__)
app.config.from_object(Config)

babel = Babel(app)

def get_user():
    """
    Get user information based on the 'login_as' parameter in the request.
    Returns:
        dict: User information dictionary or None.
    """
    user_id = request.args.get('login_as')
    if user_id and int(user_id) in users:
        return users[int(user_id)]
    return None

@app.before_request
def before_request():
    """
    Execute before all requests to set the current user in the global context.
    """
    g.user = get_user()

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
    if g.user and g.user['locale'] in app.config['LANGUAGES']:
        return g.user['locale']
    return request.accept_languages.best_match(app.config['LANGUAGES'])

@app.route('/')
def index():
    """
    Render the main index page.
    Returns:
        str: Rendered HTML template.
    """
    return render_template('5-index.html', home_title=_("home_title"), home_header=_("home_header"))

if __name__ == '__main__':
    app.run(debug=True)
