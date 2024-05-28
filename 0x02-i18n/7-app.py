#!/usr/bin/env python3
"""Flask application with Babel for i18n, timezone support, and mock user login"""

from flask import Flask, render_template, request, g
from flask_babel import Babel, _, format_datetime
import pytz
from pytz import UnknownTimeZoneError

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
    The order of priority is:
    1. Locale from URL parameters
    2. Locale from user settings
    3. Locale from request headers
    4. Default locale
    Returns:
        str: Best match locale string.
    """
    # Locale from URL parameters
    locale = request.args.get('locale')
    if locale and locale in app.config['LANGUAGES']:
        return locale
    
    # Locale from user settings
    if g.user and g.user['locale'] in app.config['LANGUAGES']:
        return g.user['locale']
    
    # Locale from request headers
    return request.accept_languages.best_match(app.config['LANGUAGES'])

@babel.timezoneselector
def get_timezone():
    """
    Determine the best match for supported time zones.
    The order of priority is:
    1. Timezone from URL parameters
    2. Timezone from user settings
    3. Default timezone
    Returns:
        str: Best match timezone string.
    """
    # Timezone from URL parameters
    timezone = request.args.get('timezone')
    if timezone:
        try:
            pytz.timezone(timezone)
            return timezone
        except UnknownTimeZoneError:
            pass
    
    # Timezone from user settings
    if g.user and g.user['timezone']:
        try:
            pytz.timezone(g.user['timezone'])
            return g.user['timezone']
        except UnknownTimeZoneError:
            pass

    # Default timezone
    return app.config['BABEL_DEFAULT_TIMEZONE']

@app.route('/')
def index():
    """
    Render the main index page.
    Returns:
        str: Rendered HTML template.
    """
    current_time = format_datetime()
    return render_template('7-index.html', home_title=_("home_title"), home_header=_("home_header"), current_time=current_time)

if __name__ == '__main__':
    app.run(debug=True)
