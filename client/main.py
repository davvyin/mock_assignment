from client import Client
from tracer import Tracer
from analysis import Analysis


def get_request_delay(target: dict, tracer: Tracer):
    if not tracer.request_end_time:
        # the request still pending
        return float("inf")
    if tracer.request_start_time >= target["end_time"]:
        # the get request is issued after the translation request finished
        return 0
    return tracer.request_end_time - target["end_time"]


def main():
    # start the experiment
    tracer = Tracer()  # this trace the algo for insert it into the client app
    analysis = Analysis()  # for doing the analysis
    my_client = Client(
        "http://127.0.0.1:5000/request", "http://127.0.0.1:5000/status", tracer
    )

    # the send_request(base_delay, var_delay, success_rate(irrelavent to this exp))
    cur_base_delay, cur_var_delay = 1, 5
    init_interval, max_interval, timeout = 1, 10, float("inf")
    exp_times = 10
    while exp_times > 0:
        target = my_client.send_request(cur_base_delay, cur_var_delay, None)
        my_client.send_backoff_get_status(init_interval, max_interval, timeout)
        analysis.add_entry(target, tracer)
        exp_times -= 1

    print(analysis.average_delay())
    print(analysis.average_tries())


if __name__ == "__main__":
    main()
