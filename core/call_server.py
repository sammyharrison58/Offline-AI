import os
import sys
import json
import threading
import http.server
from typing import Dict, Any, List, Optional, Callable

class CallBridgeHandler(http.server.BaseHTTPRequestHandler):

    server_agent = None
    call_history: List[Dict[str, str]] = []
    active_call = False

    def log_message(self, format, *args):
        pass

    def send_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_cors_headers()
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_cors_headers()
        self.end_headers()
        data = {
            "status": "online",
            "active_call": CallBridgeHandler.active_call,
            "history": CallBridgeHandler.call_history[-20:]
        }
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def do_POST(self):
        content_len = int(self.headers.get('Content-Length', 0))
        post_body = self.rfile.read(content_len)
        try:
            req_data = json.loads(post_body.decode('utf-8'))
        except Exception:
            req_data = {}

        query = req_data.get('query', '').strip()
        action = req_data.get('action', '')

        if action == 'start_call':
            CallBridgeHandler.active_call = True
            resp_data = {"status": "call_started", "greeting": "Call connected. Nexus-Jarvis online and listening. Go ahead."}
        elif action == 'end_call':
            CallBridgeHandler.active_call = False
            resp_data = {"status": "call_ended", "farewell": "Call ended. Standing by."}
        elif query:
            if CallBridgeHandler.server_agent:
                response = CallBridgeHandler.server_agent.process_request(query)
            else:
                response = f"Echo: {query}"

            CallBridgeHandler.call_history.append({"user": query, "ai": response})
            resp_data = {"response": response, "user": query}
        else:
            resp_data = {"error": "Empty query or invalid action"}

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_cors_headers()
        self.end_headers()
        self.wfile.write(json.dumps(resp_data).encode('utf-8'))

class CallBridgeServer:

    _instance = None
    _server = None
    _port = 8502

    @classmethod
    def start(cls, agent, host: str = "127.0.0.1", port: int = 8502) -> int:
        if cls._server is not None:
            return cls._port

        CallBridgeHandler.server_agent = agent
        for p in [port, port + 1, port + 2, 8585]:
            try:
                server = http.server.ThreadingHTTPServer((host, p), CallBridgeHandler)
                cls._server = server
                cls._port = p
                thread = threading.Thread(target=server.serve_forever, daemon=True)
                thread.start()
                return p
            except OSError:
                continue
        return cls._port

    @classmethod
    def get_port(cls) -> int:
        return cls._port

    @classmethod
    def get_history(cls) -> List[Dict[str, str]]:
        return list(CallBridgeHandler.call_history)

    @classmethod
    def clear_history(cls):
        CallBridgeHandler.call_history.clear()
