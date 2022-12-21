"""Flask configuration."""
from os import environ, path
from dotenv import load_dotenv


class Config(object):
    """
    Reading configuration from environment variables or .env.
    """

    basedir = path.abspath(path.dirname(__file__))
    load_dotenv(path.join(basedir, ".env"))
    MATTERMOST_ENABLED = environ.get("MATTERMOST_ENABLED", False)
    MATTERMOST_URL = environ.get("MATTERMOST_URL", "chat.example.com")
    MATTERMOST_PORT = int(environ.get("MATTERMOST_PORT", 443))
    MATTERMOST_SCHEMA = environ.get("MATTERMOST_SCHEMA", "https")
    MATTERMOST_USER = environ.get("MATTERMOST_USER")
    MATTERMOST_PASSWORD = environ.get("MATTERMOST_PASSWORD")
    MATTERMOST_DEBUG = environ.get("MATTERMOST_DEBUG", False)
    TELEGRAM_ENABLED = environ.get("TELEGRAM_ENABLED", False)
    TELEGRAM_TOKEN = environ.get("TELEGRAM_TOKEN")
    GOALERT_URL = environ.get("GOALERT_URL", "https://goalert.example.com")
    DEBUG = environ.get("DEBUG", False)
    PORT = int(environ.get("PORT", 8080))
    HOST = environ.get("HOST", "0.0.0.0")
