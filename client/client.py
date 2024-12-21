"""
This is the client lib code
Author: Dawei Yin
"""

import requests
import time
import logging
import random
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
        self.tracer = tracer  # insert this to trace the algo performance

    # create the job
    def send_job(self, base_delay=None, var_delay=None, success_rate=None):
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

    # Using backoff (optinal: 1. jitter 2. approx_base_duration)
    # jitter: true if using jitter, scale from
    # approx_base_duration: A rough estimate of job duration (x in x ± rand(y)). If provided, we can adapt intervals more intelligently.
    def send_backoff_get_status(
        self,
        initial_interval,
        max_interval,
        timeout,
        jitter_scale=(1, 1),
        approx_base_duration=None,
    ):
        start_time = time.time()
        interval = initial_interval
        tries = 0

        ###tracer###
        self.tracer.clean()
        self.tracer.set_trace_algo("backoff")
        self.tracer.init_interval = initial_interval
        self.tracer.max_interval = max_interval
        self.tracer.request_start_time = start_time
        self.tracer.timeout = timeout
        self.tracer.approx_base_duration = approx_base_duration
        ###tracer###

        while True:
            status = self.get_status()
            tries += 1
            ###tracer###
            self.tracer.tries = tries
            ###tracer###

            # logger.info(f"send get status, total tires: {tries}")
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
                # logger.info(f"time out when back off, total tries: {tries}")
                return "max_time_reach"

            # default not using jitter
            jitter = random.uniform(jitter_scale[0], jitter_scale[1])

            next_interval = interval * 2 * jitter
            next_interval = min(next_interval, max_interval)

            # If learn approximate job length remains
            # try not to let the interval get too large
            if approx_base_duration and elapsed > approx_base_duration * 0.75:
                # If beyond .75 of the expected job length, slow down
                next_interval = min(next_interval, approx_base_duration * 0.2)

            # logger.info(f"do back off, preparing sleep for {interval}s")

            time.sleep(interval)
            ###tracer###
            self.tracer.jitters.append(jitter)
            self.tracer.intervals.append(interval)
            ###tracer###

            interval = next_interval
