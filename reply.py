from database import ix, parser
import requests
import pprint
import json
import time
import sys
import os
from dotenv import load_dotenv
load_dotenv()


TOKEN = os.getenv("TOKEN")
BASE_URL = "https://api.telegram.org/bot{}".format(TOKEN)
message_responses = {
    "who are you?": "Kono Dio Da!",
    "who are you": "Kono Dio Da!",
    "what are you?": "Kono Dio Da!",
    "what are you": "Kono Dio Da!",
    "hi": "_Oh, you're approaching me?_",
}
gif_responses = [
    "hello there",
    "hello there!",
    "hello there."
]
gifs = "https://media.giphy.com/media/8JTFsZmnTR1Rs1JFVP/giphy.gif"

default_message = "Wryyyyyyy"
LAST_UPDATE_FILE = "last_id.txt"

with open(LAST_UPDATE_FILE, "rt") as f:
    last_update = int(f.read()) + 1


def send_message(text, chat_id):
    url = "{}/sendMessage".format(BASE_URL)
    params = {"chat_id": chat_id,
              "text": text,
              "parse_mode": "Markdown"
              }
    response = requests.get(url=url, params=params)


def send_gif_response(text, chat_id):
    url = "{}/sendAnimation".format(BASE_URL)
    params = {
        "chat_id": chat_id,
        "animation": gifs,
    }
    response = requests.get(url=url, params=params)
    data = response.json()
    pprint.pprint(data)


def send_inline_query(query, query_id, searcher):
    results = list(map(dict, searcher.search(parser.parse(query+"*"))))
    list(map(lambda x: x.update({"type": "audio"}), results))
    pprint.pprint(results)
    response = requests.post(f"{BASE_URL}/answerInlineQuery",
                             json={
                                 "inline_query_id": query_id,
                                 "results": results
                             })
    pprint.pprint(response.json())


update_url = "{}/getUpdates".format(BASE_URL)
# headers = {'Prefer': 'wait=120'}

print("Listening...")

with ix.searcher() as searcher:
    while True:
        print(".", end="")
        update_params = {"offset": last_update, "timeout": 5}
        # headers = {'Prefer': 'wait=120'}
        headers = {}
        response = requests.get(
            url=update_url, params=update_params, headers=headers)

        if response.status_code == 200:
            data = response.json()

            for update in data["result"]:
                pprint.pprint(update)
                if "message" in update and "text" in update["message"] and not update["message"]["from"]["is_bot"]:
                    text = update["message"]["text"].lower()
                    if text in message_responses:
                        send_message(
                            message_responses[text], update["message"]["chat"]["id"])
                    elif text in gif_responses:
                        send_gif_response(
                            text, update["message"]["chat"]["id"])
                    else:
                        send_message(default_message,
                                     update["message"]["chat"]["id"])
                if "inline_query" in update:
                    send_inline_query(update["inline_query"]["query"],
                                      update["inline_query"]["id"],
                                      searcher)
                with open(LAST_UPDATE_FILE, "wt") as f:
                    last_update = update["update_id"] + 1
                    f.write(str(last_update))

        elif response.status_code != 304:
            time.sleep(60)

        time.sleep(0.1)
