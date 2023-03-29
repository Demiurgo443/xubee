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

    # L'operazione di cambio consiste nella trasformazione di AND in XNOR.
    def set_change(self, node_id: str):
        # innanzitutto cambio op (ha solo val 0 e 1 - xor e and)
        self.nodes[node_id].op = not self.nodes[node_id].op
        # per rendere effettivo lo XNOR, vado nei nodi figli (superiori) e faccio sì che
        # il nodo modificato entri loro negato
        for child in self.nodes[node_id].children:
            for parent in self.nodes[child].parents:
                if parent[0] == node_id:
                    parent[1] = not parent[1]
