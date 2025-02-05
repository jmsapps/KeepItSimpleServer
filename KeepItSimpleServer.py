from http.server import SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qsl
from re import fullmatch
from json import dumps, loads, JSONDecodeError


class RequestHandler(SimpleHTTPRequestHandler):
	routes = {}
	params = {}
	dbConnection = {}

	def do_GET(self):
		self.handle_request("get")

	def do_POST(self):
		self.handle_request("post")

	def do_PUT(self):
		self.handle_request("put")

	def do_PATCH(self):
		self.handle_request("patch")

	def do_DELETE(self):
		self.handle_request("delete")

	def do_PREPARE(self):
		if hasattr(self, "prepare"):
			getattr(self, "prepare")()

	def do_ON_FINISH(self):
		if hasattr(self, "on_finish"):
			getattr(self, "on_finish")()

	def handle_request(self, method):
		handler_class = None
		parsed_path = urlparse(self.path)
		path = parsed_path.path
		path_params = ()
		self.params = {
			**dict(parse_qsl(parsed_path.query)),
			**self.parse_json_body()
		}

		for route, handler in self.routes.items():
			match = fullmatch(route, path)

			if match:
				handler_class = handler
				path_params = match.groups()

				break

		if handler_class:
			self.__class__ = handler_class

			try:
				self.do_PREPARE()
			except Exception as e:
				self.send_error(500, f"{e}")

			if hasattr(self, method):
				method_func = getattr(self, method)

				try:
					method_func(*path_params)

					self.do_ON_FINISH()
				except Exception as e:
					self.do_ON_FINISH()
					self.send_error(500, f"{e}")

			else:
				self.do_ON_FINISH()
				self.send_error(405, "Method not allowed")

		else:
			self.send_error(404, "Not found")

	def send_json_response(self, response, status=200):
		response_body = dumps(response).encode("utf-8")

		self.send_response(status)
		self.send_header("Content-Type", "application/json")
		self.send_header("Content-Length", str(len(response_body)))
		self.end_headers()

		self.wfile.write(response_body)

	def parse_json_body(self):
		content_length = int(self.headers.get("Content-Length", 0))
		if content_length > 0:
			try:
				return loads(self.rfile.read(content_length).decode("utf-8"))
			except JSONDecodeError:
				self.send_error(400, "Invalid JSON")

				return {}

		return {}

	def send_error(self, code, message=None):
		self.send_json_response({"error": message or "Unknown error"}, status=code)
