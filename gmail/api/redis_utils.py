from googleapiclient.discovery import build
import redis
import json


class RedisUtils:
    def __init__(self, creds):
        self.service = build('gmail', 'v1', credentials=creds)

        self.client = redis.Redis(host='localhost', port=6379)
        discover_config = 'Your purchase exceeds the amount you set'
        amex_config = '{}'
        bofa_config = 'Activity Alert: Electronic or Online Withdrawal Over Your Chosen Alert Limit'
        default_preferences = '{"cardsToTrack": ["Amex", "Discover", "BoFA"]}'
        self.client.set('Discover', discover_config)
        # self.client.set('Amex', amex_config)
        self.client.set('BoFA', bofa_config)
        self.client.set('defaultPreferences', default_preferences)

    def update_preferences(self, json_string):
        email_address = self.service.users().getProfile(userId='me').execute()['emailAddress']
        self.client.set(email_address, json_string)
        print(f"Successfully set the key {email_address} to {json_string} on Redis")

    def get_preferences(self):
        email_address = self.service.users().getProfile(userId='me').execute()['emailAddress']
        if self.client.exists(email_address):
            return json.loads(self.client.get(email_address))
        return json.loads(self.client.get('defaultPreferences'))
