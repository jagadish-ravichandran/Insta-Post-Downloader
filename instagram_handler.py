from instagrapi import Client
import json
import os
from decouple import config

from instagrapi.exceptions import (
    MediaNotFound,
    LoginRequired
)
IG_USERNAME = config("IG_USERNAME")
IG_PASSWORD = config("IG_PASSWORD")
IG_CREDENTIAL_PATH = "./ig_settings.json"

class InstaBot:
    _cl = None

    def __init__(self):
        self._cl = Client()
        if os.path.exists(IG_CREDENTIAL_PATH):
            self._cl.load_settings(IG_CREDENTIAL_PATH)
            self._cl.login(IG_USERNAME, IG_PASSWORD)
        else:
            self._cl.login(IG_USERNAME, IG_PASSWORD)
            self._cl.dump_settings(IG_CREDENTIAL_PATH)

    def getPost(self, url):
        data = {}
        id = self._cl.media_pk_from_url(url)
        exception_handled = False

        try:
            res = self._cl.media_info(id).dict()

        except (MediaNotFound, LoginRequired) as e:
            exception_handled = True
            print(e)

        # finally:
        #     self._cl.logout()

        if exception_handled:
            return {}

        data["caption"] = res["caption_text"]
        data["resources"] = []

        # check if video
        if res["media_type"] == 2:
            item = {}
            item["type"] = "video"
            item["download_url"] = res["video_url"]
            data["resources"].append(item)
        
        # check if photo
        elif res["media_type"] == 1:
            item = {}
            item["type"] = "photo"
            item["download_url"] = res["thumbnail_url"]
            data["resources"].append(item)

        # check if album
        elif res["media_type"] == 8:

            for each_post in res["resources"]:
                if each_post["media_type"] == 1:
                    item = {}
                    item["type"] = "photo"
                    item["download_url"] = each_post["thumbnail_url"]
                    data["resources"].append(item)
                elif each_post["media_type"] == 2:
                    item = {}
                    item["type"] = "video"
                    item["download_url"] = each_post["video_url"]
                    data["resources"].append(item)
        return data
    


if __name__ == "__main__":
    d = InstaBot()
    #private post => 
    url = "https://www.instagram.com/p/Ckin64-hviyr5i7bVCcHnxssUmOOdoZpZZIQBc0/"


    #public post=>
    # url = "https://www.instagram.com/reel/CqaBSmiJL2W/?utm_source=ig_web_copy_link"
    url = "https://www.instagram.com/reel/CqLEUCYuYRG/"
    r = d.getPost(url)
    print(json.dumps(r, indent= 4))