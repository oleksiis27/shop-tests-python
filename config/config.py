import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
UI_URL = os.getenv("UI_URL", "http://localhost:3000")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@shop.com")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
USER_EMAIL = os.getenv("USER_EMAIL", "user@shop.com")
USER_PASSWORD = os.getenv("USER_PASSWORD", "user123")
