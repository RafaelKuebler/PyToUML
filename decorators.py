import logging
import functools


def log_exception(func):
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        value = None
        try:
            value = func(*args, **kwargs)
        except Exception:
            logging.error(f"Could not process node in {func.__name__}")
        return value
    return wrapper_decorator
