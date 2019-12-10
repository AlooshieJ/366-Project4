# Authors: Matthew Braniff, Trent Mathews, Michael Wenzl
# Version: Final

import math

currCycle = 0


# -------------------asm function definitions-------------------------#
# This is all of our instruction functions
def addi(instr, config, data, stage=1):
    if (config.processorType):  # AP
        if(stage == 1):
            # Decode
            control.RegWrite = 1
            control.MemtoReg = 0
            control.MemWrite = 0
            control.ALUControl = 2
            control.ALUSrc = 1
            control.RegDst = 0
            control.Branch = 0
            control.regwritecount += 1
            control.alusrccount += 1
        else:
            if (pipeLine.SrcA & pow(2, 31)):
                pipeLine.SrcA = -1 * ((pipeLine.SrcA ^ (pow(2, 32) - 1)) + 1)
            pipeLine.ALUOut = (pipeLine.SrcA + pipeLine.SrcB) & (pow(2, 32) - 1)

    else:  # MC
        # Cycle 3
        control.ALUSrcA = 1
        control.ALUSrcB = 2
        control.ALUControl = 2
        data.regALUOut = data.read(instr.rs) + instr.imm
        data.regALUOut = data.regALUOut & int("0xFFFFFFFF", 16)  # This stops any overflow
        control.alusrccount += 1

        debugCheck(config, data)

        # Cycle 4
        control.RegDst = 0
        control.MemtoReg = 0
        control.RegWrite = 1
        control.regwritecount += 1
        control.fourcycle += 1
        data.write(instr.rt, data.regALUOut)

        debugCheck(config, data)

    return


def addu(instr, config, data, stage=1):
    if (config.processorType):  # AP
        if (stage == 1):
            # Decode
            control.RegWrite = 1
            control.MemtoReg = 0
            control.MemWrite = 0
            control.ALUControl = 2
            control.ALUSrc = 0
            control.RegDst = 1
            control.Branch = 0
            control.regwritecount += 1
            control.regdstcount += 1
        else:
            if (pipeLine.SrcA < 0):
                pipeLine.SrcA = pow(2, 32) + pipeLine.SrcA
            if (pipeLine.SrcB < 0):
                pipeLine.SrcB = pow(2, 32) + pipeLine.SrcB
            pipeLine.ALUOut = (pipeLine.SrcA + pipeLine.SrcB) & (pow(2, 32) - 1)
    else:  # MC
        # Cycle 3
        control.ALUSrcA = 1
        control.ALUSrcB = 0
        control.ALUControl = 2
        rs = data.regRead1
        rt = data.regRead2
        if (rs < 0):
            rs *= -1
            rs = (rs ^ int("0xffffffff", 16)) + 1
        if (rt < 0):
            rt *= -1
            rt = (rs ^ int("0xffffffff", 16)) + 1
        data.regALUOut = rs + rt
        data.regALUOut = data.regALUOut & int("0xFFFFFFFF", 16)

        debugCheck(config, data)

        # Cycle 4
        control.RegDst = 1
        control.MemtoReg = 0
        control.RegWrite = 1
        control.regwritecount += 1
        control.regdstcount += 1
        control.fourcycle += 1
        data.write(instr.rd, data.regALUOut)

        debugCheck(config, data)

    return


def addiu(instr, config, data, stage=1):
    if (config.processorType):  # AP
        if (stage == 1):
            # Decode
            control.RegWrite = 1
            control.MemtoReg = 0
            control.MemWrite = 0
            control.ALUControl = 2
            control.ALUSrc = 1
            control.RegDst = 0
            control.Branch = 0
            control.regwritecount += 1
            control.alusrccount += 1
        else:
            if(pipeLine.SrcA < 0):
                pipeLine.SrcA = pow(2,32) + pipeLine.SrcA
            pipeLine.ALUOut = (pipeLine.SrcA + pipeLine.SrcB) & (pow(2, 32) - 1)
    else:  # MC
        # Cycle 3
        control.ALUSrcA = 1
        control.ALUSrcB = 2
        control.ALUControl = 2
        if (instr.imm < 0):
            mask = int("0xFFFF0000", 16)
            instr.imm *= -1
            instr.imm = twosComp(instr.imm) | mask
        data.regALUOut = data.read(instr.rs) + instr.imm
        data.regALUOut = data.regALUOut & int("0xFFFFFFFF", 16)
        control.alusrccount += 1

        debugCheck(config, data)

        # Cycle 4
        control.RegDst = 0
        control.MemtoReg = 0
        control.RegWrite = 1
        control.regwritecount += 1
        control.fourcycle += 1
        data.write(instr.rt, data.regALUOut)

        debugCheck(config, data)

    return


def j(instr, config, data):
    if (config.processorType):  # AP
        print("AP")
    else:  # MC
        # Cycle 3
        control.ALUSrcA = 0
        control.ALUSrcB = 2
        control.ALUControl = 2
        pc = format(data.read("pc"), '032b')
        data.regALUOut = int(pc[0:6] + str(format(int(instr.jump * 4), '026b')), 2)

        debugCheck(config, data)

        # Cycle 4
        control.RegDst = 0
        control.MemtoReg = 0
        control.RegWrite = 1
        control.regwritecount += 1
        control.threecycle += 1
        data.write(instr.rt, data.regALUOut)

        debugCheck(config, data)

    return


def lb(instr, config, data, stage=1):
    if (config.processorType):  # AP
        if (stage == 1):
            control.RegWrite = 1
            control.MemtoReg = 1
            control.MemWrite = 0
            control.ALUControl = 2
            control.ALUSrc = 1
            control.RegDst = 0
            control.Branch = 0
            control.regwritecount += 1
            control.alusrccount += 1
            control.memtoregcount += 1
        if (stage == 2):
            pipeLine.ALUOut = pipeLine.SrcA + pipeLine.SrcB
    else:  # MC
        # Cycle 3
        control.ALUSrcA = 1
        control.ALUSrcB = 2
        control.ALUControl = 2
        data.regALUOut = data.regRead1 + instr.imm
        data.regALUOut = data.regALUOut & int("0xFFFFFFFF", 16)
        control.alusrccount += 1

        debugCheck(config, data)

        # Cycle 4
        control.IorD = 1

        global cache
        code = memDecode(config, data.regRead1 + instr.imm)
        result = cache.read(config, code, False)

        data.regData = result

        debugCheck(config, data)

        # Cycle 5
        control.RegDst = 0
        control.MemtoReg = 1
        control.RegWrite = 1
        control.regwritecount += 1
        control.memtoregcount += 1
        control.fivecycle += 1
        data.write(instr.rt, data.regData)

        debugCheck(config, data)
    return


def sb(instr, config, data, stage=1):
    if (config.processorType):  # AP
        if (stage == 1):
            control.RegWrite = 0
            control.MemtoReg = 0
            control.MemWrite = 1
            control.ALUControl = 2
            control.ALUSrc = 1
            control.RegDst = 0
            control.Branch = 0
            control.memwritecount  += 1
            control.regwritecount += 1
            control.alusrccount += 1
        else:
            pipeLine.ALUOut = pipeLine.SrcA + pipeLine.SrcB
    else:  # MC
        # Cycle 3
        control.ALUSrcA = 1
        control.ALUSrcB = 2
        control.ALUControl = 2
        data.regALUOut = data.regRead1 + instr.imm
        control.alusrccount += 1

        debugCheck(config, data)

        # Cycle 4
        control.IorD = 1
        control.MemWrite = 1
        control.memwritecount += 1
        control.fourcycle += 1

        global cache
        code = memDecode(config, data.regRead1 + instr.imm)
        cache.write(config, code, data.regRead2, False)

        debugCheck(config, data)
    return


def lw(instr, config, data, stage=1):
    if (config.processorType):  # AP
        if(stage == 1):
            control.RegWrite = 1
            control.MemtoReg = 1
            control.MemWrite = 0
            control.ALUControl = 2
            control.ALUSrc = 1
            control.RegDst = 0
            control.Branch = 0
            control.regwritecount += 1
            control.memtoregcount += 1
            control.alusrccount += 1
        if(stage == 2):
            pipeLine.ALUOut = pipeLine.SrcA + pipeLine.SrcB
    else:  # MC
        # Cycle 3
        control.ALUSrcA = 1
        control.ALUSrcB = 2
        control.ALUControl = 2
        data.regALUOut = data.regRead1 + instr.imm
        control.alusrccount += 1

        debugCheck(config, data)

        # Cycle 4
        control.IorD = 1

        global cache
        code = memDecode(config, data.regRead1 + instr.imm)
        result = cache.read(config, code, True)

        data.regData = result

        debugCheck(config, data)

        # Cycle 5
        control.RegDst = 0
        control.MemtoReg = 1
        control.RegWrite = 1
        control.regwritecount += 1
        control.memtoregcount += 1
        control.fivecycle += 1
        data.write(instr.rt, data.regData)

        debugCheck(config, data)
    return


def sw(instr, config, data, stage=1):
    if (config.processorType):  # AP
        if(stage == 1):
            control.RegWrite = 0
            control.MemtoReg = 0
            control.MemWrite = 1
            control.ALUControl = 2
            control.ALUSrc = 1
            control.RegDst = 0
            control.Branch = 0
            control.memwritecount += 1
            control.alusrccount += 1
        else:
            pipeLine.ALUOut = pipeLine.SrcA + pipeLine.SrcB
    else:  # MC
        # Cycle 3
        control.ALUSrcA = 1
        control.ALUSrcB = 2
        control.ALUControl = 2
        data.regALUOut = data.regRead1 + instr.imm
        control.alusrccount += 1

        debugCheck(config, data)

        # Cycle 4
        control.IorD = 1
        control.MemWrite = 1
        control.memwritecount += 1
        control.fourcycle += 1

        global cache
        code = memDecode(config, data.regRead1 + instr.imm)
        cache.write(config, code, data.regRead2, True)

        debugCheck(config, data)

    return


def beq(instr, config, data, stage=1):
    if (config.processorType):  # AP
        if(stage == 1):
            control.RegWrite = 0
            control.MemtoReg = 0
            control.MemWrite = 0
            control.ALUControl = 0
            control.ALUSrc = 0
            control.RegDst = 0
            control.Branch = 1
            control.brachcount += 1
    else:  # MC
        # Cycle 3
        control.ALUSrcA = 1
        control.ALUSrcB = 0
        control.ALUControl = 6
        control.Branch = 1
        control.PCSrc = 1
        control.brachcount += 1
        control.threecycle += 1
        if (data.regRead1 == data.regRead2):
            data.write("pc", data.regALUOut)

        debugCheck(config, data)
    return


def bne(instr, config, data, stage=1):
    if (config.processorType):  # AP
        if (stage == 1):
            control.RegWrite = 0
            control.MemtoReg = 0
            control.MemWrite = 0
            control.ALUControl = 0
            control.ALUSrc = 0
            control.RegDst = 0
            control.Branch = 1
            control.brachcount += 1
    else:  # MC
        # Cycle 3
        control.ALUSrcA = 1
        control.ALUSrcB = 0
        control.ALUControl = 6
        control.Branch = 1
        control.brachcount += 1
        control.threecycle += 1
        control.PCSrc = 1
        if (data.regRead1 != data.regRead2):
            data.write("pc", data.regALUOut)

        debugCheck(config, data)
    return


