import json
import os

with open("info.json", "r") as f:
    DATA = json.load(f)

OWNER_IDS = DATA["OWNER_IDS"]
EXTENSIONS = DATA["EXTENSIONS"]
No_Prefix = DATA["np"]
load_current_language = "en"
INTERNET_ACCESS = "True"
API_BASE_URL = "https://api.groq.com/openai/v1/"
MODEL_ID = "mixtral-8x7b-32768"
