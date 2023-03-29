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

    def run_input(self, val: int | float, truth_table: dict[str, dict[str, bool]]) -> dict[str, dict[str, bool]]:
        input_str = format(val, 'b')  # Binary format. Outputs the number in base 2
        while len(input_str) < self.input_num:
            input_str = "0" + input_str

        # se nella truth table non c'è una voce corrispondente (riga specifica della tabella di verità), la crea
        # es.: ttable = {}. Non c'è 0000. Allora faccio inserimento e ttable diventa {'0000': {}}
        if not hasattr(truth_table, input_str):
            truth_table[input_str] = {}

        # assegna i valori alle foglie (variabili input),
        # in base al loro varole nella stringa che identifica la riga della truth table
        # - input_str[idx]: valore attuale variabile (0 o 1)
        # - node_id: identificativo variabile (es.: x0)
        for idx, node_id in enumerate(self.leaves):
            self.nodes[node_id].set_value(bool(int(input_str[idx])))

        # calcola i valori finali di output per tutte le variabili in output
        # truth_table[input_str][out]: risultato (True o False)
        for out in self.roots:
            # in caso di singolo output nodes[out] è il nodo y0
            truth_table[input_str][out] = self.nodes[out].run(self.nodes)

        return truth_table
