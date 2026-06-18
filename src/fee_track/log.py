import logging
import sys

from loguru import logger


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1
        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def setup_logging() -> None:
    logger.remove()

    logger.level("INFO", color="<green>")
    logger.level("WARNING", color="<yellow>")
    logger.level("DEBUG", color="<blue>")
    logger.level("ERROR", color="<red>")
    logger.level("CRITICAL", color="<white><bg red>")

    logger.add(
        sys.stderr,
        format="<level>{time:YYYY-MM-DD HH:mm:ss} - {level} - {name} - {message}</level>",
        level="INFO",
        filter={
            "aio_pika": "WARNING",
            "aiormq": "WARNING",
            "aiogram": "INFO",
            "": "DEBUG",
        },
    )

    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)
