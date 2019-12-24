from math import *
#-----allows raw input------#
try: input = raw_input
except NameError: pass
#--------Extra Funcs------
def minBitsSig(dec):
    if(dec == 0 or dec == -1 ):
        numBits = 1
    elif(dec < 0):
        dec = dec + 1
        numBits = int(log(abs(dec), 2) + 2 )
    else:
        numBits = int(log(abs(dec), 2) + 2 )
    return numBits

def printRegisters(list):
    i = 0
    while(i < len(list)):
        if(i>= 8 and i<= 23):
            print(f" ${i} = {list[i]}")
        i+= 1

def listPrint(list):
    i = 0
    while(i < len(list)):
        print(f"{i} = {list[i]}")
        i+= 1

def shiftLeft(binary, shifts):
    i=0
    while(i < shifts):
        binary = binary + "0"
        binary= binary[1:]
        i += 1
    return binary

def twosComplementBin(binary):
    if(binary[0] == "1"):
        length = len(binary)
        binary = (int(binary,2) ^ int(("1"*length), 2)) + 1
        length = str(length)
        binary = format(binary, "0{}b".format(length))
    return binary

def decToBinSig(dec, numBits):
    if(dec < 0 ):
        if(numBits < minBitsSig(dec)):
            return "Not enough bits"
        dec = dec + (2 ** numBits)
        binary = format(dec, "0b")

    elif(numBits < minBitsSig(dec)):
            return "Not enough bits"
    else:
        binary = format(dec, "0{}b".format(numBits))

    return binary


def printMemory(memory):
    k = 0
    a = 0
    print("\nAddress\t\tValue(+0)\tValue(+4)\tValue(+8)\tValue(+c)\tValue(+10)\tValue(+14)\tValue(+18)\tValue(+1c)", end = "")
    for i in range(0,9):
        print("")
        address = '0x' + format(a + 0x2000, '08x')
        print(f"{address}\t", end = "")
        a += 32
        for j in range(0,8):
            byte0 = format(memory[k + 0], "02x")
            byte1 = format(memory[k + 1], "02x")
            byte2 = format(memory[k + 2], "02x")
            byte3 = format(memory[k + 3], "02x")
            print(f"0x{byte3.upper()}{byte2.upper()}{byte1.upper()}{byte0.upper()}", end = "\t")
            k = k + 4
    print('')

def formatFloat(fnum, whole, decimal):
    fnum = str(fnum)
    fnum = fnum[:fnum.find('.')+1+decimal]
    if(len(fnum[:fnum.find('.')]) >= whole):
        fnum = fnum[fnum.find('.')-whole:]
        return fnum
    else:
        while(len(fnum[:fnum.find('.')]) < whole):
            fnum = '0'+ fnum
        return fnum


#------------------------------------------------------------------------------Classes----------------------------------------------------#
class Row:
    def __init__(self, instNum, column):
        self.instNum = instNum
        self.column = column[:]

    def addColumn(self, numColumns):
        for i in range(numColumns):
            self.column.append("-")


#State class#
class State:

    def __init__(self, memory, registers, instruction, stateNumber):
        self.mem = memory[:]
        self.reg = registers[:]
        self.inst = instruction
        self.stateNum = stateNumber

    def printState(self):
        print("-----------------------")
        print(f"State:{self.stateNum}")
        print('Registers: $8 - $23')
        printRegisters(self.reg)
        print('\nMemory contents 0x2000 - 0x2100 ', end = '')
        printMemory(self.mem)
        print("-----------------------")
        print('')


#Cycle Class#
class Cycle:
    def __init__(self, MemToReg, MemWrite, Branch, Alusrca, Alusrcb, Regdst, Regwrite):
        self.MemToReg = MemToReg
        self.MemWrite = MemWrite
        self.Branch = Branch
        self.Alusrca = Alusrca
        self.Alusrcb = Alusrcb
        self.Regdst =  Regdst
        self.Regwrite = Regwrite


    def printCycle(self):
        print(f"\t MemToReg =  {self.MemToReg}")
        print(f"\t MemWrite =  {self.MemWrite}")
        print(f"\t Branch   =  {self.Branch}")
        print(f"\t Alusrca  =  {self.Alusrca}")
        print(f"\t Alusrcb  =  {self.Alusrcb}")
        print(f"\t Regdst   =  {self.Regdst}")
        print(f"\t Regwrite =  {self.Regwrite}")



