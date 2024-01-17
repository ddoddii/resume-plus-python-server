import os
from dotenv import load_dotenv

load_dotenv()

TECH_QUESTION_NUM = 2
BEHAV_QUESTION_NUM = 2
MAX_SESSION = 5
FOUNDATION_MODEL = "gemini-pro"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
