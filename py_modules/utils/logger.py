import logging
import os
from py_modules.utils.constants import LOG_FILE
from py_modules.utils.di import bean

class CustomFormatter(logging.Formatter):
    def format(self, record):
        record.name = record.name[:15].ljust(15)
        return super().format(record)
    
@bean
class Logger:

    def __init__(self, name='asustray'):
        # Configurar el logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        # Formato de los mensajes de log
        formatter = CustomFormatter('[%(asctime)s][%(name)s][%(levelname)s] %(message)s')

        # Manejador de consola
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # Manejador de archivo
        file_handler = logging.FileHandler(LOG_FILE)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        self.tabs = 0

    def add_tab(self):
        self.tabs=self.tabs + 1

    def rem_tab(self):
        self.tabs=max(self.tabs - 1, 0)

    def tab_message(self, message:str):
        return ('\t' * self.tabs) + message
    
    def debug(self, message):
        self.logger.debug(self.tab_message(message))

    def info(self, message):
        self.logger.info(self.tab_message(message))

    def warning(self, message):
        self.logger.warning(self.tab_message(message))

    def error(self, message):
        self.logger.error(self.tab_message(message))

    def critical(self, message):
        self.logger.critical(self.tab_message(message))
