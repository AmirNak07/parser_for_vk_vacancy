import os

from dotenv import load_dotenv

load_dotenv(override=True)

TABLE_ID = os.environ.get("ID_TABLE")
NAME_WORKSHEET = os.environ.get("SPREADSHEET")
