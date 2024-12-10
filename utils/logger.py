import os
import json
import logging

# Get logging configuration
if not (os.path.isfile("flappy_bird.cfg")):
    log_setting = False
else:
    with open("flappy_bird.cfg", "r") as infile:
        settings = json.load(infile)
        # don't log anything if false else log everything
        log_setting = settings["Logging"]


def get_logger(name):
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        logger.setLevel(logging.DEBUG)

        fileHandler = logging.FileHandler("flappy_bird.log", "a", "utf-8")
        fileHandler.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(name)s - %(message)s",
            datefmt="%d-%m-%Y %H:%M:%S",
        )
        fileHandler.setFormatter(formatter)

        logger.addHandler(fileHandler)
    return logger


if log_setting:

    def log(name, msg, type):
        # if not logging:
        #   return
        logger = get_logger(name)

        if type.lower() == "debug":
            logger.debug(str(msg), stack_info=True)
        elif type.lower() == "warn":
            logger.warning(str(msg))
        elif type.lower() == "error":
            logger.error(str(msg), stack_info=True)
        else:
            logger.info(str(msg))

else:

    def log(name, msg, type):
        return
