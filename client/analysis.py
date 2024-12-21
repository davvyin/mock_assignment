"""
Contain all target and request info for doing analysis
author: Dawei Yin
"""

import copy
from tracer import Tracer


##helper functions
def get_request_completion_delay(target: dict, request: Tracer):
    if not request.request_end_time or "end_time" not in target:
        # the request still pending
        return float("inf")
    if request.request_start_time >= target["end_time"]:
        # the get request is issued after the translation request finished
        return 0
    return request.request_end_time - target["end_time"]


def get_request_total_time(request: Tracer):
    return request.request_end_time - request.request_start_time


def get_hit_rate(request: Tracer):
    return 1 / request.tries


def get_efficiency_ratio(target: dict, request: Tracer):
    completion_delay = get_request_completion_delay(target, request)
    total_time = get_request_total_time(request)
    if total_time == 0:
        return float("inf")
    return completion_delay / total_time


##helper functions end


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

    def average_delay(self):
        # the average delay from calling the get status to learn the result
        n = len(self.requests)
        total_delay = 0
        for i in range(len(self.requests)):
            t, r = self.targests[i], self.requests[i]
            total_delay += get_request_completion_delay(t, r)
        return total_delay / n

    def average_tries(self):
        n = len(self.requests)
        total_tries = 0
        for i in range(len(self.requests)):
            total_tries += self.requests[i].tries
        return total_tries / n

    # Need to maximize this
    def average_hit_rate(self):
        return 1 / self.average_tries()

    # Need to minimize this
    # larger means longer gap
    def average_efficiency_ratio(self):
        n = len(self.requests)
        tr = 0

        for i in range(len(self.requests)):
            t, r = self.targests[i], self.requests[i]
            tr += get_efficiency_ratio(t, r)

        return tr / n

    def delay_std(self):
        return

    def tries_std(self):
        return

    def get_report(self):
        # prints all report
        res = f"Analysis report from {len(self.requests)} results\n"
        res += f"Average Delay: \n{self.average_delay():.4f}\n"
        res += f"Average tries: \n{self.average_tries()}\n"
        res += f"Average Hit rates: \n{self.average_hit_rate():.4f}\n"
        res += f"Average Efficiency ratio: \n{self.average_efficiency_ratio():.4f}\n"
        return res
