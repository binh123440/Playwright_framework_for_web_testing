import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

# Logger configuration (run once)
_logger_configured = False


def _configure_logger():
    """Configure logger once at startup"""
    global _logger_configured
    if _logger_configured:
        return
    
    _logger_configured = True
    logs_dir = Path(__file__).parents[1] / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # File handler with rotation
    file_handler = RotatingFileHandler(
        logs_dir / "test.log",
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)


def get_logger(name: str = __name__) -> logging.Logger:
    """Get or create logger instance"""
    _configure_logger()
    return logging.getLogger(name)