def add(instr, config, data, stage=1):
    if (config.processorType):  # AP
        if(stage == 1):
            control.RegWrite = 1
            control.MemtoReg = 0
            control.MemWrite = 0
            control.ALUControl = 2
            control.ALUSrc = 0
            control.RegDst = 1
            control.Branch = 0
            control.regwritecount += 1
            control.regdstcount += 1
        else:
            if (pipeLine.SrcA & pow(2, 31)):
                pipeLine.SrcA = -1 * ((pipeLine.SrcA ^ (pow(2, 32) - 1)) + 1)
            if (pipeLine.SrcB & pow(2, 31)):
                pipeLine.SrcB = -1 * ((pipeLine.SrcB ^ (pow(2, 32) - 1)) + 1)
            pipeLine.ALUOut = (pipeLine.SrcA + pipeLine.SrcB) & (pow(2, 32) - 1)
    else:  # MC
        control.ALUSrcA = 1
        control.ALUSrcB = 0
        control.ALUControl = 2
        rs = data.regRead1
        rt = data.regRead2
        data.regALUOut = rs + rt
        data.regALUOut = data.regALUOut & int("0xFFFFFFFF", 16)

        debugCheck(config, data)

        # Cycle 4
        control.RegDst = 1
        control.MemtoReg = 0
        control.RegWrite = 1
        control.regwritecount += 1
        control.regdstcount += 1
        control.fourcycle += 1
        data.write(instr.rd, data.regALUOut)

        debugCheck(config, data)
    return


def sub(instr, config, data, stage=1):
    if (config.processorType):  # AP
        if (stage == 1):
            control.RegWrite = 1
            control.MemtoReg = 0
            control.MemWrite = 0
            control.ALUControl = 6
            control.ALUSrc = 0
            control.RegDst = 1
            control.Branch = 0
            control.regwritecount += 1
            control.regdstcount += 1
        else:
            if(pipeLine.SrcA & pow(2, 31)):
                pipeLine.SrcA = -1 * ((pipeLine.SrcA ^ (pow(2, 32) - 1)) + 1)
            if (pipeLine.SrcB & pow(2, 31)):
                pipeLine.SrcB = -1 * ((pipeLine.SrcB ^ (pow(2, 32) - 1)) + 1)
            result = pipeLine.SrcA - pipeLine.SrcB
            if(result < 0):
                result = (pow(2,32) + result) & (pow(2, 32) - 1)
            pipeLine.ALUOut = result
    else:  # MC
        control.ALUSrcA = 1
        control.ALUSrcB = 0
        control.ALUControl = 6
        rs = data.regRead1
        rt = data.regRead2
        data.regALUOut = rs - rt
        data.regALUOut = data.regALUOut & int("0xFFFFFFFF", 16)

        debugCheck(config, data)

        # Cycle 4
        control.RegDst = 1
        control.MemtoReg = 0
        control.RegWrite = 1
        control.regwritecount += 1
        control.regdstcount += 1
        control.fourcycle += 1
        data.write(instr.rd, data.regALUOut)

        debugCheck(config, data)
    return


def slt(instr, config, data, stage=1):
    if (config.processorType):  # AP
        if (stage == 1):
            control.RegWrite = 1
            control.MemtoReg = 0
            control.MemWrite = 0
            control.ALUControl = 7
            control.ALUSrc = 0
            control.RegDst = 1
            control.Branch = 0
            control.regwritecount += 1
            control.regdstcount += 1
        else:
            if(pipeLine.SrcA & pow(2,31)):
                pipeLine.SrcA = -1 * ((pipeLine.SrcA ^ (pow(2,32) - 1)) + 1)
            if (pipeLine.SrcB & pow(2, 31)):
                pipeLine.SrcB = -1 * ((pipeLine.SrcB ^ (pow(2, 32) - 1)) + 1)
            pipeLine.ALUOut = (pipeLine.SrcA < pipeLine.SrcB)
    else:
        # Cycle 3
        control.ALUSrcA = 1
        control.ALUSrcB = 0
        control.ALUControl = 7
        temp1 = data.regRead1
        temp2 = data.regRead2
        if (data.regRead1 & pow(2, 31)):
            temp1 = (data.regRead1 ^ (pow(2, 32) - 1)) + 1
            temp1 *= -1
        if (data.regRead2 & pow(2, 31)):
            temp2 = (data.regRead2 ^ (pow(2, 32) - 1)) + 1
            temp2 *= -1
        data.regALUOut = (temp1 < temp2)

        debugCheck(config, data)

        # Cycle 4
        control.RegDst = 1
        control.MemtoReg = 0
        control.RegWrite = 1
        control.regwritecount += 1
        control.regdstcount += 1
        control.fourcycle += 1
        data.write(instr.rd, data.regALUOut)

        debugCheck(config, data)

    return


def srl(instr, config, data, stage=1):
    if (config.processorType):  # AP
        if(stage == 1):
            control.RegWrite = 1
            control.MemtoReg = 0
            control.MemWrite = 0
            control.ALUSrc = 0
            control.RegDst = 1
            control.Branch = 0
            control.regwritecount += 1
            control.regdstcount += 1
        else:
            if(pipeLine.SrcB < 0):
                pipeLine.SrcB = pow(2, 32) + pipeLine.SrcB
            pipeLine.ALUOut = (pipeLine.SrcB >> pipeLine.E.shamt) & (pow(2, 32) - 1)
    else:  # MC
        # Cycle 3
        temp = data.read(instr.rt)
        if (temp < 0):
            temp *= -1
            temp = (temp ^ int("0xffffffff", 16)) + 1
        control.ALUSrcA = 1
        control.ALUSrcB = 0
        data.regALUOut = temp >> int(instr.sh)

        debugCheck(config, data)

        # Cycle 4
        control.RegDst = 1
        control.MemtoReg = 0
        control.RegWrite = 1
        control.regwritecount += 1
        control.regdstcount += 1
        control.fourcycle += 1
        data.write(instr.rd, data.regALUOut)

        debugCheck(config, data)
    return


def sll(instr, config, data, stage=1):
    if (config.processorType):  # AP
        if (stage == 1):
            control.RegWrite = 1
            control.MemtoReg = 0
            control.MemWrite = 0
            control.ALUSrc = 0
            control.RegDst = 1
            control.Branch = 0
            control.regwritecount += 1
            control.regdstcount += 1
        else:
            if (pipeLine.SrcB < 0):
                pipeLine.SrcB = pow(2, 32) + pipeLine.SrcB
            pipeLine.ALUOut = (pipeLine.SrcB << pipeLine.E.shamt) & (pow(2, 32) - 1)
    else:  # MC
        # Cycle 3
        temp = data.read(instr.rt)
        if (temp < 0):
            temp *= -1
            temp = (temp ^ int("0xffffffff", 16)) + 1
        control.ALUSrcA = 1
        control.ALUSrcB = 0
        data.regALUOut = temp << int(instr.sh)

        debugCheck(config, data)

        # Cycle 4
        control.RegDst = 1
        control.MemtoReg = 0
        control.RegWrite = 1
        control.regwritecount += 1
        control.regdstcount += 1
        control.fourcycle += 1
        data.write(instr.rd, data.regALUOut)

        debugCheck(config, data)
    return


def sltu(instr, config, data, stage=1):
    if (config.processorType):  # AP
        if (stage == 1):
            control.RegWrite = 1
            control.MemtoReg = 0
            control.MemWrite = 0
            control.ALUControl = 7
            control.ALUSrc = 0
            control.RegDst = 1
            control.Branch = 0
            control.regwritecount += 1
            control.regdstcount += 1
        else:
            if (pipeLine.SrcA < 0):
                pipeLine.SrcA = pow(2, 32) + pipeLine.SrcA
            if (pipeLine.SrcB < 0):
                pipeLine.SrcB = pow(2, 32) + pipeLine.SrcB
            pipeLine.ALUOut = (pipeLine.SrcA < pipeLine.SrcB)
    else:
        # Cycle 3
        control.ALUSrcA = 1
        control.ALUSrcB = 0
        control.ALUControl = 7
        temp1 = data.read(instr.rs)
        temp2 = data.read(instr.rt)
        if (temp1 < 0):  # If the value is negative get the twos compliment
            temp1 *= -1
            temp1 = (temp1 ^ (int("0xffffffff", 16))) + 1
        if (temp2 < 0):  # If the value is negative get the twos compliment
            temp2 *= -1
            temp2 = (temp2 ^ (int("0xffffffff", 16))) + 1
        data.regALUOut = (temp1 < temp2)

        debugCheck(config, data)

        # Cycle 4
        control.RegDst = 1
        control.MemtoReg = 0
        control.RegWrite = 1
        control.regwritecount += 1
        control.regdstcount += 1
        control.fourcycle += 1
        data.write(instr.rd, data.regALUOut)

        debugCheck(config, data)
    return


def andi(instr, config, data, stage=1):
    if (config.processorType):  # AP
        if (stage == 1):
            # Decode
            control.RegWrite = 1
            control.MemtoReg = 0
            control.MemWrite = 0
            control.ALUControl = 0
            control.ALUSrc = 1
            control.RegDst = 0
            control.Branch = 0
            control.regwritecount += 1
            control.alusrccount += 1
        else:
            if (pipeLine.SrcA < 0):
                pipeLine.SrcA = pow(2, 32) + pipeLine.SrcA
            if (pipeLine.SrcB < 0):
                pipeLine.SrcB = pow(2, 32) + pipeLine.SrcB
            pipeLine.ALUOut = pipeLine.SrcA & pipeLine.SrcB
    else:  # MC
        # Cycle 3
        control.ALUSrcA = 1
        control.ALUSrcB = 2
        control.ALUControl = 0
        imm = instr.imm
        rs = data.regRead1
        if (imm < 0):
            imm *= -1
            imm = twosComp(imm)
        if (rs < 0):
            rs *= -1
            rs = (rs ^ int("0xffffffff", 16)) + 1
        data.regALUOut = rs & imm
        control.alusrccount += 1

        debugCheck(config, data)

        # Cycle 4
        control.RegDst = 0
        control.MemtoReg = 0
        control.RegWrite = 1
        control.regwritecount += 1
        control.fourcycle += 1
        data.write(instr.rt, data.regALUOut)

        debugCheck(config, data)
    return


def lui(instr, config, data, stage=1):
    if (config.processorType):  # AP
        if (stage == 1):
            # Decode
            control.RegWrite = 1
            control.MemtoReg = 0
            control.MemWrite = 0
            control.ALUControl = 0
            control.ALUSrc = 1
            control.RegDst = 0
            control.Branch = 0
            control.regwritecount += 1
            control.alusrccount += 1
        else:
            if (pipeLine.SrcB < 0):
                pipeLine.SrcB = pow(2, 16) + pipeLine.SrcB
            pipeLine.ALUOut = pipeLine.SrcB << 16
    else:  # MC

        # Cycle 3
        control.ALUSrcA = 1
        control.ALUSrcB = 2
        if (instr.imm < 0):
            instr.imm *= -1
            instr.imm = (instr.imm ^ pow(2, 16)) + 1
        data.regALUOut = instr.imm << 16
        control.alusrccount += 1

        debugCheck(config, data)

        # Cycle 4
        control.RegDst = 0
        control.MemtoReg = 0
        control.RegWrite = 1
        control.regwritecount += 1
        control.fourcycle += 1
        data.write(instr.rt, data.regALUOut)

        debugCheck(config, data)
    return


def ori(instr, config, data, stage=1):
    if (config.processorType):  # AP
        if (stage == 1):
            # Decode
            control.RegWrite = 1
            control.MemtoReg = 0
            control.MemWrite = 0
            control.ALUControl = 1
            control.ALUSrc = 1
            control.RegDst = 0
            control.Branch = 0
            control.regwritecount += 1
            control.alusrccount += 1
        else:
            if (pipeLine.SrcA < 0):
                pipeLine.SrcA = pow(2, 32) + pipeLine.SrcA
            if (pipeLine.SrcB < 0):
                pipeLine.SrcB = pow(2, 32) + pipeLine.SrcB
            pipeLine.ALUOut = pipeLine.SrcA | pipeLine.SrcB
    else:  # MC

        # Cycle 3
        control.ALUSrcA = 1
        control.ALUSrcB = 2
        control.ALUControl = 1
        if (instr.imm < 0):
            instr.imm *= -1
            instr.imm = (instr.imm ^ pow(2, 16)) + 1
        data.regALUOut = data.regRead1 | instr.imm
        control.alusrccount += 1

        debugCheck(config, data)

        # Cycle 4
        control.RegDst = 0
        control.MemtoReg = 0
        control.RegWrite = 1
        control.regwritecount += 1
        control.fourcycle += 1
        data.write(instr.rt, data.regALUOut)

        debugCheck(config, data)
    return


