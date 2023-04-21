from node import Node


class Graph:
    """
    Represents the whole graph.
    """
    def __init__(self, leaves: list[str], internal_nodes: list[str], roots: list[str], nodes: dict[str, Node]):
        """Initializes graph attributes

        Parameters
        ---------------
        leaves: list[str],
            A list of leaves identifiers
        internal_nodes: list[str],
            A list of gate nodes identifiers
        roots: list[str],
            A list of roots identifiers
        nodes: dict[str, Node]
            A nodes dictionary. Key: node id; value: Node object
        """
        self.leaves = leaves
        self.internal_nodes = internal_nodes
        self.roots = roots
        self.nodes = nodes

    @property
    def input_num(self):
        """
        :return: Number of input variables.
        """
        return len(self.leaves)

    def set_change(self, node_id: str):
        """This function transforms AND in XNOR. In other words, it generates the error.

        Parameters
        -------------------------
        node_id: str,
            the identifier of the node whose operator will be transformed to generate the error.
        """
        # first, change op (it has only val 0/1 - xor/and)
        self.nodes[node_id].op = not self.nodes[node_id].op
        # to concretize XNOR, go to children and set current node as complemented (in parents attribute)
        for child in self.nodes[node_id].children:
            for parent in self.nodes[child].parents:
                if parent[0] == node_id:
                    parent[1] = not parent[1]

    def run_input(self, val: int | float, truth_table: dict[str, dict[str, bool]]) -> dict[str, dict[str, bool]]:
        """This function calculate for each entry in truth table, the output values of the graph

        Parameters
        -------------------
        val: int,
            the value corresponding to a truth table entry
        truth_table:  dict[str, dict[str, bool]]
            the original truth table

        Returns
        ------------------
        dict[str, dict[str, bool]]
            The modified truth table.
        """
        input_str = format(val, 'b')  # Binary format. Outputs the number in base 2
        while len(input_str) < self.input_num:
            input_str = "0" + input_str

        # In the truth table if there is not a corresponding entry (specific row), then create it
        # es.: ttable = {}. There is not 0000. So insert it into ttable, which becomes {'0000': {}}
        if not hasattr(truth_table, input_str):
            truth_table[input_str] = {}

        # assign leaves values (input variables),
        # On the basis of their value in string identifying truth table row
        # - input_str[idx]: current variable value (0 or 1)
        # - node_id: variable identifier (es.: x0)
        for idx, node_id in enumerate(self.leaves):
            self.nodes[node_id].set_value(bool(int(input_str[idx])))

        # Compute final output value for all output variables
        # truth_table[input_str][out]: results (True or False)
        for out in self.roots:
            # if single output, nodes[out] is node y0
            truth_table[input_str][out] = self.nodes[out].run(self.nodes)

        return truth_table
