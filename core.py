from graph import Graph
from deepdiff import DeepDiff
from utility import Timer


def error_estimation(xag: Graph, xag2: Graph, nodes_of_interest: list)-> tuple[dict, dict, float, float]:
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

        # nodo successivo a quello modificato è AND e ha più figli
        # -> qua valuto direttamente l'errore perché rischierei di valutare solo un ramo in cui si è propagato
        if (xag.nodes[xag.nodes[inode].children[0]].op == 1) and \
                (len(xag.nodes[xag.nodes[inode].children[0]].children) > 1):
            external_leaves = xag.nodes[xag.nodes[inode].children[0]].leaves.difference(xag.nodes[inode].leaves)
            # TODO andrebbe valutato caso tautologico, per semplicità skip
            if len(external_leaves) == 0:
                print(f"STOP. Il nodo {inode} non viene considerato per la stima. Foglie est = coinvolte.")
                xag.set_change(inode)
                continue
            estimated_error = 2 ** (xag.input_num - 2) // 2 ** len(external_leaves)
            if estimated_error == 0:
                print(f"STOP. Il nodo {inode} non viene considerato per la stima. Qualcosa è andato storto")
                xag.set_change(inode)
                continue
            else:
                estimated_error_dict[inode] = estimated_error
                exact_error_dict[inode] = exact_error
                xag.set_change(inode)
            # return truth_table, truth_table_2, estimated_error
        # nodo successivo a quello modificato è XOR e ha più figli
        elif (xag.nodes[xag.nodes[inode].children[0]].op == 0) and \
                (len(xag.nodes[xag.nodes[inode].children[0]].children) > 1):
            print(f"STOP. Il nodo {inode} non viene considerato per la stima. XNOR - XOR - >1 child")
            xag.set_change(inode)
            continue
        # nodo successivo a quello modificato è XOR e 1 figlio
        elif (xag.nodes[xag.nodes[inode].children[0]].op == 0) and \
                (len(xag.nodes[xag.nodes[inode].children[0]].children) == 1):
            # nodo 2 successivo a quello modificato è XOR e ha 1 figlio
            if xag.nodes[xag.nodes[xag.nodes[inode].children[0]].children[0]].op == 0 and \
                (len(xag.nodes[xag.nodes[inode].children[0]].children) == 1):
                # nodo 3 volte successivo a quello modificato è XOR
                if xag.nodes[xag.nodes[xag.nodes[xag.nodes[inode].children[0]].children[0]].children[0]].op == 0:
                    print(f"STOP. Il nodo {inode} non viene considerato per la stima. XNOR - XOR - XOR - XOR")
                    xag.set_change(inode)
                    continue
                # se, invece, è AND, prendo le foglie dall'altro suo nodo figlio
                else:
                    if any(isinstance(el, list) for el in
                           xag.nodes[xag.nodes[xag.nodes[xag.nodes[inode].children[0]].children[0]].children[0]].parents):
                        for i in xag.nodes[xag.nodes[xag.nodes[xag.nodes[inode].children[0]].children[0]].children[0]].parents:
                            if (i[0] != xag.nodes[xag.nodes[xag.nodes[inode].children[0]].children[0]].id) and (len(xag.nodes[i[0]].leaves) != 0):
                                external_leaves = xag.nodes[i[0]].leaves.difference(xag.nodes[inode].leaves)
                                if len(external_leaves) == 0:
                                    print(
                                        f"STOP. Il nodo {inode} non viene considerato per la stima. Altro nodo figlio ha stesi genitori")
                                    xag.set_change(inode)
                                    continue
                                else:
                                    estimated_error = 2 ** (xag.input_num - 2) // 2 ** len(external_leaves)
                                    if estimated_error == 0:
                                        print(
                                            f"STOP. Il nodo {inode} non viene considerato per la stima. Qualcosa è andato storto")
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
                                        f"STOP. Il nodo {inode} non viene considerato per la stima. Foglia est. = foglie coinvolte")
                                    xag.set_change(inode)
                                    continue
                                else:
                                    estimated_error = 2 ** (xag.input_num - 2) // 2 ** len(external_leaves)
                                    if estimated_error == 0:
                                        print(
                                            f"STOP. Il nodo {inode} non viene considerato per la stima. Qualcosa è andato storto")
                                        xag.set_change(inode)
                                        continue
                                    else:
                                        estimated_error_dict[inode] = estimated_error
                                        exact_error_dict[inode] = exact_error
                                        xag.set_change(inode)
                    else:
                        print(
                            f"STOP. Il nodo {inode} non viene considerato per la stima. Sei incappato in radice")
                        xag.set_change(inode)
                        continue
            # nodo 2 volte modificato XOR 2 figli
            elif xag.nodes[xag.nodes[xag.nodes[inode].children[0]].children[0]].op == 0 and \
                    (len(xag.nodes[xag.nodes[inode].children[0]].children) > 1):
                    print(f"STOP. Il nodo {inode} non viene considerato per la stima. XNOR - XOR - XOR - >1 figlio")
                    xag.set_change(inode)
                    continue
            # se nodo due volte successivo a quello modificato è AND
            else:
                if any(isinstance(el, list) for el in
                       xag.nodes[xag.nodes[xag.nodes[inode].children[0]].children[0]].parents):
                    for i in xag.nodes[xag.nodes[xag.nodes[inode].children[0]].children[0]].parents:
                        if (i[0] != xag.nodes[xag.nodes[inode].children[0]].id) and (
                                len(xag.nodes[i[0]].leaves) != 0):
                            external_leaves = xag.nodes[i[0]].leaves.difference(xag.nodes[inode].leaves)
                            if len(external_leaves) == 0:
                                print(
                                    f"STOP. Il nodo {inode} non viene considerato per la stima. Altro nodo figlio ha stesi genitori")
                                xag.set_change(inode)
                                continue
                            else:
                                estimated_error = 2 ** (xag.input_num - 2) // 2 ** len(external_leaves)
                                if estimated_error == 0:
                                    print(
                                        f"STOP. Il nodo {inode} non viene considerato per la stima. Qualcosa è andato storto")
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
                                    f"STOP. Il nodo {inode} non viene considerato per la stima. Foglia est. = foglie coinvolte")
                                xag.set_change(inode)
                                continue
                            else:
                                estimated_error = 2 ** (xag.input_num - 2) // 2 ** len(external_leaves)
                                if estimated_error == 0:
                                    print(
                                        f"STOP. Il nodo {inode} non viene considerato per la stima. Qualcosa è andato storto")
                                    xag.set_change(inode)
                                    continue
                                else:
                                    estimated_error_dict[inode] = estimated_error
                                    exact_error_dict[inode] = exact_error
                                    xag.set_change(inode)
                else:
                    print(
                        f"STOP. Il nodo {inode} non viene considerato per la stima. Sei incappato in radice")
                    xag.set_change(inode)
                    continue
        # nodo successivo a quello modificato è AND 1 figlio
        elif (xag.nodes[xag.nodes[inode].children[0]].op == 1) and \
                (len(xag.nodes[xag.nodes[inode].children[0]].children) == 1):
            # nodo 2 successivo è AND #TODO valutare... nella versione precedente si lascia così senza valutare ulteriormente
            if xag.nodes[xag.nodes[xag.nodes[inode].children[0]].children[0]].op == 1:
                external_leaves = xag.nodes[xag.nodes[xag.nodes[inode].children[0]].children[0]].leaves \
                    .difference(xag.nodes[inode].leaves)
                if len(external_leaves) == 0:
                    print(
                        f"STOP. Il nodo {inode} non viene considerato per la stima. Foglie est. = foglie coinvolte")
                    xag.set_change(inode)
                    continue
                else:
                    estimated_error = 2 ** (xag.input_num - 2) // 2 ** len(external_leaves)
                    if estimated_error == 0:
                        print(
                            f"STOP. Il nodo {inode} non viene considerato per la stima. Qualcosa è andato storto")
                        xag.set_change(inode)
                        continue
                    else:
                        estimated_error_dict[inode] = estimated_error
                        exact_error_dict[inode] = exact_error
                        xag.set_change(inode)
            # nodo 2 successivo XOR > 1 figlio #TODO controlla, non mi pareee
            elif (xag.nodes[xag.nodes[xag.nodes[inode].children[0]].children[0]].op == 0) and \
                (len(xag.nodes[xag.nodes[xag.nodes[inode].children[0]].children[0]].children) > 1):
                # prendo foglie da nodo successivo modificato
                external_leaves = xag.nodes[xag.nodes[inode].children[0]].leaves.difference(xag.nodes[inode].leaves)
                if len(external_leaves) == 0:
                    print(
                        f"STOP. Il nodo {inode} non viene considerato per la stima. Foglie est. = foglie coinvolte")
                    xag.set_change(inode)
                    continue
                else:
                    estimated_error = 2 ** (xag.input_num - 2) // 2 ** len(external_leaves)
                    if estimated_error == 0:
                        print(
                            f"STOP. Il nodo {inode} non viene considerato per la stima. Qualcosa è andato storto")
                        xag.set_change(inode)
                        continue
                    else:
                        estimated_error_dict[inode] = estimated_error
                        exact_error_dict[inode] = exact_error
                        xag.set_change(inode)
            # nodo 2 successivo XOR 1 figlio
            elif (xag.nodes[xag.nodes[xag.nodes[inode].children[0]].children[0]].op == 0) and \
                (len(xag.nodes[xag.nodes[xag.nodes[inode].children[0]].children[0]].children) == 1):
                # nodo 3 successivo XOR
                if xag.nodes[xag.nodes[xag.nodes[xag.nodes[inode].children[0]].children[0]].children[0]].op == 0:
                    # prendo foglie da nodo successivo modificato
                    external_leaves = xag.nodes[xag.nodes[inode].children[0]].leaves.difference(xag.nodes[inode].leaves)
                    if len(external_leaves) == 0:
                        print(
                            f"STOP. Il nodo {inode} non viene considerato per la stima. Foglia est. = foglie coinvolte")
                        xag.set_change(inode)
                        continue
                    else:
                        estimated_error = 2 ** (xag.input_num - 2) // 2 ** len(external_leaves)
                        if estimated_error == 0:
                            print(
                                f"STOP. Il nodo {inode} non viene considerato per la stima. Qualcosa è andato storto")
                            xag.set_change(inode)
                            continue
                        else:
                            estimated_error_dict[inode] = estimated_error
                            exact_error_dict[inode] = exact_error
                            xag.set_change(inode)
                # nodo 3 successivo è AND
                else:
                    if any(isinstance(el, list) for el in
                           xag.nodes[xag.nodes[xag.nodes[xag.nodes[inode].children[0]].children[0]].children[0]].parents):
                        for i in xag.nodes[xag.nodes[xag.nodes[xag.nodes[inode].children[0]].children[0]].children[0]].parents:
                            if (i[0] != xag.nodes[xag.nodes[xag.nodes[inode].children[0]].children[0]].id) and (len(xag.nodes[i[0]].leaves) != 0):
                                union_leaves = xag.nodes[xag.nodes[inode].children[0]].leaves.union(xag.nodes[i[0]].leaves)
                                external_leaves = union_leaves.difference(xag.nodes[inode].leaves)
                                if len(external_leaves) == 0:
                                    print(
                                        f"STOP. Il nodo {inode} non viene considerato per la stima. Altro nodo figlia ha stesi genitori")
                                    xag.set_change(inode)
                                    continue
                                else:
                                    estimated_error = 2 ** (xag.input_num - 2) // 2 ** len(external_leaves)
                                    if estimated_error == 0:
                                        print(
                                            f"STOP. Il nodo {inode} non viene considerato per la stima. Qualcosa è andato storto")
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
                                        f"STOP. Il nodo {inode} non viene considerato per la stima. Foglia est. = foglie coinvolte")
                                    xag.set_change(inode)
                                    continue
                                else:
                                    estimated_error = 2 ** (xag.input_num - 2) // 2 ** len(external_leaves)
                                    if estimated_error == 0:
                                        print(
                                            f"STOP. Il nodo {inode} non viene considerato per la stima. Qualcosa è andato storto")
                                        xag.set_change(inode)
                                        continue
                                    else:
                                        estimated_error_dict[inode] = estimated_error
                                        exact_error_dict[inode] = exact_error
                                        xag.set_change(inode)
                    else:
                        print(
                            f"STOP. Il nodo {inode} non viene considerato per la stima. Sei incappato in radice")
                        xag.set_change(inode)
    function_timer.stop()
    # elapsed_time = function_timer.elapsed_time - elapsed_time_truth_tables
    return estimated_error_dict, exact_error_dict, function_timer.elapsed_time(), elapsed_time_truth_tables