def andd(instr, config, data, stage=1):
    if (config.processorType):  # AP
        if (stage == 1):
            # Decode
            control.RegWrite = 1
            control.MemtoReg = 0
            control.MemWrite = 0
            control.ALUControl = 0
            control.ALUSrc = 0
            control.RegDst = 1
            control.Branch = 0
            control.regwritecount += 1
            control.regdstcount += 1
        else:
            if (pipeLine.SrcA < 0):
                pipeLine.SrcA = pow(2, 32) + pipeLine.SrcA
            if (pipeLine.SrcB < 0):
                pipeLine.SrcB = pow(2, 32) + pipeLine.SrcB
            pipeLine.ALUOut = pipeLine.SrcA & pipeLine.SrcB
    else:
        # Cycle 3
        control.ALUSrcA = 1
        control.ALUSrcB = 0
        control.ALUControl = 7
        rs = data.read(instr.rs)
        rt = data.read(instr.rt)
        if (rs < 0):  # If the value is negative get the twos compliment
            rs *= -1
            rs = (rs ^ (int("0xffffffff", 16))) + 1
        if (rt < 0):  # If the value is negative get the twos compliment
            rt *= -1
            rt = (rt ^ (int("0xffffffff", 16))) + 1
        data.regALUOut = rs & rt

        debugCheck(config, data)

        # Cycle 4
        control.RegDst = 1
        control.MemtoReg = 0
        control.RegWrite = 1
        control.regwritecount += 1
        control.regdstcount += 1
        control.fourcycle += 1
        data.write(instr.rd, data.regALUOut)

        debugCheck(config, data)
    return


def xor(instr, config, data, stage=1):
    if (config.processorType):  # AP
        if (stage == 1):
            # Decode
            control.RegWrite = 1
            control.MemtoReg = 0
            control.MemWrite = 0
            control.ALUControl = 0
            control.ALUSrc = 0
            control.RegDst = 1
            control.Branch = 0
            control.regwritecount += 1
            control.regdstcount += 1
        else:
            if (pipeLine.SrcA < 0):
                pipeLine.SrcA = pow(2, 32) + pipeLine.SrcA
            if (pipeLine.SrcB < 0):
                pipeLine.SrcB = pow(2, 32) + pipeLine.SrcB
            pipeLine.ALUOut = pipeLine.SrcA ^ pipeLine.SrcB
    else:
        # Cycle 3
        control.ALUSrcA = 1
        control.ALUSrcB = 0
        control.ALUControl = 7
        rs = data.read(instr.rs)
        rt = data.read(instr.rt)
        if (rs < 0):  # If the value is negative get the twos compliment
            rs *= -1
            rs = (rs ^ (int("0xffffffff", 16))) + 1
        if (rt < 0):  # If the value is negative get the twos compliment
            rt *= -1
            rt = (rt ^ (int("0xffffffff", 16))) + 1
        data.regALUOut = rs ^ rt

        debugCheck(config, data)

        # Cycle 4
        control.RegDst = 1
        control.MemtoReg = 0
        control.RegWrite = 1
        control.regwritecount += 1
        control.regdstcount += 1
        control.fourcycle += 1
        data.write(instr.rd, data.regALUOut)

        debugCheck(config, data)
    return


def reset(instr, config, data):
    if (config.processorType):
        global pipeLine
        PCPlus4 = data.read("pc") + 4
        if(pipeLine.PCSrc == 0):
            data.write("pc", PCPlus4)
        else:
            data.write("pc", pipeLine.PCBranch)
        pipeLine.D.instr = instr
        pipeLine.D.PCPlus4 = PCPlus4
        pipeLine.PCSrc = 0
        pipeLine.ALUOut = 0
        pipeLine.PCBranch = 0
    else:
        data.regInstr = int(instr.binary_string, 2)
        data.write("pc", data.read("pc") + 4)
        data.regALUOut = data.read("pc")
        control.IorD = 0
        control.ALUSrcA = 0
        control.ALUSrcB = 1
        control.ALUControl = 0
        control.PCSrc = 0
        control.IRWrite = 1
        control.PCWrite = 1
        control.RegWrite = 0
        control.MemWrite = 0
        global currCycle
        currCycle = 0
        debugCheck(config, data)


def decode(instr, config, data):
    if (config.processorType):
        print("AP")
    else:
        control.ALUSrcA = 0
        control.ALUSrcB = 3
        control.ALUOp = 0
        data.regALUOut = data.read("pc") + (instr.imm * 4)
        data.regRead1 = data.read(instr.rs)
        data.regRead2 = data.read(instr.rt)

    debugCheck(config, data)


# ----------------------------------function dictionaries----------------------------------------#

# Each function has an op code associated with it in machine language. These dictionaries will determine what function we
# should call based on the binary op code.

i_type_func_dict = {'001000': addi,
                    '001001': addiu,
                    '001100': andi,
                    '001111': lui,
                    '001101': ori,
                    '000010': j,
                    '100000': lb,
                    '101000': sb,
                    '100011': lw,
                    '101011': sw,
                    '000100': beq,
                    '000101': bne
                    }

r_type_func_dict = {'100000': add,
                    '100001': addu,
                    '100100': andd,
                    '100110': xor,
                    '101010': slt,
                    '000010': srl,
                    '000000': sll,
                    '101011': sltu,
                    '100010': sub
                    }

cache_dict = {0: "Directly-Mapped",
              1: "Fully-Associated",
              2: "2-Way Set-Associative",
              3: "4-Way Set-Associative"
              }

func_name_dict = {addi: "addi",
                  addiu: "addiu",
                  andi: "andi",
                  lui: "lui",
                  ori: "ori",
                  j: "j",
                  lb: "lb",
                  sb: "sb",
                  lw: "lw",
                  sw: "sw",
                  beq: "beq",
                  bne: "bne",
                  add: "add",
                  addu: "addu",
                  andd: "and",
                  xor: "xor",
                  slt: "slt",
                  srl: "srl",
                  sll: "sll",
                  sltu: "sltu",
                  sub: "sub"}

i_type_name = {"addi":True,
               "addiu":True,
               "andi":True,
               "lui":True,
               "ori":True,
               "j":True,
               "lb":True,
               "sb":True,
               "lw":True,
               "sw":True,
               "beq":True,
               "bne":True,
               "add":False,
               "addu":False,
               "and":False,
               "xor":False,
               "slt":False,
               "srl":False,
               "sll":False,
               "sltu":False,
               "sub":False,
               "bubble":True
               }


# -----------------------------Object definitions----------------------------------------------#

class controlCounter():
    def __init__(self):
        self.nothing = 0

class memDecode():
    def __init__(self, config, intAddr):
        self.binary_string = format(intAddr, '032b')
        if (config.cache == 0):  # Directly mapped
            start = int(32 - math.log2(config.blksize))
            end = 32
            self.byte = int(self.binary_string[start:end], 2)
            self.byteStr = self.binary_string[start:end]
            end = start
            start = int(end - math.log2(config.setsize))
            self.set = int(self.binary_string[start:end], 2)
            self.setStr = self.binary_string[start:end]
            end = start
            start = 0
            self.tag = int(self.binary_string[start:end], 2)
            self.tagStr = self.binary_string[start:end]

        elif (config.cache == 1):  # Fully-Associated
            start = int(32 - math.log2(config.blksize))
            end = 32
            self.byte = int(self.binary_string[start:end], 2)
            self.byteStr = self.binary_string[start:end]
            end = start
            start = 0
            self.tag = int(self.binary_string[start:end], 2)
            self.tagStr = self.binary_string[start:end]

        elif (config.cache == 2 or config.cache == 3):
            start = int(32 - math.log2(config.blksize))
            end = 32
            self.byte = int(self.binary_string[start:end], 2)
            self.byteStr = self.binary_string[start:end]
            end = start
            start = int(end - math.log2(config.setsize))
            self.set = int(self.binary_string[start:end], 2)
            self.setStr = self.binary_string[start:end]
            end = start
            start = 0
            self.tag = int(self.binary_string[start:end], 2)
            self.tagStr = self.binary_string[start:end]


class LRU():
    def __init__(self, config):
        self.list = []
        self.lastUse = []
        if (config.cache == 1):
            for i in range(config.waysize):
                self.list.append(-1)
                self.lastUse.append(0)
        elif (config.cache == 2 or config.cache == 3):
            for i in range(config.waysize):
                self.list.append(-1)
                self.lastUse.append(0)

    def push(self, val, use):
        self.list.pop()
        self.list.insert(0, val)
        self.lastUse.pop()
        self.lastUse.insert(0, use)

    def replace(self, val, use):
        ind = self.list.index(val)
        self.list.remove(val)
        self.list.insert(0, val)
        self.lastUse[ind] = -1
        self.lastUse.remove(-1)
        self.lastUse.insert(0, use)

    def updateleast(self, use):
        self.list.insert(0, self.list.pop())
        self.lastUse.pop()
        self.lastUse.insert(0, use)


class SetStructure():
    def __init__(self, config, SA=False):
        if (SA):
            self.valid = 0
            self.tag = 0
            self.inblk = []
            for i in range(config.blksize):
                self.inblk.append(0)
        elif (config.cache == 0):
            self.valid = 0
            self.tag = 0
            self.inblk = []
            for i in range(config.blksize):
                self.inblk.append(0)
        elif (config.cache == 1):
            self.valid = 0
            self.tag = 0
            self.inblk = []
            for i in range(config.blksize):
                self.inblk.append(0)
        elif (config.cache == 2 or config.cache == 3):
            self.way = []
            self.lru = LRU(config)
            for i in range(config.waysize):
                self.way.append(SetStructure(config, True))


