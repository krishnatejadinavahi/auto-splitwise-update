from googleapiclient.discovery import build
import redis
import json


class RedisUtils:
    def __init__(self, creds):
        self.service = build('gmail', 'v1', credentials=creds)

        self.client = redis.Redis(host='localhost', port=6379)
        discover_config = 'Your purchase exceeds the amount you set'
        # amex_config = '{}'
        bofa_config = 'Activity Alert: Electronic or Online Withdrawal Over Your Chosen Alert Limit'
        default_preferences = '{"cardsToTrack": ["Amex", "Discover", "BoFA"]}'

        self.email_address = self.service.users().getProfile(userId='me').execute()['emailAddress']

        self.client.set('Discover', discover_config)
        # self.client.set('Amex', amex_config)
        self.client.set('BoFA', bofa_config)
        self.client.set('defaultPreferences', default_preferences)
        if not self.client.exists(f"${self.email_address}-lastPushedEmail"):
            self.client.set(f"${self.email_address}-lastPushedEmail", '{}')

    def update_preferences(self, json_string):
        self.client.set(f"${self.email_address}-preferences", json_string)
        print(f"Successfully set the key {self.email_address}-preferences to {json_string} on Redis")

    def get_preferences(self):
        if self.client.exists(f"${self.email_address}-preferences"):
            return json.loads(self.client.get(f"${self.email_address}-preferences"))
        return json.loads(self.client.get('defaultPreferences'))

    def get_or_create_last_pushed_email_structure(self, card):
        last_pushed_email_json = json.loads(self.client.get(f"${self.email_address}-lastPushedEmail").decode('utf-8'))

        if card not in last_pushed_email_json:
            last_pushed_email_json[card] = ""

        return last_pushed_email_json

    def update_last_pushed_email_structure(self, last_pushed_email_json):
        self.client.set(f"${self.email_address}-lastPushedEmail", json.dumps(last_pushed_email_json))
