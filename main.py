# Xag Upper Bound Error Evaluation (valuta se inserire uno fra i seguenti termini: Experimental, Estimation, Framework)

# import sys
from utility import parser

if __name__ == '__main__':
    truth_table = {}
    truth_table_2 = {}
    error_list = {}

    # makes this program launchable with bash scripts
    # filename = sys.argv[1]

    # TODO sobstitute "e_pla_6i_1.v_opt.v" with filename variable when program is finished

    # xag, nodes_of_interest = parser("verilogs/x7dn.v_opt.v")
    # xag2, nodes_of_interest2 = parser("verilogs/x7dn.v_opt.v")
    # xag, nodes_of_interest = parser("verilogs/e_pla_4i_5_xor.v_opt.v")
    # xag2, nodes_of_interest2 = parser("verilogs/e_pla_4i_5_xor.v_opt.v")
    xag, nodes_of_interest = parser("verilogs/e_pla_6i_1.v_opt.v")
    xag2, nodes_of_interest2 = parser("verilogs/e_pla_6i_1.v_opt.v")

    max_num = 2 ** xag.input_num
    for val in range(max_num):
        truth_table = xag.run_input(val, truth_table)
    print(truth_table)
