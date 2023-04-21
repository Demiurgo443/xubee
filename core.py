from graph import Graph
from deepdiff import DeepDiff
from utility import Timer


def error_estimation(xag: Graph, xag2: Graph, nodes_of_interest: list) -> tuple[dict, dict, float, float]:
    """Algorithm 1: tight error estimation"""
    function_timer = Timer()
    truth_table1_timer = Timer()
    truth_table2_timer = Timer()

    elapsed_time_truth_tables = 0
    function_timer.start()
    truth_table = {}
    truth_table_2 = {}
    estimated_error_dict = {}
    exact_error_dict = {}

    truth_table1_timer.start()
    max_num = 2 ** xag.input_num
    for val in range(max_num):
        truth_table = xag2.run_input(val, truth_table)
    truth_table1_timer.stop()
    elapsed_time_truth_tables += truth_table1_timer.elapsed_time()

    for inode in nodes_of_interest:
        xag.set_change(inode)

        truth_table2_timer.start()
        for val in range(max_num):
            truth_table_2 = xag.run_input(val, truth_table_2)

        ddiff = DeepDiff(truth_table, truth_table_2)

        exact_error = len(ddiff.affected_root_keys)
        truth_table2_timer.stop()
        elapsed_time_truth_tables += truth_table2_timer.elapsed_time()

        # XNOR - AND - >1 children
        # evaluate it directly: no control over error propagation
        if (xag.nodes[xag.nodes[inode].children[0]].op == 1) and \
                (len(xag.nodes[xag.nodes[inode].children[0]].children) > 1):
            external_leaves = xag.nodes[xag.nodes[inode].children[0]].leaves.difference(xag.nodes[inode].leaves)
            # TODO evaluate tautology, for now skip
            if len(external_leaves) == 0:
                print(f"STOP. Node {inode} not considered for estimation. Ext. leaves = involved leaves.")
                xag.set_change(inode)
                continue
            estimated_error = 2 ** (xag.input_num - 2) // 2 ** len(external_leaves)
            if estimated_error == 0:
                print(f"STOP. Node {inode} not considered for estimation. Something went wrong.")
                xag.set_change(inode)
                continue
            else:
                estimated_error_dict[inode] = estimated_error
                exact_error_dict[inode] = exact_error
                xag.set_change(inode)
        # XNOR - XOR - >1 children
        elif (xag.nodes[xag.nodes[inode].children[0]].op == 0) and \
                (len(xag.nodes[xag.nodes[inode].children[0]].children) > 1):
            print(f"STOP. Node {inode} not considered for estimation. XNOR - XOR - >1 child.")
            xag.set_change(inode)
            continue
        # XNOR - XOR - 1 children
        elif (xag.nodes[xag.nodes[inode].children[0]].op == 0) and \
                (len(xag.nodes[xag.nodes[inode].children[0]].children) == 1):
            # XNOR - XOR - XOR - 1 children
            if xag.nodes[xag.nodes[xag.nodes[inode].children[0]].children[0]].op == 0 and \
                    (len(xag.nodes[xag.nodes[inode].children[0]].children) == 1):
                # XNOR - XOR - XOR - XOR
                if xag.nodes[xag.nodes[xag.nodes[xag.nodes[inode].children[0]].children[0]].children[0]].op == 0:
                    print(f"STOP. Node {inode} not considered for estimation. XNOR - XOR - XOR - XOR.")
                    xag.set_change(inode)
                    continue
                # XNOR - XOR - XOR - AND
                else:
                    if any(isinstance(el, list) for el in
                           xag.nodes[
                               xag.nodes[xag.nodes[xag.nodes[inode].children[0]].children[0]].children[0]].parents):
                        for i in xag.nodes[
                            xag.nodes[xag.nodes[xag.nodes[inode].children[0]].children[0]].children[0]].parents:
                            if (i[0] != xag.nodes[xag.nodes[xag.nodes[inode].children[0]].children[0]].id) and (
                                    len(xag.nodes[i[0]].leaves) != 0):
                                external_leaves = xag.nodes[i[0]].leaves.difference(xag.nodes[inode].leaves)
                                if len(external_leaves) == 0:
                                    print(
                                        f"STOP. Node {inode} not considered for estimation. "
                                        f"The other child has same parents.")
                                    xag.set_change(inode)
                                    continue
                                else:
                                    estimated_error = 2 ** (xag.input_num - 2) // 2 ** len(external_leaves)
                                    if estimated_error == 0:
                                        print(
                                            f"STOP. Node {inode} not considered for estimation. Something went wrong.")
                                        xag.set_change(inode)
                                        continue
                                    else:
                                        estimated_error_dict[inode] = estimated_error
                                        exact_error_dict[inode] = exact_error
                                        xag.set_change(inode)
                            elif (i[0] != xag.nodes[xag.nodes[xag.nodes[inode].children[0]].children[0]].id) and (
                                    len(xag.nodes[i[0]].leaves) == 0):
                                leaf_founded = {xag.nodes[i[0]].id}
                                external_leaves = leaf_founded.difference(xag.nodes[inode].leaves)
                                if len(external_leaves) == 0:
                                    print(
                                        f"STOP. Node {inode} not considered for estimation. "
                                        f"Ext. leaves = involved leaves.")
                                    xag.set_change(inode)
                                    continue
                                else:
                                    estimated_error = 2 ** (xag.input_num - 2) // 2 ** len(external_leaves)
                                    if estimated_error == 0:
                                        print(
                                            f"STOP. Node {inode} not considered for estimation. Something went wrong.")
                                        xag.set_change(inode)
                                        continue
                                    else:
                                        estimated_error_dict[inode] = estimated_error
                                        exact_error_dict[inode] = exact_error
                                        xag.set_change(inode)
                    else:
                        print(
                            f"STOP. Node {inode} not considered for estimation. Root found.")
                        xag.set_change(inode)
                        continue
            # XNOR - XOR - XOR - >1 children
            elif xag.nodes[xag.nodes[xag.nodes[inode].children[0]].children[0]].op == 0 and \
                    (len(xag.nodes[xag.nodes[inode].children[0]].children) > 1):
                print(f"STOP. Node {inode} not considered for estimation. XNOR - XOR - XOR - >1 children")
                xag.set_change(inode)
                continue
            # XNOR - XOR - AND
            else:
                if any(isinstance(el, list) for el in
                       xag.nodes[xag.nodes[xag.nodes[inode].children[0]].children[0]].parents):
                    for i in xag.nodes[xag.nodes[xag.nodes[inode].children[0]].children[0]].parents:
                        if (i[0] != xag.nodes[xag.nodes[inode].children[0]].id) and (
                                len(xag.nodes[i[0]].leaves) != 0):
                            external_leaves = xag.nodes[i[0]].leaves.difference(xag.nodes[inode].leaves)
                            if len(external_leaves) == 0:
                                print(
                                    f"STOP. Node {inode} not considered for estimation. "
                                    f"The other child has same parents")
                                xag.set_change(inode)
                                continue
                            else:
                                estimated_error = 2 ** (xag.input_num - 2) // 2 ** len(external_leaves)
                                if estimated_error == 0:
                                    print(
                                        f"STOP. Node {inode} not considered for estimation. Something went wrong.")
                                    xag.set_change(inode)
                                    continue
                                else:
                                    estimated_error_dict[inode] = estimated_error
                                    exact_error_dict[inode] = exact_error
                                    xag.set_change(inode)
                        elif (i[0] != xag.nodes[xag.nodes[inode].children[0]].id) and (
                                len(xag.nodes[i[0]].leaves) == 0):
                            leaf_founded = {xag.nodes[i[0]].id}
                            external_leaves = leaf_founded.difference(xag.nodes[inode].leaves)
                            if len(external_leaves) == 0:
                                print(
                                    f"STOP. Node {inode} not considered for estimation. Ext. leaves = involved leaves")
                                xag.set_change(inode)
                                continue
                            else:
                                estimated_error = 2 ** (xag.input_num - 2) // 2 ** len(external_leaves)
                                if estimated_error == 0:
                                    print(
                                        f"STOP. Node {inode} not considered for estimation. Something went wrong.")
                                    xag.set_change(inode)
                                    continue
                                else:
                                    estimated_error_dict[inode] = estimated_error
                                    exact_error_dict[inode] = exact_error
                                    xag.set_change(inode)
                else:
                    print(
                        f"STOP. Node {inode} not considered for estimation. Root found")
                    xag.set_change(inode)
                    continue
        # XNOR - AND - 1 children
        elif (xag.nodes[xag.nodes[inode].children[0]].op == 1) and \
                (len(xag.nodes[xag.nodes[inode].children[0]].children) == 1):
            # XNOR - AND - AND
            if xag.nodes[xag.nodes[xag.nodes[inode].children[0]].children[0]].op == 1:
                external_leaves = xag.nodes[xag.nodes[xag.nodes[inode].children[0]].children[0]].leaves \
                    .difference(xag.nodes[inode].leaves)
                if len(external_leaves) == 0:
                    print(
                        f"STOP. Node {inode} not considered for estimation. Ext. leaves = involved leaves")
                    xag.set_change(inode)
                    continue
                else:
                    estimated_error = 2 ** (xag.input_num - 2) // 2 ** len(external_leaves)
                    if estimated_error == 0:
                        print(
                            f"STOP. Node {inode} not considered for estimation. Something went wrong.")
                        xag.set_change(inode)
                        continue
                    else:
                        estimated_error_dict[inode] = estimated_error
                        exact_error_dict[inode] = exact_error
                        xag.set_change(inode)
            # XNOR - AND - XOR - >1 children
            elif (xag.nodes[xag.nodes[xag.nodes[inode].children[0]].children[0]].op == 0) and \
                    (len(xag.nodes[xag.nodes[xag.nodes[inode].children[0]].children[0]].children) > 1):
                external_leaves = xag.nodes[xag.nodes[inode].children[0]].leaves.difference(xag.nodes[inode].leaves)
                if len(external_leaves) == 0:
                    print(
                        f"STOP. Node {inode} not considered for estimation. Ext. leaves = involved leaves")
                    xag.set_change(inode)
                    continue
                else:
                    estimated_error = 2 ** (xag.input_num - 2) // 2 ** len(external_leaves)
                    if estimated_error == 0:
                        print(
                            f"STOP. Node {inode} not considered for estimation. Something went wrong.")
                        xag.set_change(inode)
                        continue
                    else:
                        estimated_error_dict[inode] = estimated_error
                        exact_error_dict[inode] = exact_error
                        xag.set_change(inode)
            # XNOR - AND - XOR - 1 children
            elif (xag.nodes[xag.nodes[xag.nodes[inode].children[0]].children[0]].op == 0) and \
                    (len(xag.nodes[xag.nodes[xag.nodes[inode].children[0]].children[0]].children) == 1):
                # XNOR - AND - XOR - XOR
                if xag.nodes[xag.nodes[xag.nodes[xag.nodes[inode].children[0]].children[0]].children[0]].op == 0:
                    external_leaves = xag.nodes[xag.nodes[inode].children[0]].leaves.difference(xag.nodes[inode].leaves)
                    if len(external_leaves) == 0:
                        print(
                            f"STOP. Node {inode} not considered for estimation. Ext. leaves = involved leaves.")
                        xag.set_change(inode)
                        continue
                    else:
                        estimated_error = 2 ** (xag.input_num - 2) // 2 ** len(external_leaves)
                        if estimated_error == 0:
                            print(
                                f"STOP. Node {inode} not considered for estimation. Something went wrong.")
                            xag.set_change(inode)
                            continue
                        else:
                            estimated_error_dict[inode] = estimated_error
                            exact_error_dict[inode] = exact_error
                            xag.set_change(inode)
                # XNOR - AND - XOR - AND
                else:
                    if any(isinstance(el, list) for el in
                           xag.nodes[xag.nodes[xag.nodes[xag.nodes[inode].children[0]].children[0]].children[0]]
                            .parents):
                        for i in xag.nodes[xag.nodes[xag.nodes[xag.nodes[inode].children[0]].children[0]].children[0]] \
                                .parents:
                            if (i[0] != xag.nodes[xag.nodes[xag.nodes[inode].children[0]].children[0]].id) and \
                                    (len(xag.nodes[i[0]].leaves) != 0):
                                union_leaves = xag.nodes[xag.nodes[inode].children[0]].leaves.union(
                                    xag.nodes[i[0]].leaves)
                                external_leaves = union_leaves.difference(xag.nodes[inode].leaves)
                                if len(external_leaves) == 0:
                                    print(
                                        f"STOP. Node {inode} not considered for estimation. "
                                        f"The other child node has same parents.")
                                    xag.set_change(inode)
                                    continue
                                else:
                                    estimated_error = 2 ** (xag.input_num - 2) // 2 ** len(external_leaves)
                                    if estimated_error == 0:
                                        print(
                                            f"STOP. Node {inode} not considered for estimation. Something went wrong.")
                                        xag.set_change(inode)
                                        continue
                                    else:
                                        estimated_error_dict[inode] = estimated_error
                                        exact_error_dict[inode] = exact_error
                                        xag.set_change(inode)
                            elif (i[0] != xag.nodes[xag.nodes[xag.nodes[inode].children[0]].children[0]].id) and (
                                    len(xag.nodes[i[0]].leaves) == 0):
                                leaf_founded = {xag.nodes[i[0]].id}
                                external_leaves = leaf_founded.difference(xag.nodes[inode].leaves)
                                if len(external_leaves) == 0:
                                    print(
                                        f"STOP. Node {inode} not considered for estimation. "
                                        f"Ext. leaves = involved leaves.")
                                    xag.set_change(inode)
                                    continue
                                else:
                                    estimated_error = 2 ** (xag.input_num - 2) // 2 ** len(external_leaves)
                                    if estimated_error == 0:
                                        print(
                                            f"STOP. Node {inode} not considered for estimation. Something went wrong.")
                                        xag.set_change(inode)
                                        continue
                                    else:
                                        estimated_error_dict[inode] = estimated_error
                                        exact_error_dict[inode] = exact_error
                                        xag.set_change(inode)
                    else:
                        print(
                            f"STOP. Node {inode} not considered for estimation. Root found.")
                        xag.set_change(inode)
    function_timer.stop()
    return estimated_error_dict, exact_error_dict, function_timer.elapsed_time(), elapsed_time_truth_tables


