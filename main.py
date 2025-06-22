import logging

from control import Controller
from log_config import setup_logger

if __name__ == "__main__":
    setup_logger()
    logger = logging.getLogger(__name__)
    logger.info("initialize...")
    try:
        app = Controller()
        app.start("test.js")
    except Exception as e:
        logger.critical(e)
        logger.critical("app failed to start")
        logger.debug("", exc_info=e)
    logger.info("app stop")
