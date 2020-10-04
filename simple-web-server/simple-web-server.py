import os
import http.server


class RequestHandler(http.server.BaseHTTPRequestHandler):
    """Regreso una página básica"""

    template = """\
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
        try:
            full_path = os.getcwd() + self.path
            if not os.path.exists(full_path) and not (
                "favicon" or "icon.png" in full_path
            ):
                raise Exception(f"{self.path} not found")
            elif os.path.isfile(full_path):
                self.handle_file(full_path)
            else:
                raise Exception(f"{self.path} is unknown object")

        except Exception as msg:
            self.handle_error(msg)

    def handle_file(self, full_path):
        try:
            html_file = open(full_path, "r")
            content = html_file.read()
        except Exception as msg:
            self.handle_error(msg)
        self.send_page(content.encode())

    def create_page(self):
        values = {
            "date_time": self.date_time_string(),
            "client_host": self.client_address[0],
            "client_port": self.client_address[1],
            "command": self.command,
            "path": self.path,
        }
        page = self.template.format(**values)
        print(page)
        return page

    def send_page(self, content=None):
        if content is None:
            content = self.create_page().encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(content)

    def handle_error(self, msg):
        print(f">>> Error:  {msg}")
        self.send_page()


if __name__ == "__main__":
    serverAddress = ("", 8080)
    server = http.server.HTTPServer(serverAddress, RequestHandler)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.shutdown()
