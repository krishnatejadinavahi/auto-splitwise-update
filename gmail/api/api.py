import base64
from gmail.api.redis_utils import RedisUtils
from bs4 import BeautifulSoup
import re
from gmail.api.card_parsers.discover_parser import Discover
from gmail.api.card_parsers.bofa_parser import BoFA


class Api(RedisUtils):

    def get_emails(self):
        preferences = self.get_preferences()
        email_address = self.service.users().getProfile(userId='me').execute()['emailAddress']

        for card in preferences['cardsToTrack']:
            last_pushed_email_json = self.get_or_create_last_pushed_email_structure(card)
            card_query = self.client.get(card)

            if card_query is not None:
                results = self.service.users().messages().list(userId='me', q=card_query.decode('utf-8')).execute()

                if not last_pushed_email_json[card] and len(results['messages']) > 0:
                    latest_email_id = results['messages'][0]['id']
                    last_pushed_email_json[card] = latest_email_id
                    self.update_last_pushed_email_structure(last_pushed_email_json)


                for message in results['messages']:
                    message_content = self.service.users().messages().get(userId='me', id=message['id'],
                                                                          format='full').execute()
                    email_content = ''

                    if 'data' in message_content['payload']['body'].keys():
                        email_content += message_content['payload']['body']['data']
                    else:
                        for part in message_content['payload']['parts']:
                            if 'data' in part['body'].keys():
                                email_content = part['body']['data'] + email_content

                    transaction_text = bytes(str(email_content), encoding='utf-8')
                    transaction_html = base64.urlsafe_b64decode(transaction_text).decode('utf-8')
                    parser = self.get_parser(card)

                    text_without_spaces = re.sub('\s+', ' ', transaction_html)
                    parser.parse(text_without_spaces)

    def get_parser(self, card):
        if card == "Discover":
            return Discover()
        # if card == "Amex":
        # return Amex()
        if card == "BoFA":
            return BoFA()


# class Amex:
