from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
from jinja2 import Environment, FileSystemLoader
import sqlite3
import os
from middleware import Middleware
from views import home_view,about_view,contact_view

class MyHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.template_env = Environment(loader=FileSystemLoader('templates'))
        self.db_connection = sqlite3.connect('mydatabase.db')
        super().__init__(*args, **kwargs)

    def render_template(self, template_name, **kwargs):
        template = self.template_env.get_template(template_name)
        return template.render(**kwargs)

    def serve_static_file(self, file_path):
        try:
            with open(file_path, 'rb') as file:
                content = file.read()
            self.send_response(200)
            self.send_header('Content-type', self.get_content_type(file_path))
            self.end_headers()
            self.wfile.write(content)
        except IOError:
            self.send_error(404, 'File Not Found')

    def get_content_type(self, file_path):
        extension = os.path.splitext(file_path)[1]
        if extension == '.css':
            return 'text/css'
        elif extension == '.js':
            return 'application/javascript'
        elif extension == '.jpg' or extension == '.jpeg':
            return 'image/jpeg'
        elif extension == '.png':
            return 'image/png'
        else:
            return 'application/octet-stream'

    def do_GET(self):
        routes = {
            '/': home_view,
            '/about': about_view,
            '/contact': contact_view
        }

        if self.path in routes:
            handler = routes[self.path]
            self.server.middleware.process_request(self)  # Pre-process request
            response = handler(self)
            self.server.middleware.process_response(response)  # Post-process response
        else:
            file_path = os.path.join('static', self.path[1:])
            if os.path.isfile(file_path):
                self.server.middleware.process_request(self)  # Pre-process request
                self.serve_static_file(file_path)
                self.server.middleware.process_response(None)  # Post-process response
            else:
                self.send_response(404)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'404 Not Found')

    def do_POST(self):
        routes = {
            '/submit': submit_view
        }

        if self.path in routes:
            content_length = int(self.headers['Content-Length'])
            request_body = self.rfile.read(content_length).decode('utf-8')
            params = parse_qs(request_body)
            handler = routes[self.path]
            self.server.middleware.process_request(self)  # Pre-process request
            response = handler(self, params)
            self.server.middleware.process_response(response)  # Post-process response
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'404 Not Found')


class MyHTTPServer(HTTPServer):
    def __init__(self, server_address, RequestHandlerClass, middleware):
        super().__init__(server_address, RequestHandlerClass)
        self.middleware = middleware


def run():
    host = 'localhost'
    port = 8000

    middleware = Middleware(MyHandler)
    server = MyHTTPServer((host, port), MyHandler, middleware)
    print(f'Starting server on {host}:{port}')
    server.serve_forever()


if __name__ == '__main__':
    run()