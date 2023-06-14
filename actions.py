import json
import requests

class Action:
    def __init__(self, db_manager, auth):
        self.db_manager = db_manager
        self.auth = auth

    def apply(self, email):
        pass


class MarkAsRead(Action):
    def apply(self, email):
        url = f"https://gmail.googleapis.com/gmail/v1/users/me/messages/{email['email_id']}/modify"
        headers = {
            'Authorization': f'Bearer {self.auth.token}',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        payload = json.dumps({'removeLabelIds': ['UNREAD']})
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
        self.db_manager.update_email(email["email_id"], True)

class MarkAsUnread(Action):
    def apply(self, email):
        url = f"https://gmail.googleapis.com/gmail/v1/users/me/messages/{email['email_id']}/modify"
        headers = {
            'Authorization': f'Bearer {self.auth.token}',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        payload = json.dumps({'addLabelIds': ['UNREAD']})
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
        self.db_manager.update_email(email["email_id"], False)


