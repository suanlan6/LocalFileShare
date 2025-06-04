import logging
import sys

class CustomFormatter(logging.Formatter):
    def format(self, record):
        # 时间、日志级别、文件名、行号、消息
        log_fmt = "[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s"
        formatter = logging.Formatter(log_fmt, datefmt="%Y-%m-%d %H:%M:%S")
        return formatter.format(record)

def get_logger(name=__name__):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(CustomFormatter())
        logger.addHandler(handler)
    return logger

_logger = get_logger()

if __name__ == "__main__":
    _logger.info("This is an info message.")
    _logger.warning("This is a warning message.")
    _logger.error("This is an error message.")