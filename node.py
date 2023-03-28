class Node:
    def __init__(self, id: str):
        self.id = id
        self.op: int  # 0=xor - 1=and
        self.value: bool
        self.parents: list[list[str, int]] | list[str, int] # [[id, not], ...]  not -> 0 = normale - 1 = esegue il not
        self.children = []  # per children si intende nodi "superiori" al nodo corrente, quindi più vicini alla radice
        self.leaves = set()