class Cache():
    def __init__(self, config):
        self.hitCount = 0
        self.missCount = 0
        self.accessCount = 0
        if (config.cache == 0):
            self.set = []
            for i in range(config.setsize):
                self.set.append(SetStructure(config))
        elif (config.cache == 1):
            self.lru = LRU(config)
            self.set = []
            for i in range(config.waysize):
                self.set.append(SetStructure(config))
        elif (config.cache == 2 or config.cache == 3):
            self.set = []
            for i in range(config.setsize):
                self.set.append(SetStructure(config))

    def read(self, config, code, word):  # This reads from cache memory
        global CacheDebug
        self.accessCount += 1
        if (config.cache == 0):  # Directly-mapped
            if (not self.set[code.set].valid):
                self.missCount += 1
                if (config.debug):
                    self.debug(config, code, 0)
                self.populate(config, code)
            else:
                if (self.set[code.set].tag == code.tag):
                    self.hitCount += 1
                    if (config.debug):
                        self.debug(config, code, 1)
                else:
                    self.missCount += 1
                    if (config.debug):
                        self.debug(config, code, 2)
                    self.writeback(config, code)
                    self.populate(config, code)
            if (word):
                result = 0
                for i in range(4):
                    temp = self.set[code.set].inblk[code.byte + i] << i * 8
                    result += temp
                return result
            else:
                result = self.set[code.set].inblk[code.byte]
                mask = pow(2, 7)
                sign = result & mask
                if (sign):
                    result = (result ^ int('0xFF', 16)) + 1
                    result *= -1
                return result

        elif (config.cache == 1):  # Fully-Associated
            hit = False
            for i in range(config.waysize):
                if (not self.set[i].valid):  # The valid bit is not set, populate this block
                    self.missCount += 1
                    if (config.debug):
                        self.debug(config, code, i)
                    self.lru.push(i, self.accessCount)
                    self.populate(config, code, i)
                    hit = True
                    break
                else:
                    if (self.set[i].tag == code.tag):  # The valid bit is set and we hit a matching tag
                        hit = True
                        self.hitCount += 1
                        if (config.debug):
                            self.debug(config, code, i, 1)
                        self.lru.replace(i, self.accessCount)
                        break
                    else:
                        if (config.debug):
                            self.debug(config, code, i, 2)
            if (not hit):  # If we didn't hit populate the lru block
                self.missCount += 1
                if (config.debug):
                    print("MISS due to FULL SET -- LRU replace block " + str(
                        self.lru.list[config.waysize-1]) + "; unused since (" + str(self.lru.lastUse[config.waysize-1]) + ")")
                    CacheDebug += "MISS due to FULL SET -- LRU replace block " + str(
                        self.lru.list[config.waysize-1]) + "; unused since (" + str(self.lru.lastUse[config.waysize-1]) + ")\n"
                self.lru.updateleast(self.accessCount)
                setnum = self.lru.list[0]
                self.writeback(config, code, setnum)
                self.populate(config, code, setnum)
            if (word):  # return a word or byte from specific block
                result = 0
                for i in range(4):
                    temp = self.set[self.lru.list[0]].inblk[code.byte + i] << i * 8
                    result += temp
                return result
            else:
                result = self.set[self.lru.list[0]].inblk[code.byte]
                mask = pow(2, 7)
                sign = result & mask
                if (sign):
                    result = (result ^ int('0xFF', 16)) + 1
                    result *= -1
                return result
        elif (config.cache == 2 or config.cache == 3):
            hit = False
            for i in range(config.waysize):
                if (not self.set[code.set].way[i].valid):
                    self.missCount += 1
                    if (config.debug):
                        self.debug(config, code, i)
                    self.set[code.set].lru.push(i, self.accessCount)
                    self.populate(config, code, i)
                    hit = True
                    break
                else:
                    if (self.set[code.set].way[i].tag == code.tag):
                        hit = True
                        self.hitCount += 1
                        if (config.debug):
                            self.debug(config, code, i, 1)
                        self.set[code.set].lru.replace(i, self.accessCount)
                        break
                    else:
                        if(config.debug):
                            self.debug(config, code, i, 2)
            if (not hit):
                self.missCount += 1
                if (config.debug):
                    print(
                        "MISS due to FULL SET -- LRU replace block " + str(self.set[code.set].lru.list[config.waysize-1])
                        + "; unused since (" + str(self.set[code.set].lru.lastUse[config.waysize -1]) + ")")
                    CacheDebug += "MISS due to FULL SET -- LRU replace block " + str(self.set[code.set].lru.list[config.waysize-1])
                    + "; unused since (" + str(self.set[code.set].lru.lastUse[config.waysize -1]) + ")\n"
                self.set[code.set].lru.updateleast(self.accessCount)
                setnum = self.set[code.set].lru.list[0]
                self.writeback(config, code, setnum)
                self.populate(config, code, setnum)
            if (word):
                result = 0
                for i in range(4):
                    temp = self.set[code.set].way[self.set[code.set].lru.list[0]].inblk[code.byte + i] << i * 8
                    result += temp
                return result
            else:
                result = self.set[code.set].way[self.set[code.set].lru.list[0]].inblk[code.byte]
                mask = pow(2, 7)
                sign = result & mask
                if (sign):
                    result = (result ^ int('0xFF', 16)) + 1
                    result *= -1
                return result

    def write(self, config, code, data, word):  # This writes into cache memory
        global CacheDebug
        self.accessCount += 1
        if (config.cache == 0):
            if (not self.set[code.set].valid):
                self.missCount += 1
                if (config.debug):
                    self.debug(config, code, 0)
                self.populate(config, code)
            else:
                if (self.set[code.set].tag == code.tag):
                    self.hitCount += 1
                    if (config.debug):
                        self.debug(config, code, 1)
                else:
                    self.missCount += 1
                    if (config.debug):
                        self.debug(config, code, 2)
                    self.writeback(config, code)
                    self.populate(config, code)
            if (word):
                mask = 255
                for i in range(4):
                    temp = data & (mask << i * 8)
                    temp = temp >> i * 8
                    self.set[code.set].inblk[code.byte + i] = temp
            else:
                self.set[code.set].inblk[code.byte] = data&25

        if (config.cache == 1):
            hit = False
            for i in range(config.waysize):
                if (not self.set[i].valid):
                    self.missCount += 1
                    if (config.debug):
                        self.debug(config, code, i)
                    self.lru.push(i, self.accessCount)
                    self.populate(config, code, i)
                    hit = True
                    break
                else:
                    if (self.set[i].tag == code.tag):
                        hit = True
                        self.hitCount += 1
                        if (config.debug):
                            self.debug(config, code, i, 1)
                        self.lru.replace(i, self.accessCount)
                        break
                    else:
                        if (config.debug):
                            self.debug(config, code, i, 2)
            if (not hit):
                self.missCount += 1
                if (config.debug):
                    print(
                        "MISS due to FULL SET -- LRU replace block " + str(self.lru.list[config.waysize-1]) + "; unused since (" + str(
                            self.lru.lastUse[config.waysize-1]) + ")")
                    CacheDebug += "MISS due to FULL SET -- LRU replace block " + str(self.lru.list[config.waysize-1]) + "; unused since (" + str(
                            self.lru.lastUse[config.waysize-1]) + ")\n"
                self.lru.updateleast(self.accessCount)
                setnum = self.lru.list[0]
                self.writeback(config, code, setnum)
                self.populate(config, code, setnum)
            if (word):
                mask = 255
                for i in range(4):
                    temp = data & (mask << i * 8)
                    temp = temp >> i * 8
                    self.set[self.lru.list[0]].inblk[code.byte + i] = temp
            else:
                self.set[self.lru.list[0]].inblk[code.byte] = data&255

        elif (config.cache == 2 or config.cache == 3):
            hit = False
            for i in range(config.waysize):
                if (not self.set[code.set].way[i].valid):
                    self.missCount += 1
                    if (config.debug):
                        self.debug(config, code, i)
                    self.set[code.set].lru.push(i, self.accessCount)
                    self.populate(config, code, i)
                    hit = True
                    break
                else:
                    if (self.set[code.set].way[i].tag == code.tag):
                        hit = True
                        self.hitCount += 1
                        if (config.debug):
                            self.debug(config, code, i, 1)
                        self.set[code.set].lru.replace(i, self.accessCount)
                        break
                    else:
                        if(config.debug):
                            self.debug(config, code, i, 2)
            if (not hit):
                self.missCount += 1
                if (config.debug):
                    print(
                        "MISS due to FULL SET -- LRU replace block " + str(self.set[code.set].lru.list[config.waysize-1])
                        + "; unused since (" + str(self.set[code.set].lru.lastUse[config.waysize-1]) + ")")
                    CacheDebug += "MISS due to FULL SET -- LRU replace block " + str(self.set[code.set].lru.list[config.waysize-1])
                    + "; unused since (" + str(self.set[code.set].lru.lastUse[config.waysize-1]) + ")\n"
                self.set[code.set].lru.updateleast(self.accessCount)
                setnum = self.set[code.set].lru.list[0]
                self.writeback(config, code, setnum)
                self.populate(config, code, setnum)
            if (word):
                mask = 255
                for i in range(4):
                    temp = data & (mask << i * 8)
                    temp = temp >> i * 8
                    self.set[code.set].way[self.set[code.set].lru.list[0]].inblk[code.byte + i] = temp
            else:
                self.set[code.set].way[self.set[code.set].lru.list[0]].inblk[code.byte] = data&255

    def populate(self, config, code, setnum=0):  # This is called to fill a block in cache
        if (config.cache == 0):
            self.set[code.set].tag = code.tag
            self.set[code.set].valid = 1
            temp = codetoIntBuilder(config, code)
            for i in range(config.blksize):
                self.set[code.set].inblk[i] = stack.read(temp + i - int('0x2000', 16))

        elif (config.cache == 1):
            self.set[setnum].tag = code.tag
            self.set[setnum].valid = 1
            temp = code.binary_string[0:29]
            temp = int(temp + '000', 2)
            for i in range(config.blksize):
                self.set[setnum].inblk[i] = stack.read(temp + i - int('0x2000', 16))

        elif (config.cache == 2 or config.cache == 3):
            self.set[code.set].way[setnum].tag = code.tag
            self.set[code.set].way[setnum].valid = 1
            temp = codetoIntBuilder(config, code, setnum)
            for i in range(config.blksize):
                self.set[code.set].way[setnum].inblk[i] = stack.read(temp + i - int('0x2000', 16))

    def writeback(self, config, code, setnum=0):  # This is called when ever cache is being replaced to write back any changed memory
        if (config.cache == 0):  # Directly-Mapped
            temp = codetoIntBuilder(config, code)
            for i in range(config.blksize):
                stack.write(temp + i - int('0x2000',16), self.set[code.set].inblk[i])

        elif (config.cache == 1):  # Fully-Associated
            temp = codetoIntBuilder(config, code, setnum)
            for i in range(config.blksize):
                stack.write(format(temp + i, '08x'), self.set[setnum].inblk[i])

        elif (config.cache == 2 or config.cache == 3):
            temp = codetoIntBuilder(config, code, setnum)
            for i in range(config.blksize):
                stack.write(format(temp + i, '08x'), self.set[code.set].way[setnum].inblk[i])

    def endWriteBack(self, config):  # This is called at the end of the program to write back any memory that is changed in cache
        if (config.cache == 0):
            for i in range(config.setsize):
                if (self.set[i].valid):
                    start = ''
                    blksize = int(math.log2(config.blksize))
                    setsize = int(math.log2(config.setsize))
                    for j in range(blksize):
                        start += '0'
                    frmt1 = '0' + str(setsize) + 'b'
                    frmt2 = '0' + str(32 - (setsize + blksize)) + 'b'
                    code = int(format(self.set[i].tag, frmt2) + format(i, frmt1) + start, 2)
                    code = memDecode(config, code)
                    self.writeback(config, code)

        elif (config.cache == 1):
            for i in range(config.waysize):
                if (self.set[i].valid):
                    start = ''
                    blksize = int(math.log2(config.blksize))
                    for j in range(blksize):
                        start += '0'
                    frmt = '0' + str(32-blksize) + 'b'
                    code = memDecode(config, int(format(self.set[i].tag, frmt) + start, 2))
                    self.writeback(config, code, i)

        elif (config.cache == 2 or config.cache == 3):
            for i in range(config.setsize):
                for j in range(config.waysize):
                    if (self.set[i].way[j].valid):
                        start = ''
                        blksize = int(math.log2(config.blksize))
                        setsize = int(math.log2(config.setsize))
                        for k in range(blksize):
                            start += '0'
                        frmt1 = '0' + str(setsize) + 'b'
                        frmt2 = '0' + str(32 - (setsize + blksize)) + 'b'
                        code = int(format(self.set[i].way[j].tag, frmt2) + format(i, frmt1) + start, 2)
                        code = memDecode(config, code)
                        self.writeback(config, code, j)

    def calcHitRate(self):
        try:
            return self.hitCount * 100 / (self.hitCount + self.missCount)
        except:
            return 0

    def debug(self, config, code, setnum=0, hit=0):
        global CacheDebug
        if (config.cache == 0):
            tag = format(code.tag, '08x')
            tag = '0x' + tag
            string = "(" + str(self.accessCount) + ") address: " + format(int(code.binary_string, 2), '08x') + " ( tag " \
                     + tag + ") block range: " + str(code.set) + "-" + str(code.set) + '\n'
            if (self.set[code.set].valid):
                tag = format(self.set[code.set].tag, '08x')
                tag = " tag 0x" + tag
            else:
                tag = " empty"
            string += "Trying block " + str(code.set) + tag + " -- "
            hit = setnum
            if (hit == 1):
                string += "HIT"
            elif (hit == 2):
                string += "OCCUPIED\n\tMISS due to FULL SET"
            else:
                string += "MISS"
            print(string)
            CacheDebug += string + '\n'


        elif (config.cache == 1):
            tag = format(code.tag, '08x')
            tag = "0x" + tag
            if (not setnum):
                string = "(" + str(self.accessCount) + ") address: " + format(int(code.binary_string, 2),
                                                                              '08x') + " ( tag " + tag + ")\t"
                string += "block range: 0-7"
                CacheDebug += string + '\n'
                print(string)
            if (self.set[setnum].valid):
                tag = format(self.set[setnum].tag, '08x')
                tag = " tag 0x" + tag
            else:
                tag = " empty"
            string = "trying block " + str(setnum) + tag + " -- "
            if (hit == 1):
                string += "HIT"
            elif (hit == 2):
                string += "OCCUPIED"
            else:
                string += "MISS"
            CacheDebug += string + '\n'
            print(string)

        elif (config.cache == 2 or config.cache == 3):
            tag = format(code.tag, '08x')
            tag = "0x" + tag
            if (not setnum):
                string = "(" + str(self.accessCount) + ") address: " + format(int(code.binary_string, 2),
                                                                              '08x') + " ( tag " + tag + ")\t"
                string += "block range: " + str(config.waysize * code.set) + "-" + str(config.waysize* code.set + config.waysize - 1)
                CacheDebug += string + '\n'
                print(string)
            if (self.set[code.set].way[setnum].valid):
                tag = format(self.set[code.set].way[setnum].tag, '08x')
                tag = " tag 0x" + tag
            else:
                tag = " empty"
            string = "trying block " + str(config.waysize * code.set + setnum) + tag + " -- "
            if (hit == 1):
                string += "HIT"
            elif (hit == 2):
                string += "OCCUPIED"
            else:
                string += "MISS"
            CacheDebug += string + '\n'
            print(string)