def error_estimation_4i(xag: Graph, xag2: Graph, nodes_of_interest: list) -> tuple[dict, dict, float, float]:
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

        # nodo successivo a quello modificato è AND e ha più figli
        # -> qua valuto direttamente l'errore perché rischierei di valutare solo un ramo in cui si è propagato
        if (xag.nodes[xag.nodes[inode].children[0]].op == 1) and \
                (len(xag.nodes[xag.nodes[inode].children[0]].children) > 1):
            external_leaves = xag.nodes[xag.nodes[inode].children[0]].leaves.difference(xag.nodes[inode].leaves)
            # TODO andrebbe valutato caso tautologico, per semplicità skip
            if len(external_leaves) == 0:
                print(f"STOP. Il nodo {inode} non viene considerato per la stima. Foglie est = coinvolte.")
                xag.set_change(inode)
                continue
            estimated_error = 2 ** (xag.input_num - 2) // 2 ** len(external_leaves)
            if estimated_error == 0:
                print(f"STOP. Il nodo {inode} non viene considerato per la stima. Qualcosa è andato storto")
                xag.set_change(inode)
                continue
            else:
                estimated_error_dict[inode] = estimated_error
                exact_error_dict[inode] = exact_error
                xag.set_change(inode)
            # return truth_table, truth_table_2, estimated_error
        # nodo successivo a quello modificato è XOR e ha più figli
        elif (xag.nodes[xag.nodes[inode].children[0]].op == 0) and \
             (len(xag.nodes[xag.nodes[inode].children[0]].children) > 1):
            print(f"STOP. Il nodo {inode} non viene considerato per la stima. XNOR - XOR - >1 child")
            xag.set_change(inode)
            continue
        # nodo successivo a quello modificato è XOR e 1 figlio
        elif (xag.nodes[xag.nodes[inode].children[0]].op == 0) and \
             (len(xag.nodes[xag.nodes[inode].children[0]].children) == 1):
            # nodo 2 successivo a quello modificato è XOR
            if xag.nodes[xag.nodes[xag.nodes[inode].children[0]].children[0]].op == 0:
                print(f"STOP. Il nodo {inode} non viene considerato per la stima. XNOR - XOR - XOR.")
                xag.set_change(inode)
                continue
            # se AND
            else:
                if any(isinstance(el, list) for el in xag.nodes[xag.nodes[xag.nodes[inode].children[0]].children[0]].parents):
                    for i in xag.nodes[xag.nodes[xag.nodes[inode].children[0]].children[0]].parents:
                        if (i[0] != xag.nodes[xag.nodes[inode].children[0]].id) and (
                                len(xag.nodes[i[0]].leaves) != 0):
                            external_leaves = xag.nodes[i[0]].leaves.difference(xag.nodes[inode].leaves)
                            if len(external_leaves) == 0:
                                print(f"STOP. Il nodo {inode} non viene considerato per la stima. Altro nodo figlio ha stesi genitori")
                                xag.set_change(inode)
                                continue
                            else:
                                estimated_error = 2 ** (xag.input_num - 2) // 2 ** len(external_leaves)
                                if estimated_error == 0:
                                    print(
                                        f"STOP. Il nodo {inode} non viene considerato per la stima. Qualcosa è andato storto")
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
                                    f"STOP. Il nodo {inode} non viene considerato per la stima. Foglia est. = foglie coinvolte")
                                xag.set_change(inode)
                                continue
                            else:
                                estimated_error = 2 ** (xag.input_num - 2) // 2 ** len(external_leaves)
                                if estimated_error == 0:
                                    print(
                                        f"STOP. Il nodo {inode} non viene considerato per la stima. Qualcosa è andato storto")
                                    xag.set_change(inode)
                                    continue
                                else:
                                    estimated_error_dict[inode] = estimated_error
                                    exact_error_dict[inode] = exact_error
                                    xag.set_change(inode)
                else:
                    print(
                        f"STOP. Il nodo {inode} non viene considerato per la stima. Sei incappato in radice")
                    xag.set_change(inode)
                    continue
        # AND 1 figlio
        elif (xag.nodes[xag.nodes[inode].children[0]].op == 1) and \
                (len(xag.nodes[xag.nodes[inode].children[0]].children) == 1):
            external_leaves = xag.nodes[xag.nodes[inode].children[0]].leaves.difference(xag.nodes[inode].leaves)
            if len(external_leaves) == 0:
                print(
                    f"STOP. Il nodo {inode} non viene considerato per la stima. Foglia est. = foglie coinvolte")
                xag.set_change(inode)
                continue
            else:
                estimated_error = 2 ** (xag.input_num - 2) // 2 ** len(external_leaves)
                if estimated_error == 0:
                    print(
                        f"STOP. Il nodo {inode} non viene considerato per la stima. Qualcosa è andato storto")
                    xag.set_change(inode)
                    continue
                else:
                    estimated_error_dict[inode] = estimated_error
                    exact_error_dict[inode] = exact_error
                    xag.set_change(inode)
    function_timer.stop()
    return estimated_error_dict, exact_error_dict, function_timer.elapsed_time(), elapsed_time_truth_tables
