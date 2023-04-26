# xubee
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg?style=flat&logo=python&logoColor=white)](https://www.python.org/downloads/release/python-3112/)

A tool for XAG Error Estimation.
It is created during my Master Degree in Cybersecurity, whose focus was to try to implement Approximate Logic Synthesis to Secure Two-Party Computation.
This program implement two algorithms that apply error estimation theorem proved in thesis work.

## PLA generation

To generate pla (functions) run:

    python pla_generator.py

1. Insert the number of inputs the function should have;
2. Insert the quantity of function you want to generate.

Resulting functions need to be processed by [ABC](https://github.com/berkeley-abc/abc) tool (pla -> verilog) and then by [Mockturtle](https://github.com/lsils/mockturtle) (AIG -> XAG).

## Preliminaries

To run the program over XAGs, Linux is strongly recommended. If you have another OS, you have to adapt the code to process multiple files in input.

Before running the program, remember to modify the absolute path to verilog files (see `main.py`).
It has to be consistent with the path specified in `run.sh`.

If you want to have log in different file (`log.txt`) or the result of the computation with a header in `results.txt`, you have to uncomment/modify some code lines of `run.sh`.

Furthermore, if you want to use a specific algorithm, you have to modify `main.py`. The default one is the most granular.

All XAGs used to test the tool are available in `all_verilogs.zip`.

**Final consideration: the program described in thesis is downloadable "as is" in release 1.0. Any further modification will be eventually implemented in other releases or just committed to the repo.**

## Run the program

For Linux users, open the terminal in project directory and run:

    bash run.sh

The output is written in `results.txt` and represent data in LaTeX table format.

If you want to compute only error estimation and not both error estimation and exact error, please consider to modify the code commenting truth table and timer generation and the output parameters.