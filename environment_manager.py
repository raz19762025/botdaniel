
import os
from dotenv import load_dotenv

def load_env_chain():
    load_dotenv(override=True)
    return os.getenv("CURRENT_CHAIN", "bsc").lower()
