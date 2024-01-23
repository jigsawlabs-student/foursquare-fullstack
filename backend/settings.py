import os

from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_USER="postgres"
DB_PASSWORD=""
DEBUG = True
TESTING = True
