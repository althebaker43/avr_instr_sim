
import re

import Instructions


LABEL_REGEX = re.compile('^([0-9abcdef]+)\ <(.+)>:$')


def AddInstrRelJump(instr):
    offset = (instr & 0x0FFF)

    # Extend sign bit
    if ((offset & 0x0800) != 0):
        # Don't ask
        offset = -(((~(((~0) & (~0xFFF)) | offset))+1)<<1)

    return Instructions.RelJump(offset)

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

def AddInstrDec(instr):
    register = ((instr & 0x01F0) >> 4)
    return Instructions.Decrement(
            register
            )

def AddInstrTest(instr):
    register = (instr & 0x01F)
    return Instructions.Test(
            register
            )

def AddInstrMove(instr):
    destRegister = ((instr & 0x01F0) >> 4)
    sourceRegister = (((instr & 0x0200) >> 5) | (instr & 0x000F))
    return Instructions.Move(
            destRegister,
            sourceRegister
            )

def AddInstrBranchEqual(instr):
    offset = ((instr & 0x03F8) >> 2)
    return Instructions.BranchEqual(
            offset
            )


OpCodeInstructionMap = {
    0x3 :   AddInstrAdd,
    0x8 :   AddInstrTest,
    0xB :   AddInstrMove,
    0xC :   AddInstrRelJump,
    0x1E1 : AddInstrBranchEqual,
    0x48F : AddInstrPop,
    0x49F : AddInstrPush,
    0x4A8 : AddInstrReturn,
    0x4AA : AddInstrDec
    }


def GetOpCode(instr):

    opcode = 0

    msNibble = ((instr & 0xF000)>>12)
    if (msNibble == 0x9):
        opcode = ((msNibble << 7) | ((instr & 0x0E00) >> 5) | (instr & 0x000F))
    elif (msNibble == 0xF):
        opcode = ((msNibble << 5) | ((instr & 0x0C00) >> 7) | (instr & 0x0007))
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

