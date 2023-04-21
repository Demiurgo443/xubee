# Xag Error Estimation

import sys
from utility import parser, to_file
from core import error_estimation_4i, error_estimation
from copy import deepcopy

if __name__ == '__main__':

    # makes this program launchable with bash scripts
    filename = sys.argv[1]

    # xag2, nodes_of_interest2 = parser("verilogs10i/e_pla_10i_16.v_opt.v")
    # xag2, nodes_of_interest2 = parser("miei_verilogs/e_pla_6i_001.v_opt.v")
    xag2, nodes_of_interest = parser(f"{filename}")
    xag = deepcopy(xag2)

    filename = filename.removeprefix("/YOUR/ABSOLUTE/PATH/TO/VERILOG/FILES/")

    print("--------------------------------------------------------------------")
    print(f"|                   Analyzing {filename}                       |")
    print("--------------------------------------------------------------------")

    if len(nodes_of_interest) == 0:
        print("No node has passed selection criteria.\n")
    else:
        if xag2.input_num == 4:
            estimated_e_dict, exact_e_dict, f_elapsed_time, tt_elapsed_time = error_estimation_4i(xag2, xag,
                                                                                                  nodes_of_interest)
            if len(estimated_e_dict) == 0 and len(exact_e_dict) == 0:
                print("No suitable node found during error estimation phase.")
            else:
                print(f"Estimated errors: {estimated_e_dict}")
                print(f"Exact errors: {exact_e_dict}")
                to_file(filename, xag, estimated_e_dict, exact_e_dict, f_elapsed_time, tt_elapsed_time)
        else:
            estimated_e_dict, exact_e_dict, f_elapsed_time, tt_elapsed_time = error_estimation(xag2, xag,
                                                                                               nodes_of_interest)
            if len(estimated_e_dict) == 0 and len(exact_e_dict) == 0:
                print("No suitable node found during error estimation phase.")
            else:
                print(f"Estimated errors: {estimated_e_dict}")
                print(f"Exact errors: {exact_e_dict}")
                to_file(filename, xag, estimated_e_dict, exact_e_dict, f_elapsed_time, tt_elapsed_time)
