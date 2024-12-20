"""
This trace client side api request for getting the target
author: Dawei Yin
"""


class Tracer:
    def __init__(self, request_start_time=None, request_end_time=None):
        self.request_start_time = request_start_time
        self.request_end_time = request_end_time
        self.init_interval = 0
        self.intervals = []
        self.get_requests = []  # all get requests
        self.max_interval = 0
        self.timeout = 0
        self.success = False
        self.tries = 0

    def set_trace_algo(self, name):
        self.traced_algo = name

    def clean(self):
        # clean the tracer
        self.traced_algo = None
        self.request_start_time = None
        self.request_end_time = None
        self.init_interval = 0
        self.intervals = []
        self.get_requests = []  # all get requests
        self.max_interval = 0
        self.timeout = 0
        self.success = False
        self.tries = 0

    def __str__(self):
        # Format the trace information into a readable summary
        duration = (
            f"{self.request_end_time - self.request_start_time:.2f}s"
            if self.request_start_time and self.request_end_time
            else "N/A"
        )
        intervals_str = ", ".join(f"{i}s" for i in self.intervals)

        return (
            "Tracer Summary:\n"
            f"  Traced algorithm: {self.traced_algo}\n"
            f"  Request Duration: {duration}\n"
            f"  Initial Interval: {self.init_interval}s\n"
            f"  Intervals: {intervals_str if intervals_str else 'N/A'}\n"
            f"  Max Interval: {self.max_interval if self.max_interval else 'N/A'}\n"
            f"  Total Tries: {self.tries}\n"
            f"  Timeout: {self.timeout}s\n"
            f"  Success: {'Yes' if self.success else 'No'}\n"
            f"  GET tries: {self.tries}\n"
        )

    def get_report(self):
        if self.traced_algo:
            return str(self)
        else:
            return "not traced yet"
