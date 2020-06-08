import base64
from gmail.api.redis_utils import RedisUtils
from bs4 import BeautifulSoup


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
                    transaction_html = base64.urlsafe_b64decode(test).decode('utf-8')
                    parser = self.get_parser(card)
                    parser.parse(transaction_html)


    def get_parser(self, card):
        if card == "Discover":
            return Discover()
        # if card == "Amex":
            # return Amex()
        # if card == "BoFA":
            # return BoFA()


class Discover:
    def parse(self, transaction_html):
        soup = BeautifulSoup(transaction_html, "html.parser")

        amount_element = soup.find("td", text="Amount:")
        transaction_dict = {}

        if amount_element is not None:
            transaction_amount = amount_element.next_sibling.next_element.strip()
            transaction_dict["amount"] = transaction_amount
        else:
            return

        merchant_element = soup.find("td", text="Merchant:")

        if merchant_element is not None:
            transaction_merchant = merchant_element.next_sibling.next_element.strip()
            transaction_dict["merchant"] = transaction_merchant

        date_element = soup.find("td", text="Date:")

        if date_element is not None:
            transaction_date = date_element.next_sibling.next_element.strip()
            transaction_dict["date"] = transaction_date

        print(transaction_dict)

# class Amex:

# class BoFA:
