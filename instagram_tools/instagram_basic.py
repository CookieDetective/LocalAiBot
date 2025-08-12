import requests
from typing import List

class InstagramBasicAPI:
    def __init__(self, access_token: str, user_id: str):
        self.access_token = access_token
        self.user_id = user_id
        self.base_url = "https://graph.instagram.com"

    def get_user_media(self) -> List[dict]:
        url = f"{self.base_url}/{self.user_id}/media"
        params = {"access_token": self.access_token}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json().get("data", [])

    def post_photo(self, image_url: str, caption: str = "") -> dict:
        # Step 1: Create media object
        creation_url = f"https://graph.facebook.com/v19.0/{self.user_id}/media"
        creation_payload = {
            "image_url": image_url,
            "caption": caption,
            "access_token": self.access_token
        }
        res = requests.post(creation_url, data=creation_payload)
        res.raise_for_status()
        creation_id = res.json().get("id")

        # Step 2: Publish media
        publish_url = f"https://graph.facebook.com/v19.0/{self.user_id}/media_publish"
        publish_payload = {
            "creation_id": creation_id,
            "access_token": self.access_token
        }
        pub_res = requests.post(publish_url, data=publish_payload)
        pub_res.raise_for_status()
        return pub_res.json()

    def get_comments(self, media_id: str) -> List[dict]:
        url = f"https://graph.instagram.com/{media_id}/comments"
        params = {"access_token": self.access_token}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json().get("data", [])

    def reply_to_comment(self, comment_id: str, text: str) -> dict:
        url = f"https://graph.instagram.com/{comment_id}/replies"
        data = {
            "message": text,
            "access_token": self.access_token
        }
        response = requests.post(url, data=data)
        response.raise_for_status()
        return response.json()