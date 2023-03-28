from node import Node


class Graph:
    def __init__(self, leaves: list[str], internal_node: list[str], roots: list[str], nodes: dict[str, Node]):
        self.leaves = leaves
        self.internal_node = internal_node
        self.roots = roots
        self.nodes = nodes

    @property
    def input_num(self):
        return len(self.leaves)
