import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
ARXIV_API_URL = "http://export.arxiv.org/api/query"
