import logging

# configure the logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(module)s - %(filename)s:%(lineno)d - %(message)s",
    datefmt="%d/%m/%y %H:%M:%S",
    handlers=[
        logging.FileHandler(filename="bot.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)

logging.getLogger("pyrogram").setLevel(logging.ERROR)


def log(name: str) -> logging.Logger:
    return logging.getLogger(name)
