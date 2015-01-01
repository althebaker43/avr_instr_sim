#!/bin/bash

# Store the filtered assembly code listing in a temporary file
LISTING=`mktemp`

avr-objdump -d adder.elf | awk -f filter_disasm.awk > $LISTING
python test_adder.py $LISTING
