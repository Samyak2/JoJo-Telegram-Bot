from dotenv import load_dotenv
load_dotenv()
import os

TOKEN = os.getenv("TOKEN")

import requests

BASE_URL = "https://api.telegram.org/bot{}".format(TOKEN)

url = "{}/sendMessage".format(BASE_URL)
params = {"chat_id": "1012659275",
            "text": "_Kono Dio Da!_",
            "parse_mode": "Markdown"
        }

response = requests.get(url=url, params=params)

data = response.json()

for update in data["result"]:
    print(update)
