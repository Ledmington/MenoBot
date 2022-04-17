import logging


class CustomFormatter(logging.Formatter):

    grey = "\x1b[38;20m"
    blue = "\x1b[34;40m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    time = "[%(asctime)s]"
    level = "%(levelname)s"
    msg = "%(message)s"

    FORMATS = {
        logging.DEBUG: time + "[" + grey + level + reset + "]: " + msg,
        logging.INFO: time + "[" + blue + level + reset + "]: " + msg,
        logging.WARNING: time + "[" + yellow + level + reset + "]: " + msg,
        logging.ERROR: time + "[" + red + level + reset + "]: " + msg,
        logging.CRITICAL: bold_red + time + "[" + level + "]: " + msg + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
