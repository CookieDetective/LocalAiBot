from instagram_tools.instagram_messaging import InstagramMessagingAPI

# Example usage in your system monitor or download manager
def notify_user_of_event(event_message: str, recipient_id: str, messenger_api: InstagramMessagingAPI):
    """Send a direct message update to user via Instagram Messenger API."""
    try:
        response = messenger_api.send_dm(recipient_id, event_message)
        return f"Notification sent: {response}"
    except Exception as e:
        return f"Failed to send notification: {e}"