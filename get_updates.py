from dotenv import load_dotenv
load_dotenv()
import os

TOKEN = os.getenv("TOKEN")

import requests

BASE_URL = "https://api.telegram.org/bot{}".format(TOKEN)

url = "{}/getUpdates".format(BASE_URL)
params = {}

response = requests.get(url=url, params=params)

data = response.json()

for update in data["result"]:
    print(update)
