from model import Base, Heroes, Motos, Stories, Battles
from sqlalchemy import create_engine
import logging
import os

logging.basicConfig(
    level=logging.getLevelName(logging.DEBUG),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename="./logs/main.log"
)


def get_console_error_logger_handler() -> logging.StreamHandler:
    console = logging.StreamHandler()
    console.setLevel(logging.ERROR)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    console.setFormatter(formatter)
    return console


def get_sqlalchemy_engine():
    return create_engine(os.getenv("DATABASE_URL"))
    #return create_engine("postgresql://dev_user:dev_password@db:5432/wh_40k_db")
