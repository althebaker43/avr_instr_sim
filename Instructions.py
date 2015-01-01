

class Instruction:

    CurInstructionAddr = 0

    def __init__(
            self
            ):
        self.instrAddr = Instruction.CurInstructionAddr
        Instruction.CurInstructionAddr += 2

    def execute(
            self,
            system
            ):
        return False


class RelJump(Instruction):

    def __init__(
            self,
            jumpAddr
            ):
        Instruction.__init__(self)
        self.jumpAddr = jumpAddr

    def __str__(self):
        return ('%x : rjmp %x' % (self.instrAddr, self.jumpAddr))


class Push(Instruction):

    def __init__(
            self,
            register
            ):
        Instruction.__init__(self)
        self.register = register

    def execute(
            self,
            system
            ):
        system.stack.append(
                system.registers[self.register]
                )
        return True

    def __str__(self):
        return ('%x : push r%d' % (self.instrAddr, self.register))


class Pop(Instruction):

    def __init__(
            self,
            register
            ):
        Instruction.__init__(self)
        self.register = register

    def execute(
            self,
            system
            ):
        system.registers[self.register] = system.stack.pop()
        return True

    def __str__(self):
        return ('%x : pop r%d' % (self.instrAddr, self.register))


class Add(Instruction):

    def __init__(
            self,
            destRegister,
            sourceRegister
            ):
        Instruction.__init__(self)
        self.destRegister = destRegister
        self.sourceRegister = sourceRegister

    def execute(
            self,
            system
            ):
        system.registers[self.destRegister] = system.registers[self.destRegister] + system.registers[self.sourceRegister]
        return True

    def __str__(self):
        return ('%x : add r%d,r%d' % (self.instrAddr, self.destRegister, self.sourceRegister))


class Move(Instruction):

    def __init__(
            self,
            destRegister,
            sourceRegister
            ):
        Instruction.__init__(self)
        self.destRegister = destRegister
        self.sourceRegister = sourceRegister

    def execute(
            self,
            system
            ):
        system.registers[self.destRegister] = system.registers[self.sourceRegister]
        return True

    def __str__(self):
        return ('%x : mov r%d,r%d' % (self.instrAddr, self.destRegister, self.sourceRegister))


class Return(Instruction):

    def __init__(
            self
            ):
        Instruction.__init__(self)

    def execute(
            self,
            system
            ):
        if (len(system.stack) == 0):
            system.isDone = True
        return True

    def __str__(self):
        return ('%s : ret' % (self.instrAddr))
