from __future__ import annotations

from typing import Dict, List, Tuple, Callable

from ._graph import Graph


class Node:
    def __init__(self, graph: Graph, name: str, node_type: str, input_nodes: Tuple[Node, ...]):
        self.graph = graph
        self.name = name
        self.node_type = node_type

        # other nodes use this node (user in torch.fx)
        self._output_nodes: Dict[Node, None] = {}

        # this node use other nodes
        # build connection: other_nodes -> this_node._input_nodes
        self._input_nodes: Dict[Node, None] = {node: None for node in input_nodes}

        # build connection: other_nodes._output_nodes -> this node
        for new_use in self._input_nodes.keys():
            new_use._output_nodes.setdefault(self)

        # use doubly linked list to store all nodes
        # note: graph relation is stored in _input_nodes and _output_nodes
        self._prev = self
        self._next = self
        self._erased = False

    @property
    def next(self) -> Node:
        return self._next

    @property
    def prev(self) -> Node:
        return self._prev

    def prepend(self, x: Node) -> None:
        assert self.graph == x.graph, "Attempting to move a Node into a different Graph"
        if self == x:
            return

        x._remove_from_list()
        p = self._prev
        p._next, x._prev = x, p
        x._next, self._prev = self, x

    def append(self, x: Node) -> None:
        self._next.prepend(x)

    def _remove_from_list(self) -> None:
        p, n = self._prev, self._next
        p._next, n._prev = n, p

    @property
    def all_input_nodes(self) -> List[Node]:
        return list(self._input_nodes)

    @property
    def all_output_nodes(self) -> List[Node]:
        return list(self._output_nodes)

    def replace_all_uses_with(self, replace_with: Node,
                              delete_user_cb: Callable[[Node], bool] = lambda user: True, ) -> List[Node]:
        # Replace all nodes use self with new node, make them use new node
        # connection: self -> output_nodes ==> new_node -> output_nodes
        # Return all changed nodes.
        # like torch.fx.node.replace_all_uses_with
        to_process = list(self._output_nodes)
        skipped = []

        for use_node in to_process:
            # new_input_nodes: Dict[Node, None] = {}
            # for node in use_node.all_input_nodes:
            #     if node != self:
            #         new_input_nodes.setdefault(node)
            #     else:
            #         new_input_nodes.setdefault(replace_with)
            # use_node.__update_input_nodes(list(new_input_nodes))
            if not delete_user_cb(use_node):
                skipped.append(use_node)
                continue

            new_input_nodes = use_node._input_nodes
            new_input_nodes.pop(self)
            new_input_nodes.setdefault(replace_with)

            use_node.__update_input_nodes(list(new_input_nodes))

        return [node for node in to_process if node not in skipped]

    def insert_node_after_with(self, append_with: Node):
        """
        insert a node after self in the graph
        self -> self_users to  self -> inserted_node -> self_users
        """
        self.replace_all_uses_with(append_with, lambda user: True if user is not append_with else False)
        append_with.__update_input_nodes([self])

    def replace_input_with(self, old_input: Node, new_input: Node) -> None:
        # replace ''old_input'' node in self._input_nodes with ''new_input'' node
        # like torch.fx.node.replace_input_with

        # new_input_nodes: Dict[Node, None] = {}
        #
        # for node in self._input_nodes.keys():
        #     if node == old_input:
        #         new_input_nodes.setdefault(new_input)
        #     else:
        #         new_input_nodes.setdefault(node)
        #
        # self._input_nodes = new_input_nodes

        new_input_nodes = self._input_nodes
        new_input_nodes.pop(old_input)
        new_input_nodes.setdefault(new_input)

        self.__update_input_nodes(list(new_input_nodes))

    def set_all_input_nodes_with(self, new_input_nodes: List[Node]):
        # change all input nodes
        # for node in self._input_nodes:
        #     # remove old input nodes
        #     node._output_nodes.pop(self)
        #     self._input_nodes.pop(node)
        #
        # for new_node in new_input_nodes:
        #     self._input_nodes.setdefault(new_node)
        #     new_node._output_nodes.setdefault(self)
        self.__update_input_nodes(new_input_nodes)

    def __update_input_nodes(self, new_input_nodes: List[Node]):
        for old_input_node in self._input_nodes:
            old_input_node._output_nodes.pop(self)

        self._input_nodes = {}
        for new_input_node in new_input_nodes:
            self._input_nodes.setdefault(new_input_node)
            new_input_node._output_nodes.setdefault(self)

    # def add_input_node(self, new_input_node: Node):
    #     new_input_node._output_nodes.setdefault(self)
    #     self._input_nodes.setdefault(new_input_node)
    #
    # def add_output_node(self, new_output_node: Node):
    #     new_output_node._input_nodes.setdefault(self)
    #     self._output_nodes.setdefault(new_output_node)
    #
    # def remove_input_node(self, to_remove_input_node: Node):
    #     to_remove_input_node._output_nodes.pop(self)
    #     self._input_nodes.pop(to_remove_input_node)
    #
    # def remove_output_node(self, to_remove_output_node: Node):
    #     to_remove_output_node._input_nodes.pop(self)
    #     self._output_nodes.pop(to_remove_output_node)
