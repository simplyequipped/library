import os
import http.server
import socketserver

def start_local_server(directory, port=8000):
    os.chdir(directory)
    Handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("", port), Handler) as httpd:
        print(f"Serving at port {port}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopping the server...")
            httpd.server_close()

if __name__ == "__main__":
    # Replace 'path/to/your/directory' with your desired directory
    directory = 'path/to/your/directory'
    start_local_server(directory)


from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        params = parse_qs(parsed_path.query)

        if path == '/hello':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Hello, World!')

        elif path == '/custom_function':
            if 'param' in params:
                param_value = params['param'][0]
                # Run your custom function with the parameter received
                result = custom_function(param_value)
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(str(result).encode())

        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'404 - Not Found')

def custom_function(param):
    # Define your custom function here
    # This is a placeholder function, replace it with your logic
    return f'Parameter received: {param}'

if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MyRequestHandler)
    print('Server running...')
    httpd.serve_forever()
