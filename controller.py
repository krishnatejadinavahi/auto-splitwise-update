import http.server
from gmail.authenticate.authenticate import GmailAuth

PORT = 8000


class HandleGmailApiRq(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        GmailAuth.authenticate()

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()


def run(server_class=http.server.HTTPServer, handler_class=HandleGmailApiRq):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...')
    httpd.serve_forever()


run()
