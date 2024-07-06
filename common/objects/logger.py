import logging
from logging.handlers import HTTPHandler
from abc import ABC, abstractmethod


class LoggerInterface(ABC):
    @abstractmethod
    def debug(self, message) -> None:
        pass

    @abstractmethod
    def info(self, message) -> None:
        pass

    @abstractmethod
    def error(self, message) -> None:
        pass

    @abstractmethod
    def warning(self, message) -> None:
        pass

    @abstractmethod
    def critical(self, message) -> None:
        pass


class Logger(LoggerInterface):
    def __init__(self):
        self.logger = logging.getLogger("save-it-logger")
        log_level = logging.DEBUG  # TODO- logging.INFO in QA and PROD
        self.logger.setLevel(log_level)

        # Create a console handler for local logging
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)

        # Create a handler for reporting logs to third party dashboard
        # dashboard_handler = HTTPHandler('')
        # dashboard_handler.setLevel(log_level)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        # dashboard_handler.setFormatter(formatter)

        self.logger.addHandler(console_handler)
        # self.logger.addHandler(dashboard_handler)

    def debug(self, message) -> None:
        self.logger.debug(message)

    def info(self, message) -> None:
        self.logger.info(message)

    def error(self, message) -> None:
        self.logger.error(message)

    def warning(self, message) -> None:
        self.logger.warning(message)

    def critical(self, message) -> None:
        self.logger.critical(message)
