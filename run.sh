#!/bin/bash
FILES="$(pwd)/verilogs/*_opt.v"
# remove comment below to have table header in results.txt
#echo -e "Nome funzione\t& Num. nodi interessanti\t& \% Nodi interessanti\t& Errore stimato\t& Err. min ttable\t& Err. max ttable\t& d err. min ttable - stimato\t& d err. max ttable - stimato\t& \% guadagno M_(C)" > results.txt
for ff in $FILES
do
# FAILSAFE #
# Check if "$ff" FILE exists and is a regular file and then execute xubee #
  if [ -f "$ff" ]
  then
    echo "Processing $(basename "$ff") file..."
    python main.py "$ff" #| tee -a log.txt #remove comment to have a more detailed log stored as a file
  else
    echo "Warning: Some problem with \"$ff\""
  fi
done