def error_estimation_4i(xag: Graph, xag2: Graph, nodes_of_interest: list) -> tuple[dict, dict, float, float]:
    """Algorithm 2: non-tight error estimation"""
    function_timer = Timer()
    truth_table1_timer = Timer()
    truth_table2_timer = Timer()

    elapsed_time_truth_tables = 0
    function_timer.start()

    truth_table = {}
    truth_table_2 = {}
    estimated_error_dict = {}
    exact_error_dict = {}

    truth_table1_timer.start()
    max_num = 2 ** xag.input_num
    for val in range(max_num):
        truth_table = xag2.run_input(val, truth_table)
    truth_table1_timer.stop()
    elapsed_time_truth_tables += truth_table1_timer.elapsed_time()

    for inode in nodes_of_interest:
        estimated_error = 0
        xag.set_change(inode)

        truth_table2_timer.start()
        for val in range(max_num):
            truth_table_2 = xag.run_input(val, truth_table_2)

        ddiff = DeepDiff(truth_table, truth_table_2)
        exact_error = len(ddiff.affected_root_keys)
        truth_table2_timer.stop()
        elapsed_time_truth_tables += truth_table2_timer.elapsed_time()

        # XNOR - AND - >= 1 child
        if (xag.nodes[xag.nodes[inode].children[0]].op == 1) and \
                (len(xag.nodes[xag.nodes[inode].children[0]].children) >= 1):
            external_leaves = xag.nodes[xag.nodes[inode].children[0]].leaves.difference(xag.nodes[inode].leaves)
            # TODO evaluate tautology, for now skip
            if len(external_leaves) == 0:
                print(f"STOP. Node {inode} not considered for estimation. Ext. leaves = involved leaves.")
                xag.set_change(inode)
                continue
            estimated_error = 2 ** (xag.input_num - 2) // 2 ** len(external_leaves)
            if estimated_error == 0:
                print(f"STOP. Node {inode} not considered for estimation. Something went wrong")
                xag.set_change(inode)
                continue
            else:
                estimated_error_dict[inode] = estimated_error
                exact_error_dict[inode] = exact_error
                xag.set_change(inode)
        # XNOR - XOR - >1 children
        elif (xag.nodes[xag.nodes[inode].children[0]].op == 0) and \
                (len(xag.nodes[xag.nodes[inode].children[0]].children) > 1):
            print(f"STOP. Node {inode} not considered for estimation. XNOR - XOR - >1 children")
            xag.set_change(inode)
            continue
        # XNOR - XOR - 1 children
        elif (xag.nodes[xag.nodes[inode].children[0]].op == 0) and \
                (len(xag.nodes[xag.nodes[inode].children[0]].children) == 1):
            # XNOR - XOR - XOR
            if xag.nodes[xag.nodes[xag.nodes[inode].children[0]].children[0]].op == 0:
                print(f"STOP. Node {inode} not considered for estimation. XNOR - XOR - XOR.")
                xag.set_change(inode)
                continue
            # XNOR - XOR - AND
            else:
                if any(isinstance(el, list) for el in xag.nodes[xag.nodes[xag.nodes[inode].children[0]].children[0]]
                        .parents):
                    for i in xag.nodes[xag.nodes[xag.nodes[inode].children[0]].children[0]].parents:
                        if (i[0] != xag.nodes[xag.nodes[inode].children[0]].id) and (
                                len(xag.nodes[i[0]].leaves) != 0):
                            external_leaves = xag.nodes[i[0]].leaves.difference(xag.nodes[inode].leaves)
                            if len(external_leaves) == 0:
                                print(f"STOP. Node {inode} not considered for estimation. "
                                      f"The other child has same parents.")
                                xag.set_change(inode)
                                continue
                            else:
                                estimated_error = 2 ** (xag.input_num - 2) // 2 ** len(external_leaves)
                                if estimated_error == 0:
                                    print(
                                        f"STOP. Node {inode} not considered for estimation. Something went wrong.")
                                    xag.set_change(inode)
                                    continue
                                else:
                                    estimated_error_dict[inode] = estimated_error
                                    exact_error_dict[inode] = exact_error
                                    xag.set_change(inode)
                        elif (i[0] != xag.nodes[xag.nodes[xag.nodes[inode].children[0]].children[0]].id) and (
                                len(xag.nodes[i[0]].leaves) == 0):
                            leaf_founded = {xag.nodes[i[0]].id}
                            external_leaves = leaf_founded.difference(xag.nodes[inode].leaves)
                            if len(external_leaves) == 0:
                                print(
                                    f"STOP. Node {inode} not considered for estimation. Ext. leaves = involed leaves.")
                                xag.set_change(inode)
                                continue
                            else:
                                estimated_error = 2 ** (xag.input_num - 2) // 2 ** len(external_leaves)
                                if estimated_error == 0:
                                    print(
                                        f"STOP. Node {inode} not considered for estimation. Something went wrong.")
                                    xag.set_change(inode)
                                    continue
                                else:
                                    estimated_error_dict[inode] = estimated_error
                                    exact_error_dict[inode] = exact_error
                                    xag.set_change(inode)
                else:
                    print(
                        f"STOP. Node {inode} not considered for estimation. Root found.")
                    xag.set_change(inode)
                    continue
    function_timer.stop()
    return estimated_error_dict, exact_error_dict, function_timer.elapsed_time(), elapsed_time_truth_tables
