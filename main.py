from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
import urllib.parse
import pathlib
import mimetypes
import json
import socket
from threading import Thread

BASE_DIR = pathlib.Path(__file__).parent


class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path
        if path in ["/", "/message"]:
            self.send_html_file(f"{path.lstrip('/') or 'index'}.html")
        else:
            file_path = BASE_DIR / path[1:]
            if file_path.exists():
                self.send_static(file_path)
            else:
                self.send_html_file("error.html", 404)

    def send_static(self, file):
        self.send_response(200)
        mime_type, _ = mimetypes.guess_type(str(file))
        self.send_header('Content-type', mime_type or 'application/octet-stream')
        self.end_headers()
        with open(file, 'rb') as f:
            self.wfile.write(f.read())

    def send_html_file(self, filename, status=200):
        file_path = BASE_DIR / filename
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(file_path, 'rb') as f:
            self.wfile.write(f.read())

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        Thread(target=send_data_by_socket, args=(post_data,)).start()
        self.send_response(302)
        self.send_header('Location', '/message')
        self.end_headers()


def send_data_by_socket(data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((socket.gethostname(), 5000))
        client_socket.sendall(data)
        client_socket.shutdown(socket.SHUT_WR)


def run_http_server():
    server_address = ('', 3000)
    httpd = HTTPServer(server_address, HttpHandler)
    print("HTTP Server running on port 3000")
    httpd.serve_forever()


if __name__ == '__main__':
    Thread(target=run_http_server).start()
