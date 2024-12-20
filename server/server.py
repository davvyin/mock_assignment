"""
This is the mock server
Auther: Dawei Yin
"""

from flask import Flask, jsonify, request
from server_request import ServerRequest
from config import ServerConfig
import time


app = Flask(__name__)

# mock server config, use default
server_config = ServerConfig()

##init
cur_request = None


@app.route("/request", methods=["POST"])
def server_request():
    # mimic sending the request
    global cur_request
    data = request.get_json()
    if data["base_delay"]:
        server_config.set_base_delay(data["base_delay"])
        print(f"Set base delay: {server_config.base_delay}")
    if data["var_delay"]:
        server_config.set_var_delay(data["var_delay"])
        print(f"Set var delay: {server_config.var_delay}")
    if data["success_rate"]:
        server_config.set_success_rate(data["success_rate"])
        print(f"Set success rate: {server_config.success_rate}")

    cur_request = ServerRequest(time.time(), server_config)
    return jsonify({"result": cur_request.to_dict()})


@app.route("/status", methods=["GET"])
def status():
    # 3 possible states: pending/error/completed
    cur_time = time.time()
    global cur_request
    if not cur_request:
        # no init request yet, return error
        return jsonify({"result": "error"})
    if cur_time >= cur_request.end_time:
        # request finished, error or completed
        return jsonify({"result": cur_request.end_status.name})
    return jsonify({"result": "pending"})


if __name__ == "__main__":
    app.run()
