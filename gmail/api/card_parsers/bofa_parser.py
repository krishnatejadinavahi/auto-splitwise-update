from bs4 import BeautifulSoup


class BoFA:
    def parse(self, transaction_html):
        soup = BeautifulSoup(transaction_html, "html.parser")

        amount_element = soup.find("td", text=" Amount: ")
        transaction_dict = {}

        if amount_element is not None:
            transaction_amount = amount_element.find_parent().find_all('td')[-1].next_element.strip()
            transaction_dict["amount"] = transaction_amount
        else:
            return

        merchant_element = soup.find("td", text=" Merchant: ")

        if merchant_element is not None:
            transaction_merchant = merchant_element.find_parent().find_all('td')[-1].next_element.strip()
            transaction_dict["merchant"] = transaction_merchant

        date_element = soup.find("td", text=" Transaction date: ")

        if date_element is not None:
            transaction_date = date_element.find_parent().find_all('td')[-1].next_element.strip()
            transaction_dict["date"] = transaction_date

        transaction_dict["card"] = "BoFA Card"

        return transaction_dict
