CC=avr-gcc
LD=avr-ld
MCU=attiny85

# Code under test
CUTS= \
	adder \
	multiplier
OBJS=$(CUTS:%=%.elf)

TEST_LAUNCHER=run_test.sh

CFLAGS=-g -Wall -Werror -mmcu=$(MCU)
INCLUDE_DIRS=-I. -I$(TIMER_ROOT)/include

RESIDUE= \
	$(OBJS) \
	$(OBJS:%.elf=%_unlinked.elf) \
	Instructions.pyc \
	Program.pyc \
	System.pyc

.PHONY : test
test : $(CUTS:%=test_%)

test_% : %.elf test_%.py
	./$(TEST_LAUNCHER) $*.elf test_$*.py

$(OBJS) : %.elf : %_unlinked.elf
	$(LD) -o $@ $<

$(OBJS:%.elf=%_unlinked.elf) : %_unlinked.elf : %.S
	$(CC) -c -o $@ $(CFLAGS) $(INCLUDE_DIRS) $<

.PHONY : clean
clean :
	rm -f $(RESIDUE)
