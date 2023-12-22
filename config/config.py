import os
from dotenv import load_dotenv

load_dotenv()

TECH_QUESTION_NUM = 2
BEHAV_QUESTION_NUM = 2
MAX_SESSION = 5
# TODO: 굳이 보여줘야 하나?
FOUNDATION_MODEL = "gpt-3.5-turbo-1106"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
