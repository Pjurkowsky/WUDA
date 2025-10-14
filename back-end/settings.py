from dotenv import load_dotenv
from os import environ


load_dotenv()
DB = environ["POSTGRES_DB"]
DATABASE_USER = environ["POSTGRES_USER"]
DATABASE_PWD = environ["POSTGRES_PASSWORD"]
DATABASE_PORT = environ.get("PORT", 5432)
DATABASE_HOST = environ.get("POSTGRES_HOST", "localhost")
DATABASE_URL = f"postgresql+psycopg2://{DATABASE_USER}:{DATABASE_PWD}@{DATABASE_HOST}:{DATABASE_PORT}/{DB}"
JWT_KEY = environ["JWT_KEY"]

APP_PORT = environ["APP_PORT"]
APP_HOST = environ.get("APP_HOST", "localhost")
