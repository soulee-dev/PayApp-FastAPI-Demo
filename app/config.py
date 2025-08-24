import os
from dotenv import load_dotenv

load_dotenv()

PAYAPP_USERID = os.getenv("PAYAPP_USERID", "판매자 아이디")
PAYAPP_LINKKEY = os.getenv("PAYAPP_LINKKEY", "연동 KEY")
PAYAPP_LINKVAL = os.getenv("PAYAPP_LINKVAL", "연동 VALUE")
SHOP_NAME = os.getenv("SHOP_NAME", "PAYAPP DEMO SHOP")
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
DB_PATH = os.getenv("DB_PATH", "app.db")