class Control():
    def __init__(self, config, stage=0):
        self.regwritecount = 0
        self.memtoregcount = 0
        self.memwritecount = 0
        self.alusrccount = 0
        self.regdstcount = 0
        self.brachcount = 0
        self.fivecycle = 0
        self.fourcycle = 0
        self.threecycle = 0
        if (config.processorType):
            if(stage == 0):
                self.RegWrite = 0
                self.MemtoReg = 0
                self.MemWrite = 0
                self.ALUControl = 0
                self.ALUSrc = 0
                self.RegDst = 0
                self.Branch = 0
            if(stage == 1):
                self.RegWrite = 0
                self.MemtoReg = 0
                self.MemWrite = 0
                self.ALUControl = 0
                self.ALUSrc = 0
                self.RegDst = 0
            elif(stage == 2):
                self.RegWrite = 0
                self.MemtoReg = 0
                self.MemWrite = 0
            elif(stage == 3):
                self.RegWrite = 0
                self.MemtoReg = 0
        else:
            self.PCWrite = 0
            self.Branch = 0
            self.PCSrc = 0
            self.ALUControl = 0
            self.ALUSrcB = 0
            self.ALUSrcA = 0
            self.RegWrite = 0
            self.IorD = 0
            self.MemWrite = 0
            self.RegDst = 0
            self.MemtoReg = 0
            self.IRWrite = 0


class Stack():

    def __init__(self):
        self.stackList = []
        for i in range(4096):
            self.stackList.append(0)

    def write(self, offset, value):  # Save data into a specific position in stack
        try:
            self.stackList[offset] = value  # Try saving data using integer offset
        except:
            self.stackList[int(offset, 16) - int("2000",
                                                 16)] = value  # If offset is in hex convert it to int (assume we start at address 0x2000)

    def read(self, offset):  # Read byte from stack
        try:
            return self.stackList[offset]
        except:
            return self.stackList[int(offset, 16) - int("2000", 16)]


# I am making our stack global to make it easier to access
stack = Stack()


class Configure():
    def __init__(self):
        self.setProcessorType()
        self.setDebug()
        self.setCache()

    def setProcessorType(self):
        try:
            self.processorType = int(input("Enter 0 for multicycle or 1 for pipeline CPU\n"))
            if (self.processorType != 0 and self.processorType != 1):
                self.setProcessorType()
        except:
            self.setProcessorType()

    def setDebug(self):
        try:
            self.debug = int(input("Enter 0 to run nonstop or 1 for debug mode\n"))
            if (self.debug != 0 and self.debug != 1):
                self.setDebug()
        except:
            self.setDebug()

    def setCache(self):
        self.blksize = 0
        self.setsize = 0
        self.waysize = 0
        try:
            self.cache = int(input(
                "Enter 0 for directly-mapped cache\nEnter 1 for fully-associated cache\nEnter 2 for 2-way set-associatative cache\nEnter 3 for 4-way set-associatative cache\n"))
            if (self.cache < 0 or self.cache > 3):
                self.setCache()
            if (int(input("Want a custom cache size? 1 for Yes and 0 for No\n"))):
                if(self.cache == 0):
                    self.blksize = int(input("Input size of block (Multiple of 4 Bytes)\t"))
                    self.setsize = int(input("Input amount of sets (Multiple of 2)\t"))
                    self.waysize = 1
                elif(self.cache == 1):
                    self.blksize = int(input("Input size of block (Multiple of 4 Bytes)\t"))
                    self.setsize = 1
                    self.waysize = int(input("Input amount of ways\t"))
                elif(self.cache == 2 or self.cache == 3):
                    if(int(input("Want a custom way size? 1 for Yes and 0 for No\n"))):
                        self.blksize = int(input("Input size of block (Multiple of 4 Bytes)\t"))
                        self.setsize = int(input("Input amount of sets (Multiple of 2)\t"))
                        self.waysize = int(input("Input amount of ways\t"))
                    else:
                        if(self.cache == 2):
                            self.blksize = int(input("Input size of block (Multiple of 4 Bytes)\t"))
                            self.setsize = int(input("Input amount of sets (Multiple of 2)\t"))
                            self.waysize = 2
                        else:
                            self.blksize = int(input("Input size of block (Multiple of 4 Bytes)\t"))
                            self.setsize = int(input("Input amount of sets (Multiple of 2)\t"))
                            self.waysize = 4
            else:
                if (self.cache == 0):
                    self.blksize = 16
                    self.setsize = 4
                    self.waysize = 1
                elif (self.cache == 1):
                    self.blksize = 8
                    self.setsize = 1
                    self.waysize = 8
                elif (self.cache == 2):
                    self.blksize = 8
                    self.setsize = 4
                    self.waysize = 2
                elif (self.cache == 3):
                    self.blksize = 8
                    self.setsize = 2
                    self.waysize = 4
        except:
            self.setCache()


# Registers class creates a object that holds all of our useable registers with write and read functions
class Registers():

    def __init__(self, config, stage=-1):  # Initialize all of our registers to 0
        if(stage == -1):
            self.regList = []
            for i in range(16):
                self.regList.append(0)
            self.regZero = 0
            self.regPC = 0

        if (config.processorType):
            self.instrName = 'bubble'
            if(stage == 0):
                self.instr = Instruction(0, True)
                self.PCPlus4 = 0
            elif(stage == 1):
                self.rs = -1
                self.rt = -1
                self.rd = -1
                self.signedImm = 0
                self.shamt = 0
                self.read1 = 0
                self.read2 = 0
                self.control = Control(config, stage)
            elif(stage == 2):
                self.ALUOut = 0
                self.writeData = 0
                self.writeReg = -1
                self.control = Control(config, stage)
            elif(stage == 3):
                self.memData = 0
                self.ALUOut = 0
                self.writeReg = -1
                self.control = Control(config, stage)

        else:  # All the utility registers we need for multicycle
            self.regInstr = 0
            self.regData = 0
            self.regRead1 = 0
            self.regRead2 = 0
            self.regALUOut = 0

    def write(self, register, value):  # Save data into a register, takes a string (for reg) and integer (value)
        if (register.isdigit()):
            register = int(register)
            if (register == 0):
                self.regZero = 0
            elif (register >= 8 and register <= 23):
                self.regList[register - 8] = value
        else:
            if (register == "pc"):
                self.regPC = value

    def read(self, register):  # Read takes in a register (string) and returns the value stored in that reg
        if (register.isdigit()):
            register = int(register)
            if (register == 0):
                return self.regZero
            elif (register >= 8 and register <= 23):
                return self.regList[register - 8]
        else:
            if (register == "pc"):
                return self.regPC


class Instruction():  # Taking inspiration from Samantha Stephans homework 2 code

    def __init__(self, hex_code, bubble=False):
        if(bubble):
            self.name = "bubble"
            self.rs = -1
            self.rt = -1
            self.rd = -1
            self.imm = 0
        else:
            self.binary_string = format(int(hex_code, 16), '032b')  # get a binary string of machine code

            self.opcode = self.binary_string[0:6]
            if (self.opcode == "000000"):  # R type instruction
                self.func = self.binary_string[26:32]
                self.type = 'r'
                self.name = func_name_dict[r_type_func_dict[self.func]]
            else:
                self.func = self.opcode
                self.type = 'i'
                self.name = func_name_dict[i_type_func_dict[self.func]]

            # Even though each func may not have all these reg, we save them anyways to make life easier
            self.rs = str(int(self.binary_string[6:11], 2))
            self.rt = str(int(self.binary_string[11:16], 2))
            self.rd = str(int(self.binary_string[16:21], 2))
            self.sh = str(int(self.binary_string[21:26], 2))
            self.jump = str(int(self.binary_string[6:32], 2))

            if self.binary_string[16] == '1': #check if immediate is negative
                self.imm = -(twosComp(int(self.binary_string[16:32],2)))
            else:
                self.imm = int(self.binary_string[16:32],2)


