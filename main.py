# Xag Upper Bound Error Evaluation (valuta se inserire uno fra i seguenti termini: Experimental, Estimation, Framework)

import sys
from utility import parser
from deepdiff import DeepDiff

if __name__ == '__main__':
    truth_table = {}
    truth_table_2 = {}
    error_list = {}
    estimated_error_list = {}
    num_same_error = 0
    num_error_bound_destroyed = 0
    tot_estimated_error = 0
    tot_error_found = 0

    # makes this program launchable with bash scripts
    filename = sys.argv[1]

    # xag, nodes_of_interest = parser("verilogs/x7dn.v_opt.v")
    # xag2, nodes_of_interest2 = parser("verilogs/x7dn.v_opt.v")
    # xag, nodes_of_interest = parser("verilogs/e_pla_4i_5_xor.v_opt.v")
    # xag2, nodes_of_interest2 = parser("verilogs/e_pla_4i_5_xor.v_opt.v")
    # xag, nodes_of_interest = parser("verilogs/e_pla_6i_1.v_opt.v")
    # xag2, nodes_of_interest2 = parser("verilogs/e_pla_6i_1.v_opt.v")
    xag, nodes_of_interest = parser(f"verilogs/{filename}")
    xag2, nodes_of_interest2 = parser(f"verilogs/{filename}")

    print("--------------------------------------------------------------------")
    print(f"|                   Analizzando {filename}                       |")
    print("--------------------------------------------------------------------")

    max_num = 2 ** xag.input_num
    for val in range(max_num):
        truth_table = xag.run_input(val, truth_table)
        # print(truth_table)

    for inode in nodes_of_interest2:
        estimated_error = 0

        xag2.set_change(inode)
        for val in range(max_num):
            truth_table_2 = xag2.run_input(val, truth_table_2)

        # nodo successivo a quello modificato è XOR e ha un solo figlio
        if (xag2.nodes[xag2.nodes[inode].children[0]].op == 0) and \
                (len(xag2.nodes[xag2.nodes[inode].children[0]].children) == 1):
            # nodo 2 volte successivo a quello modificato è XOR e ha più figli
            if (xag2.nodes[xag2.nodes[xag2.nodes[inode].children[0]].children[0]].op == 0) and \
                    (len(xag2.nodes[xag2.nodes[inode].children[0]].children) != 1):
                print(f"La ricerca si ferma. Il nodo {inode} non viene considerato per la stima precisa dell'errore.")
                xag2.set_change(inode)
                continue
            # se, invece, ha un solo figlio
            elif (xag2.nodes[xag2.nodes[xag2.nodes[inode].children[0]].children[0]].op == 0) and \
                    (len(xag2.nodes[xag2.nodes[inode].children[0]].children) == 1):
                # se nodo 3 volte successivo a quello modificato è XOR
                if xag2.nodes[xag2.nodes[xag2.nodes[xag2.nodes[inode].children[0]].children[0]].children[0]].op == 0:
                    print(
                        f"La ricerca si ferma. Il nodo {inode} non viene considerato per la stima precisa dell'errore.")
                    xag2.set_change(inode)
                    continue
                # se, invece, è AND, prendo le foglie dall'altro suo nodo figlio
                else:
                    for i in xag2.nodes[xag2.nodes[xag2.nodes[xag2.nodes[inode].children[0]].children[0]].children[0]] \
                            .parents:
                        if (i[0] != xag2.nodes[xag2.nodes[xag2.nodes[inode].children[0]].children[0]].id) and (
                                len(xag2.nodes[i[0]].leaves) != 0):
                            external_leaves = xag2.nodes[i[0]].leaves.difference(xag2.nodes[inode].leaves)
                            estimated_error = 2 ** (xag2.input_num - 2) // 2 ** len(external_leaves)
                        elif (i[0] != xag2.nodes[xag2.nodes[xag2.nodes[inode].children[0]].children[0]].id) and (
                                len(xag2.nodes[i[0]].leaves) == 0):
                            external_leaves = {xag2.nodes[i[0]].id}.difference(xag2.nodes[inode].leaves)
                            if len(external_leaves) == 0:
                                print("Data la sequenza E-XOR-XOR-AND,"
                                      " l'altro genitore del nodo AND corrisponde a un nodo foglia")
                                print(f"La ricerca si ferma. "
                                      f"Il nodo {inode} non viene considerato per la stima precisa dell'errore.")
                                xag2.set_change(inode)
                                continue
                            estimated_error = 2 ** (xag2.input_num - 2) // 2 ** len(external_leaves)

        # nodo successivo a quello modificato è XOR e ha più figli
        elif (xag2.nodes[xag2.nodes[inode].children[0]].op == 0) and \
                (len(xag2.nodes[xag2.nodes[inode].children[0]].children) != 1):
            print(f"La ricerca si ferma. Il nodo {inode} non viene considerato per la stima precisa dell'errore.")
            xag2.set_change(inode)
            continue

        # nodo successivo a quello modificato è AND e ha 1 figlio
        elif (xag2.nodes[xag2.nodes[inode].children[0]].op == 1) and \
                (len(xag2.nodes[xag2.nodes[inode].children[0]].children) == 1):
            # nodo due volte successivo a quello modificato è XOR e ha più figli
            if (xag2.nodes[xag2.nodes[xag2.nodes[inode].children[0]].children[0]].op == 0) and \
                    (len(xag2.nodes[xag2.nodes[inode].children[0]].children) != 1):
                # si prende nodo precedente
                external_leaves = xag2.nodes[xag2.nodes[inode].children[0]].leaves.difference(xag2.nodes[inode].leaves)
                estimated_error = 2 ** (xag2.input_num - 2) // 2 ** len(external_leaves)
            # nodo due volte successivo a quello modificato è XOR e ha 1 figlio
            elif (xag2.nodes[xag2.nodes[xag2.nodes[inode].children[0]].children[0]].op == 0) and \
                    (len(xag2.nodes[xag2.nodes[inode].children[0]].children) == 1):
                # nodo tre volte successivo a quello modificato è XOR
                # -> vado a valutare nodo successivo a quello modificato
                if xag2.nodes[xag2.nodes[xag2.nodes[xag2.nodes[inode].children[0]].children[0]].children[0]].op == 0:
                    external_leaves = xag2.nodes[xag2.nodes[inode].children[0]].leaves \
                        .difference(xag2.nodes[inode].leaves)
                    estimated_error = 2 ** (xag2.input_num - 2) // 2 ** len(external_leaves)
                # se, invece, è AND, vado a fare unione foglie del nodo successivo a quello modificato con
                # foglie dell'altro nodo genitore del nodo tre volte successivo.
                # N.B.: visto che in qualche modo "si torna indietro" nel grafo, è opportuno appurare se "nodo indietro"
                # sia nodo intermedio o nodo foglia (leaves set vuoto)
                else:
                    for i in xag2.nodes[
                                xag2.nodes[xag2.nodes[xag2.nodes[inode].children[0]].children[0]].children[0]].parents:
                        if (i[0] != xag2.nodes[xag2.nodes[xag2.nodes[inode].children[0]].children[0]].id) and (
                                len(xag2.nodes[i[0]].leaves) != 0):
                            external_leaves = xag2.nodes[xag2.nodes[inode].children[0]].leaves \
                                .union(xag2.nodes[i[0]].leaves).difference(xag2.nodes[inode].leaves)
                            estimated_error = 2 ** (xag2.input_num - 2) // 2 ** len(external_leaves)
                        elif (i[0] != xag2.nodes[xag2.nodes[xag2.nodes[inode].children[0]].children[0]].id) and (
                                len(xag2.nodes[i[0]].leaves) == 0):
                            external_leaves = xag2.nodes[xag2.nodes[inode].children[0]].leaves \
                                .union({xag2.nodes[i[0]].id}).difference(xag2.nodes[inode].leaves)
                            estimated_error = 2 ** (xag2.input_num - 2) // 2 ** len(external_leaves)
            # nodo due volte successivo a quello modificato è AND
            elif xag2.nodes[xag2.nodes[xag2.nodes[inode].children[0]].children[0]].op == 1:
                external_leaves = xag2.nodes[xag2.nodes[xag2.nodes[inode].children[0]].children[0]].leaves \
                    .difference(xag2.nodes[inode].leaves)
                estimated_error = 2 ** (xag2.input_num - 2) // 2 ** len(external_leaves)

        # nodo successivo a quello modificato è AND e ha più figli
        # -> qua valuto direttamente l'errore perché rischierei di valutare solo un ramo in cui si è propagato
        elif (xag2.nodes[xag2.nodes[inode].children[0]].op == 1) and \
                (len(xag2.nodes[xag2.nodes[inode].children[0]].children) != 1):
            external_leaves = xag2.nodes[xag2.nodes[inode].children[0]].leaves.difference(xag2.nodes[inode].leaves)
            estimated_error = 2 ** (xag2.input_num - 2) // 2 ** len(external_leaves)

        xag2.set_change(inode)
        if estimated_error == 0:
            print(f"Qualcosa in {inode} è andato storto...")
            continue
        else:
            print(f"La tabella di verità ha {max_num} righe...")
            print(f"l'errore stimato con il cambiamento di {inode} è: {estimated_error}")
            print(f"Percentuale di errore stimato: {'{:.3f}'.format((estimated_error / max_num) * 100)}%")
            num_and_nodes = 0
            for and_node_id in xag.internal_nodes:
                if xag.nodes[and_node_id].op == 1:
                    num_and_nodes += 1
            print(f"Percentuale di guadagno complessità moltiplicativa: {'{:.3f}'.format((1 / num_and_nodes) * 100)}%")

            # decommenta solo se hai truth table complete
            ddiff = DeepDiff(truth_table, truth_table_2)
            print(f"{inode} porta ad avere {len(ddiff.affected_root_keys)} errori.")
            print(f"Percentuale errore esatto: {'{:.3f}'.format((len(ddiff.affected_root_keys) / max_num) * 100)}%")
            print(
                f"L'errore esatto è "
                f"{'{:.2f}'.format(((estimated_error - (len(ddiff.affected_root_keys))) / estimated_error) * 100)}% "
                f"più piccolo dell'errore stimato.")
            error_list[inode] = len(ddiff.affected_root_keys)
            estimated_error_list[inode] = estimated_error
            print("--------------------------------------------------------------------")
    print("--------------------------------------------------------------------\n")
    for key in error_list:
        if error_list[key] - estimated_error_list[key] == 0:
            num_same_error += 1
        elif error_list[key] > estimated_error_list[key]:
            num_error_bound_destroyed += 1
        tot_error_found += error_list[key]
        tot_estimated_error += estimated_error_list[key]
    with open("results.txt", "a") as f_res:
        f_res.write("-----------------------------------------------------------------------")
        f_res.write(f"Risultati di {filename}")
        f_res.write("-----------------------------------------------------------------------")
        num_same_error_perc = f"Numero di volte in cui l'errore è stato il medesimo: {num_same_error} ->" \
                              f" {'{:.2f}'.format((num_same_error/len(error_list))*100)}%"
        num_out_error_bound = f"Numero di volte in cui l'error bound è stato violato: {num_error_bound_destroyed} ->" \
                              f" {'{:.2f}'.format((num_same_error/len(error_list))*100)}%"
        mean_error_diff = f"Differenza errore media: " \
                          f"{'{:.2f}'.format(((tot_estimated_error - tot_error_found) / tot_estimated_error)*100)}%"
        minval_estimated = min(estimated_error_list.values())
        res = str(list(filter(lambda x: estimated_error_list[x] == minval_estimated, estimated_error_list)))
        min_est_nodes = f"Nodi con errore minimo stimato, considerati nella modifica finale: {res}.\n" \
                        f"Essi, infatti, hanno errore stimato pari a: {minval_estimated}"
        f_res.write(num_same_error_perc)
        f_res.write(num_out_error_bound)
        f_res.write(mean_error_diff)
        f_res.write(min_est_nodes)
        f_res.write("-----------------------------------------------------------------------")
        f_res.write("-----------------------------------------------------------------------\n")
