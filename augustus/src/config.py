import configparser
from pathlib import Path

CONFIG_PATH = Path.home() / ".augustus.cnf"

_config = None


def load_config():
    global _config
    if _config is None:
        _config = configparser.ConfigParser()
        if CONFIG_PATH.exists():
            _config.read(CONFIG_PATH)
    return _config


def get_api_key(service_name):
    config = load_config()
    if config.has_section(service_name) and config.has_option(service_name, "api_key"):
        key = config.get(service_name, "api_key").strip()
        return key if key else None
    return None
