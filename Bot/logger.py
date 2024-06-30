import logging

# configure the logging
logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt="%d/%m/%y %H:%M:%S",
    handlers=[
        logging.FileHandler(f"{__name__}"),
        logging.StreamHandler(),
    ],
)

logging.getLogger("pyrogram").setLevel(logging.ERROR)


def log(name: str) -> logging.Logger:
    return logging.getLogger(name)
