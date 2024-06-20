from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    USER = os.environ["USER"]
    PASSWORD = os.environ["PASSWORD"]
    HOST = os.environ["HOST"]
    DATABASE = os.environ["DATABASE"]
    SERVER = os.environ["SERVER"]

    DATABASE_CONNECTION_URI = f'{SERVER}://{USER}:{PASSWORD}@{HOST}/{DATABASE}'
    SQLALCHEMY_DATABASE_URI = DATABASE_CONNECTION_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False

print(Config.DATABASE_CONNECTION_URI)
