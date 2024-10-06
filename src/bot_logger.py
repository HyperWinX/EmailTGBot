import logging
import sys

def get_dual_logger() -> logging.Logger:
  logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s] [%(filename)s.%(funcName)s]  %(message)s")
  logger = logging.getLogger("dual_logger")
  fileHandler = logging.FileHandler("data/log.txt")
  fileHandler.setFormatter(logFormatter)
  logger.addHandler(fileHandler)
  consoleHandler = logging.StreamHandler(sys.stdout)
  consoleHandler.setFormatter(logFormatter)
  logger.addHandler(consoleHandler)
  return logger

def get_console_logger() -> logging.Logger:
  logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s] [%(filename)s.%(funcName)s]  %(message)s")
  logger = logging.getLogger("console_logger")
  logger.setLevel(logging.INFO)
  consoleHandler = logging.StreamHandler(sys.stdout)
  consoleHandler.setFormatter(logFormatter)
  logger.addHandler(consoleHandler)
  return logger
