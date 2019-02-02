"""
Decorator library for code performance and efficiency measurements.
"""

import functools
import time

class _Profile:
    def __init__(self, func, stats=None):
        functools.update_wrapper(self, func)
        self.func = func
        self.num_calls = 0
        self.stats = stats
        
    def __call__(self, *args, **kwargs):
        self.num_calls += 1
        start_time = time.perf_counter()
        ret_values = self.func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        self.stats.append([self.func.__name__, run_time])
        return ret_values

def Profile(stats=None):
    def wrapper_Profile(func):
        return _Profile(func, stats)
    return wrapper_Profile
