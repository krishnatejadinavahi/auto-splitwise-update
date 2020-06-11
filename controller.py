import http.server
from gmail.authenticate.authenticate import GmailAuth
from gmail.api.api import Api

PORT = 8000


class HandleGmailApiRq(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        creds = self.get_creds()

        api = Api(creds)
        list_to_splitwise = api.get_emails()

        api.post_to_splitwise(
            [{'amount': '$8.03', 'merchant': 'Pressed Cafe LLC', 'date': 'May 27, 2020', 'card': 'Discover Card'},
             {'amount': '$27.86', 'merchant': 'MARKET BASKET 17', 'date': 'May 25, 2020', 'card': 'Discover Card'}])

        self.return_res()

    def do_POST(self):
        creds = self.get_creds()

        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        request_string = body.decode('utf-8')

        api = Api(creds)
        api.update_preferences(request_string)

        self.return_res()

    def get_creds(self):
        return GmailAuth.authenticate()

    def return_res(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()


def run(server_class=http.server.HTTPServer, handler_class=HandleGmailApiRq):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...')
    httpd.serve_forever()


run()
