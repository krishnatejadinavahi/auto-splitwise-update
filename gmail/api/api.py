import base64
from googleapiclient.discovery import build
import redis
import json
from gmail.api.redis_utils import RedisUtils


class Api(RedisUtils):

    def get_emails(self):
        preferences = self.get_preferences()

        for card in preferences['cardsToTrack']:
            card_query = self.client.get(card)

            if card_query is not None:
                results = self.service.users().messages().list(userId='me', q=card_query.decode('utf-8')).execute()
                for message in results['messages']:
                    message_content = self.service.users().messages().get(userId='me', id=message['id'], format='full').execute()
                    email_content = ''

                    if 'data' in message_content['payload']['body'].keys():
                        email_content += message_content['payload']['body']['data']
                    else:
                        for part in message_content['payload']['parts']:
                            if 'data' in part['body'].keys():
                                email_content = part['body']['data'] + email_content

                    test = bytes(str(email_content), encoding='utf-8')
                    print(base64.urlsafe_b64decode(test))
