class Node:
    """Represents the single node entity."""
    def __init__(self, id: str):
        """Receives node identifier and initializes node attributes.

        Parameters
        ----------
        id: str
            A string that represent the node identifier.
        """
        self.id = id
        self.op: int  # 0 = xor  -  1 = and
        self.value: bool
        self.parents: list[list[str, int]] | list[str, int]  # [[id, not], ...]  not -> 0 = normal - 1 = exec. not
        self.children = []  # children are "upper" nodes compared to the current one, so they are closer to root
        self.leaves = set()

    def add_child(self, child: str):
        """Appends a child to a children list.

        Parameters
        ----------
        child: str
            Node identifier of the child.
        """
        self.children.append(child)

    def add_leaves(self, leaves: set):
        """Stores all input variables involved directly or indirectly in the current node.

        Parameters
        ----------
        leaves: set
            A set of leaves id
        """
        self.leaves.update(leaves)

    def set_value(self, value: bool):
        """Changes leaves value.

        Parameters
        ----------
        value: bool
            Current value of the leaf
        """
        self.value = value

    def set_operation(self, parents, op=None):
        """Sets operation and record node parents"""
        self.op = op
        self.parents = parents

    def run(self, node_list: dict) -> bool:
        """Compute value of current node.

        Parameters
        ----------
        node_list: dict
            The entire node dictionary.

        Returns
        --------
        bool
            The boolean value of current node.
        """
        if hasattr(self, "parents"):
            if self.op is not None:
                p1 = node_list[self.parents[0][0]].run(node_list)
                if self.parents[0][1]:
                    p1 = not p1
                p2 = node_list[self.parents[1][0]].run(node_list)
                if self.parents[1][1]:
                    p2 = (not p2)
                self.value = (p1 and p2) if self.op else (p1 ^ p2)
            else:
                self.value = (not node_list[self.parents[0]].run(node_list)) if self.parents[1] else node_list[
                    self.parents[0]].run(node_list)
        return self.value
