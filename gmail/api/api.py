import base64
from googleapiclient.discovery import build
import redis


class Api:

    def __init__(self):
        self.client = redis.Redis(host='localhost', port=6379)
        self.client.rpush('Amex', 'American Express', 'Amex')
        self.client.lrange('Amex', 0, -1)

    def update_preferences(self, creds):
        service = build('gmail', 'v1', credentials=creds)
        email_address = service.users().getProfile(userId='me').execute()['emailAddress']

    def get_emails(self, creds):
        service = build('gmail', 'v1', credentials=creds)

        results = service.users().messages().list(userId='me',
                                                  q='from:discover@service.discover.com subject:Your purchase exceeds the amount you set').execute()

        message = service.users().messages().get(userId='me', id='1725846a231489fe', format='full').execute()

        email_content = ''

        if 'data' in message['payload']['body'].keys():
            email_content += message['payload']['body']['data']
        else:
            for part in message['payload']['parts']:
                email_content = part['body']['data'] + email_content

        test = bytes(str(email_content), encoding='utf-8')
        print(base64.urlsafe_b64decode(test))
