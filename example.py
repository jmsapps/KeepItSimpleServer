from http.server import HTTPServer, ThreadingHTTPServer
from json import dumps

from KeepItSimpleServer import RequestHandler


class BaseHandler(RequestHandler):
	def prepare(self):
		print("DbConnection -> ", self.dbConnection.get("open"))

	def on_finish(self):
		print("DbConnection -> ", self.dbConnection.get("close"))

	def respond(self, response, status=200):
		self.send_response(status)
		self.send_header("Content-Type", "application/json")
		self.end_headers()
		self.wfile.write(dumps(response).encode("utf-8"))


class HomeHandler(BaseHandler):
	def get(self, userId=None):
		if userId:
			self.respond({"message": f"Successful GET from HomeHandler! -> userId: {userId}"})

			return

		self.respond({"message": f"Successful GET from HomeHandler!"})

	def post(self):
		self.respond({"message": f"Successful POST to HomeHandler! -> {self.params}"}, 201)


def run_server(serverType="sync", port=8080):
	RequestHandler.routes = {
		r"/": HomeHandler,
		r"/([\d]+)": HomeHandler,
	}

	RequestHandler.dbConnection = {
		"open": "opening connection...",
		"close": "closing connection...",
	}

	server_address = ("", port)

	if serverType == "sync":
		httpd = HTTPServer(server_address, RequestHandler)
		print(f"Server running on port {port}...")

	else:
		httpd = ThreadingHTTPServer(server_address, RequestHandler)
		print(f"Async server running on port {port}...")

	httpd.serve_forever()


if __name__ == "__main__":
	run_server()
