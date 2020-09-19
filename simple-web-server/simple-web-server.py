import http.server

class RequestHandler(http.server)
if __name__ == "__main__":
    serverAddress = ("", 8080)
    server = HTTPServer.HTTPServer(serverAddress, RequestHandler)
    server.serve_forever()
