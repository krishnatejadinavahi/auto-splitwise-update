import http.server
import json
from splitwiseapp.splitwise_api_utils import SplitwiseApiUtils

PORT = 8001


class HandleSplitwiseApiRq(http.server.BaseHTTPRequestHandler):

    def do_GET(self):

        if self.path.startswith("/?oauth_token"):
            oauth_token = self.path.split("oauth_token=")[1].split("&oauth_verifier=")[0]
            oauth_verifier = self.path.split("oauth_token=")[1].split("&oauth_verifier=")[1]
            splitwise_api_utils = SplitwiseApiUtils()
            splitwise_api_utils.post_transactions_to_splitwise(oauth_token, oauth_verifier)
            self.return_res()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        request_to_splitwise = json.loads(body.decode('utf-8'))

        splitwise_api_utils = SplitwiseApiUtils()
        splitwise_api_utils.get_or_request_splitwise_creds(request_to_splitwise)

        self.return_res()

    def return_res(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()


def run(server_class=http.server.HTTPServer, handler_class=HandleSplitwiseApiRq):
    server_address = ('', PORT)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...')
    httpd.serve_forever()


run()
