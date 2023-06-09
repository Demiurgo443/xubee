from node import Node
from graph import Graph
from time import perf_counter


def parser(file_name: str) -> tuple[Graph, list[str]]:
    """Parses verilog files and build the graph. It selects also nodes candidates for error generation."""
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
                    # iterate among input nodes, create corresponding ones with Node class and add them to node dict.
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
                # if formula has only one element:
                # 1) understand if it is complemented
                # 2) mark involved node as operator node child (ex.: y0 = n35 -> n35.child = y0)
                if len(formula) == 1:
                    has_not = formula[0].count("~")
                    parent_node = formula[0].removeprefix("~")
                    node_list[parent_node].add_child(node_id)
                    node_list[node_id].set_operation([parent_node, has_not])
                    if parent_node.startswith("x"):
                        print("Edge case: root (output) has a leaves (input) as child")
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

                    # Given the current node, mark it in its parents as child
                    node_list[parent1].add_child(node_id)
                    node_list[parent2].add_child(node_id)

                    node_list[node_id].set_operation(
                        [[parent1, parent1_has_not], [parent2, parent2_has_not]], int(formula[1] == "&"))

                    # chosen nodes for error estimation must have leaves as parents
                    if parent1.startswith("x") and parent2.startswith("x"):
                        interest_list.append(node_id)

        # exclude XOR from nodes of interest
        # exclude AND >1 children from nodes of interest
        start_length = len(interest_list)
        for i in range(start_length):
            if node_list[interest_list[start_length - i - 1]].op == 0:
                interest_list.remove(interest_list[start_length - i - 1])
            elif (len(node_list[interest_list[start_length-i-1]].children) != 1) and \
                    (node_list[interest_list[start_length-i-1]].op == 1):
                interest_list.remove(interest_list[start_length-i-1])

    return Graph(input_list, internal_list, output_list, node_list), interest_list


def visualizer():
    pass


def to_file(filename: str, xag, estimated_e_dict: dict, exact_e_dict: dict,
            f_elapsed_time: float, tt_elapsed_time: float):
    """Writes results in latex table ready format to file"""
    filename = filename.removesuffix(".v_opt.v").replace("_", "\\_")
    num_and_nodes = 0

    for and_node_id in xag.internal_nodes:
        if xag.nodes[and_node_id].op == 1:
            num_and_nodes += 1

    minval_estimated = min(estimated_e_dict.values())
    res = list(filter(lambda x: estimated_e_dict[x] == minval_estimated, estimated_e_dict))
    correspondence_eexact_found = []
    for el in res:
        value_found = [val for key, val in exact_e_dict.items() if key == el]
        correspondence_eexact_found.append(value_found[0])
    min_exact_error = min(correspondence_eexact_found)
    max_exact_error = max(correspondence_eexact_found)

    # SECOND TO LAST ROW -> when calculate timing, remember to insert & after \t. In normal way remove & and put \\\\\n
    with open("results.txt", "a") as f_res:
        table_row = f"{filename}\t& {len(estimated_e_dict)}\t& " \
                    f"{'{:.2f}'.format((len(estimated_e_dict) / len(xag.internal_nodes)) * 100)}\\%\t& " \
                    f"{minval_estimated}\t& " \
                    f"{min_exact_error}\t& {max_exact_error}\t& {minval_estimated - min_exact_error}\t& " \
                    f"{minval_estimated - max_exact_error}\t& {'{:.3f}'.format((1 / num_and_nodes) * 100)}\\%\t&  "\
                    f"{((f_elapsed_time-tt_elapsed_time)*1000):.2f}ms\t& {f_elapsed_time:.2f}s\t\\\\\n"
        f_res.write(table_row)


class Timer:
    def __init__(self):
        self._start_time = None
        self._end_time = None

    def start(self):
        if self._end_time is not None:
            self._end_time = None
        self._start_time = perf_counter()

    def stop(self):
        if (self._start_time is not None) and (self._end_time is None):
            self._end_time = perf_counter()

    def elapsed_time(self):
        return self._end_time - self._start_time
