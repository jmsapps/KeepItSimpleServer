# KeepItSimpleServer

A lightweight HTTP server framework for Python.

## Features
✅ Minimalist, no unnecessary dependencies

✅ Supports `GET`, `POST`, `PUT`, `PATCH`, and `DELETE` methods

✅ Pre & post-request hooks (`prepare()`, `on_finish()`)

✅ Supports both **query parameters** (`?id=5`) and **JSON body parsing** (`POST {}`)

✅ JSON-based error handling

✅ Supports **both synchronous (`HTTPServer`) and asynchronous (`ThreadingHTTPServer`)**

# Quickstart
```bash
git clone https://github.com/jmsapps/KeepItSimpleServer.git
cd KeepItSimpleServer
python example.py
```

# Runnable Example
```python
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
```

### Make API Requests
- **GET Request:**
  ```bash
  curl -X GET "http://localhost:8080/"
  ```
  **Response:**
  ```json
  {"message": "Successful GET from HomeHandler!"}
  ```

- **GET Request with path param:**
  ```bash
  curl -X GET "http://localhost:8080/1"
  ```
  **Response:**
  ```json
  {"message": "Successful GET from HomeHandler! -> userId: 1"}
  ```

- **POST Request:**
  ```bash
  curl -X POST "http://localhost:8080/" \
       -H "Content-Type: application/json" \
       -d '{"key": "value"}'
  ```
  **Response:**
  ```json
  {"message": "Successful POST! -> {'key': 'value'}"}
  ```

### Logs
```bash
Server running on port 8080...
DbConnection ->  opening connection...
127.0.0.1 - - [05/Feb/2025 00:22:10] "GET / HTTP/1.1" 200 -
DbConnection ->  closing connection...
```
---

## License
MIT License
