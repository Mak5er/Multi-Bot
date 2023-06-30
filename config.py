import os
from pathlib import Path


token = str(os.environ['token'])
admin_id = int(os.environ['admin_ids'])

I18N_DOMAIN = 'multitool'
BASE_DIR = Path(__file__).parent
LOCALES_DIR = BASE_DIR / 'locales'

