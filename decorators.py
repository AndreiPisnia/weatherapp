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
