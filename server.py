from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
from typing import Dict, Any

app = Flask(__name__)
CORS(app)

# Configuration
class Config:
    def __init__(self):
        self.config_file = "config.json"
        self.config_data = {}
        self.load_config()

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as f:
                self.config_data = json.load(f)
        else:
            self.config_data = {
                "port": 5000,
                "host": "0.0.0.0",
                "debug": True
            }
            self.save_config()

    def save_config(self):
        with open(self.config_file, "w") as f:
            json.dump(self.config_data, f, indent=4)

    def get(self, key: str, default: Any = None) -> Any:
        return self.config_data.get(key, default)

config = Config()

# Error Handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

# Basic Health Check Endpoint
@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "mcp-server",
        "version": "1.0.0"
    })

# MCP Command Handler
@app.route("/api/v1/command", methods=["POST"])
def handle_command():
    try:
        data = request.get_json()
        
        if not data or "command" not in data:
            return jsonify({
                "error": "Invalid request format. 'command' field is required"
            }), 400

        command = data["command"]
        params = data.get("parameters", {})

        # TODO: Implement command handling logic here
        # This is where you would add your specific command implementations
        
        return jsonify({
            "status": "success",
            "command": command,
            "result": f"Command '{command}' processed successfully"
        })

    except Exception as e:
        return jsonify({
            "error": f"Failed to process command: {str(e)}"
        }), 500

# WebSocket support can be added here if needed
# from flask_socketio import SocketIO
# socketio = SocketIO(app)

def main():
    try:
        app.run(
            host=config.get("host", "0.0.0.0"),
            port=config.get("port", 5000),
            debug=config.get("debug", True)
        )
    except Exception as e:
        print(f"Failed to start server: {e}")
        exit(1)

if __name__ == "__main__":
    main()