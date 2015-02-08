#!/usr/bin/python

import sys
import unittest

import Program
import System


ProgramListingFileName = ''


class TestMultiplier(unittest.TestCase):

    def setUp(self):

        programListingFile = open(ProgramListingFileName, 'r')
        self.program = Program.Program(programListingFile)
        programListingFile.close()

        self.system = System.System()


    def test_simple(self):

        self.system.registers[16] = 3
        self.system.registers[17] = 2
        self.system.run(self.program)

        self.assertEqual(6, self.system.registers[18])
        self.assertEqual(3, self.system.registers[16])
        self.assertEqual(2, self.system.registers[17])


if (__name__ == "__main__"):

    if (len(sys.argv) < 2):
        print('Usage: %s <program_listing> [<unittest_options>]' % sys.argv[0])
        sys.exit(1)

    ProgramListingFileName = sys.argv.pop(1)
    unittest.main()
