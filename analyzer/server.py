from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import json
import os
import urllib.parse
from pathlib import Path
import gettingdata

WORDLIST_PATH = Path(__file__).parent / "data" / "wordlist.txt"
IMG_SAVE_PATH = Path(__file__).parent / "img"

class Handler(BaseHTTPRequestHandler):
    # request = empty
    # response = { words: list[str] }
    with open(WORDLIST_PATH) as f:
        words = {"words" : [w.strip() for w in f.readlines()]}

    def wordlist_handler(self, body):
        return self.words

    # request = { keywords: list[str] }
    # response = { image: str }
    # in this response, you should save the image file to analyzer/img/graph.png
    # and return the file name of the file
    def draw_graph_handler(self, body):
        # print(body['keywords'])
        keywords = body.get('keywords')
        if keywords is None:
            raise ValueError('keywords query parameter is required')

        if isinstance(keywords, list):
            keyword_list = keywords
        else:
            keyword_list = [keywords]

        keyword_list = [str(k).strip() for k in keyword_list if str(k).strip()]
        if not keyword_list:
            raise ValueError('At least one keyword must be provided')

        file_path = IMG_SAVE_PATH / ("-".join(keyword_list) + ".png")

        years: list = []
        values: list = []
        gettingdata.graph_of_words(keyword_list, years=years, values=values, save_path=file_path)
        return {'image':str(file_path) }
    
    def do_GET(self):
        response = { 'type': 'error', 'reason': 'Not found' }
        status = 404

        parsed_path = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_path.query)

        try:
            if parsed_path.path == "/":
                response = {'type': "hello", "reason": 'world'}
                status = 200
            elif parsed_path.path == "/graph":
                response = self.draw_graph_handler(query_params)
                status = 200
            elif parsed_path.path == "/wordlist":
                response = self.wordlist_handler(query_params)
                status = 200
            elif parsed_path.path == "/getsecret":
                response = self.getsecret_handler(query_params)
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
        return 8082
    try:
        return int(s)
    except:
        return 8082

def run():
    server = ThreadingSimpleServer(('0.0.0.0', getPort()), Handler)
    print(f"Server started on 0.0.0.0:{getPort()}")
    server.serve_forever()

if __name__ == '__main__':
    
    run()
