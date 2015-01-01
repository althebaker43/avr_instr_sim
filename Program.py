
import re

import Instructions


LABEL_REGEX = re.compile('^([0-9abcdef]+)\ <(.+)>:$')


def AddInstrRelJump(instr):
    jumpAddr = (instr & 0x0FFF)
    return Instructions.RelJump(jumpAddr)

def AddInstrPush(instr):
    register = ((instr & 0x01F0) >> 4)
    return Instructions.Push(register)

def AddInstrPop(instr):
    register = ((instr & 0x01F0) >> 4)
    return Instructions.Pop(register)

def AddInstrReturn(instr):
    return Instructions.Return()

def AddInstrAdd(instr):
    destRegister = ((instr & 0x01F0) >> 4)
    sourceRegister = (((instr & 0x0200) >> 5) | (instr & 0x000F))
    return Instructions.Add(
            destRegister,
            sourceRegister
            )

def AddInstrMove(instr):
    destRegister = ((instr & 0x01F0) >> 4)
    sourceRegister = (((instr & 0x0200) >> 5) | (instr & 0x000F))
    return Instructions.Move(
            destRegister,
            sourceRegister
            )


OpCodeInstructionMap = {
    0x3 : AddInstrAdd,
    0xB : AddInstrMove,
    0xC : AddInstrRelJump,
    0x48 : AddInstrPop,
    0x49 : AddInstrPush,
    0x4A : AddInstrReturn
    }


def GetOpCode(instr):

    opcode = 0

    msNibble = ((instr & 0xF000)>>12)
    if (msNibble == 0x9):
        opcode = ((msNibble << 3) | ((instr & 0x0E00) >> 9))
    elif (msNibble == 0x0 or msNibble == 0x2):
        opcode = ((msNibble << 2) | ((instr & 0x0C00) >> 10))
    else:
        opcode = msNibble

    return opcode


class Program:

    def __init__(
            self,
            programFile
            ):

        self.labels = {}
        self.instructions = []

        while (True):

            curLine = programFile.readline()
            if (curLine == ''):
                break

            # Process label
            labelMatches = LABEL_REGEX.match(curLine)
            if (labelMatches != None and len(labelMatches.groups()) == 2):
                label = labelMatches.group(2)
                addr = int(labelMatches.group(1), 16)
                self.labels[label] = addr
                continue

            # Process instruction
            instr = int(curLine, 16)
            opCode = GetOpCode(instr)
            if (opCode not in OpCodeInstructionMap):
                print('Error: %x not a valid instruction.' % instr)
                break

            instrCreator = OpCodeInstructionMap[opCode]
            self.instructions.append(instrCreator(instr))