#CycleInfo Class#
class CycleInfo:
    def __init__(self, InstructionName, Type):
        self.instruction = InstructionName
        self.Type = Type
        self.taken = False
        self.c1 = Cycle('0','0','0','0','00','0','0')
        self.c2 = Cycle('0','0','0','0','11','0','0')                                           #(MemToReg, MemWrite, Branch, Alusrca, Alusrcb, Regdst, Regwrite)
        self.c3 = Cycle('0','0','0','0','00','0','0')
        self.c4 = Cycle('0','0','0','0','00','0','0')
        self.c5 = Cycle('0','0','0','0','00','0','0')

    def cycleUpdate(self):
        if(self.Type == 'R'):				#R-Type
            self.c3 = Cycle('1','0','0','1','00','0','0')                               #(MemToReg, MemWrite, Branch, Alusrca, Alusrcb, Regdst, Regwrite)
            self.c4 = Cycle('0','0','0','0','00','1','1')


        elif(self.Type == 'I'): #I-Type
            if(self.instruction == "ADDI"):
                self.c3 = Cycle('0','0','0','1','10','0','0')
                self.c4 = Cycle('0','0','0','0','00','0','1')                                         #(MemToReg, MemWrite, Branch, Alusrca, Alusrcb, Regdst, Regwrite)

            elif(self.instruction == "LUI"):
                self.c3 = Cycle('0','0','0','0','00','0','0')
                self.c4 = Cycle('0','0','0','0','00','0','0')

            elif(self.instruction == "ORI"):
                self.c3 = Cycle('0','0','0','0','00','0','0')
                self.c4 = Cycle('0','0','0','0','00','0','0')                       #(MemToReg, MemWrite, Branch, Alusrca, Alusrcb, Regdst, Regwrite)

            elif(self.instruction == "ANDI"):
                self.c3 = Cycle('0','0','0','0','00','0','0')
                self.c4 = Cycle('0','0','0','0','00','0','0')



        elif(self.Type == 'Branch'):		#Branching-Type
                self.c3 = Cycle('0','0','1','1','00','0','0')                           #(MemToReg, MemWrite, Branch, Alusrca, Alusrcb, Regdst, Regwrite)

        elif(self.Type == 'SW'):				#StoreWord
            self.c3 = Cycle('0','0','0','1','10','0','0')
            self.c4 = Cycle('0','1','0','0','00','0','0')

        elif(self.Type == 'LW'):				#LoadWord
            self.c3 = Cycle('0','0','0','1','10','0','0')
            self.c4 = Cycle('0','0','0','0','00','0','0')               #(MemToReg, MemWrite, Branch, Alusrca, Alusrcb, Regdst, Regwrite)
            self.c5 = Cycle('0','0','0','0','00','0','0')



#Double Signal Counter#
class DoubleBitSignal():
    def __init__(self, bit00, bit01, bit10, bit11, dontCares):
        self.bit00 = bit00
        self.bit01 = bit01
        self.bit10 = bit10
        self.bit11 = bit11
        self.dontCares = dontCares

#Single Signal Counter#
class SingleBitSignal():
    def __init__(self, zeros, ones, dontCares):
        self.zeros = zeros
        self.ones = ones
        self.dontCares = dontCares


