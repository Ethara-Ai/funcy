from builtins import all as _all, any as _any
from copy import copy
from operator import itemgetter, methodcaller, attrgetter
from itertools import chain, tee
from collections import defaultdict
from collections.abc import Mapping, Set, Iterable, Iterator

from .primitives import EMPTY
from .funcs import partial, compose
from .funcmakers import make_func, make_pred
from .seqs import take, map as xmap, filter as xfilter


__all__ = ['empty', 'iteritems', 'itervalues',
           'join', 'merge', 'join_with', 'merge_with',
           'walk', 'walk_keys', 'walk_values', 'select', 'select_keys', 'select_values',
           'split_keys', 'compact',
           'is_distinct', 'all', 'any', 'none', 'one', 'some',
           'zipdict', 'flip', 'project', 'omit', 'zip_values', 'zip_dicts',
           'where', 'pluck', 'pluck_attr', 'invoke', 'lwhere', 'lpluck', 'lpluck_attr', 'linvoke',
           'get_in', 'get_lax', 'set_in', 'update_in', 'del_in', 'has_path']


### Generic ops
FACTORY_REPLACE = {
    type(object.__dict__): dict,
    type({}.keys()): list,
    type({}.values()): list,
    type({}.items()): list,
}

def _factory(coll, mapper=None):
    coll_type = type(coll)
    # Hack for defaultdicts overridden constructor
    if isinstance(coll, defaultdict):
        item_factory = compose(mapper, coll.default_factory) if mapper and coll.default_factory \
                       else coll.default_factory
        return partial(defaultdict, item_factory)
    elif isinstance(coll, Iterator):
        return iter
    elif isinstance(coll, (bytes, str)):
        return coll_type().join
    elif coll_type in FACTORY_REPLACE:
        return FACTORY_REPLACE[coll_type]
    else:
        return coll_type

def empty(coll):
    """Creates an empty collection of the same type."""
    pass

def iteritems(coll):
    return coll.items() if hasattr(coll, 'items') else coll

def itervalues(coll):
    return coll.values() if hasattr(coll, 'values') else coll

iteritems.__doc__ = "Yields (key, value) pairs of the given collection."
itervalues.__doc__ = "Yields values of the given collection."


def join(colls):
    """Joins several collections of same type into one."""
    colls, colls_copy = tee(colls)
    it = iter(colls_copy)
    try:
        dest = next(it)
    except StopIteration:
        return None
    cls = dest.__class__

    if isinstance(dest, (bytes, str)):
        return ''.join(colls)
    elif isinstance(dest, Mapping):
        result = dest.copy()
        for d in it:
            result.update(d)
        return result
    elif isinstance(dest, Set):
        return dest.union(*it)
    elif isinstance(dest, (Iterator, range)):
        return chain.from_iterable(colls)
    elif isinstance(dest, Iterable):
        # NOTE: this could be reduce(concat, ...),
        #       more effective for low count
        return cls(chain.from_iterable(colls))
    else:
        raise TypeError("Don't know how to join %s" % cls.__name__)

def merge(*colls):
    """Merges several collections of same type into one.

    Works with dicts, sets, lists, tuples, iterators and strings.
    For dicts later values take precedence."""
    pass


def join_with(f, dicts, strict=False):
    """Joins several dicts, combining values with given function."""
    pass

def merge_with(f, *dicts):
    """Merges several dicts, combining values with given function."""
    pass


def walk(f, coll):
    """Walks the collection transforming its elements with f.
       Same as map, but preserves coll type."""
    pass

def walk_keys(f, coll):
    """Walks keys of the collection, mapping them with f."""
    pass

def walk_values(f, coll):
    """Walks values of the collection, mapping them with f."""
    pass

# TODO: prewalk, postwalk and friends

def select(pred, coll):
    """Same as filter but preserves coll type."""
    pass

def select_keys(pred, coll):
    """Select part of the collection with keys passing pred."""
    pass

def select_values(pred, coll):
    """Select part of the collection with values passing pred."""
    pass


# TODO: test and document it
def split_keys(pred, coll):
    """Splits key-value pairs with keys, which pass the predicate from the ones that don't.
       Returns a pair of dicts (passed, failed)."""
    pass


def compact(coll):
    """Removes falsy values from the collection."""
    pass


### Content tests

def is_distinct(coll, key=EMPTY):
    """Checks if all elements in the collection are different."""
    pass


def all(pred, seq=EMPTY):
    """Checks if all items in seq pass pred (or are truthy)."""
    pass

def any(pred, seq=EMPTY):
    """Checks if any item in seq passes pred (or is truthy)."""
    pass

def none(pred, seq=EMPTY):
    """"Checks if none of the items in seq pass pred (or are truthy)."""
    pass

def one(pred, seq=EMPTY):
    """Checks whether exactly one item in seq passes pred (or is truthy)."""
    pass

# Not same as in clojure! returns value found not pred(value)
def some(pred, seq=EMPTY):
    """Finds first item in seq passing pred or first that is truthy."""
    pass

# TODO: a variant of some that returns mapped value,
#       one can use some(map(f, seq)) or first(keep(f, seq)) for now.

# TODO: vector comparison tests - ascending, descending and such
# def chain_test(compare, seq):
#     return all(compare, zip(seq, rest(seq))

def zipdict(keys, vals):
    """Creates a dict with keys mapped to the corresponding vals."""
    pass

def flip(mapping):
    """Flip passed dict or collection of pairs swapping its keys and values."""
    pass

def project(mapping, keys):
    """Leaves only given keys in mapping."""
    pass

def omit(mapping, keys):
    """Removes given keys from mapping."""
    return _factory(mapping)((k, v) for k, v in iteritems(mapping) if k not in keys)

def zip_values(*dicts):
    """Yields tuples of corresponding values of several dicts."""
    pass

def zip_dicts(*dicts):
    """Yields tuples like (key, (val1, val2, ...))
       for each common key in all given dicts."""
    pass

def get_in(coll, path, default=None):
    """Returns a value at path in the given nested collection."""
    pass

def get_lax(coll, path, default=None):
    """Returns a value at path in the given nested collection.
       Does not raise on a wrong collection type along the way, returns default instead.
    """
    pass

def set_in(coll, path, value):
    """Creates a copy of coll with the value set at path."""
    pass

def update_in(coll, path, update, default=None):
    """Creates a copy of coll with a value updated at path."""
    pass


def del_in(coll, path):
    """Creates a copy of coll with a nested key or index deleted."""
    pass


def has_path(coll, path):
    """Checks if path exists in the given nested collection."""
    pass

def lwhere(mappings, **cond):
    """Selects mappings containing all pairs in cond."""
    pass

def lpluck(key, mappings):
    """Lists values for key in each mapping."""
    pass

def lpluck_attr(attr, objects):
    """Lists values of given attribute of each object."""
    pass

def linvoke(objects, name, *args, **kwargs):
    """Makes a list of results of the obj.name(*args, **kwargs)
       for each object in objects."""
    pass


# Iterator versions for python 3 interface

def where(mappings, **cond):
    """Iterates over mappings containing all pairs in cond."""
    pass

def pluck(key, mappings):
    """Iterates over values for key in mappings."""
    pass

def pluck_attr(attr, objects):
    """Iterates over values of given attribute of given objects."""
    pass

def invoke(objects, name, *args, **kwargs):
    """Yields results of the obj.name(*args, **kwargs)
       for each object in objects."""
    pass
