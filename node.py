class Node:
    def __init__(self, id: str):
        self.id = id
        self.op: int  # 0=xor - 1=and
        self.value: bool
        self.parents: list[list[str, int]] | list[str, int] # [[id, not], ...]  not -> 0 = normale - 1 = esegue il not
        self.children = []  # per children si intende nodi "superiori" al nodo corrente, quindi più vicini alla radice
        self.leaves = set()

    def add_child(self, child: str):
        self.children.append(child)

    # specifica tutti i nodi variabile coinvolti direttamente e indirettamente dal nodo
    def add_leaves(self, leaves: set):
        self.leaves.update(leaves)

    def set_value(self, value: bool):  # cambio valore per nodi foglia
        self.value = value

    def set_operation(self, parents, op=None):
        self.op = op
        self.parents = parents

    def run(self, node_list: dict) -> bool:
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
