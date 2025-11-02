from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import json
import os
import urllib.parse

class Handler(BaseHTTPRequestHandler):
    # request = empty
    # response = { words: list[str] }
    def wordlist_handler(self, body):
        raise Exception("TODO")

    # request = empty
    # response = { secret: str }
    def getsecret_handler(self, body):
        raise Exception("TODO")

    # request = { keywords: list[str] }
    # response = { image: str }
    # in this response, you should save the image file to /freq-scraping/img
    # and return the file name of the file
    def draw_graph_dandler(self, body):
        raise Exception("TODO")

    def do_GET(self):
        response = { 'type': 'error', 'reason': 'Not found' }
        status = 404

        parsed_path = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_path.query)

        match parsed_path.path:
            case "/":
                response = {'type': "hello", "reason": 'world'}
                status = 200
            case "/graph":
                self.draw_graph_dandler(query_params)
                status = 200

        self.send_response(status)  # Bad request
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])  # Get the size of the POST data
        post_data = self.rfile.read(content_length)  # Read the POST data
        # Assuming the POST data is JSON

        response = { 'type': 'error', 'reason': 'Not found' }
        status = 404
        try:
            data = json.loads(post_data)

            match self.path:
                case "/wordlist":
                    response = self.wordlist_handler(data)
                    status = 200
                case "/getsecret":
                    response = self.getsecret_handler(data)
                    status = 200
        except json.JSONDecodeError:
            response = {'type': "error", "reason": 'Invalid JSON'}
            status = 400
        except Exception as e:
            response = {'type': "error", "reason": str(e)}
            status = 500

        self.send_response(status)  # Bad request
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))
        
class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    pass

def getPort():
    s = os.getenv("PORT")
    if s == None:
        return 8082
    try:
        return int(s)
    except:
        return 8082

def run():
    server = ThreadingSimpleServer(('127.0.0.1', getPort()), Handler)
    print(f"Server started on 127.0.0.1:{getPort()}")
    server.serve_forever()

if __name__ == '__main__':
    run()
