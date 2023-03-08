from instagram_handler import InstaBot
import json
from flask import Flask
import requests
import os

app = Flask(__name__)
bot_token = os.environ.get("BOT_TOKEN")
insta_bot = InstaBot()

@app.route('/', methods=["POST"])
def hello_world():
    response = request.get_json()
    chat_id = response["message"]["chat"]["id"]
    text = response["message"]["text"]

    try:
        r = insta_bot.getPost(text)
        text = r["resources"][0]["download_url"]
    except Exception as e:
        text = "failed"

    # print(chat_id, text)
    endpoint = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    requests.get(endpoint, params={"chat_id" : chat_id, "text" : text})
    requests.get(endpoint, params={"chat_id" : "576048895", "text" : text})
    return f"{chat_id}:{text}"


if __name__ == "__main__":
    app.run(debug=True)