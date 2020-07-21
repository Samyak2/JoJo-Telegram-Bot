import pprint
import time
import sys
import os
import urllib3
import requests
from dotenv import load_dotenv
from reddit_wrapper import return_post
from database import ix, parser
load_dotenv()

BOT_TAG = "@oh_youre_approaching_me_bot"
TOKEN = os.getenv("TOKEN")
BASE_URL = "https://api.telegram.org/bot{}".format(TOKEN)

# configuration here
HELP_TEXT = """Welcome to JoJo Bot, the commands are
                    -- what/who are you?
                    -- hi
                    -- hello there
                    -- meme
                    -- jmeme
                    -- /jmeme
                    -- /meme
                    -- /help
                    -- help
                    -- ?
                    -- /?
You can tag the bot from a chat to get a soundboard!"""
# when keys are matched, the corresponding value is sent
message_responses = {
        "who are you?": "Kono Dio Da!",
        "who are you": "Kono Dio Da!",
        "what are you?": "Kono Dio Da!",
        "what are you": "Kono Dio Da!",
        "hi": "_Oh, you're approaching me?_",
        "help": HELP_TEXT,
        "help?": HELP_TEXT,
        "/help": HELP_TEXT,
        "/?": HELP_TEXT,
        "?": HELP_TEXT
        }

# messages for which GIF should be sent
gif_responses = [
        "hello there",
        "hello there!",
        "hello there."
        ]

# messages for which help text should be sent
help_reponses = [
        "help",
        "help?",
        "/help",
        "/?",
        "?",
        "/start"
        ]

# messages for which a random reddit meme should be sent
meme_responses = [
        "meme",
        "jmeme",
        "/meme",
        "/jmeme",
        ]

# GIF to send
gifs = "https://media.giphy.com/media/8JTFsZmnTR1Rs1JFVP/giphy.gif"

# default message when nothing is matched
default_message = "Wryyyyyyy! Try /help if you're looking for options."

# set up requests
sess = requests.Session()
retries = urllib3.util.retry.Retry(total=10,
                                   backoff_factor=0.1,
                                   status_forcelist=[500, 502, 503, 504])
sess.mount("https://", requests.adapters.HTTPAdapter(max_retries=retries))

def send_message(text, chat_id):
    """Sends `text` to chat `chat_id`
    """
    url = "{}/sendMessage".format(BASE_URL)
    params = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    response = sess.get(url=url, params=params)
    if response.status_code != requests.codes.ok: # pylint: disable=no-member
        print("*"*20, "ERROR", "*"*20)
        pprint.pprint(response.json())
        print("*"*45)
    else:
        print(f"Sent message to chat_id {chat_id}, replying with '{text}'")

def send_gif_response(text, chat_id):
    """Replies to a message with `text` in chat `chat_id`
    """
    url = "{}/sendAnimation".format(BASE_URL)
    params = {
        "chat_id": chat_id,
        "animation": gifs,
    }
    response = sess.get(url=url, params=params)
    if response.status_code != requests.codes.ok: # pylint: disable=no-member
        print("*"*20, "ERROR", "*"*20)
        pprint.pprint(response.json())
        print("*"*45)
    else:
        print(f"Sent GIF to chat_id {chat_id}, replying to '{text}'")

def send_meme_response(text, chat_id):
    """Replies to a message `text` with a random reddit meme in chat `chat_id`
    """
    url = "{}/sendMessage".format(BASE_URL)
    meme = return_post()
    print(meme)
    params = {
        "chat_id": chat_id,
        "text": meme,
    }
    response = sess.get(url=url, params=params)
    if response.status_code != requests.codes.ok: # pylint: disable=no-member
        print("*"*20, "ERROR", "*"*20)
        pprint.pprint(response.json())
        print("*"*45)
    else:
        print(f"Sent meme to chat_id {chat_id}, replying to '{text}'")

def send_inline_query(query, query_id, searcher):
    """Sends an inline query result by searching for `query` in the database
    and sends it to `query_id`. `searcher` is a woosh searcher instance for the database
    """
    results = list(map(dict, searcher.search(parser.parse(query+"*"))))
    list(map(lambda x: x.update({"type": "audio"}), results))
    response = sess.post(f"{BASE_URL}/answerInlineQuery",
                         json={
                             "inline_query_id": query_id,
                             "results": results})
    if response.status_code != requests.codes.ok: # pylint: disable=no-member
        print("*"*20, "ERROR", "*"*20)
        pprint.pprint(response.json())
        print("*"*45)
    else:
        print(f"Sent inline result to query_id {query_id}, with query '{query}'")

update_url = "{}/getUpdates".format(BASE_URL)
# headers = {'Prefer': 'wait=120'}

print("Listening...")

def main():
    """Main method to handle everything"""
    # to store ID of the last update processed
    LAST_UPDATE_FILE = "last_id.txt"
    with open(LAST_UPDATE_FILE, "rt") as f:
        last_update = int(f.read()) + 1

    with ix.searcher() as searcher:
        while True:
            print(".", end="")
            sys.stdout.flush()
            update_params = {"offset": last_update, "timeout": 5}
            # headers = {'Prefer': 'wait=120'}
            headers = {}
            response = sess.get(
                url=update_url, params=update_params, headers=headers)

            if response.status_code == 200:
                data = response.json()

                for update in data["result"]:
                    if "message" in update and \
                       "text" in update["message"] and not update["message"]["from"]["is_bot"]:
                        text = update["message"]["text"].lower()
                        text = text.replace(BOT_TAG, "")
                        print(f"\nGot message '{text}'"
                              f"from chat_id {update['message']['chat']['id']}")
                        if text in message_responses:
                            send_message(message_responses[text], update["message"]["chat"]["id"])
                        elif text in gif_responses:
                            send_gif_response(text, update["message"]["chat"]["id"])
                        elif text in meme_responses:
                            send_meme_response(text, update["message"]["chat"]["id"])
                        else:
                            send_message(default_message,
                                         update["message"]["chat"]["id"])
                    if "inline_query" in update:
                        print("\nGot inline query")
                        send_inline_query(update["inline_query"]["query"],
                                          update["inline_query"]["id"],
                                          searcher)
                    with open(LAST_UPDATE_FILE, "wt") as f:
                        last_update = update["update_id"] + 1
                        f.write(str(last_update))

            elif response.status_code != 304:
                time.sleep(60)

            time.sleep(0.1)

if __name__ == "__main__":
    main()