#Overall Counters: CycleLengths ,SingleSig, DoubleSig
class Counter():
    def __init__(self, threeCycles, fourCycles, fiveCycles):
        self.threeCycles = threeCycles
        self.fourCycles = fourCycles
        self.fiveCycles = fiveCycles
        self.MemToReg = SingleBitSignal(0,0,0) #zeros, ones, dontCares
        self.MemWrite = SingleBitSignal(0,0,0) #zeros, ones, dontCares
        self.Branch = SingleBitSignal(0,0,0) #zeros, ones, dontCares
        self.Alusrca = SingleBitSignal(0,0,0) #zeros, ones, dontCares
        self.Alusrcb = DoubleBitSignal(0,0,0,0,0)  #bit00, bit01, bit10, bit11, dontCares
        self.Regdst = SingleBitSignal(0,0,0) #zeros, ones, dontCares
        self.Regwrite = SingleBitSignal(0,0,0) #zeros, ones, dontCares


                 #MemToReg, MemWrite, Branch, Alusrca, Alusrcb, Regdst, Regwrite,
    def printCounters(self):

        print(f"\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t#-------------Total Cycle Count For-------------#")
        print(f"\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tTotal Cycles = {(self.MemToReg.zeros + self.MemToReg.ones +self.MemToReg.dontCares)}\n")
        print(f"\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t3 Cycle = {self.threeCycles:04}")
        print(f"\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t4 Cycle = {self.fourCycles:04}")
        print(f"\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t5 Cycle = {self.fiveCycles:04}\n")
        print(f"\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t#---------Value Distribution of Signals-------------#")
        print(f"MemToReg:\t\t\t\t\tMemWrite:\t\t\t\t\tBranch:\t\t\t\t\t\t Alusrca:\t\t\t\t\t\tAlusrcb:\t\t\t\t\tRegdst:\t\t\t\t\t\t\tRegwrite:")

        # zeros printout#
        print(f"0 = {self.MemToReg.zeros:04} - {formatFloat((((self.MemToReg.zeros)/ (self.MemToReg.zeros + self.MemToReg.ones +self.MemToReg.dontCares)) * 100), 3, 1)}%   \t    "  #MemToReg
              f"0 = {self.MemWrite.zeros:04} - {formatFloat(((self.MemWrite.zeros)/ (self.MemWrite.zeros + self.MemWrite.ones +self.MemWrite.dontCares)) * 100,3,1)}%   \t    " #MemWrite
              f"0 = {self.Branch.zeros:04} - {formatFloat(((self.Branch.zeros)/ (self.Branch.zeros + self.Branch.ones +self.Branch.dontCares)) * 100,3,1)}%       "              #Branch
              f"     "
              f"0 = {self.Alusrca.zeros:04} - {formatFloat(((self.Alusrca.zeros)/ (self.Alusrca.zeros + self.Alusrca.ones +self.Alusrca.dontCares)) * 100,3,1)}%"                  #Alusrca
              f"   \t\t    0 = {self.Alusrcb.bit00:04} - {formatFloat(((self.Alusrcb.bit00)/ (self.Alusrcb.bit00 + self.Alusrcb.bit01 + self.Alusrcb.bit10 + self.Alusrcb.bit11 + self.Alusrcb.dontCares)) * 100,3,1)}%"  #Alusrcb
              f"   \t    0 = {self.Regdst.zeros:04} - {formatFloat(((self.Regdst.zeros)/ (self.Regdst.zeros + self.Regdst.ones +self.Regdst.dontCares)) * 100,3,1)}%"                                #Regdst
              f"   \t\t    0 = {self.Regwrite.zeros:04} - {formatFloat(((self.Regwrite.zeros)/ (self.Regwrite.zeros + self.Regwrite.ones +self.Regwrite.dontCares)) * 100,3,1)}%")                 #Regwrite

        # ones printout#
        print(f"1 = {self.MemToReg.ones:04} - {formatFloat(((self.MemToReg.ones)/ (self.MemToReg.zeros + self.MemToReg.ones +self.MemToReg.dontCares)) * 100,3,1)}%   \t    "  #MemToReg
              f"1 = {self.MemWrite.ones:04} - {formatFloat(((self.MemWrite.ones)/ (self.MemWrite.zeros + self.MemWrite.ones +self.MemWrite.dontCares)) * 100, 3, 1)}%   \t    " #MemWrite
              f"1 = {self.Branch.ones:04} - {formatFloat(((self.Branch.ones)/ (self.Branch.zeros + self.Branch.ones +self.Branch.dontCares)) * 100,3,1)}%       "              #Branch
              f"     "
              f"1 = {self.Alusrca.ones:04} - {formatFloat(((self.Alusrca.ones)/ (self.Alusrca.zeros + self.Alusrca.ones +self.Alusrca.dontCares)) * 100,3,1)}%"                  #Alusrca
              f"   \t\t    1 = {self.Alusrcb.bit01:04} - {formatFloat(((self.Alusrcb.bit01)/ (self.Alusrcb.bit00 + self.Alusrcb.bit01 + self.Alusrcb.bit10 + self.Alusrcb.bit11 + self.Alusrcb.dontCares)) * 100,3,1)}%"  #Alusrcb
              f"   \t    1 = {self.Regdst.ones:04} - {formatFloat(((self.Regdst.ones)/ (self.Regdst.zeros + self.Regdst.ones +self.Regdst.dontCares)) * 100,3,1)}%"                                #Regdst
              f"   \t\t    1 = {self.Regwrite.ones:04} - {formatFloat(((self.Regwrite.ones)/ (self.Regwrite.zeros + self.Regwrite.ones +self.Regwrite.dontCares)) * 100,3,1)}%")                 #Regwrite

        #dont cares printout +10 for srcb

        print(f"x = {self.MemToReg.dontCares:04} - {formatFloat(((self.MemToReg.dontCares)/ (self.MemToReg.zeros + self.MemToReg.ones +self.MemToReg.dontCares)) * 100,3,1)}%   \t    "  #MemToReg
              f"x = {self.MemWrite.dontCares:04} - {formatFloat(((self.MemWrite.dontCares)/ (self.MemWrite.zeros + self.MemWrite.ones +self.MemWrite.dontCares)) * 100,3,1)}%   \t    " #MemWrite
              f"x = {self.Branch.dontCares:04} - {formatFloat(((self.Branch.dontCares)/ (self.Branch.zeros + self.Branch.ones +self.Branch.dontCares)) * 100,3,1)}%       "              #Branch
              f"     "
              f"x = {self.Alusrca.dontCares:04} - {formatFloat(((self.Alusrca.dontCares)/ (self.Alusrca.zeros + self.Alusrca.ones +self.Alusrca.dontCares)) * 100,3,1)}%"                  #Alusrca
              f"   \t\t    2 = {self.Alusrcb.bit10:04} - {formatFloat(((self.Alusrcb.bit10)/ (self.Alusrcb.bit00 + self.Alusrcb.bit01 + self.Alusrcb.bit10 + self.Alusrcb.bit11 + self.Alusrcb.dontCares)) * 100,3,1)}%"  #Alusrcb
              f"   \t    x = {self.Regdst.dontCares:04} - {formatFloat(((self.Regdst.dontCares)/ (self.Regdst.zeros + self.Regdst.ones +self.Regdst.dontCares)) * 100,3,1)}%"                                #Regdst
              f"   \t\t    x = {self.Regwrite.dontCares:04} - {formatFloat(((self.Regwrite.dontCares)/ (self.Regwrite.zeros + self.Regwrite.ones +self.Regwrite.dontCares)) * 100,3,1)}%")                 #Regwrite

        print(f"\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t3 = {self.Alusrcb.bit11:04} - {formatFloat(((self.Alusrcb.bit11)/ (self.Alusrcb.bit00 + self.Alusrcb.bit01 + self.Alusrcb.bit10 + self.Alusrcb.bit11 + self.Alusrcb.dontCares)) * 100,3,1)}%")  #Alusrcb
        print(f"\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tx = {self.Alusrcb.dontCares:04} - {formatFloat(((self.Alusrcb.dontCares)/ (self.Alusrcb.bit00 + self.Alusrcb.bit01 + self.Alusrcb.bit10 + self.Alusrcb.bit11 + self.Alusrcb.dontCares)) * 100,3,1)}%")  #Alusrcb

    def updateCounters(self, cycle):
        if(cycle.MemToReg == "1"):                                                                           #MemToReg
            self.MemToReg.ones += 1
        elif(cycle.MemToReg == "0"):
            self.MemToReg.zeros += 1
        elif(cycle.MemToReg == "x"):
            self.MemToReg.dontCares += 1

        if(cycle.MemWrite == "1"):                                                                           #MemWrite
            self.MemWrite.ones += 1
        elif(cycle.MemWrite == "0"):
            self.MemWrite.zeros += 1
        elif(cycle.MemWrite == "x"):
            self.MemWrite.dontCares += 1

        if(cycle.Branch == "1"):                                                                           #Branch
            self.Branch.ones += 1
        elif(cycle.Branch == "0"):
            self.Branch.zeros += 1
        elif(cycle.Branch == "x"):
            self.Branch.dontCares += 1

        if(cycle.Alusrca == "1"):                                                                           #AlusrcA
            self.Alusrca.ones += 1
        elif(cycle.Alusrca == "0"):
            self.Alusrca.zeros += 1
        elif(cycle.Alusrca == "x"):
            self.Alusrca.dontCares += 1


        if(cycle.Alusrcb ==  "00"):                                                                           #Alusrcb
            self.Alusrcb.bit00 += 1
        elif(cycle.Alusrcb == "01"):
            self.Alusrcb.bit01 += 1
        elif(cycle.Alusrcb == "10"):
            self.Alusrcb.bit10 += 1
        elif(cycle.Alusrcb == "11"):
            self.Alusrcb.bit11 += 1
        elif(cycle.Alusrcb == "x"):
            self.Alusrcb.dontCares += 1

        if(cycle.Regdst == "1"):                                                                           #Regdst
            self.Regdst.ones += 1
        elif(cycle.Regdst == "0"):
            self.Regdst.zeros += 1
        elif(cycle.Regdst == "x"):
            self.Regdst.dontCares += 1

        if(cycle.Regwrite == "1"):                                                                           #Regwrite
            self.Regwrite.ones += 1
        elif(cycle.Regwrite == "0"):
            self.Regwrite.zeros += 1
        elif(cycle.Regwrite == "x"):
            self.Regwrite.dontCares += 1
