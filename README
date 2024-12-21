# Mock server & get status api

To see how everything works, simply run `demo.sh` (located in the project’s root directory).

## Poblem statement

HeyGen offers an AI-powered video translation feature that takes time to complete due to various factors, and I called this a "job". The task is to build a client library to query a simulated translation service’s status endpoint. This client should avoid naive constant calling and instead use some smarter strategies.

## Assumptions

1.
    Each job’s duration is approximately x ± rand(y) seconds, where:

    - x is the base duration.
    - rand(y) returns a random value in the range [0, y].
    - Because x > y, each job’s total duration is to be less than x + y, which is always less than 2x.

    For larger jobs, we assume they are split into multiple smaller jobs, each independently following the same time estimate of x ± rand(y) seconds.
2.
    No network/server side issues

## Define metrics

1. Hit Rate:
    - The porportion of API calls that return a final state (completed or error) relative to the total API calls
    - Formula: HR = # of api calls that return a final state / # of total api calls
    - Aim: Ensure the api call attempts are not wasted

2. Efficiency Ratio
    - Compares how quickly the client make the completion get status call to how long the job took to complete from the moment the client started polling.
    - Formula: ER = Completion Delay after the job done / Time to completion from client start
    - Aim: Lower the ER means the lower the delay

## Objective function definition

Since we have 2 metrics to evaluate our design, our target is the maximize the our objective functions which can be calculated as:

```latex
score = (w_i * HR) + (-w_j * ER)
```

Our aim is to maximize this score by increasing the Hit Rate and reducing the Efficiency Ratio.

## Implementation

1. Server: A mock server that simulates a job's status. It remains in a pending state for the configured time before returning completed or error.
2. Client:

- Initiates a translation job request using ```POST /request```.
- Implement different adaptive backoff (if known the job length approximation) with jitter integration
- Integrate a Tracer in the client to record the necessay data for conducting the performance analysis.

## How to use the client library

1. Install Dependencies
Make sure you have any required packages installed by running `pip install -r requirements.txt`
2. Import and Initialize
In your Python code, import the Client class and any other needed components, such as the Tracer, which records metrics for analysis
3. Call the `send_backoff_get_status` Method, and this method supports
    - exponential backoff
    - jitter (optional)
    - knowledge of the approximate job duration (optional)

Code snippet:

```python
from client import Client
from tracer import Tracer
# init the tracer
tracer = Tracer()
# init the client
my_client = Client("http://127.0.0.1:5000/request", "http://127.0.0.1:5000/status", tracer) 

# mock a job with base delay with variance
job = my_client.send_job(cur_base_delay, cur_var_delay, None)

# call the get status
final_status = my_client.send_backoff_get_status(
    initial_interval=1,
    max_interval=10,
    timeout=60,
    jitter_scale=(0.3, 0.3),         # (optional) Adds a +/- 30% random variation to the interval
    approx_base_duration=30   # (optional) Estimated job duration in seconds
)
```

## Integration Test & Experiment

In the integration test, we simulate a series of translation jobs and observe how the client library behaves under varying delays and other configurations.

Please refer the the `main.py` under the `/client` to learn how to use the client, tracer, and analysis modules together.

Here are the results from running the configuration:

```python

# The mock translation job parameters, unit is second
cur_base_delay, cur_var_delay = 1.5, 0.9

# The client side parameters
init_interval, max_interval, timeout, jitter_scale, approx_base_duration = (
    0.1,
    3,
    float("inf"),
    (1, 1),
    1.5,
)
... 
# Repeat for 10 trials
```

Result

```txt
Analysis report from 10 results
Average Delay: 
1.2638
Average tries: 
6.0
Average Hit rates: 
0.1667
Average Efficiency ratio: 
0.4007
```

## Conclusion

- Client Efficiency: By using backoff strategies (optionally with jitter and knowledge of approximate job duration), the client minimizes unproductive calling while still detecting job completion quickly.
- Metrics & Logging: With the Tracer and Analysis modules, it’s straightforward to gather data and visualize the trade-offs, helping users fine-tune their polling strategies for various conditions.

## Future works

1. Consider integrating machine learning or heuristic feedback loops to dynamically adjust polling intervals, aiming to maximize the combined score of Hit Rate and Efficiency Ratio.
2. Add graphical plots to the analysis tool to make data more accessible and highlight patterns visually.
