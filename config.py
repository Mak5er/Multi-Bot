import os

from dotenv import load_dotenv

load_dotenv()
from pathlib import Path

token = str(os.getenv("token"))
admin_id = int(os.getenv("admin_id"))

I18N_DOMAIN = 'multitool'
BASE_DIR = Path(__file__).parent
LOCALES_DIR = BASE_DIR / 'locales'

