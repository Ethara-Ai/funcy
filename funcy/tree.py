from collections import deque
from .types import is_seqcont


__all__ = ['tree_leaves', 'ltree_leaves', 'tree_nodes', 'ltree_nodes']


def tree_leaves(root, follow=is_seqcont, children=iter):
    """Iterates over tree leaves."""
    pass

def ltree_leaves(root, follow=is_seqcont, children=iter):
    """Lists tree leaves."""
    pass


def tree_nodes(root, follow=is_seqcont, children=iter):
    """Iterates over all tree nodes."""
    pass

def ltree_nodes(root, follow=is_seqcont, children=iter):
    """Lists all tree nodes."""
    pass
