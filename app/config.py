import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/")

if not SECRET_KEY:
    raise ValueError("No SECRET_KEY set for Flask application. Please set it in the .env file.")