class Pipeline:

    def __init__(self, config):
        # Init all registers in pipeline
        self.D = Registers(config, 0)
        self.E = Registers(config, 1)
        self.M = Registers(config, 2)
        self.W = Registers(config, 3)

        # Useful data lines
        self.ALUOut = 0
        self.WriteData = 0
        self.PCSrc = 0
        self.PCBranch = 0
        self.SrcA = 0
        self.SrcB = 0
        self.rsD = 0
        self.rtD = 0
        self.rdD = 0

        # Forward control lines
        self.forwardAE = 0
        self.forwardBE = 0
        self.forwardAD = 0
        self.forwardBD = 0

        # Forward Data lines
        self.forwardResult = 0
        self.forwardALU = 0

        # Hazard detection holds
        self.flush = False
        self.stall = 0
        self.hold = False
        self.insertStall = False
        self.save = None

        # FDEMW lists
        self.funcFDEMW = []

        # Hazard Counts
        self.totalDelays = 0
        self.forwardA = 0
        self.forwardB = 0
        self.forwardC = 0
        self.forwardD = 0
        self.forward1 = 0
        self.forward2 = 0
        self.forward3 = 0
        self.forward4 = 0
        self.lw_br = 0
        self.lw_use = 0
        self.comp_br = 0
        self.flushes = 0
        for i in range(5):  # initialize pipeline to all bubbles
            self.funcFDEMW.append('bubble')

    def hazard_detection(self, regs):  # assume forwarding is good
        global instruction_calls

        if self.D.instrName == 'beq' or self.D.instrName == 'bne':
            # check comp - br or lw - br then return number of stalls
            if(i_type_name[self.E.instrName]):
                if (self.E.instrName == 'lw' or self.E.instrName == 'lb') and (
                        self.E.rt == self.D.instr.rt or self.E.rt == self.D.instr.rs):  # lw - br
                    self.lw_br += 1
                    return 2
                elif self.E.control.RegWrite and (self.D.instr.rs == self.E.rt or self.D.instr.rt == self.E.rt) and (self.E.instrName != 'lw' or self.E.instrName != 'lb'):
                    self.comp_br += 1
                    return 1
            elif self.E.control.RegWrite and (self.D.instr.rs == self.E.rd or self.D.instr.rt == self.E.rd):  # comp - br
                self.comp_br += 1
                return 1

        elif self.E.instrName == 'lw':  # lw - use     still need to check if actually a hazard
            # if registers match return 1
            if self.E.rt == self.D.instr.rs or self.E.rt == self.D.instr.rt:  # if both then resultw -> srcA/B
                self.lw_use += 1
                return 1

        if (self.D.instrName == "beq" or self.D.instrName == "bne"):
            if (self.forwardAD == 1):
                source1 = self.forwardResult
            elif (self.forwardAD == 2):
                source1 = self.forwardALU
            else:
                source1 = regs.read(self.D.instr.rs)
            if (self.forwardBD == 1):
                source2 = self.forwardResult
            elif (self.forwardBD == 2):
                source2 = self.forwardALU
            else:
                source2 = regs.read(self.D.instr.rt)
            if (self.D.instrName == 'beq' and source1 == source2) or (self.D.instrName == 'bne' and source1 != source2):
                self.PCSrc = 1
                self.flushes += 1
                instruction_calls += 1
                return -1
            else:
                self.PCSrc = 0
                return 0
        else:
            self.PCSrc = 0
            return 0




    # i think that we got all of the forwarding cases
    def forwarding(self):
        self.forwardAE = 0
        self.forwardBE = 0
        self.forwardAD = 0
        self.forwardBD = 0
        # Source A and B forward
        if self.W.writeReg == self.E.rs == self.E.rt and (self.W.writeReg != -1) and not i_type_name[self.E.instrName]:
            # ResultW -> SrcAE && ResultW -> SrcBE
            self.forwardAE = 1
            self.forwardBE = 1
            self.forward1 += 1
            self.forward2 += 1
        elif self.M.writeReg == self.E.rs == self.E.rt and (self.M.writeReg != -1) and not i_type_name[self.E.instrName]:
            # ALUOutM -> SrcAE && ALUOutM -> SrcBE
            self.forwardAE = 2
            self.forwardBE = 2
            self.forwardA += 1
            self.forwardB += 1

        else:
            # Source A forward
            if self.W.writeReg == self.E.rs and (self.W.writeReg != -1):
                # need to forward to srcAE
                # ResultW -> SrcAE
                self.forwardAE = 1
                self.forward1 += 1
            if self.M.writeReg == self.E.rs and (self.M.writeReg != -1):
                # ALUOutM -> SrcAE
                self.forwardAE = 2
                self.forwardA += 1

            # Source B forward
            if self.W.writeReg == self.E.rt and (self.W.writeReg != -1):
                self.forwardBE = 1
                self.forward2 += 1
            if self.M.writeReg == self.E.rt and (self.M.writeReg != -1):
                self.forwardBE = 2
                self.forwardB += 1

        # Branch cases
        if self.W.writeReg == self.D.instr.rs and (self.D.instrName == "beq" or self.D.instrName == "bne"):
            # ResultW -> EqualD
            self.forwardAD = 1
            self.forward4 += 1
        if self.M.writeReg == self.D.instr.rs and (self.D.instrName == "beq" or self.D.instrName == "bne"):
            # ALUOutM -> EqualD
            self.forwardAD = 2
            self.forwardD += 1
        if self.W.writeReg == self.D.instr.rt and (self.D.instrName == "beq" or self.D.instrName == "bne"):
            self.forwardBD = 1
            self.forwardD += 1
        if self.M.writeReg == self.D.instr.rt and (self.D.instrName == "beq" or self.D.instrName == "bne"):
            self.forwardBD = 2
            self.forwardD += 1
        return

    def Flush(self, index):
        if(index == 0):
            self.D.instr = Instruction(0, True)
            self.D.PCPlus4 = 0
            self.D.instrName = 'bubble'
            control.RegWrite = 0
            control.MemtoReg = 0
            control.MemWrite = 0
            control.ALUControl = 0
            control.ALUSrc = 0
            control.RegDst = 0
            control.Branch = 0
        else:
            self.funcFDEMW[2] = 'bubble'
            self.E.instrName = 'bubble'
            self.E.rs = -1
            self.E.rt = -1
            self.E.rd = -1
            self.E.signedImm = 0
            self.E.read1 = 0
            self.E.read2 = 0
            self.E.control.RegWrite = 0
            self.E.control.MemWrite = 0

    def cycle(self, config, instr, regs, function, mcLength):
        global control
        global instruction_calls
        global programEnd

        self.funcFDEMW[0] = function

        if (self.M.control.MemWrite):
            if (self.M.instrName == "sw"):
                code = memDecode(config, self.M.ALUOut)
                cache.write(config, code, self.M.writeData, True)
            else:
                code = memDecode(config, self.M.ALUOut)
                cache.write(config, code, self.M.writeData, False)

        self.forwardALU = self.M.ALUOut
        if (self.W.control.MemtoReg):
            self.forwardResult = self.W.memData
        else:
            self.forwardResult = self.W.ALUOut

        if(not self.stall):
            self.flush = False
            self.push(instr, regs)
        else:
            self.funcFDEMW[1] = self.save[1]
            self.funcFDEMW[2] = 'bubble'

            self.push(self.save[0], regs)

            self.forwardALU = self.M.ALUOut
            if (self.W.control.MemtoReg):
                self.forwardResult = self.W.memData
            else:
                self.forwardResult = self.W.ALUOut

            self.stall -= 1
            self.push(instr, regs)

            if(self.stall):
                self.hold = True

        # Setting up the ALU sources for any instructions that use them
        if (self.forwardAE == 1):
            self.SrcA = self.forwardResult
        elif (self.forwardAE == 2):
            self.SrcA = self.forwardALU
        else:
            self.SrcA = self.E.read1
        if (self.forwardBE == 1):
            hold = self.forwardResult
            self.M.writeData = self.forwardResult
        elif (self.forwardBE == 2):
            hold = self.forwardALU
            self.M.writeData = self.forwardALU
        else:
            hold = self.E.read2
            self.M.writeData = self.E.read2
        if (self.E.control.ALUSrc):
            self.SrcB = self.E.signedImm
        else:
            self.SrcB = hold
        if(self.save != None and self.save[1] != 'bubble'):
            self.save[1](self.save[0], config, regs)
        else:
            if(self.funcFDEMW[1] != 'bubble'):
                (self.funcFDEMW[1])(instr, config, regs)
        if(self.funcFDEMW[2] != 'bubble'):
            (self.funcFDEMW[2])(instr, config, regs, 2)

        # Pushing Write cycle out
        if (instr.name == self.D.instrName == self.E.instrName == self.M.instrName == self.W.instrName == 'bubble'):
            programEnd = True
            return
        else:
            debugCheck(config, regs, instr)

        if(self.W.instrName != 'bubble' and not self.hold):
            instruction_calls += 1

        self.pushMW(config, regs)

        self.pushEW()

        if (self.hold):
            self.save = [self.D.instr, self.funcFDEMW[1]]
            self.funcFDEMW[1] = 'bubble'
            self.Flush(0)
            if(not self.flush):
                regs.write("pc", regs.read("pc") - 4)

        if (self.flush):
            reset(Instruction(0, True), config, regs)
            if(self.W.instrName != 'bubble'):
                instruction_calls += 1
            instruction_calls += 1
            self.Flush(1)
            return

        self.pushDE(regs)

        if(self.hold):
            self.hold = False
            self.D.instrName = self.save[0].name
            reset(self.save[0], config, regs)
            return

        # Filling Decode Cycle with Fetch Cycle
        self.D.instrName = instr.name
        self.funcFDEMW[1] = self.funcFDEMW[0]
        self.save = None
        if(regs.read("pc") == mcLength):
            regs.write("pc", regs.read("pc") - 4)
        reset(instr, config, regs)

    def pushMW(self, config, regs):
        # Filling Write cycle with Mem cycle
        if (self.W.control.RegWrite):
            if (self.W.control.MemtoReg):
                regs.write(str(self.W.writeReg), self.W.memData)
                self.forwardResult = self.W.memData
            else:
                regs.write(str(self.W.writeReg), self.W.ALUOut)
                self.forwardResult = self.W.ALUOut
        self.W.instrName = self.M.instrName
        self.funcFDEMW[4] = self.funcFDEMW[3]
        self.W.control.RegWrite = self.M.control.RegWrite
        self.W.control.MemtoReg = self.M.control.MemtoReg
        if (self.M.instrName == "lw"):
            code = memDecode(config, self.M.ALUOut)
            self.W.memData = cache.read(config, code, True)
        elif (self.M.instrName == 'lb'):
            code = memDecode(config, self.M.ALUOut)
            self.W.memData = cache.read(config, code, False)
        self.W.ALUOut = self.M.ALUOut
        self.W.writeReg = self.M.writeReg

    def pushEW(self):
        # Filling Mem Cycle with Execute cycle
        if (self.D.instr.imm < 0):
            self.PCBranch = self.D.PCPlus4 + (-1 * ((-1 * self.D.instr.imm) << 2))
        else:
            self.PCBranch = self.D.PCPlus4 + (self.D.instr.imm << 2)
        self.M.instrName = self.E.instrName
        self.funcFDEMW[3] = self.funcFDEMW[2]
        self.M.control.RegWrite = self.E.control.RegWrite
        self.M.control.MemtoReg = self.E.control.MemtoReg
        self.M.control.MemWrite = self.E.control.MemWrite
        self.M.ALUOut = self.ALUOut
        if (self.E.control.RegDst):
            self.M.writeReg = self.E.rd
        else:
            self.M.writeReg = self.E.rt

    def pushDE(self, regs):
        # Filling Execute Cycle with Decode Cycle
        if (self.D.instrName != 'bubble'):
            self.rsD = self.D.instr.rs
            self.rtD = self.D.instr.rt
            if (i_type_name[self.D.instrName]):
                self.rdD = -1
            else:
                self.rdD = self.D.instr.rd
        self.E.instrName = self.D.instrName
        self.funcFDEMW[2] = self.funcFDEMW[1]
        self.E.control.RegWrite = control.RegWrite
        self.E.control.MemtoReg = control.MemtoReg
        self.E.control.MemWrite = control.MemWrite
        self.E.control.ALUControl = control.ALUControl
        self.E.control.ALUSrc = control.ALUSrc
        self.E.control.RegDst = control.RegDst
        if(self.D.instrName != "bubble"):
            self.E.read1 = regs.read(str(self.rsD))
            self.E.read2 = regs.read(str(self.rtD))
            self.E.rs = self.rsD
            self.E.rt = self.rtD
            self.E.rd = self.rdD
            self.E.signedImm = self.D.instr.imm
            self.E.shamt = int(self.D.instr.sh)
        else:
            self.E.read1 = 0
            self.E.read2 = 0
            self.E.rs = -1
            self.E.rt = -1
            self.E.rd = -1
            self.E.signedImm = 0

    # can be adjusted to receive stalls instead of instruction depending on what we want to do
    def push(self, instr, regs):  # push new instruction into "pipeline" then remove instructions on the end
        if(not self.stall):
            self.forwarding()
            hazards = self.hazard_detection(regs)
            if hazards == -1:  # flush not delay
                self.totalDelays += 1
                self.flush = True
                self.hold = True
                return
            self.totalDelays += hazards
            if hazards > 0:
                self.stall = hazards
                self.hold = True
                return

    def print_pipeline(self):  # self explanatory
        print(self.funcFDEMW)





# ---------------------------Helper Functions-------------------------------------#

def twosComp(binVal):  # Get the two's compliment of a value (16 bit)
    binVal = binVal ^ 65535
    binVal += 1
    return binVal


def convertToHex(string):  # Convert a binary string into hexadecimal
    return format(int(string, 2), '08x')


def pause():
    input("Hit Enter to Continue")

def codetoIntBuilder(config, code, setnum=0):
    global cache
    if(config.cache == 0):
        start = ''
        blksize = int(math.log2(config.blksize))
        setsize = int(math.log2(config.setsize))
        for i in range(blksize):
            start += '0'
        frmt1 = '0' + str(setsize) + 'b'
        frmt2 = '0' + str(32 - (setsize + blksize)) + 'b'
        return int(format(cache.set[code.set].tag, frmt2) + format(code.set, frmt1) + start, 2)
    elif(config.cache == 1):
        start = ''
        blksize = int(math.log2(config.blksize))
        for i in range(blksize):
            start += '0'
        frmt = '0' + str(32-blksize) + 'b'
        return int(format(cache.set[setnum].tag, frmt) + start, 2)
    else:
        start = ''
        blksize = int(math.log2(config.blksize))
        setsize = int(math.log2(config.setsize))
        for i in range(blksize):
            start += '0'
        frmt1 = '0' + str(setsize) + 'b'
        frmt2 = '0' + str(32 - (setsize + blksize)) + 'b'
        return int(format(cache.set[code.set].way[setnum].tag, frmt2) + format(code.set, frmt1) + start, 2)

