from operator import __not__
from functools import partial, reduce, wraps

from ._inspect import get_spec, Spec
from .primitives import EMPTY
from .funcmakers import make_func, make_pred


__all__ = ['identity', 'constantly', 'caller',
           # reexport functools for convenience
           'reduce', 'partial',
           'rpartial', 'func_partial',
           'curry', 'rcurry', 'autocurry',
           'iffy',
           'compose', 'rcompose', 'complement', 'juxt', 'ljuxt']


def identity(x):
    """Returns its argument."""
    pass

def constantly(x):
    """Creates a function accepting any args, but always returning x."""
    pass

# an operator.methodcaller() brother
def caller(*a, **kw):
    """Creates a function calling its sole argument with given *a, **kw."""
    pass

def func_partial(func, *args, **kwargs):
    """A functools.partial alternative, which returns a real function.
       Can be used to construct methods."""
    pass

def rpartial(func, *args, **kwargs):
    """Partially applies last arguments.
       New keyworded arguments extend and override kwargs."""
    pass


def curry(func, n=EMPTY):
    """Curries func into a chain of one argument functions."""
    pass


def rcurry(func, n=EMPTY):
    """Curries func into a chain of one argument functions.
       Arguments are passed from right to left."""
    pass


def autocurry(func, n=EMPTY, _spec=None, _args=(), _kwargs={}):
    """Creates a version of func returning its partial applications
       until sufficient arguments are passed."""
    pass


def iffy(pred, action=EMPTY, default=identity):
    """Creates a function, which conditionally applies action or default."""
    pass


def compose(*fs):
    """Composes passed functions."""
    if fs:
        pair = lambda f, g: lambda *a, **kw: f(g(*a, **kw))
        return reduce(pair, map(make_func, fs))
    else:
        return identity

def rcompose(*fs):
    """Composes functions, calling them from left to right."""
    pass

def complement(pred):
    """Constructs a complementary predicate."""
    pass


# NOTE: using lazy map in these two will result in empty list/iterator
#       from all calls to i?juxt result since map iterator will be depleted

def ljuxt(*fs):
    """Constructs a juxtaposition of the given functions.
       Result returns a list of results of fs."""
    pass

def juxt(*fs):
    """Constructs a lazy juxtaposition of the given functions.
       Result returns an iterator of results of fs."""
    pass
