from node import Node
from graph import Graph


def parser(file_name: str) -> tuple[Graph, list[str]]:

    input_list = []
    internal_list = []
    output_list = []
    node_list = {}
    interest_list = []

    with open(file_name, 'r') as file:
        for line in file:
            line = line.strip().removesuffix(";")

            if line.startswith("input"):
                # same as removeprefix() without if checks and function call
                node_ids = line[len("input "):].split(", ")
                input_list = node_ids
                for idx in range(len(node_ids)):
                    # scorre vari nodi input, crea dei corrispettivi con classe Nodo e li aggiunge al dizionario nodi
                    node_list[node_ids[idx]] = Node(node_ids[idx])

            elif line.startswith("output"):
                node_ids = line[len("output "):].split(", ")
                output_list = node_ids
                for idx in range(len(node_ids)):
                    node_list[node_ids[idx]] = Node(node_ids[idx])

            elif line.startswith("wire"):
                node_ids = line[len("wire "):].split(", ")
                internal_list = node_ids
                for idx in range(len(node_ids)):
                    node_list[node_ids[idx]] = Node(node_ids[idx])

            elif line.startswith("assign"):
                line = line[len("assign "):].split(" = ")
                node_id = line[0]
                formula = line[1].split(" ")
                # se formula è costituita da un solo elemento:
                # 1) si capisce se sia negato
                # 2) si segna il nodo coinvolto come figlio del nodo della formula (es.: y0 = n35 -> n35.child = y0)
                if len(formula) == 1:
                    has_not = formula[0].count("~")
                    parent_node = formula[0].removeprefix("~")
                    node_list[parent_node].add_child(node_id)
                    node_list[node_id].set_operation([parent_node, has_not])
                    if parent_node.startswith("x"):
                        print("Si è verificato il caso limite in cui un nodo radice (output) "
                              "ha come unico figlio un nodo foglia (input)")
                        node_list[node_id].add_leaves({parent_node})
                    else:
                        node_list[node_id].add_leaves(node_list[parent_node].leaves)
                else:
                    parent1_has_not = formula[0].count("~")
                    parent1 = formula[0].removeprefix("~")
                    if parent1.startswith("x"):
                        node_list[node_id].add_leaves({parent1})
                    else:
                        node_list[node_id].add_leaves(node_list[parent1].leaves)

                    parent2_has_not = formula[2].count("~")
                    parent2 = formula[2].removeprefix("~")
                    if parent2.startswith("x"):
                        node_list[node_id].add_leaves({parent2})
                    else:
                        node_list[node_id].add_leaves(node_list[parent2].leaves)

                    # Dato il nodo attuale, lo segno ai suoi genitori come figlio
                    node_list[parent1].add_child(node_id)
                    node_list[parent2].add_child(node_id)

                    node_list[node_id].set_operation(
                        [[parent1, parent1_has_not], [parent2, parent2_has_not]], int(formula[1] == "&"))

                    # i nodi scelti per la generazione dell'errore saranno solo quelli aventi come genitori due foglie
                    if parent1.startswith("x") and parent2.startswith("x"):
                        interest_list.append(node_id)

        # dei nodi di interesse del primo layer, si vanno a escludere quelli che sono XOR
        # quelli che hanno più di un figlio e che sono AND
        # o s
        start_length = len(interest_list)
        for i in range(start_length):
            if node_list[interest_list[start_length - i - 1]].op == 0:
                interest_list.remove(interest_list[start_length - i - 1])
            elif (len(node_list[interest_list[start_length-i-1]].children) != 1) and \
                    (node_list[interest_list[start_length-i-1]].op == 1):
                interest_list.remove(interest_list[start_length-i-1])

    return Graph(input_list, internal_list, output_list, node_list), interest_list