def debugCheck(config, data, instr=0):
    global totCycle
    totCycle += 1
    if (config.debug):
        printDebug(config, data, instr)
        pause()
        return
    else:
        return


def printDebug(config, data, instr=0):
    global instruction_calls
    if (config.processorType):
        global pipeLine
        printOutput(data, 20, instruction_calls)
        printCache(config)
        print("In Pipeline:\nFetch: " + instr.name + " Decode: " + pipeLine.D.instr.name + " Execute: " + pipeLine.E.instrName
              + "\nMemory: " + pipeLine.M.instrName + " Write: " + pipeLine.W.instrName)
        print("Control:\nRegWrite: " + str(control.RegWrite) + " MemtoReg: " + str(control.MemtoReg) + " MemWrite: " + str(control.MemWrite)
              + "\nALUControl: " + str(control.ALUControl) + " ALUSrc " + str(control.ALUSrc) + " RegDst: " + str(control.RegDst)
              + "\nBranch: " + str(control.Branch))
        print("Decode instr: " + pipeLine.D.instr.name)
        if (pipeLine.D.instr.name != 'bubble'):
            code = format(int(pipeLine.D.instr.binary_string, 2), '08x')
            pc4 = str(pipeLine.D.PCPlus4)
        else:
            code = 'bubble'
            pc4 = '0'
        print("\nDecode:\nInstruction: " + code + " PCPlus4: " + pc4)
        print("\nExecute Control:\nRegWrite: " + str(pipeLine.E.control.RegWrite) + " MemtoReg: " + str(pipeLine.E.control.MemtoReg)
              + " MemWrite " + str(pipeLine.E.control.MemWrite) + "\nALUControl: " + format(pipeLine.E.control.ALUControl, '03b')
              + " ALUSrc: " + str(pipeLine.E.control.ALUSrc) + " RegDst: " + str(pipeLine.E.control.RegDst))
        print("\nExecute Registers:\nRead1: " + str(pipeLine.E.read1) + " Read2: " + str(pipeLine.E.read2) + "\nRs: " + str(pipeLine.E.rs)
              + " Rt: " + str(pipeLine.E.rt) + " Rd: " + str(pipeLine.E.rd) + " Imm: " + str(pipeLine.E.signedImm))
        print("\nMemory Control:\nRegWrite: " + str(pipeLine.M.control.RegWrite) + " MemtoReg: " + str(pipeLine.M.control.MemtoReg)
              + " MemWrite: " + str(pipeLine.M.control.MemWrite))
        print("\nMemory Registers:\nALUOut: " + str(pipeLine.M.ALUOut) + " WriteData: " + str(pipeLine.M.writeData) + " WriteReg: " + str(pipeLine.M.writeReg))
        print("\nWrite Control:\nRegWrite: " + str(pipeLine.W.control.RegWrite) + " MemtoReg: " + str(pipeLine.W.control.MemtoReg))
        print("\nWrite Registers:\nReadData: " + str(pipeLine.W.memData) + " ALUOut: " + str(pipeLine.W.ALUOut) + " WriteReg: " + str(pipeLine.W.writeReg))
        print("\nHazard:\nForwardAE: " + str(pipeLine.forwardAE) + " ForwardBE: " + str(pipeLine.forwardBE) + "\nForwardAD: " + str(pipeLine.forwardAD)
              + " ForwardBD: " + str(pipeLine.forwardBD))
        pipeLine.print_pipeline()
    else:
        printOutput(data, 20, instruction_calls)
        printCache(config)
        global currCycle
        currCycle += 1
        print("Cycle: " + str(currCycle))
        print("Control:\nPCWrite: " + str(control.PCWrite) + "\nBranch: " + str(control.Branch) + "\nPCSrc: " + str(
            control.PCSrc) +
              "\nALUControl: " + str(format(control.ALUControl, '03b')) + "\nALUSrcB: " + format(control.ALUSrcB,
                                                                                                 '02b') + "\nALUSrcA: " + str(
            control.ALUSrcA)
              + "\nRegWrite: " + str(control.RegWrite) + "\nIorD: " + str(control.IorD) + "\nMemWrite: " + str(
            control.MemWrite) + "\nIRWrite: " + str(control.IRWrite))
        print("Utility Regs:\nregInstr: " + convertToHex(bin(data.regInstr)) + "\nregData: " + convertToHex(
            bin(data.regData)) + "\nregRead1: " +
              convertToHex(bin(data.regRead1)) + "\nregRead2: " + convertToHex(
            bin(data.regRead2)) + "\nregALUOut: " + convertToHex(format(data.regALUOut, '0b')))


# ----------------------------Main funcitonality modules----------------------------#


# Remember where each of the jump label is, and the target location
def saveJumpLabel(asm, labelIndex, labelName):
    lineCount = 0
    index = 0
    for line in asm:
        line = line.replace(" ", "")
        if (line.count(":")):
            labelName.append(line[0:line.index(":")])  # append the label name
            labelIndex.append(lineCount)  # append the label's index
            asm[index] = line[line.index(":") + 1:]
            temp = asm[index]
            if (temp == "\n"):  # We should not increment our lineCount if a label is found on a line by itself
                index += 1
                continue
        lineCount += 1
        index += 1
    for item in range(asm.count('\n')):  # Remove all empty lines '\n'
        asm.remove('\n')


# Assemble will convert all of our assembly code in "mips.asm" into machine code and put it into a .txt file named "mc.txt" (hex output)
def assemble():
    labelIndex = []
    labelName = []
    f = open("mc.txt", "w+")
    h = open("B1.asm", "r")
    asm = h.readlines()
    h.close()

    currLine = 1

    index = 0
    for line in asm:  # Remove all comments in code
        asm[index], par, extra = asm[index].partition("#")
        asm[index] = asm[index].replace('\n', '')  # Incase our deleting of comments got rid of a '\n'...
        asm[index] += '\n'  # ... We will replace all the '\n' for every single line.
        asm[index] = asm[index].replace("\t", "")
        index += 1

    for item in range(asm.count('\n')):  # Remove all empty lines '\n'
        asm.remove('\n')

    for item in range(asm.count('')):  # Remove all blank lines left from removing comments
        asm.remove('')

    saveJumpLabel(asm, labelIndex, labelName)  # Save all jump's destinations

    # Read every line individually and convert it into a hex machine code value that represents that same instruction
    for line in asm:
        line = line.replace("\n", "")  # Removes extra chars
        line = line.replace("$zero", "$0")
        line = line.replace("$", "")
        line = line.replace(" ", "")
        if (line[0:5] == "addiu"):  # ADDIU
            line = line.replace("addiu", "")
            line = line.split(",")

            try:
                imm = format(twosComp(-1 * int(line[2])), '016b') if (int(line[2]) < 0) else format(int(line[2]),
                                                                                                    '016b')
            except:
                imm = format(int(line[2], 16), '016b')
            rs = format(int(line[1]), '05b')
            rt = format(int(line[0]), '05b')
            f.write(convertToHex(str('001001') + str(rs) + str(rt) + str(imm)) + '\n')

        elif (line[0:4] == "addi"):  # ADDI
            line = line.replace("addi", "")
            line = line.split(",")
            try:
                imm = format(int(line[2]), '016b') if (int(line[2]) >= 0) else format(65536 + int(line[2]), '016b')
            except:
                imm = format(int(line[2], 16), '016b')
            rs = format(int(line[1]), '05b')
            rt = format(int(line[0]), '05b')
            f.write(convertToHex(str('001000') + str(rs) + str(rt) + str(imm)) + '\n')

        elif (line[0:4] == "addu"):  # ADDU
            line = line.replace("addu", "")
            line = line.split(",")
            rd = format(int(line[0]), '05b')
            rs = format(int(line[1]), '05b')
            rt = format(int(line[2]), '05b')
            f.write(convertToHex(str('000000') + str(rs) + str(rt) + str(rd) + str('00000100001')) + '\n')

        elif (line[0:3] == "add"):  # ADD
            line = line.replace("add", "")
            line = line.split(",")
            rd = format(int(line[0]), '05b')
            rs = format(int(line[1]), '05b')
            rt = format(int(line[2]), '05b')
            f.write(convertToHex(str('000000') + str(rs) + str(rt) + str(rd) + str('00000100000')) + '\n')

        elif (line[0:3] == "sub"):  # SUB
            line = line.replace("sub", "")
            line = line.split(",")
            rd = format(int(line[0]), '05b')
            rs = format(int(line[1]), '05b')
            rt = format(int(line[2]), '05b')
            f.write(convertToHex(str('000000') + str(rs) + str(rt) + str(rd) + str('00000100010')) + '\n')

        elif (line[0:1] == "j"):  # JUMP
            line = line.replace("j", "", 1)  # Fixed bug where it would remove j from label names
            line = line.split(",")

            # Since jump instruction has 2 options:
            # 1) jump to a label
            # 2) jump to a target (integer)
            # We need to save the label destination and its target location

            if (line[0].isdigit()):  # First,test to see if it's a label or a integer
                f.write(convertToHex(str('000010') + str(format(int(line[0]), '026b'))) + '\n')

            else:  # Jumping to label
                for i in range(len(labelName)):
                    if (labelName[i] == line[0]):
                        f.write(convertToHex(str('000010') + str(format(int(labelIndex[i]), '026b'))) + '\n')

        elif (line[0:3] == "sll"):
            line = line.replace("sll", "")
            line = line.split(",")
            shamt = format(int(line[2]), '05b') if (int(line[2]) >= 0) else format(33 + int(line[2]), '05b')
            rt = format(int(line[1]), '05b')
            rd = format(int(line[0]), '05b')
            f.write(convertToHex(str('000000000000') + str(rt) + str(rd) + str(shamt) + str('000000')) + '\n')

        elif (line[0:3] == "srl"):  # SRL
            line = line.replace("srl", "")
            line = line.split(",")
            shamt = format(int(line[2]), '05b') if (int(line[2]) >= 0) else format(33 + int(line[2]), '05b')
            rt = format(int(line[1]), '05b')
            rd = format(int(line[0]), '05b')
            f.write(convertToHex(str('00000000000') + str(rt) + str(rd) + str(shamt) + str('000010')) + '\n')

        elif (line[0:2] == "lb"):  # LB
            line = line.replace("lb", "")
            line = line.replace("(", ",")
            line = line.replace(")", "")
            line = line.split(",")
            try:
                imm = format(int(line[1]), '016b') if (int(line[1]) >= 0) else format(65536 + int(line[1]), '016b')
            except:
                imm = format(int(line[1], 16), '016b') if (int(line[1], 16) >= 0) else format(65536 + int(line[1], 16),
                                                                                              '016b')
            rs = format(int(line[2]), '05b')
            rt = format(int(line[0]), '05b')
            f.write(convertToHex(str('100000') + str(rs) + str(rt) + str(imm)) + '\n')

        elif (line[0:2] == "sb"):  # SB
            line = line.replace("sb", "")
            line = line.replace("(", ",")
            line = line.replace(")", "")
            line = line.split(",")
            try:
                imm = format(int(line[1]), '016b') if (int(line[1]) >= 0) else format(65536 + int(line[1]), '016b')
            except:
                imm = format(int(line[1], 16), '016b')
            rs = format(int(line[2]), '05b')
            rt = format(int(line[0]), '05b')
            f.write(convertToHex(str('101000') + str(rs) + str(rt) + str(imm)) + '\n')

        elif (line[0:2] == "lw"):  # LW
            line = line.replace("lw", "")
            line = line.replace("(", ",")
            line = line.replace(")", "")
            line = line.split(",")
            try:
                imm = format(int(line[1]), '016b') if (int(line[1]) >= 0) else format(65536 + int(line[1]), '016b')
            except:
                imm = format(int(line[1], 16), '016b')
            rs = format(int(line[2]), '05b')
            rt = format(int(line[0]), '05b')
            f.write(convertToHex(str('100011') + str(rs) + str(rt) + str(imm)) + '\n')

        elif (line[0:2] == "sw"):  # SW
            line = line.replace("sw", "")
            line = line.replace("(", ",")
            line = line.replace(")", "")
            line = line.split(",")
            try:
                imm = format(int(line[1]), '016b') if (int(line[1]) >= 0) else format(65536 + int(line[1]), '016b')
            except:
                imm = format(int(line[1], 16), '016b')
            rs = format(int(line[2]), '05b')
            rt = format(int(line[0]), '05b')
            f.write(convertToHex(str('101011') + str(rs) + str(rt) + str(imm)) + '\n')

        elif (line[0:3] == "beq"):  # BEQ
            line = line.replace("beq", "")
            line = line.split(",")

            # Branching to label
            for i in range(len(labelName)):
                if (labelName[i] == line[2]):
                    temp = labelIndex[i] - currLine  # Since branching uses local values so we have to find the
                    if (temp < 0):  # difference between the current line and label location
                        temp *= -1
                        temp = twosComp(temp)
                        imm = format(temp, '016b')
                    else:
                        imm = format(temp, '016b')

            rs = format(int(line[0]), '05b')
            rt = format(int(line[1]), '05b')
            f.write(convertToHex(str('000100') + str(rs) + str(rt) + str(imm)) + '\n')

        elif (line[0:3] == "bne"):  # BNE
            line = line.replace("bne", "")
            line = line.replace("\t", "")
            line = line.split(",")

            # Branching to label
            for i in range(len(labelName)):
                if (labelName[i] == line[2]):
                    temp = labelIndex[i] - currLine
                    if (temp < 0):
                        temp *= -1
                        temp = twosComp(temp)
                        imm = format(temp, '016b')
                    else:
                        imm = format(temp, '016b')

            rs = format(int(line[0]), '05b')
            rt = format(int(line[1]), '05b')
            f.write(convertToHex(str('000101') + str(rs) + str(rt) + str(imm)) + '\n')

        elif (line[0:4] == "sltu"):  # SLTU
            line = line.replace("sltu", "")
            line = line.split(",")
            rt = format(int(line[2]), '05b')
            rs = format(int(line[1]), '05b')
            rd = format(int(line[0]), '05b')
            f.write(convertToHex(str('000000') + str(rs) + str(rt) + str(rd) + str('00000101011')) + '\n')

        elif (line[0:3] == "slt"):  # SLT
            line = line.replace("slt", "")
            line = line.split(",")
            rt = format(int(line[2]), '05b')
            rs = format(int(line[1]), '05b')
            rd = format(int(line[0]), '05b')
            f.write(convertToHex(str('000000') + str(rs) + str(rt) + str(rd) + str('00000101010')) + '\n')

        elif (line[0:3] == "lui"):  # LUI
            line = line.replace("lui", "")
            line = line.split(",")
            try:
                imm = format(int(line[1]), '016b') if (int(line[1]) >= 0) else format(65536 + int(line[1]), '016b')
            except:
                imm = format(int(line[1], 16), '016b')
            rt = format(int(line[0]), '05b')
            f.write(convertToHex(str('001111') + str('00000') + str(rt) + str(imm)) + '\n')

        elif (line[0:3] == "ori"):  # ORI
            line = line.replace("ori", "")
            line = line.split(",")
            try:
                imm = format(int(line[2]), '016b') if (int(line[2]) >= 0) else format(65536 + int(line[2]), '016b')
            except:
                imm = format(int(line[2], 16), '016b')
            rt = format(int(line[0]), '05b')
            rs = format(int(line[1]), '05b')
            f.write(convertToHex(str('001101') + str(rs) + str(rt) + str(imm)) + '\n')

        elif (line[0:3] == "xor"):  # XOR
            line = line.replace("xor", "")
            line = line.split(",")
            rd = format(int(line[0]), '05b')
            rs = format(int(line[1]), '05b')
            rt = format(int(line[2]), '05b')
            f.write(convertToHex(str('000000') + str(rs) + str(rt) + str(rd) + str('00000100110')) + '\n')

        elif (line[0:4] == "andi"):  # ANDI
            line = line.replace("andi", "")
            line = line.split(",")
            try:
                imm = format(int(line[2]), '016b') if (int(line[2]) >= 0) else format(65536 + int(line[2]), '016b')
            except:
                imm = format(int(line[2], 16), '016b')
            rt = format(int(line[0]), '05b')
            rs = format(int(line[1]), '05b')
            f.write(convertToHex(str('001100') + str(rs) + str(rt) + str(imm)) + '\n')

        elif (line[0:3] == "and"):  # AND
            line = line.replace("and", "")
            line = line.split(",")
            rd = format(int(line[0]), '05b')
            rs = format(int(line[1]), '05b')
            rt = format(int(line[2]), '05b')
            f.write(convertToHex(str('000000') + str(rs) + str(rt) + str(rd) + str('00000') + str('100100')) + '\n')

        else:
            print(line + " is undefined")

        currLine += 1

    f.close()


