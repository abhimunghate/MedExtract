from pathlib import Path


# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Data directory
DATA_DIR = BASE_DIR / "data"

# Flask configuration
DEBUG = True

HOST = "127.0.0.1"
PORT = 5000