import structlog
import logging
import sys
from pythonjsonlogger import jsonlogger

def setup_logging(debug: bool = False):
    """
    Set up structured logging for the RAG chatbot application
    """
    # Configure standard logging
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.INFO,
        format="%(message)s",
        stream=sys.stdout
    )

    # Configure structlog
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            # Use JSONRenderer for production, ConsoleRenderer for development
            structlog.processors.JSONRenderer() if not debug else
            structlog.dev.ConsoleRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    return structlog.get_logger()

def get_logger(debug: bool = False):
    """
    Get the configured logger instance
    """
    return setup_logging(debug=debug)

# Initialize the logger with debug setting from config
from config import settings
logger = setup_logging(debug=settings.debug)

def get_logger_instance():
    """
    Get the configured logger instance
    """
    return logger