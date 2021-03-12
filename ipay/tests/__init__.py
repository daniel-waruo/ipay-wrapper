# settings.py
import os
from pathlib import Path

from dotenv import load_dotenv

env_path = Path('.') / '.env'

load_dotenv(dotenv_path=env_path, verbose=True)

IPAY_VENDOR_ID = os.getenv('IPAY_VENDOR_ID')
IPAY_SECURITY_KEY = os.getenv('IPAY_SECURITY_KEY')
