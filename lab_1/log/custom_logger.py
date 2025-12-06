import logging
from logging import DEBUG
from typing import cast

from colorama import init, Fore, Style

init(autoreset=True)

CURRENT_LVL = DEBUG


class CustomLogger(logging.Logger):
    def __init__(self, name: str, level=logging.NOTSET):
        super().__init__(name=name, level=level)


class ColorFormatter(logging.Formatter):
    def format(self, record):
        level = record.levelno
        if not hasattr(record, "sub_lvl"):
            record.sub_lvl = "-"

        if level == logging.DEBUG:
            record.msg = f"{Fore.YELLOW}{record.msg}{Style.RESET_ALL}"
        elif level == logging.INFO:
            record.msg = f"{Fore.LIGHTMAGENTA_EX}{record.msg}{Style.RESET_ALL}"
        elif level == logging.WARNING:
            record.msg = f"{Fore.LIGHTYELLOW_EX}{record.msg}{Style.RESET_ALL}"
        elif level == logging.ERROR:
            record.msg = f"{Fore.RED}{record.msg}{Style.RESET_ALL}"
        return super().format(record)


def get_custom_logger(name: str = "custom") -> CustomLogger:
    logger = logging.getLogger(name)
    return cast(CustomLogger, logger)


logging.setLoggerClass(CustomLogger)
logger = get_custom_logger()
logger.setLevel(level=CURRENT_LVL)

custom_handler = logging.StreamHandler()
custom_handler.setFormatter(
    ColorFormatter(
        fmt="%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d %(funcName)s() - %(message)s",
        datefmt="%H:%M:%S",
    )
)
logger.addHandler(custom_handler)
