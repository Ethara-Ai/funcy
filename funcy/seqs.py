import sys
from itertools import islice, chain, tee, groupby, filterfalse, accumulate, \
                      takewhile as _takewhile, dropwhile as _dropwhile
from collections.abc import Sequence
from collections import defaultdict, deque
import operator

from .primitives import EMPTY
from .types import is_seqcont
from .funcmakers import make_func, make_pred


__all__ = [
    'count', 'cycle', 'repeat', 'repeatedly', 'iterate',
    'take', 'drop', 'first', 'second', 'nth', 'last', 'rest', 'butlast', 'ilen',
    'map', 'filter', 'lmap', 'lfilter', 'remove', 'lremove', 'keep', 'lkeep', 'without', 'lwithout',
    'concat', 'lconcat', 'chain', 'cat', 'lcat', 'flatten', 'lflatten', 'mapcat', 'lmapcat',
    'interleave', 'interpose', 'distinct', 'ldistinct',
    'dropwhile', 'takewhile', 'split', 'lsplit', 'split_at', 'lsplit_at', 'split_by', 'lsplit_by',
    'group_by', 'group_by_keys', 'group_values', 'count_by', 'count_reps',
    'partition', 'lpartition', 'chunks', 'lchunks', 'partition_by', 'lpartition_by',
    'with_prev', 'with_next', 'pairwise', 'lzip',
    'reductions', 'lreductions', 'sums', 'lsums', 'accumulate',
]

_map, _filter = map, filter

def _lmap(f, *seqs):
    return list(map(f, *seqs))

def _lfilter(f, seq):
    return list(filter(f, seq))


# Re-export
from itertools import count, cycle, repeat

def repeatedly(f, n=EMPTY):
    """Takes a function of no args, presumably with side effects,
       and returns an infinite (or length n) iterator of calls to it."""
    pass

def iterate(f, x):
    """Returns an infinite iterator of `x, f(x), f(f(x)), ...`"""
    pass


def take(n, seq):
    """Returns a list of first n items in the sequence,
       or all items if there are fewer than n."""
    pass

def drop(n, seq):
    """Skips first n items in the sequence, yields the rest."""
    pass

def first(seq):
    """Returns the first item in the sequence.
       Returns None if the sequence is empty."""
    pass

def second(seq):
    """Returns second item in the sequence.
       Returns None if there are less than two items in it."""
    pass

def nth(n, seq):
    """Returns nth item in the sequence or None if no such item exists."""
    pass

def last(seq):
    """Returns the last item in the sequence or iterator.
       Returns None if the sequence is empty."""
    pass

def rest(seq):
    """Skips first item in the sequence, yields the rest."""
    pass

def butlast(seq):
    """Iterates over all elements of the sequence but last."""
    pass

def ilen(seq):
    """Consumes an iterable not reading it into memory
       and returns the number of items."""
    pass


# TODO: tree-seq equivalent

def lmap(f, *seqs):
    """An extended version of builtin map() returning a list.
       Derives a mapper from string, int, slice, dict or set."""
    pass

def lfilter(pred, seq):
    """An extended version of builtin filter() returning a list.
       Derives a predicate from string, int, slice, dict or set."""
    pass

def map(f, *seqs):
    """An extended version of builtin map().
       Derives a mapper from string, int, slice, dict or set."""
    pass

def filter(pred, seq):
    """An extended version of builtin filter().
       Derives a predicate from string, int, slice, dict or set."""
    pass

def lremove(pred, seq):
    """Creates a list if items passing given predicate."""
    pass

def remove(pred, seq):
    """Iterates items passing given predicate."""
    pass

def lkeep(f, seq=EMPTY):
    """Maps seq with f and keeps only truthy results.
       Simply lists truthy values in one argument version."""
    pass

def keep(f, seq=EMPTY):
    """Maps seq with f and iterates truthy results.
       Simply iterates truthy values in one argument version."""
    pass

def without(seq, *items):
    """Iterates over sequence skipping items."""
    pass

def lwithout(seq, *items):
    """Removes items from sequence, preserves order."""
    pass


def lconcat(*seqs):
    """Concatenates several sequences."""
    pass
concat = chain

def lcat(seqs):
    """Concatenates the sequence of sequences."""
    return list(cat(seqs))
cat = chain.from_iterable

def flatten(seq, follow=is_seqcont):
    """Flattens arbitrary nested sequence.
       Unpacks an item if follow(item) is truthy."""
    pass

def lflatten(seq, follow=is_seqcont):
    """Iterates over arbitrary nested sequence.
       Dives into when follow(item) is truthy."""
    pass

def lmapcat(f, *seqs):
    """Maps given sequence(s) and concatenates the results."""
    pass

def mapcat(f, *seqs):
    """Maps given sequence(s) and chains the results."""
    pass

def interleave(*seqs):
    """Yields first item of each sequence, then second one and so on."""
    pass

def interpose(sep, seq):
    """Yields items of the sequence alternating with sep."""
    pass

def takewhile(pred, seq=EMPTY):
    """Yields sequence items until first predicate fail.
       Stops on first falsy value in one argument version."""
    pass

def dropwhile(pred, seq=EMPTY):
    """Skips the start of the sequence passing pred (or just truthy),
       then iterates over the rest."""
    pass


def ldistinct(seq, key=EMPTY):
    """Removes duplicates from sequences, preserves order."""
    pass

def distinct(seq, key=EMPTY):
    """Iterates over sequence skipping duplicates"""
    pass


