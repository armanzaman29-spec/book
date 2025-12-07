import logging
import sys
from datetime import datetime
from typing import Any, Dict

# Create a custom logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create handlers
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)

# Create formatters and add to handlers
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
console_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(console_handler)

# Also configure the root logger to use the same format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[console_handler]
)

def log_info(message: str, extra: Dict[str, Any] = None):
    """Log an info message"""
    if extra:
        logger.info(message, extra=extra)
    else:
        logger.info(message)

def log_error(message: str, extra: Dict[str, Any] = None, exc_info: bool = False):
    """Log an error message"""
    if extra:
        logger.error(message, extra=extra, exc_info=exc_info)
    else:
        logger.error(message, exc_info=exc_info)

def log_warning(message: str, extra: Dict[str, Any] = None):
    """Log a warning message"""
    if extra:
        logger.warning(message, extra=extra)
    else:
        logger.warning(message)

def log_debug(message: str, extra: Dict[str, Any] = None):
    """Log a debug message"""
    if extra:
        logger.debug(message, extra=extra)
    else:
        logger.debug(message)

class LoggerMixin:
    """Mixin class to add logging capabilities to other classes"""

    @property
    def logger(self):
        return logging.getLogger(f"{self.__class__.__module__}.{self.__class__.__name__}")