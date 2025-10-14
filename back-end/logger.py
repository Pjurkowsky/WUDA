import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="app_errors.log",
)
LOGGER = logging.getLogger(__name__)
