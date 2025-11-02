from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import json
import os
import readdb

class Handler(BaseHTTPRequestHandler):
    # request = empty body
    # response = { words: list[str] }
    def wordlist_handler(self):
        print("got here")
        return { 'words': list(map((lambda i : readdb.id_to_title[i]), readdb.relations.keys())) }

    # request = { guess: str, secret: str, n: int } you should return n hints
    # response = { words: list[str] }
    def gethint_handler(self, body):
        raise Exception("TODO")

    def do_GET(self):
        response = { 'type': 'error', 'reason': 'Not found' }
        status = 404

        match self.path:
            case "/":
                response = {'type': "hello", "reason": 'world'}
                status = 200
            case "/wordlist":
                response = self.wordlist_handler()
                status = 200

        self.send_response(status)  # Bad request
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))

    def do_POST(self):
        post_data = self.rfile.read()  # Read the POST data
        # Assuming the POST data is JSON

        response = { 'type': 'error', 'reason': 'Not found' }
        status = 404
        try:
            data = json.loads(post_data)

            match self.path:
                case "/gethint":
                    response = self.gethint_handler(data)
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
        return 8081
    try:
        return int(s)
    except:
        return 8081

def run():
    server = ThreadingSimpleServer(('127.0.0.1', getPort()), Handler)
    print(f"Server started on 127.0.0.1:{getPort()}")
    server.serve_forever()

if __name__ == '__main__':
    run()
