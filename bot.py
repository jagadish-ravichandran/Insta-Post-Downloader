from instagram_handler import InstaBot
import json


insta_bot = InstaBot()


d = insta_bot.getPost(url)
print(json.dumps(d, indent=4))