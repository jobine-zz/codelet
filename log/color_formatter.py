import logging


class ColorFormatter(logging.Formatter):
    red = "\x1b[31;21m"
    bold_red = "\x1b[31;1m"
    green = "\x1b[32;21m"
    yellow = "\x1b[33;21m"
    blue = "\x1b[34;21m"
    grey = "\x1b[38;21m"
    reset = "\x1b[0m"

    log_colors = {
        logging.DEBUG: grey,
        logging.INFO: green,
        logging.WARNING: yellow,
        logging.ERROR: red,
        logging.CRITICAL: bold_red
    }

    def format(self, record):
        log_color = self.log_colors.get(record.levelno)
        log_format = f"{log_color}{self._fmt}{self.reset}"
        formatter = logging.Formatter(log_format)
        return formatter.format(record)
