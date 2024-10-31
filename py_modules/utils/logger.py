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

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)

# Ejemplo de uso
if __name__ == "__main__":
    log = Logger()
    log.info("Este es un mensaje de información.")
    log.error("Este es un mensaje de error.")
