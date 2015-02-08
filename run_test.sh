#!/bin/bash

if [ $# -lt 2 ]
then
    echo "Usage: run_test.sh <elf> <test_script> [debug]" 1>&2
    exit 1
fi

ELF_FILE=$1
TEST_SCRIPT=$2

debug=0
if [ $# -eq 3 -a "$3" == "debug" ]
then
    debug=1
fi

LISTING=$ELF_FILE.lst
if [ $debug -eq 0 ]
then
    # Store the filtered assembly code listing in a temporary file
    LISTING=`mktemp`
fi

avr-objdump -d $ELF_FILE | awk -f filter_disasm.awk > $LISTING
python $TEST_SCRIPT $LISTING
