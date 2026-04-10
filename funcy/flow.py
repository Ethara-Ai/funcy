from collections.abc import Hashable
from datetime import datetime, timedelta
import time
import threading
from contextlib import suppress  # reexport

from .decorators import decorator, wraps, get_argnames, arggetter, contextmanager


__all__ = ['raiser', 'ignore', 'silent', 'suppress', 'nullcontext', 'reraise', 'retry', 'fallback',
           'limit_error_rate', 'ErrorRateExceeded', 'throttle',
           'post_processing', 'collecting', 'joining',
           'once', 'once_per', 'once_per_args',
           'wrap_with']


### Error handling utilities

def raiser(exception_or_class=Exception, *args, **kwargs):
    """Constructs function that raises the given exception
       with given arguments on any invocation."""
    pass


# Not using @decorator here for speed,
# since @ignore and @silent should be used for very simple and fast functions
def ignore(errors, default=None):
    """Alters function to ignore given errors, returning default instead."""
    pass

def silent(func):
    """Alters function to ignore all exceptions."""
    pass


### Backport of Python 3.7 nullcontext
try:
    from contextlib import nullcontext
except ImportError:
    class nullcontext(object):
        """Context manager that does no additional processing.

        Used as a stand-in for a normal context manager, when a particular
        block of code is only sometimes used with a normal context manager:

        cm = optional_cm if condition else nullcontext()
        with cm:
            # Perform operation, using optional_cm if condition is True
        """

        def __init__(self, enter_result=None):
            self.enter_result = enter_result

        def __enter__(self):
            return self.enter_result

        def __exit__(self, *excinfo):
            pass


@contextmanager
def reraise(errors, into):
    """Reraises errors as other exception."""
    pass


@decorator
def retry(call, tries, errors=Exception, timeout=0, filter_errors=None):
    """Makes decorated function retry up to tries times.
       Retries only on specified errors.
       Sleeps timeout or timeout(attempt) seconds between tries."""
    pass


def fallback(*approaches):
    """Tries several approaches until one works.
       Each approach has a form of (callable, expected_errors)."""
    pass

def _ensure_exceptable(errors):
    """Ensures that errors are passable to except clause.
       I.e. should be BaseException subclass or a tuple."""
    pass


def _is_exception_type(value):
    return isinstance(value, type) and issubclass(value, BaseException)


class ErrorRateExceeded(Exception):
    pass

def limit_error_rate(fails, timeout, exception=ErrorRateExceeded):
    """If function fails to complete fails times in a row,
       calls to it will be intercepted for timeout with exception raised instead."""
    pass


def throttle(period):
    """Allows only one run in a period, the rest is skipped"""
    pass


### Post processing decorators

@decorator
def post_processing(call, func):
    """Post processes decorated function result with func."""
    return func(call())

collecting = post_processing(list)
collecting.__name__ = 'collecting'
collecting.__doc__ = "Transforms a generator into list returning function."

@decorator
def joining(call, sep):
    """Joins decorated function results with sep."""
    pass


### Initialization helpers

def once_per(*argnames):
    """Call function only once for every combination of the given arguments."""
    def once(func):
        lock = threading.Lock()
        done_set = set()
        done_list = list()

        get_arg = arggetter(func)

        @wraps(func)
        def wrapper(*args, **kwargs):
            with lock:
                values = tuple(get_arg(name, args, kwargs) for name in argnames)
                if isinstance(values, Hashable):
                    done, add = done_set, done_set.add
                else:
                    done, add = done_list, done_list.append

                if values not in done:
                    add(values)
                    return func(*args, **kwargs)
        return wrapper
    return once

once = once_per()
once.__doc__ = "Let function execute once, noop all subsequent calls."

def once_per_args(func):
    """Call function once for every combination of values of its arguments."""
    pass


@decorator
def wrap_with(call, ctx):
    """Turn context manager into a decorator"""
    pass