def split(pred, seq):
    """Lazily splits items which pass the predicate from the ones that don't.
       Returns a pair (passed, failed) of respective iterators."""
    pred = make_pred(pred)
    yes, no = deque(), deque()
    splitter = (yes.append(item) if pred(item) else no.append(item) for item in seq)

    def _split(q):
        while True:
            while q:
                yield q.popleft()
            try:
                next(splitter)
            except StopIteration:
                return

    return _split(yes), _split(no)

def lsplit(pred, seq):
    """Splits items which pass the predicate from the ones that don't.
       Returns a pair (passed, failed) of respective lists."""
    pass


def split_at(n, seq):
    """Lazily splits the sequence at given position,
       returning a pair of iterators over its start and tail."""
    pass

def lsplit_at(n, seq):
    """Splits the sequence at given position,
       returning a tuple of its start and tail."""
    pass

def split_by(pred, seq):
    """Lazily splits the start of the sequence,
       consisting of items passing pred, from the rest of it."""
    pass

def lsplit_by(pred, seq):
    """Splits the start of the sequence,
       consisting of items passing pred, from the rest of it."""
    pass


def group_by(f, seq):
    """Groups given sequence items into a mapping f(item) -> [item, ...]."""
    pass


def group_by_keys(get_keys, seq):
    """Groups items having multiple keys into a mapping key -> [item, ...].
       Item might be repeated under several keys."""
    pass


def group_values(seq):
    """Takes a sequence of (key, value) pairs and groups values by keys."""
    pass


def count_by(f, seq):
    """Counts numbers of occurrences of values of f()
       on elements of given sequence."""
    pass


def count_reps(seq):
    """Counts number occurrences of each value in the sequence."""
    pass


# For efficiency we use separate implementation for cutting sequences (those capable of slicing)
def _cut_seq(drop_tail, n, step, seq):
    limit = len(seq)-n+1 if drop_tail else len(seq)
    return (seq[i:i+n] for i in range(0, limit, step))

def _cut_iter(drop_tail, n, step, seq):
    it = iter(seq)
    pool = take(n, it)
    while True:
        if len(pool) < n:
            break
        yield pool
        pool = pool[step:]
        pool.extend(islice(it, step))
    if not drop_tail:
        for item in _cut_seq(drop_tail, n, step, pool):
            yield item

def _cut(drop_tail, n, step, seq=EMPTY):
    if seq is EMPTY:
        step, seq = n, step
    if isinstance(seq, Sequence):
        return _cut_seq(drop_tail, n, step, seq)
    else:
        return _cut_iter(drop_tail, n, step, seq)

def partition(n, step, seq=EMPTY):
    """Lazily partitions seq into parts of length n.
       Skips step items between parts if passed. Non-fitting tail is ignored."""
    pass

def lpartition(n, step, seq=EMPTY):
    """Partitions seq into parts of length n.
       Skips step items between parts if passed. Non-fitting tail is ignored."""
    pass

def chunks(n, step, seq=EMPTY):
    """Lazily chunks seq into parts of length n or less.
       Skips step items between parts if passed."""
    pass

def lchunks(n, step, seq=EMPTY):
    """Chunks seq into parts of length n or less.
       Skips step items between parts if passed."""
    pass

def partition_by(f, seq):
    """Lazily partition seq into continuous chunks with constant value of f."""
    pass

def lpartition_by(f, seq):
    """Partition seq into continuous chunks with constant value of f."""
    pass


def with_prev(seq, fill=None):
    """Yields each item paired with its preceding: (item, prev)."""
    pass

def with_next(seq, fill=None):
    """Yields each item paired with its following: (item, next)."""
    pass

# An itertools recipe
# NOTE: this is the same as ipartition(2, 1, seq) only faster and with distinct name
def pairwise(seq):
    """Yields all pairs of neighboring items in seq."""
    pass

if sys.version_info >= (3, 10):
    def lzip(*seqs, strict=False):
        """List zip() version."""
        pass
else:
    def lzip(*seqs, strict=False):
        """List zip() version."""
        pass

    def _zip_strict(*seqs):
        try:
            # Try compare lens if they are available and use a fast zip() builtin
            len_1 = len(seqs[0])
            for i, s in enumerate(seqs, start=1):
                len_i = len(s)
                if len_i != len_1:
                    short_i, long_i = (1, i) if len_1 < len_i else (i, 1)
                    raise _zip_strict_error(short_i, long_i)
        except TypeError:
            return _zip_strict_iters(*seqs)
        else:
            return zip(*seqs)

    def _zip_strict_iters(*seqs):
        iters = [iter(s) for s in seqs]
        while True:
            values, stop_i, val_i = [], 0, 0
            for i, it in enumerate(iters, start=1):
                try:
                    values.append(next(it))
                    if not val_i:
                        val_i = i
                except StopIteration:
                    if not stop_i:
                        stop_i = i

            if stop_i:
                if val_i:
                    raise _zip_strict_error(stop_i, val_i)
                break
            yield tuple(values)

    def _zip_strict_error(short_i, long_i):
        if short_i == 1:
            return ValueError("zip() argument %d is longer than argument 1" % long_i)
        else:
            start = "argument 1" if short_i == 2 else "argument 1-%d" % (short_i - 1)
            return ValueError("zip() argument %d is shorter than %s" % (short_i, start))


def _reductions(f, seq, acc):
    last = acc
    for x in seq:
        last = f(last, x)
        yield last

def reductions(f, seq, acc=EMPTY):
    """Yields intermediate reductions of seq by f."""
    pass

def lreductions(f, seq, acc=EMPTY):
    """Lists intermediate reductions of seq by f."""
    pass

def sums(seq, acc=EMPTY):
    """Yields partial sums of seq."""
    pass

def lsums(seq, acc=EMPTY):
    """Lists partial sums of seq."""
    pass
