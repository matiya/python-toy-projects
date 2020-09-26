import http.server


class RequestHandler(http.server.BaseHTTPRequestHandler):
    """Regreso una página básica"""

    Page = """\
    <html>
    <body>
    <table>
    <tr>  <td>Header</td>         <td>Value</td>          </tr>
    <tr>  <td>Date and time</td>  <td>{date_time}</td>    </tr>
    <tr>  <td>Client host</td>    <td>{client_host}</td>  </tr>
    <tr>  <td>Client port</td>    <td>{client_port}s</td> </tr>
    <tr>  <td>Command</td>        <td>{command}</td>      </tr>
    <tr>  <td>Path</td>           <td>{path}</td>         </tr>
    </table>
    </body>
    </html>
    """
   
    def do_GET(self):
        self.send_page()

    def create_page(self):
        values = {
            'date_time': self.date_time_string(),
            'client_host': self.client_address[0],
            'client_port': self.client_address[1],
            'command': self.command,
            'path': self.path
        }
        page = self.Page.format(**values)
        print(page)
        return page

    def send_page(self):
        page = self.create_page()
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(page.encode())


if __name__ == "__main__":
    serverAddress = ("", 8080)
    server = HTTPServer.HTTPServer(serverAddress, RequestHandler)
    server.serve_forever()
