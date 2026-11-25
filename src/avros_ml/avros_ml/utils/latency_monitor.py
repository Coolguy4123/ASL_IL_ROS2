# utils/latency_monitor.py
#
# A stopwatch every node can use to answer "where does the time go?".
#
#   with monitor.stage("infer"):      # times a block with a monotonic clock
#       result = model(frame)
#   monitor.record_age("input", msg.header.stamp, node.get_clock().now())
#
# It keeps the last few hundred samples per stage and reports p50 / p95 / p99 / max.
# Later it will publish those numbers once per second on /avros/metrics
# (diagnostic_msgs/DiagnosticArray) and optionally write a CSV for offline plots.
#
# IMPORTANT for GPU code: CUDA is asynchronous. Call torch.cuda.synchronize() (or sync the
# TensorRT stream) INSIDE the timed block, otherwise you only measure the launch time.

import time
from collections import defaultdict, deque
from contextlib import contextmanager

import numpy as np


class LatencyMonitor:
    def __init__(self, node_name, window=300):
        self.node_name = node_name
        self._samples = defaultdict(lambda: deque(maxlen=window))

    @contextmanager
    def stage(self, name):
        t0 = time.perf_counter()
        try:
            yield
        finally:
            self._samples[name].append((time.perf_counter() - t0) * 1000.0)  # milliseconds

    def record_ms(self, name, value_ms):
        self._samples[name].append(float(value_ms))

    def record_age(self, name, header_stamp, now):
        """Age of a message = now - its header stamp (ROS time). Needs a trustworthy camera clock."""
        age_ms = (now.nanoseconds - (header_stamp.sec * 10**9 + header_stamp.nanosec)) / 1e6
        self.record_ms(name + "_age", age_ms)

    def summary(self):
        """{stage: {p50, p95, p99, max, n}} in milliseconds."""
        out = {}
        for name, values in self._samples.items():
            if values:
                a = np.asarray(values)
                out[name] = {
                    "p50": float(np.percentile(a, 50)),
                    "p95": float(np.percentile(a, 95)),
                    "p99": float(np.percentile(a, 99)),
                    "max": float(a.max()),
                    "n": int(a.size),
                }
        return out

    # TODO: add attach(node, topic="/avros/metrics", period_s=1.0) to publish summary() as diagnostics.
