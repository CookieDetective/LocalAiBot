import requests

class InstagramMessagingAPI:
    def __init__(self, page_access_token: str):
        # Page access token for sending messages via Messenger API
        self.page_access_token = page_access_token
        self.base_url = "https://graph.facebook.com/v19.0/me/messages"

    def send_dm(self, recipient_id: str, message: str) -> dict:
        # recipient_id is the Instagram user's PSID (Page-Scoped ID)
        payload = {
            "recipient": {"id": recipient_id},
            "message": {"text": message},
            "messaging_type": "UPDATE",
            "access_token": self.page_access_token
        }
        response = requests.post(self.base_url, json=payload)
        response.raise_for_status()
        return response.json()