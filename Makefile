CC=avr-gcc
MCU=attiny85

# Code under test
CUT=adder

TEST_LAUNCHER=run_test.sh

CFLAGS=-g -Wall -Werror -mmcu=$(MCU)
INCLUDE_DIRS=-I. -I$(TIMER_ROOT)/include

RESIDUE= \
	$(CUT).elf \
	Instructions.pyc \
	Program.pyc \
	System.pyc

test : $(CUT).elf
	./$(TEST_LAUNCHER)

$(CUT).elf : $(CUT).S
	$(CC) -c -o $@ $(CFLAGS) $(INCLUDE_DIRS) $<

.PHONY : clean
clean :
	rm -f $(RESIDUE)
