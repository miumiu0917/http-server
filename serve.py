import socketserver
import traceback


HOST, PORT = "", 8080


class HTTPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        try:
            address = self.client_address[0]
            print(f"[debug] request from {address}")
            data = self.request.recv(4096)
            if len(data) == 0:
                return
            request_data = data.decode('utf-8')
            lines = request_data.split('\r\n')
            request_line = lines[0]
            method, path, version = request_line.split(' ')

            doc = self._read_doc(path)

            self.request.send(f"HTTP/1.1 200 OK\r\n\r\n{doc}".encode('utf-8'))
        except FileNotFoundError as e:
            print(e)
            self.request.send("HTTP/1.1 404 NotFound\r\n\r\n".encode('utf-8'))
        except Exception:
            print(traceback.format_exc())
            print(request_line)
            self.request.send("HTTP/1.1 500 InternalServerError\r\n\r\n".encode('utf-8'))

    def _read_doc(self, path):
        if path[-1] == '/':
            path += 'index.html'
        with open(f'www{path}', 'r') as f:
            return f.read()


if __name__ == "__main__":
    try:
        server = socketserver.TCPServer((HOST, PORT), HTTPHandler)
        server.serve_forever()
    except Exception as e:
        print(e)
    finally:
        server.server_close()
