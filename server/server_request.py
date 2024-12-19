"""
Metadata of the video translation request
Author: Dawei Yin
"""

import random
from enum import Enum


class Status(Enum):
    error = "error"
    pending = "pending"
    completed = "completed"


# simulate random delay
def cal_random_ddl(base_delay, var_delay):
    return base_delay + random.randint(0, var_delay)


class ServerRequest:
    def __init__(self, request_time, base_delay, var_delay, success_rate):
        self.request_time = request_time
        self.base_delay = base_delay
        self.var_delay = var_delay
        # predetermined end time
        self.delay = cal_random_ddl(base_delay, var_delay)
        self.end_time = request_time + self.delay
        # predetermined result
        self.end_status = (
            Status.error if random.uniform(0, 1) > success_rate else Status.completed
        )

    def to_dict(self):
        return {
            "request_time": self.request_time,
            "end_time": self.end_time,
            "end_status": self.end_status.name,
            "delay": self.delay,
        }

    def __str__(self):
        return f"request_time: {self.request_time}\nend_time: {self.end_time}\nend_status: {self.end_status.name}\ndelay: {self.delay}"
