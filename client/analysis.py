"""
Contain all target and request info for doing analysis
author: Dawei Yin
"""

import copy
from tracer import Tracer


class Analysis:
    def __init__(self):
        self.targests = []
        self.requests = []

    def reset(self):
        self.targests = []
        self.requests = []

    def __add_targest(self, target: dict):
        self.targests.append(target)

    def __add_request(self, request: Tracer):
        self.requests.append(request)

    def add_entry(self, target, request):
        # take a snapshot of both and add to the list
        ntarget = copy.deepcopy(target)
        nrequest = copy.deepcopy(request)
        self.__add_request(nrequest)
        self.__add_targest(ntarget)

    @staticmethod
    def get_request_delay(target: dict, request: Tracer):
        if not request.request_end_time:
            # the request still pending
            return float("inf")
        if request.request_start_time >= target["end_time"]:
            # the get request is issued after the translation request finished
            return 0
        return request.request_end_time - target["end_time"]

    def average_delay(self):
        # the average delay from calling the get status to learn the result
        n = len(self.requests)
        total_delay = 0
        for i in range(len(self.requests)):
            t, r = self.targests[i], self.requests[i]
            total_delay += self.get_request_delay(t, r)
        return total_delay / n

    def average_tries(self):
        n = len(self.requests)
        total_tries = 0
        for i in range(len(self.requests)):
            total_tries += self.requests[i].tries
        return total_tries / n

    def delay_std(self):
        return

    def tries_std(self):
        return
