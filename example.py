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


class TreatmentHandler(BaseHandler):
	def get(self, userId):

		# try-catch
		# user = getUser(db, userId)

		# getTreatments = getTreatments(db, user["id"])

		# getImageUrl

		treatments = [
				{
						"userId": 1,
						"label": "Weight loss Treatment",
						"ailment": "weight-loss",
						"action-items": "checkup",
						"due-date": "some date",
						"isRequiredReq": True
				},
		]

		self.respond({"message": {"treatments": treatments}})


class ActionItemsHandler(BaseHandler):
	def get(self, userId):

		actionItems = [
			{
				"label": "Checkup",
				"value": "checkup"
			}
		]

		print(userId, type(userId))

		user = None

		users = [{
			"id": 1,
			"action-items": actionItems
		}]

		for u in users:
			if u["id"] == userId:
				user = u
				break

		if not user:
			self.send_error(404, f"user with id '{userId}' not found")

			return

		self.respond({"message": {"action-items": user["action-items"]}})


def run_server(serverType="sync", port=8080):
	RequestHandler.routes = {
		r"/": HomeHandler,
		r"/([\d]+)": HomeHandler,
		r"/treatments": TreatmentHandler,
		r"/actionitems/([\d]+)": ActionItemsHandler,
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
