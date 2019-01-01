import time

def one_moment(func):
    """Stop running function for 1 second. """
    def wrapper(*args, **kwargs):
        time.sleep(5)
        print('use sleep functon for 1 second')
        return func(*args, **kwargs)
    return wrapper
