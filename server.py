from http.server import BaseHTTPRequestHandler, HTTPServer

hostname = "localhost"
port = 8080
file = None


class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(2000)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(file.encode())


def start_server(file_to_serve):
    global file
    file = file_to_serve
    server = HTTPServer((hostname, port), Server)

    print("Results: http://{}:{}".format(hostname, port))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Server stopped")
        server.server_close()
