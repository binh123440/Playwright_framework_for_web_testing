import logging


def get_logger(name: str = __name__):
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
    return logging.getLogger(name)
