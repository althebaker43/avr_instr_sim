
class System:

    def __init__(self):

        self.registers = []
        for index in range(32):
            self.registers.append(0)

        self.programCounter = 0

        self.stack = []

        self.isDone = False


    def run(
            self,
            program
            ):

        self.isDone = False

        for instr in program.instructions:

            if (instr.execute(self) == False):
                print('Error: execution failed at the following instruction: %s' % instr)
                break

            if (self.isDone == True):
                break

            self.programCounter += 2


    def dump(
            self,
            dumpFile
            ):

        dumpFile.write('System Dump:\n')

        dumpFile.write('Program Counter : %x\n' % self.programCounter)

        for index in range(len(self.registers)-1):
            dumpFile.write('  r%d : %x\n' % (index, self.registers[index]))

        dumpFile.write('Stack:\n')
        for word in self.stack:
            dumpFile.write('  %x\n' % word)
