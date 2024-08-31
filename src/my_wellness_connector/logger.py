import logging

logging.basicConfig(format="%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p")
app_logger: logging.Logger = logging.getLogger("my_wellness_connector")
app_logger.setLevel(logging.INFO)
