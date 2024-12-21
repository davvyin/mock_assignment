from client import Client
from tracer import Tracer
from analysis import Analysis
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger(__name__)


def main():
    # start the experiment
    tracer = Tracer()  # this trace the algo for insert it into the client app
    analysis = Analysis()  # for doing the analysis
    my_client = Client(
        "http://127.0.0.1:5000/request", "http://127.0.0.1:5000/status", tracer
    )

    # the send_job(base_delay, var_delay, success_rate(irrelavent to this exp))
    cur_base_delay, cur_var_delay = 1.5, 0.9

    # the client side parameters
    init_interval, max_interval, timeout, jitter_scale, approx_base_duration = (
        0.1,
        3,
        float("inf"),
        (1, 1),
        1.5,
    )
    exp_times = 10
    i = 1
    # Testing
    while i <= exp_times:
        target = my_client.send_job(
            cur_base_delay, cur_var_delay, None
        )  # This to customize the job
        my_client.send_backoff_get_status(
            init_interval, max_interval, timeout, jitter_scale, approx_base_duration
        )
        analysis.add_entry(target, tracer)
        # print(tracer.get_report())
        logger.info(f"Exp number: {i}, Result: {tracer.get_report()}")
        i += 1

    print(analysis.get_report())


if __name__ == "__main__":
    main()