# Print formatted output into a txt file
def printOutput(regs, lineCount, instrCount, config):
    o = open("output.txt", "w")
    string = ''
    for i in range(4):
        for k in range(4):
            if (regs.read(str(k + (i * 4) + 8))):
                regs.write(str(k + (i * 4) + 8), (pow(2, 32) + regs.read(str(k + (i * 4) + 8))) & pow(2, 32) - 1)
            else:
                regs.write(str(k + (i * 4) + 8), regs.read(str(k + (i * 4) + 8)) & pow(2, 32) - 1)
            string += str(('$' + str(k + (i * 4) + 8) + ':').rjust(4) + ' ' + convertToHex(
                format(regs.read(str(k + (i * 4) + 8)), '032b')) + '\t')
        o.write(string + '\n')
        string = ''

    string += str(' $0: ' + convertToHex(format(regs.read("0"), '032b')) + '\t')
    string += str(" pc: " + convertToHex(format(regs.read("pc"), '032b')) + '\t')
    o.write(string + '\n\n')
    global totCycle
    global cache
    o.write(" Dynamic Instruction Count: " + str(instrCount) + "\n Total Cycle Count: " + str(
        totCycle) + "\n Cache Hit Rate: " + str(cache.calcHitRate()) + "%\n")
    o.write("\n Control Signals: \n")
    o.write(" MemToReg: " + str(control.memtoregcount))
    o.write("\n MemWrite: " + str(control.memwritecount))
    o.write("\n Branch: " + str(control.brachcount))
    o.write("\n ALUSrc: " + str(control.alusrccount))
    o.write("\n RegDst: " + str(control.regdstcount))
    o.write("\n RegWrite: " + str(control.regwritecount))
    if(config.processorType == 0):
        o.write("\n\n Five cycle instructions: " + str(control.fivecycle))
        o.write("\n Four cycle instructions: " + str(control.fourcycle))
        o.write("\n Three cycle instructions: " + str(control.threecycle))

    o.write("\n\nAddress:\tvalue(+0)\tvalue(+4)\tvalue(+8)\tvalue(+c)\n")

    string = ''
    for i in range(lineCount):
        string += str(convertToHex(format(int("0x2000", 16) + (i * 16), '032b')) + ':')
        for k in range(4):
            string += '\t'
            for l in range(4):
                string += format(stack.read((k * 4) + (i * 16) + (3 - l)), '02x')
        o.write(string + '\n')
        string = ''

def printHazardandForward(pipeLine):
    o = open("HazardsandForwards.txt", "w")
    string = "Hazards:\n"
    string += "lw_br: " + str(pipeLine.lw_br)
    string += "\nlw_use: " + str(pipeLine.lw_use)
    string += "\ncomp_br: " + str(pipeLine.comp_br)
    string += "\nflushes: " + str(pipeLine.flushes)
    string += "\nTotal Delays: " + str(pipeLine.totalDelays)
    o.write(string)
    string = "\nForwards:\n"
    string += "ALUOutM -> SrcAE: " + str(pipeLine.forwardA)
    string += "\nALUOutM -> SrcBE: " + str(pipeLine.forwardB)
    string += "\nALUOutM -> WriteDataE: " + str(pipeLine.forwardC)
    string += "\nALUOutM -> EqualD: " + str(pipeLine.forwardD)
    string += "\nResultW -> SrcAE: " + str(pipeLine.forward1)
    string += "\nResultW -> SrcBE: " + str(pipeLine.forward2)
    string += "\nResultW -> WriteDataE: " + str(pipeLine.forward3)
    string += "\nResultW -> EqualD: " + str(pipeLine.forward4)
    o.write(string)


def printCache(config):
    o = open("cache.txt", "w")
    string = ''
    global cache
    global CacheDebug
    o.write("Cache type: " + cache_dict[config.cache] + '\n')
    if (config.cache == 0):
        for i in range(config.setsize):
            string += "Block: " + str(i) + "\tValid Bit: " + str(cache.set[i].valid) + "\tTag: 0x" + format(cache.set[i].tag, '08x') + '\n'
            for j in range(config.blksize):
                string += str(j) + ": " + format(cache.set[i].inblk[j], '02x') + '\t'
                if (not (j + 1) % 4):
                    string += '\n'
    elif (config.cache == 1):
        for i in range(config.waysize):
            string += "Block: " + str(i) + '\n'
            for j in range(config.blksize):
                string += str(j) + ": " + format(cache.set[i].inblk[j], '02x') + '\t'
            string += '\n'
    elif (config.cache == 2 or config.cache == 3):
        for i in range(config.setsize):
            string += "Set: " + str(i) + '\n'
            for j in range(config.waysize):
                string += "Block: " + str(j) + '\n'
                for k in range(config.blksize):
                    string += str(k) + ": " + format(cache.set[i].way[j].inblk[k], '02x') + '\t'
                string += '\n'
            string += '\n'

    if(config.debug):
        string += CacheDebug

    o.write(string)


# This function interprets our machine code and runs the instructions line by line
def run(config):
    global instruction_calls
    global control
    global cache
    global programEnd
    global pipeLine
    global totCycle
    h = open("mc.txt", "r")
    mc = h.readlines()
    h.close()
    regs = Registers(config)
    control = Control(config)
    instruction_calls = 0

    mcLength = len(mc) * 4  # This really is the value of the last instruction in memory.
    if(config.processorType):
        pipeLine = Pipeline(config)
    while (not programEnd):
        if(regs.read("pc") == mcLength):
            instr = Instruction(0, True)
            function = 'bubble'
            control.RegWrite = 0
            control.MemtoReg = 0
            control.MemWrite = 0
            control.ALUControl = 0
            control.ALUSrc = 0
            control.RegDst = 0
            control.Branch = 0
        else:
            line = mc[int(regs.read("pc") / 4)]
            line = line.replace("\n", "")
            instr = Instruction(line)
            if (instr.type == "i"):
                function = i_type_func_dict[instr.func]  # if it is an i type instruction look at i type dictionary
            else:
                function = r_type_func_dict[instr.func]  # if it is an r type instruction look at r type dictionary
        if(config.processorType):
            pipeLine.cycle(config, instr, regs, function, mcLength)
        else:
            if (config.debug):
                print("Function: " + func_name_dict[function])
            reset(instr, config, regs)
            decode(instr, config, regs)
            debug = function(instr, config, regs)  # call the function
            instruction_calls += 1
            if (config.processorType == 0):
                if (regs.read("pc") == mcLength):
                    programEnd = True
    cache.endWriteBack(config)
    printOutput(regs, 11, instruction_calls, config)
    printCache(config)
    if(config.processorType):
        printHazardandForward(pipeLine)


def main():
    global cache
    global totCycle
    global programEnd
    global CacheDebug
    CacheDebug = ''
    programEnd = False
    assemble()
    config = Configure()
    cache = Cache(config)
    totCycle = 0
    run(config)


if __name__ == "__main__":
    main()
