"""
This is the mock server
Auther: Dawei Yin
"""

from flask import Flask, jsonify
from server_request import ServerRequest
from config import ServerConfig
import time


app = Flask(__name__)

# mock server config
BASE_DELAY = ServerConfig.BASE_DELAY
VAR_DELAY = ServerConfig.VAR_DELAY
SUCCESS_RATE = ServerConfig.SUCCESS_RATE

##init
cur_request = None


@app.route("/request", methods=["GET"])
def server_request():
    # mimic sending the request
    global cur_request
    cur_request = ServerRequest(time.time(), BASE_DELAY, VAR_DELAY, SUCCESS_RATE)
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



if __name__ == '__main__':  
   app.run()