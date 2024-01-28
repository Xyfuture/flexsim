from __future__ import annotations
from typing import Dict, Optional

from ._node import Node


class _NodeList:
    def __init__(self, graph: Graph, direction: str = '_next'):
        assert direction in ['_next', '_prev']
        self.graph = graph
        self.direction = direction

    def __len__(self):
        return self.graph._len

    def __iter__(self):
        root, direction = self.graph._root, self.direction
        cur = getattr(root, direction)
        while cur is not root:
            if not cur._erased:
                yield cur
            cur = getattr(cur, direction)

    def __reversed__(self):
        return _NodeList(self.graph, '_next' if self.direction == '_prev' else '_prev')


class _InsertPoint:
    def __init__(self, graph: Graph, new_insert):
        self.graph = graph
        # functions
        self.origin_insert, graph._insert = graph._insert, new_insert

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.graph._insert = self.origin_insert


class Graph:
    def __init__(self):
        self._root: Node = Node(self, '', 'root', ())
        self._used_names: Dict[str, int] = {}

        # function, always insert before root
        self._insert = self._root.prepend

        self._len = 0

    @property
    def nodes(self) -> _NodeList:
        return _NodeList(self, '_next')

    def add_node(self, n: Node) -> Node:
        self._insert(n)
        self._len += 1
        return n

    def erase_node(self, n: Node) -> None:
        if len(n.all_output_nodes) > 0:
            raise RuntimeError(f"Node still has users {n.all_output_nodes}")

        if n._erased:
            return

        n._remove_from_list()
        n._erased = True
        self._len -= 1

        n._input_nodes = {}

    def insert_before(self, n: Optional[Node] = None):
        if n is None:
            return self.insert_after(self._root)

        assert n.graph == self

        return _InsertPoint(self, n.prepend)

    def insert_after(self, n: Optional[Node] = None):
        if n is None:
            return self.insert_before(self._root)

        assert n.graph == self

        return _InsertPoint(self, n.append)
