import logging
import sys

def setup_logging(level: int = logging.INFO) -> None:
    """Configure structured logging for the entire application."""
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)
    
    # Avoid duplicate handlers on repeated calls
    if not root_logger.handlers:
        root_logger.addHandler(handler)
    
    # Suppress noisy third-party loggers
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("apscheduler").setLevel(logging.WARNING)
