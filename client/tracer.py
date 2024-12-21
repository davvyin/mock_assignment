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
        self.jitters = []
        self.max_interval = 0
        self.timeout = 0
        self.success = False
        self.tries = 0
        self.approx_base_duration = None

    def set_trace_algo(self, name):
        self.traced_algo = name

    def clean(self):
        # clean the tracer
        self.traced_algo = None
        self.request_start_time = None
        self.request_end_time = None
        self.init_interval = 0
        self.intervals = []
        self.jitters = []
        self.max_interval = 0
        self.timeout = 0
        self.success = False
        self.tries = 0
        self.approx_base_duration = None

    def __str__(self):
        if self.request_start_time is not None and self.request_end_time is not None:
            duration = f"{self.request_end_time - self.request_start_time:.2f}s"
        else:
            duration = "N/A"

        intervals_str = (
            ", ".join(f"{i:.2f}s" for i in self.intervals) if self.intervals else "N/A"
        )
        jitters_str = (
            ", ".join(f"{j:.2f}" for j in self.jitters) if self.jitters else "N/A"
        )
        lines = [
            "Tracer Summary:",
            f"  Traced Algorithm: {self.traced_algo if self.traced_algo else 'N/A'}",
            f"  Request Duration: {duration}",
            f"  Initial Interval: {self.init_interval:.2f}s",
            f"  Intervals: {intervals_str}",
            f"  Jitters: {jitters_str}",
            f"  Max Interval: {self.max_interval if self.max_interval else 'N/A'}",
            f"  Total Tries: {self.tries}",
            f"  Timeout: {self.timeout}s",
            f"  Success: {'Yes' if self.success else 'No'}",
            f"  Approx. Base Duration: {self.approx_base_duration if self.approx_base_duration else 'N/A'}",
        ]

        return "\n".join(lines)

    def get_report(self):
        if self.traced_algo:
            return str(self)
        else:
            return "not traced yet"
