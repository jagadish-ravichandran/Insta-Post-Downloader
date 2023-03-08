from instagrapi import Client
import json
import os

IG_USERNAME = os.environ.get("USER")
IG_PASSWORD = os.environ.get("PASS")
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
        res = self._cl.media_info(id).dict()
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
    