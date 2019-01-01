import time

def one_moment(func):
    """Stop running function for 1 second. """
    def wrapper(*args, **kwargs):
        time.sleep(5)
        print('use sleep functon for 1 second')
        return func(*args, **kwargs)
    return wrapper


def slow_down(sec=1):
    def one_moment(func):
        """Stop running function for given amount of seconds. """
        def wrapper(*args, **kwargs):
            print(f'use slow_running functon for {sec} seconds')            
            time.sleep(sec)
            return func(*args, **kwargs)
        return wrapper
    return one_moment


def timer(func):
    """Print the runtime of the decorated function"""
    def wrapper(*args, **kwargs):
        print('-' * 20)
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        run_time = time.perf_counter() - start_time
        print(f"finished running {func.__name__!r} in {run_time:.4f} seconds")
        return result
    return wrapper
