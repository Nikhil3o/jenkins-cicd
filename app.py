import os
import json
from http.server import HTTPServer, SimpleHTTPRequestHandler

PORT = int(os.environ.get("PORT", 8080))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# HTML template matching the exact UI requirement
HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CI/CD DevOps Project</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            height: 100vh;
            width: 100vw;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            background-color: #1a2332;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            text-align: center;
            user-select: none;
        }
        h1 {
            color: #38bdf8;
            font-size: 2.8rem;
            font-weight: 700;
            letter-spacing: -0.5px;
            margin-bottom: 1.2rem;
        }
        h2 {
            color: #ffffff;
            font-size: 1.8rem;
            font-weight: 700;
            margin-bottom: 1.2rem;
        }
        p {
            color: #e2e8f0;
            font-size: 1.15rem;
            font-weight: 400;
        }
    </style>
</head>
<body>
    <h1>Welcome to CI/CD Pipeline!</h1>
    <h2>Jenkins + Docker + Kubernetes</h2>
    <p>Application deployed successfully.</p>
</body>
</html>
"""

# Attempt to use Flask if available; otherwise fallback to Python standard library
try:
    from flask import Flask, Response, jsonify
    app = Flask(__name__)

    @app.route("/")
    def home():
        return Response(HTML_PAGE, mimetype="text/html")

    @app.route("/health")
    def health():
        return jsonify({"status": "UP", "healthy": True}), 200

    if __name__ == "__main__":
        print(f" * Server running on http://localhost:{PORT}")
        app.run(host="0.0.0.0", port=PORT)

except ImportError:
    from http.server import HTTPServer, BaseHTTPRequestHandler

    class CustomHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == "/health":
                payload = json.dumps({"status": "UP", "healthy": True}).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(payload)))
                self.end_headers()
                self.wfile.write(payload)
            else:
                payload = HTML_PAGE.encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(payload)))
                self.end_headers()
                self.wfile.write(payload)

        def log_message(self, format, *args):
            print(f"[{self.log_date_time_string()}] {format % args}")

    if __name__ == "__main__":
        server = HTTPServer(("0.0.0.0", PORT), CustomHandler)
        print(f"============================================================")
        print(f" * Application running at: http://localhost:{PORT}")
        print(f" * Press Ctrl+C in this terminal to stop the server.")
        print(f"============================================================")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server...")
            server.server_close()
