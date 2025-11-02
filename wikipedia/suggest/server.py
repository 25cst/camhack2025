from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import json
import os
import readdb
import urllib.parse
from suggest import get_hints

class Handler(BaseHTTPRequestHandler):
    # request = empty body
    # response = { words: list[str] }
    def wordlist_handler(self):
        return { 'words': list(map((lambda i : readdb.id_to_title[i]), readdb.relations.keys())) }

    # request = { guess: str, secret: str, n: int } you should return n hints
    # response = { words: list[tuple[str, int]], closeness: int } closeness should be a int from 0 to 100
    def gethint_handler(self, body):
        hints, closeness = get_hints(body["guess"], body["secret"], body["n"], body["hint_level"])
        return { 'words': list(zip(hints, [closeness] * len(hints))) }

    def do_GET(self):
        response = { 'type': 'error', 'reason': 'Not found' }
        status = 404

        parsed_path = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_path.query)

        try:
            match self.path:
                case "/":
                    response = {'type': "hello", "reason": 'world'}
                    status = 200
                case "/wordlist":
                    response = self.wordlist_handler()
                    status = 200
                case "/gethint":
                    response = self.gethint_handler(query_params)
                    status = 200
        except Exception as e:
            response = { 'type': 'error', 'reason': str(e) }
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
