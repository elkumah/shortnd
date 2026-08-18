import json
import logging
import logging.config
import os
from logging.config import dictConfig

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGGING_CONFIG_FILE = os.path.join(BASE_DIR, 'logging_config.json')

# Load logging configuration from a JSON file
def load_logging_config(config_file: str = LOGGING_CONFIG_FILE) -> None:
    """
    Load the application's logging configuration.
    """
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                dictConfig(config)
        except json.JSONDecodeError:
            logging.basicConfig(level=logging.INFO)
    else:
        # Fallback to basic configuration if the config file is not found
        logging.basicConfig(level=logging.INFO)
        logger.warning( "Logging configuration file '%s' not found. Using basic configuration.",config_file,)
load_logging_config()


# Create a logger instance
def get_logger(name: str = __name__) -> logging.Logger:
    """
    Return a configured logger instance.
    """
    return logging.getLogger(name)  


