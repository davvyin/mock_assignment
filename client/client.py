"""
This is the client lib code
Author: Dawei Yin
"""

import requests
import time
import logging
from tracer import Tracer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger(__name__)


class Client:
    def __init__(self, request_url, status_url, tracer: Tracer):
        self.request_url = request_url
        self.status_url = status_url
        self.tracer = tracer #insert this to trace the algo performance

    # create the request
    def send_request(self, base_delay=None, var_delay=None, success_rate=None):
        try:
            json_data = {
                "base_delay": base_delay,
                "var_delay": var_delay,
                "success_rate": success_rate,
            }
            response = requests.post(self.request_url, json=json_data)
            json_res = response.json()
            return json_res.get("result")
        except Exception as e:
            logger.error(f"error when sending translation request {e}")
            return {"result": "sending error"}

    # get the status
    def get_status(self):
        try:
            response = requests.get(self.status_url)
            json_res = response.json()
            return json_res.get("result")
        except Exception as e:
            logger.error(f"error when fetching translation request status {e}")
            return {"result": "getting status error"}

    # using basic backoff
    def send_backoff_get_status(self, initial_interval, max_interval, timeout):
        start_time = time.time()
        interval = initial_interval
        tries = 0

        ###tracer###
        self.tracer.set_trace_algo("simple_backoff")
        self.tracer.init_interval = initial_interval
        self.tracer.max_interval = max_interval
        self.tracer.request_start_time = start_time
        self.tracer.timeout = timeout
        ###tracer###

        while True:
            status = self.get_status()
            tries += 1
            ###tracer###
            self.tracer.tries = tries
            ###tracer###

            logger.info(f"send get status, total tires: {tries}")
            if status in ["completed", "error"]:
                ###tracer###
                self.tracer.success = True
                self.tracer.request_end_time = time.time()
                ###tracer###
                return status
            elapsed = time.time() - start_time
            if elapsed > timeout:
                ###tracer###
                self.tracer.success = False
                ###tracer###
                logger.info(f"time out when back off, total tries: {tries}")
                return "max_time_reach"
            logger.info(f"do back off, preparing sleep for {interval}s")

            time.sleep(interval)
            ###tracer###
            self.tracer.intervals.append(interval)
            ###tracer###

            interval = min(interval * 2, max_interval)

    # using backoff + jitter
    def send_backoff_jitter_get_status(self, initial_interval, max_interval, timeout):
        start_time = time.time()
        interval = initial_interval
        tries = 0

        self.tracer.init_interval = initial_interval
        self.tracer.max_interval = max_interval
        self.tracer.request_start_time = start_time
        self.tracer.timeout = timeout

        while True:
            status = self.get_status()
            tries += 1
            self.tracer.tries = tries

            logger.info(f"send get status, total tires: {tries}")
            if status in ["completed", "error"]:
                self.tracer.success = True
                self.tracer.request_end_time = time.time()
                return status
            elapsed = time.time() - start_time
            if elapsed > timeout:
                self.tracer.success = False
                logger.info(f"time out when back off, total tries: {tries}")
                return "max_time_reach"
            logger.info(f"do back off, preparing sleep for {interval}s")

            time.sleep(interval)
            self.tracer.intervals.append(interval)

            interval = min(interval * 2, max_interval)
        pass
