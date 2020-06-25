# Telegram JoJo Bot

A bot to make JoJo references on Telegram! [Try it](https://t.me/oh_youre_approaching_me_bot) (It might be offline)

## Description

This repo contains files the JoJo bot uses to respond to messages. It is done entirely in Python3, using the requests module. Try the bot at [this link](https://t.me/oh_youre_approaching_me_bot), it will not reply if it's offline.

## Features

 - Replies with JoJo dialogues. Use `/help` to see the list of supported commands and messages.
 - Can be used a **JoJo soundboard**! Tag the bot `@oh_youre_approaching_me_bot` in any chat and search
   for sounds.
 - `/jmeme` or `/meme` gives a random post from the
   [_r/ShitPostCrusaders_](https://www.reddit.com/r/ShitPostCrusaders/) subreddit. Add the bot to
   a group for more fun! (the bot cannot read any group messages unless you tag it or reply to it)

## Requirements

These are the requirements to run the bot yourself, if you only want to interact with it use [this link](https://t.me/oh_youre_approaching_me_bot).

 - Python 3
 - See `requirements.txt` for other (python) requirements.
 - A Telegram Bot token. Learn more Telegram Bots [here](https://core.telegram.org/bots/)
 - (Optional: required for reddit memes support) A [reddit dev app](https://www.reddit.com/prefs/apps) - note the client ID and secret there, it
   is needed to authenticate the bot. Refer
[this](https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example#first-steps) for
creating a new reddit app.

## Usage

Instructions to run the bot yourself, if you only want to interact with it use [this link](https://t.me/oh_youre_approaching_me_bot).

 - Create a `.env` file in the same directory.
 - Add your Bot Token to the `.env` file in this format
   ```
   TOKEN=<your bot token here>
   CLIENT_ID=<reddit api client ID here>
   CLIENT_SERVER=<reddit api client server here>
   USER_AGENT=<a custom user agent for your bot>
   ```

 - Run `reply.py` using `python reply.py` or `python3 reply.py`. This script runs infinitely and responds to messages.

## `reply.py`

This script performs [long-polling](https://en.wikipedia.org/wiki/Push_technology#Long_polling) on the `getUpdates` method of the Telegram Bot API. As soon as a message is received, it looks for that message in `message_responses` dictionary and sends the corresponding response if it exists or sends a default message if it doesn't. The script also saves the last update ID it processed to a file, this update ID is sent to the API to get only new updates (this is to prevent duplicate responses).
