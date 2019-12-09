from math import *
from decimal import Decimal, ROUND_HALF_UP
import copy

#-----allows raw input------#
try: input = raw_input
except NameError: pass
#--------extra funcs------#
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
        address = '0x' + format(a, '08x')
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
#state class#
class State:

    def __init__(self, memory, registers, instruction, stateNumber):
        self.mem = memory[:]
        self.reg = registers[:]
        self.inst = instruction
        self.stateNum = stateNumber

    def printState(self):
        print("-----------------------")
        print(f"During instruction: 0x{self.inst}'s cycles , State:{self.stateNum}")
        print('Registers: $8 - $23')
        printRegisters(self.reg)
        print('\nMemory contents 0x2000 - 0x2100 ', end = '')
        printMemory(self.mem)
        print("-----------------------")
        print('')


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
        print(f"MemToReg =  {self.MemToReg}")
        print(f"MemWrite =  {self.MemWrite}")
        print(f"Branch   =  {self.Branch}")
        print(f"Alusrca  =  {self.Alusrca}")
        print(f"Alusrcb  =  {self.Alusrcb}")
        print(f"Regdst   =  {self.Regdst}")
        print(f"Regwrite =  {self.Regwrite}")


#(MemToReg, MemWrite, Branch, Alusrca, Alusrcb, Regdst, Regwrite)

class CycleInfo:
    def __init__(self, InstructionName, Type):
        self.instruction = InstructionName
        self.type = Type
        self.taken = False
        self.c1 = Cycle('0','0','0','0','00','0','0')
        self.c2 = Cycle('0','0','0','0','11','0','0')
        self.c3 = Cycle('0','0','0','0','0','0','0')
        self.c4 = Cycle('0','0','0','0','0','0','0')
        self.c5 = Cycle('0','0','0','0','0','0','0')

    def cycleUpdate(self):
        if(self.type == 'R'):				#R-Type
            self.c3 = Cycle('0','0','0','1','00','0','0')
            self.c4 = Cycle('0','0','0','0','0','1','1')

        # IGNORE FOR NOW #SIGNAL DONE FOR ADDI
        elif(self.type == 'addi'): # addi, lui, ori, andi

            self.c3 = Cycle('0','0','1','1','10','0','0')
            self.c4 = Cycle('0','0','0','0','0','0','1')
        # IGNORE FOR NOW


       ## YOU WERE HERE (START) # Need to research the control signals for LUI, OR, ANDI
        elif(self.type == 'I'): #I-Type
            if(self.instruction == "ADDI"):
                self.c3 = Cycle('0','0','0','0','00','0','0')
                self.c4 = Cycle('0','0','0','0','0','0','0')

            elif(self.instruction == "LUI"):
                self.c3 = Cycle('0','0','0','0','00','0','0')
                self.c4 = Cycle('0','0','0','0','0','0','0')

            elif(self.instruction == "ORI"):
                self.c3 = Cycle('0','0','0','0','00','0','0')
                self.c4 = Cycle('0','0','0','0','0','0','0')

            elif(self.instruction == "ANDI"):
                self.c3 = Cycle('0','0','0','0','00','0','0')
                self.c4 = Cycle('0','0','0','0','0','0','0')



        elif(self.type == 'Branch'):		#Branching-Type
            if(self.taken == True):
                self.c3 = Cycle('0','0','1','1','00','0','0')
            else: #For NotTaken not sure about this either
                self.c3 = Cycle('0','0','0','0','0','0','0')


        elif(self.type == 'SW'):				#StoreWord (DONE)
            self.c3 = Cycle('0','0','0','1','10','0','0')
            self.c4 = Cycle('0','1','0','0','0','0','0')

        elif(self.type == 'LW'):				#LoadWord
            self.c3 = Cycle('0','0','0','1','10','0','0')
            self.c4 = Cycle('0','0','0','0','0','0','0') # no need to IorD = 1
            self.c5 = Cycle('0','0','0','0','00','0','0')



class DoubleBitSignal():
    def __init__(self, bit00, bit01, bit10, bit11, dontCares):
        self.bit00 = bit00
        self.bit01 = bit01
        self.bit10 = bit10
        self.bit11 = bit11
        self.dontCares = dontCares

class SingleBitSignal():
    def __init__(self, zeros, ones, dontCares):
        self.zeros = zeros
        self.ones = ones
        self.dontCares = dontCares

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
              f"   \t\t    00 = {self.Alusrcb.bit00:04} - {formatFloat(((self.Alusrcb.bit00)/ (self.Alusrcb.bit00 + self.Alusrcb.bit01 + self.Alusrcb.bit10 + self.Alusrcb.bit11 + self.Alusrcb.dontCares)) * 100,3,1)}%"  #Alusrcb
              f"   \t    0 = {self.Regdst.zeros:04} - {formatFloat(((self.Regdst.zeros)/ (self.Regdst.zeros + self.Regdst.ones +self.Regdst.dontCares)) * 100,3,1)}%"                                #Regdst
              f"   \t\t    0 = {self.Regwrite.zeros:04} - {formatFloat(((self.Regwrite.zeros)/ (self.Regwrite.zeros + self.Regwrite.ones +self.Regwrite.dontCares)) * 100,3,1)}%")                 #Regwrite

        # ones printout#
        print(f"1 = {self.MemToReg.ones:04} - {formatFloat(((self.MemToReg.ones)/ (self.MemToReg.zeros + self.MemToReg.ones +self.MemToReg.dontCares)) * 100,3,1)}%   \t    "  #MemToReg
              f"1 = {self.MemWrite.ones:04} - {formatFloat(((self.MemWrite.ones)/ (self.MemWrite.zeros + self.MemWrite.ones +self.MemWrite.dontCares)) * 100, 3, 1)}%   \t    " #MemWrite
              f"1 = {self.Branch.ones:04} - {formatFloat(((self.Branch.ones)/ (self.Branch.zeros + self.Branch.ones +self.Branch.dontCares)) * 100,3,1)}%       "              #Branch
              f"     "
              f"1 = {self.Alusrca.ones:04} - {formatFloat(((self.Alusrca.ones)/ (self.Alusrca.zeros + self.Alusrca.ones +self.Alusrca.dontCares)) * 100,3,1)}%"                  #Alusrca
              f"   \t\t    01 = {self.Alusrcb.bit01:04} - {formatFloat(((self.Alusrcb.bit01)/ (self.Alusrcb.bit00 + self.Alusrcb.bit01 + self.Alusrcb.bit10 + self.Alusrcb.bit11 + self.Alusrcb.dontCares)) * 100,3,1)}%"  #Alusrcb
              f"   \t    1 = {self.Regdst.ones:04} - {formatFloat(((self.Regdst.ones)/ (self.Regdst.zeros + self.Regdst.ones +self.Regdst.dontCares)) * 100,3,1)}%"                                #Regdst
              f"   \t\t    1 = {self.Regwrite.ones:04} - {formatFloat(((self.Regwrite.ones)/ (self.Regwrite.zeros + self.Regwrite.ones +self.Regwrite.dontCares)) * 100,3,1)}%")                 #Regwrite

        #dont cares printout +10 for srcb

        print(f"x = {self.MemToReg.dontCares:04} - {formatFloat(((self.MemToReg.dontCares)/ (self.MemToReg.zeros + self.MemToReg.ones +self.MemToReg.dontCares)) * 100,3,1)}%   \t    "  #MemToReg
              f"x = {self.MemWrite.dontCares:04} - {formatFloat(((self.MemWrite.dontCares)/ (self.MemWrite.zeros + self.MemWrite.ones +self.MemWrite.dontCares)) * 100,3,1)}%   \t    " #MemWrite
              f"x = {self.Branch.dontCares:04} - {formatFloat(((self.Branch.dontCares)/ (self.Branch.zeros + self.Branch.ones +self.Branch.dontCares)) * 100,3,1)}%       "              #Branch
              f"     "
              f"x = {self.Alusrca.dontCares:04} - {formatFloat(((self.Alusrca.dontCares)/ (self.Alusrca.zeros + self.Alusrca.ones +self.Alusrca.dontCares)) * 100,3,1)}%"                  #Alusrca
              f"   \t\t    10 = {self.Alusrcb.bit10:04} - {formatFloat(((self.Alusrcb.bit10)/ (self.Alusrcb.bit00 + self.Alusrcb.bit01 + self.Alusrcb.bit10 + self.Alusrcb.bit11 + self.Alusrcb.dontCares)) * 100,3,1)}%"  #Alusrcb
              f"   \t    x = {self.Regdst.dontCares:04} - {formatFloat(((self.Regdst.dontCares)/ (self.Regdst.zeros + self.Regdst.ones +self.Regdst.dontCares)) * 100,3,1)}%"                                #Regdst
              f"   \t\t    x = {self.Regwrite.dontCares:04} - {formatFloat(((self.Regwrite.dontCares)/ (self.Regwrite.zeros + self.Regwrite.ones +self.Regwrite.dontCares)) * 100,3,1)}%")                 #Regwrite

        print(f"\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t 3 = {self.Alusrcb.bit11:04} - {formatFloat(((self.Alusrcb.bit11)/ (self.Alusrcb.bit00 + self.Alusrcb.bit01 + self.Alusrcb.bit10 + self.Alusrcb.bit11 + self.Alusrcb.dontCares)) * 100,3,1)}%")  #Alusrcb
        print(f"\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t x = {self.Alusrcb.dontCares:04} - {formatFloat(((self.Alusrcb.dontCares)/ (self.Alusrcb.bit00 + self.Alusrcb.bit01 + self.Alusrcb.bit10 + self.Alusrcb.bit11 + self.Alusrcb.dontCares)) * 100,3,1)}%")  #Alusrcb

    def updateCounters(self, cycle):
        if(cycle.MemToReg == "1"):                                                                           #MemToReg
            self.MemToReg.ones += 1
        elif(cycle.MemToReg == "0"):
            self.MemToReg.zeros += 1
        elif(cycle.MemToReg == "x"):
            self.MemToReg.dontCares += 1

        if(cycle.MemWrite == "1"):                                                                           #MemWrite
            self.MemWrite.ones += 1
        elif(cycle.MemToReg == "0"):
            self.MemWrite.zeros += 1
        elif(cycle.MemToReg == "x"):
            self.MemWrite.dontCares += 1

        if(cycle.Branch == "1"):                                                                           #Branch
            self.Branch.ones += 1
        elif(cycle.Branch == "0"):
            self.Branch.zeros += 1
        elif(cycle.Branch == "x"):
            self.Branch.dontCares += 1

        if(cycle.Alusrca == "1"):                                                                           #AlusrcA
            self.Alusrca.ones += 1
        elif(cycle.Branch == "0"):
            self.Alusrca.zeros += 1
        elif(cycle.Branch == "x"):
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
#------------------------SIM---------------#
def sim(program, deBug, CpuType):
    finished = False      # Is the simulation finished? 
    PC = 0                # Program Counter
    HI = 0                
    LO = 0
    register = [0] * 32   # Let's initialize 32 empty registers
    mem = [0] * 0x1000     # Let's initialize 0x3000 or 12288 spaces in memory. I know this is inefficient...
    DIC = 0               # Dynamic Instr Count
    skip = False    #for deBug
    skipCount = 0   #for deBug
    printDicInput = "n"     #for deBug
    m = open("memAddr.txt","w+") #outPut File for cash

    #------------------------ForCycleMode--------------------------#
    cycle = {
        'count'  : 0,
        'length' : 0
    }
    nextCycle = False
    multiSkip = 0
    userStop = 1
    m_cyclePrint = False
    cycInfo = CycleInfo('None','None')
    counter = Counter(0,0,0)

    #-----For previous state------#
    oldRegister = []
    oldMem = []
    states = []



    #----------------------------------------------------SIMULATOR LOOP-----------------------------------------------------------------------#
    while(not(finished)):
        if PC == len(program) :
            finished = True
            break
        fetch = program[PC]
        register[0] = 0 # keep $0 = 0


        #-----------Saving pre-simulator state------------------#

        oldMem = mem[:]
        oldRegister = register[:]
        currentState = State(mem, register, format(int(fetch,2), '08x'),DIC)
        states.append(currentState)



        #-----------------------------------------------------------------Begining to simulate instruction-------------------------------------------------------------------#

        if fetch[0:6] == '001000': #<--------------------------------#  ADDI
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            imm = -(65536 - int(fetch[16:],2)) if fetch[16]=='1' else int(fetch[16:],2)
            register[t] = register[s] + imm
            #For Multi-Cycle
            cycle.update({"length": 4})
            cycInfo.instruction = "ADDI"
            cycInfo.Type = 'I'



        elif fetch[0:6] == '000000' and fetch[21:32] == '00000100001':#<--------------------------------#  ADDU
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            d = int(fetch[16:21],2)
            temp = 0
            s = int(decToBinSig(register[s], 32), 2)
            t = int(decToBinSig(register[t], 32), 2)
            temp = s + t
            temp = decToBinSig(temp,minBitsSig(temp))
            if(len(temp) > 32):
                temp = temp[(len(temp)-32):]
            if(temp[0]== "1"):
                temp = twosComplementBin(temp)
                temp = int(temp, 2) * -1
            else:
                temp = int(temp,2)
            register[d] = temp
            #For Multi-Cycle
            cycle.update({"length": 4})
            cycInfo.instruction = "ADDU"
            cycInfo.Type = 'R'

        elif fetch[0:6] == '000000' and fetch[21:32] == '00000100000':#<--------------------------------# ADD
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            d = int(fetch[16:21],2)
            register[d] = register[s] + register[t]
            #For Multi-Cycle
            cycle.update({"length": 4})
            cycInfo.instruction = "ADD"
            cycInfo.Type = 'R'

        elif fetch[0:6] == '000000' and fetch[21:32] == '00000100010': #<--------------------------------#  SUB
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            d = int(fetch[16:21],2)
            register[d] = register[s] - register[t]
            #For Multi-Cycle
            cycle.update({"length": 4})
            cycInfo.instruction = "SUB"
            cycInfo.Type = 'R'


        elif fetch[0:6] == '000000' and fetch[26:32] == '000010':#<--------------------------------#  SRL
            PC += 4
            t = int(fetch[11:16],2)
            d = int(fetch[16:21],2)
            h = int(fetch[21:26],2)
            register[d] = register[t] >> h
            #For Multi-Cycle
            cycle.update({"length": 4})
            cycInfo.instruction = "SRL"
            cycInfo.Type = 'R'

        elif fetch[0:6] == '000000' and fetch[26:32] == '000000':#<--------------------------------#  SLL
            PC += 4
            t = int(fetch[11:16],2)
            d = int(fetch[16:21],2)
            h = int(fetch[21:26],2)
            t = decToBinSig(register[t],32)
            t = shiftLeft(t, h)
            if(t[0] == "1"):
                t = twosComplementBin(t)
                t = int(t,2) * -1
            else:
                t = int(t, 2)
            register[d] = t
            #For Multi-Cycle
            cycle.update({"length": 4})
            cycInfo.instruction = "SLL"
            cycInfo.Type = 'R'
            
        elif fetch[0:6] == '000100':  #<--------------------------------#    # BEQ
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            imm = -(65536 - int(fetch[16:],2)) if fetch[16]=='1' else int(fetch[16:],2)
            #For Multi-Cycle
            cycle.update({"length": 3})
            cycInfo.instruction = "BEQ"
            cycInfo.Type = 'I'
            # Compare the registers and decide if jumping or not
            if register[s] == register[t]:
                PC += imm*4
                cycInfo.taken = True
            else:
                cycInfo.taken = False

        elif fetch[0:6] == '000101':        #<--------------------------------BNE
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            imm = -(65536 - int(fetch[16:],2)) if fetch[16]=='1' else int(fetch[16:],2)
            #For Multi-Cycle
            cycle.update({"length": 3})
            cycInfo.instruction = "BEQ"
            cycInfo.Type = 'I'
            # Compare the registers and decide if jumping or not
            if register[s] != register[t]:
                PC += imm*4
                cycInfo.taken = True
            else:
                cycInfo.taken = False

        
        elif fetch[0:6] == '001101':      #<--------------------------------# ORI
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            imm = int(fetch[16:],2)
            register[t] = register[s] | imm
            #for multi-cycle#
            cycle.update({'length':4})
            cycInfo.type = "I"
            cycInfo.instruction = "ORI"



        elif fetch[0:6] == '001100':    #<--------------------------------# ANDI
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            imm = int(fetch[16:],2)
            register[t] = register[s] & imm
            #For Multi-Cycle
            cycle.update({"length": 4})
            cycInfo.instruction = "ANDI"
            cycInfo.Type = 'I'

        elif fetch[0:6] == '101011':    #<--------------------------------# SW
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            offset = -(65536 - int(fetch[16:],2)) if fetch[16]=='1' else int(fetch[16:],2)
            offset = offset + register[s]-0x2000
            m.write(f"SW @ dic:, {DIC - 1}, {format((offset + 0x2000), '08x')}  \n")
            if (offset % 4) == 0:
                mem[offset+3] = (register[t] >> 24) & 0x000000ff  # +3
                mem[offset+2] = (register[t] >> 16) & 0x000000ff # +2
                mem[offset+1] = (register[t] >> 8) & 0x000000ff # +1
                mem[offset+0] = register[t] & 0x000000ff  # +0
            #For Multi-Cycle
            cycle.update({"length": 4})
            cycInfo.instruction = "SW"
            cycInfo.Type = 'SW'

        elif fetch[0:6] == '100011': #<--------------------------------# LW
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            offset = -(65536 - int(fetch[16:],2)) if fetch[16]=='1' else int(fetch[16:],2)
            offset = offset + register[s]-0x2000
            m.write(f"LW @ dic:, {DIC - 1}, {format((offset + 0x2000), '08x')}  \n")
            memoffset0 = format((mem[offset+0]), '02x')
            memoffset1 = format((mem[offset+1]), '02x')
            memoffset2 = format((mem[offset+2]), '02x')
            memoffset3 = format((mem[offset+3]), '02x')
            loaded = memoffset3 + memoffset2 + memoffset1 + memoffset0
            loaded = format(int(loaded, 16), "0b")
            if(len(loaded) != 32 ):
                while(len(loaded) < 32):
                    loaded = "0" + loaded
            if(loaded[0] == "1"):
                loaded = twosComplementBin(loaded)
                loaded = int(loaded, 2) * -1
            else:
                loaded = int(loaded,2)
            register[t] = loaded
            #For Multi-Cycle
            cycle.update({"length": 5})
            cycInfo.instruction = "LW"
            cycInfo.Type = 'LW'

        elif fetch[0:6] == '000000' and fetch[21:32] == '00000101010':#<--------------------------------#  SLT
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            d = int(fetch[16:21],2)
            if (register[s] < register[t]): 
                register[d] = 1
            else:
                register[d] = 0
            #For Multi-Cycle
            cycle.update({"length": 4})
            cycInfo.instruction = "SLT"
            cycInfo.Type = 'R'

        elif fetch[0:6] == '001111': #<--------------------------------#  LUI
            PC += 4
            t = int(fetch[11:16],2)
            imm = int(fetch[16:],2)
            imm = imm << 16
            register[t] = imm
            #For Multi-Cycle
            cycle.update({"length": 4})
            cycInfo.instruction = "LUI"
            cycInfo.Type = 'I'

        elif fetch[0:6] == '000000' and fetch[21:32] == '00000011001': # MULTU
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            result = register[s] * register[t]
            result = format(result,'064b')    
            HI = int(result[0:32],2)
            LO = int(result[32:64],2)

        elif fetch[0:6] == '000000' and fetch[21:32] == '00000100110': #<--------------------------------# XOR
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            d = int(fetch[16:21],2)
            register[d] = register[s] ^ register[t]
            #For Multi-Cycle
            cycle.update({"length": 4})
            cycInfo.instruction = "XOR"
            cycInfo.Type = 'R'


        elif fetch[0:6] == '000000' and fetch[21:32] == '00000010000':#<--------------------------------#  MFHI
            PC += 4
            d = int(fetch[16:21],2)
            register[d] = HI

        elif fetch[0:6] == '000000' and fetch[21:32] == '00000010010':#<--------------------------------#  MFLO
            PC += 4
            d = int(fetch[16:21],2)
            register[d] =  LO            

        else:
            # This is not implemented on purpose
            PC += 4
            print('Not implemented')


        bit32Mem = []*0x400
        for i in range (0,0x400,4):
            bits = hex((mem[i+3]<<24) + (mem[i+2]<<16) + (mem[i+1]<<8) + (mem[i]))
            bit32Mem.append(("%08X" % int(bits, 16)))

        DIC += 1

        #------------------------------------------------------------Simulation Part Done----------------------------------------------------------------------------------------#


        #-----------------------------------------------------Multi-Cycle---------------------------------------------------------------------------------------------#
        cycInfo.cycleUpdate()                   #Update cycles based on instruction
        if(CpuType == "m" ) :
            cycleStop = cycle['count'] + cycle['length']
            cycleStart = cycle['count']
            if(cycle['length'] == 3):
                counter.threeCycles += 1
            elif(cycle['length'] == 4):
                counter.fourCycles += 1
            elif(cycle['length'] == 5):
                counter.fiveCycles += 1

            while(cycle['count'] < cycleStop):
                cycle['count'] += 1

                if(userStop == cycle['count']):
                    m_cyclePrint = False
                    userStop == "n"

                if( (m_cyclePrint == True and type(userStop) == int)  or (userStop == "n" and deBug == "y")  or userStop == 1 or userStop == cycle['count'] ):
                    print(f"inst = {cycInfo.instruction},     C.L = {cycle.get('length')},    C.S-C.L = {cycleStop - cycle.get('length')},    C.L-1 = {cycle.get('length') -1 },  DIC = {DIC-1}  ")
                    print(f"Cycle : {cycle.get('count')}\n")
                    if( (cycleStop - cycle.get('count')) == (cycle.get('length') -1 ) ):
                        print(f"{cycInfo.instruction}'s Cycle 1\n")
                        cycInfo.c1.printCycle()
                        counter.updateCounters(cycInfo.c1)
                        counter.printCounters()
                    elif((cycleStop - cycle.get('count')) == (cycle.get('length') -2 ) ):
                        print(f"{cycInfo.instruction}'s Cycle 2\n")
                        cycInfo.c2.printCycle()
                        counter.updateCounters(cycInfo.c2)
                        counter.printCounters()
                    elif((cycleStop - cycle.get('count')) == (cycle.get('length') -3 ) ):
                        print(f"{cycInfo.instruction}'s Cycle 3\n")
                        cycInfo.c3.printCycle()
                        counter.updateCounters(cycInfo.c3)
                        counter.printCounters()
                    elif((cycleStop - cycle.get('count')) == (cycle.get('length') -4 ) ):
                        print(f"{cycInfo.instruction}'s Cycle 4\n")
                        cycInfo.c4.printCycle()
                        counter.updateCounters(cycInfo.c4)
                        counter.printCounters()
                    elif((cycleStop - cycle.get('count')) == (cycle.get('length') -5 ) ):
                        print(f"{cycInfo.instruction}'s Cycle 5\n")
                        cycInfo.c5.printCycle()
                        counter.updateCounters(cycInfo.c5)
                        counter.printCounters()
                    print('')
                    print("-------------------------------------------------------------------------------------------------------------------")
                    print('')


                    # print("-----------------------")
                    # print(f"cycleCount:{cycle['count']},       cycleStop:{cycleStop},    cycleLength:{cycle.get('length')}      fetch = {format(int(fetch,2), '08x')},  ")
                    # print("PC: {}, HI: {}, LO:{}".format(PC-4, HI, LO))
                    # print('Dynamic Instr Count: ', DIC-1)
                    # print('Registers: $8 - $23')
                    # printRegisters(oldRegister)
                    # print('\nMemory contents 0x2000 - 0x2100 ')
                    # printMemory(oldMem)
                    # print('')

                if( (  (deBug == "y")  and (userStop != "n")  and (m_cyclePrint == False) and (userStop == cycle['count'])  ) or nextCycle == True):
                    userStop = input("Want to skip to certain cycle? type 'n' for NO, or type cycle number you wish to skip to\n")
                    if(userStop != "n"):
                        userStop = int(userStop)
                        multiSkip = input("Want to print along the way? 'y' for yes\n")
                        nextCycle = False
                        if(multiSkip == "y"):
                            m_cyclePrint = True
                        else:
                            m_cyclePrint = False



                if(userStop == "n" and deBug == "y"):
                    deBug = input("Next Cycle?\n")
                    if(deBug == "y"):
                        nextCycle = True
                    else:
                        nextCycle = False




        #---------------------------------------------For Debug---------------------------------------------------------------------------------#
        if(printDicInput == "y" and (skip == True) ):
            print("-----------------------")
            print("PC: {}, HI: {}, LO:{}".format(PC, HI, LO))
            print('Dynamic Instr Count: ', DIC)
            print('Registers: $8 - $23')
            printRegisters(register)
            printMemory(mem)
            print('')

        if(skip == False):
            printDicInput = "n"

            if(deBug == "y" and CpuType == "n"):
                print("-----------------------")
                print("PC: {}, HI: {}, LO:{}".format(PC, HI, LO))
                print('Dynamic Instr Count: ', DIC)
                print('Registers: $8 - $23')
                printRegisters(register)
                print('\nMemory contents 0x2000 - 0x2100 ', end = '')
                printMemory(mem)
                print('')

                userInput = input("Want to skip to certain dic? type 'n' for NO, or type dic number you wish to skip to\n")
                if(userInput == "n"):
                    userInput = input("Next Step? type y for yes \n")
                    if(userInput == "y"):
                        deBug = "y"
                    else:
                        deBug = "n"
                else:
                    skip = True
                    skipCount = int(userInput)
                    printDicInput = input("Want to print along the way? 'y' for yes\n")

        if(DIC == skipCount - 1):
            skip = False
    print("")



    currentState = State(mem, register, format(int(fetch,2), '08x'),DIC)
    states.append(currentState)




#---------------------------Final Print Out stats---------------------------------------------------------------------#
    print('***Simulation finished***')
    print("PC: {}, HI: {}, LO:{}".format(PC, HI, LO))
    print('Dynamic Instr Count: ', DIC)
    print('Registers: $8 - $23')
    printRegisters(register)
    print('\nMemory contents 0x2000 - 0x2100 ')
    printMemory(mem)


    outMem = open('outputMemory.txt', "w+")
    outMem.write("Address Value(+0)\tValue(+4)\tValue(+8)\tValue(+c)\tValue(+10)\tValue(+14)\tValue(+18)\tValue(1c)\n")
    for j in range(0,9):   # j is a row of 0x20 addresses in Mars (can be from 0 to 32 - but need at least 9 to show all addresses for project1)
        outMem.write(hex(j*32+0x2000)+"\t")
        for i in range(0,8):        # i is the column in MARS such that: address + value(i*4)
            outMem.write(("0x" +bit32Mem[j*8+i]))
            outMem.write("\t")
        outMem.write("\n")

    #counter.printCounters()

    m.close()
    outMem.close()

    # for state in states:
    #     state.printState()
    # print(f"length of states: {len(states)}")

#-----MAIN-----#
def main():
    validInstructions = []  #list of valid instructions
    labelName= []           #list of label names
    labelIndex= []          #list of label indicies



    #----opening files----#
    f = open("output.txt","w+")
    h = open("TestCase24.asm","r")                 # INPUT FILE NAME WITH ASM CODE HERE
    asm = h.readlines()


    #------removing unnecessary characters-------#
    i = 0
    while(i < len(asm)):
        line = asm[i]

        line = line.replace("\n", "")
        line = line.replace("\t", "")
        line = line.replace("$","")
        line = line.replace("zero","0")
        line = line.replace(" ","")

            #-----removing comments------#
        if(line.find("#") != -1):
            line = line[0: line.find("#")]

            #-----replacing hex with decimal------#
        if(line.find('0x') != -1): #finding if line contains hex number
            if(line.find('(') != -1):
                hex = line[line.find('0x') : line.find('(')]
                decimal = str(int(line[line.find('0x')+2 : line.find('(')],16))
                line = line.replace(hex, decimal)

            else:
                start = line.find('0x') #finding the starting index of the hex number
                hex = line[start+2:]
                line = line[:start]
                decimal = str(int(hex, 16))
                line = line + decimal



            #-----only adding valid instructions and Labels------#
        if(line[0:5] == "addiu"): validInstructions.append(line)   # ADDIU
        elif(line[0:4] == "addi"): validInstructions.append(line)   # ADDI
        elif(line[0:4] == "addu"): validInstructions.append(line)   # ADDU
        elif(line[0:3] == "add"): validInstructions.append(line)  # ADD
        elif(line[0:3] == "sub"): validInstructions.append(line)  # SUB
        elif(line[0:5] == "multu"): validInstructions.append(line)  # MULTU
        elif(line[0:4] == "mult"): validInstructions.append(line) # MULT
        elif(line[0:4] == "sltu"): validInstructions.append(line)   # SLTU
        elif(line[0:3] == "slt"): validInstructions.append(line)  # SLT
        elif(line[0:3] == "srl"): validInstructions.append(line)  # SRL
        elif(line[0:3] == "sll"): validInstructions.append(line)  # SLL
        elif(line[0:2] == "sw"): validInstructions.append(line)  # SW
        elif(line[0:2] == "lw"): validInstructions.append(line)   # LW
        elif(line[0:2] == "lb"): validInstructions.append(line) # LB
        elif(line[0:2] == "sb"): validInstructions.append(line)  # SB
        elif(line[0:2] == "lb"): validInstructions.append(line)  # LB
        elif(line[0:4] == "mfhi"): validInstructions.append(line) # MFHI
        elif(line[0:4] == "mflo"): validInstructions.append(line)  # MFLO
        elif(line[0:3] == "xor"): validInstructions.append(line)  # XOR
        elif(line[0:3] == "lui"): validInstructions.append(line)  # LUI
        elif(line[0:3] == "ori"): validInstructions.append(line)  # ORI
        elif(line[0:4] == "andi"): validInstructions.append(line)  # ANDI
        elif(line[0:4] == "fold"): validInstructions.append(line)  # FOLD
        elif(line[0:3] == "bne"): validInstructions.append(line)   # BNE
        elif(line[0:3] == "beq"): validInstructions.append(line)   # BEQ
        elif(line[0:1] == "j"): validInstructions.append(line)   # JUMP
        elif(line.find(":") != -1): validInstructions.append(line)

        i+=1


    #-----saving Label Names and Indexes-----#
    #-----and deleting Labels from ValidInstructions-----#
    i = 0
    while(i < len(validInstructions)):
        line = validInstructions[i]
        if(line.find(":") != -1):
            labelName.append(line[:line.find(":")])
            labelIndex.append(i)
            del validInstructions[i]

        i +=1



    #-----making list of pure valid binary instructions at every 4th index------#
    binaryInstructions = [0] * (len(validInstructions) * 4)


    #-----printing machine code------#
    i = 0
    while(i < len(validInstructions)):
        line = validInstructions[i]
        if(line[0:5] == "addiu"): # ADDIU
            line = line.replace("addiu","")
            line = line.split(",")
            imm = format(int(line[2]),'016b') if (int(line[2]) >= 0) else format(65536 + int(line[2]),'016b')
            rs = format(int(line[1]),'05b')
            rt = format(int(line[0]),'05b')
            binary = str('001001' + str(rs) + str(rt) + str(imm))
            binaryInstructions[i * 4] = binary
            #f.write(binary + "\n")
            f.write("0x" + format(int(binary,2), "08x") + "\n")



        elif(line[0:4] == "addi"): # ADDI
            line = line.replace("addi","")
            line = line.split(",")
            imm = format(int(line[2]),'016b') if (int(line[2]) >= 0) else format(65536 + int(line[2]),'016b')
            rs = format(int(line[1]),'05b')
            rt = format(int(line[0]),'05b')
            binary = str('001000') + str(rs) + str(rt) + str(imm)
            binaryInstructions[i * 4] = binary
            #f.write(binary + "\n")
            f.write("0x" + format(int(binary,2), "08x") + "\n")


        elif(line[0:4] == "addu"): # ADDU
            line = line.replace("addu","")
            line = line.split(",")
            rd = format(int(line[0]),'05b')
            rs = format(int(line[1]),'05b')
            rt = format(int(line[2]),'05b')
            binary = str('000000') + str(rs) + str(rt) + str(rd) + str('00000100001')
            binaryInstructions[i * 4] = binary
            #f.write(binary + "\n")
            f.write("0x" + format(int(binary,2), "08x") + "\n")


        elif(line[0:3] == "add"): # ADD
            line = line.replace("add","")
            line = line.split(",")
            rd = format(int(line[0]),'05b')
            rs = format(int(line[1]),'05b')
            rt = format(int(line[2]),'05b')
            binary = str('000000') + str(rs) + str(rt) + str(rd) + str('00000100000')
            binaryInstructions[i * 4] = binary
            #f.write(binary + "\n")
            f.write("0x" + format(int(binary,2), "08x") + "\n")

        elif(line[0:3] == "sub"): # SUB
            line = line.replace("sub","")
            line = line.split(",")
            rd = format(int(line[0]),'05b')
            rs = format(int(line[1]),'05b')
            rt = format(int(line[2]),'05b')
            binary = str('000000') + str(rs) + str(rt) + str(rd) + str('00000100010')
            binaryInstructions[i * 4] = binary
            #f.write(binary + "\n")
            f.write("0x" + format(int(binary,2), "08x") + "\n")

        elif(line[0:4] == "fold"): # FOLD
            line = line.replace("fold","")
            line = line.split(",")
            rd = format(int(line[0]),'05b')
            rs = format(int(line[1]),'05b')
            rt = format(int(line[2]),'05b')
            binary = str('000000') + str(rs) + str(rt) + str(rd) + str('00000011111')
            binaryInstructions[i * 4] = binary
            #f.write(binary + "\n")
            f.write("0x" + format(int(binary,2), "08x") + "\n")


        elif(line[0:5] == "multu"): # MULTU
            line = line.replace("multu","")
            line = line.split(",")
            rs = format(int(line[0]),'05b')
            rt = format(int(line[1]),'05b')
            binary = str('000000') + str(rs) + str(rt) + str('0000000000011001')
            binaryInstructions[i * 4] = binary
            #f.write(binary + "\n")
            f.write("0x" + format(int(binary,2), "08x") + "\n")



        elif(line[0:4] == "mult"): # MULT
            line = line.replace("mult","")
            line = line.split(",")
            rs = format(int(line[0]),'05b')
            rt = format(int(line[1]),'05b')
            binary = str('000000') + str(rs) + str(rt) + str('0000000000011000')
            binaryInstructions[i * 4] = binary
            #f.write(binary + "\n")
            f.write("0x" + format(int(binary,2), "08x") + "\n")



        elif(line[0:4] == "sltu"): # SLTU
            line = line.replace("sltu","")
            line = line.split(",")
            rd = format(int(line[0]),'05b')
            rs = format(int(line[1]),'05b')
            rt = format(int(line[2]),'05b')
            binary = str('000000') + str(rs) + str(rt) + str(rd) + str('00000101011')
            binaryInstructions[i * 4] = binary
            #f.write(binary + "\n")
            f.write("0x" + format(int(binary,2), "08x")  + "\n")



        elif(line[0:3] == "slt"): # SLT
            line = line.replace("slt","")
            line = line.split(",")
            rd = format(int(line[0]),'05b')
            rs = format(int(line[1]),'05b')
            rt = format(int(line[2]),'05b')
            binary = str('000000') + str(rs) + str(rt) + str(rd) + str('00000101010')
            binaryInstructions[i * 4] = binary
            #f.write(binary + "\n")
            f.write("0x" + format(int(binary,2), "08x")  + "\n")



        elif(line[0:3] == "srl"): # SRL
            line = line.replace("srl","")
            line = line.split(",")
            imm = format(int(line[2]),'05b') if (int(line[2]) > 0) else format(65536 + int(line[2]),'05b')
            rs = format(int(line[1]),'05b')
            rt = format(int(line[0]),'05b')
            binary = str('00000000000') + str(rs) + str(rt) + str(imm) + str('000010')
            binaryInstructions[i * 4] = binary
            #f.write(binary + "\n")
            f.write("0x" + format(int(binary,2), "08x")+ "\n")

        elif(line[0:3] == "sll"): # SLL
            line = line.replace("sll","")
            line = line.split(",")
            imm = format(int(line[2]),'05b') if (int(line[2]) > 0) else format(65536 + int(line[2]),'05b')
            rs = format(int(line[1]),'05b')
            rt = format(int(line[0]),'05b')
            binary = str('00000000000') + str(rs) + str(rt) + str(imm) + str('000000')
            binaryInstructions[i * 4] = binary
            #f.write(binary + "\n")
            f.write("0x" + format(int(binary,2), "08x")+ "\n")



        elif(line[0:2] == "sw"): # SW
            line = line.replace("sw","")
            line = line.replace("(",",")
            line = line.replace(")","")
            line = line.split(",")
            imm = format(int(line[1]),'016b') if (int(line[1]) >= 0) else format(65536 + int(line[1]),'016b')
            rs = format(int(line[2]),'05b')
            rt = format(int(line[0]),'05b')
            binary = str('101011') + str(rs) + str(rt) + str(imm)
            binaryInstructions[i * 4] = binary
            #f.write(binary + "\n")
            f.write("0x" + format(int(binary,2), "08x")+ "\n")



        elif(line[0:2] == "lw"): # LW
            line = line.replace("lw","")
            line = line.replace("(",",")
            line = line.replace(")","")
            line = line.split(",")
            imm = format(int(line[1]),'016b') if (int(line[1]) >= 0) else format(65536 + int(line[1]),'016b')
            rs = format(int(line[2]),'05b')
            rt = format(int(line[0]),'05b')
            binary = str('100011') + str(rs) + str(rt) + str(imm)
            binaryInstructions[i * 4] = binary
            #f.write(binary + "\n")
            f.write("0x" + format(int(binary,2), "08x")  + "\n")



        elif(line[0:2] == "lb"): # LB
            line = line.replace("lb","")
            line = line.replace("(",",")
            line = line.replace(")","")
            line = line.split(",")

            imm = format(int(line[1]),'016b') if (int(line[1]) > 0) else format(65536 + int(line[1]),'016b')
            rs = format(int(line[2]),'05b')
            rt = format(int(line[0]),'05b')
            binary = str('100000') + str(rs) + str(rt) + str(imm)
            binaryInstructions[i * 4] = binary
            #f.write(binary + "\n")
            f.write("0x" + format(int(binary,2), "08x")  + "\n")



        elif(line[0:2] == "sb"): # SB
            line = line.replace("sb","")
            line = line.replace("(",",")
            line = line.replace(")","")
            line = line.split(",")
            imm = format(int(line[1]),'016b') if (int(line[1]) > 0) else format(65536 + int(line[1]),'016b')
            rs = format(int(line[2]),'05b')
            rt = format(int(line[0]),'05b')
            binary = str('101000') + str(rs) + str(rt) + str(imm)
            binaryInstructions[i * 4] = binary
            #f.write(binary + "\n")
            f.write("0x" + format(int(binary,2), "08x")+ "\n")


        elif(line[0:2] == "lb"): # LB
            line = line.replace("lb","")
            line = line.replace("(",",")
            line = line.replace(")","")
            line = line.split(",")
            imm = format(int(line[1],16),'016b') if (int(line[1]) > 0) else format(65536 + int(line[1]),'016b')
            rs = format(int(line[2]),'05b')
            rt = format(int(line[0]),'05b')
            binary = str('100000') + str(rs) + str(rt) + str(imm)
            binaryInstructions[i * 4] = binary
            #f.write(binary + "\n")
            f.write("0x" + format(int(binary,2), "08x")  + "\n")


        elif(line[0:4] == "mfhi"): # MFHI
            line = line.replace("mfhi", "")
            rd = format(int(line), '05b')
            binary = str("0000000000000000") + str(rd) + str("00000010000")
            binaryInstructions[i * 4] = binary
            #f.write(binary + "\n")
            f.write("0x" + format(int(binary,2), "08x") + "\n")



        elif(line[0:4] == "mflo"): # MFLO
            line = line.replace("mflo", "")
            rd = format(int(line), '05b')
            binary = str("0000000000000000") + str(rd) + str("00000010010")
            binaryInstructions[i * 4] = binary
            #f.write(binary + "\n")
            f.write("0x" + format(int(binary,2), "08x") + "\n")


        elif(line[0:3] == "xor"): # XOR
            line = line.replace("xor", "")
            line = line.split(",")
            rd = format(int(line[0]),'05b')
            rs = format(int(line[1]),'05b')
            rt = format(int(line[2]),'05b')
            binary = str("000000") + str(rs) + str(rt) + str(rd) +str("00000100110")
            binaryInstructions[i * 4] = binary
            #f.write(binary + "\n")
            f.write("0x" + format(int(binary,2), "08x")  + "\n")


        elif(line[0:3] == "lui"): # LUI
            line = line.replace("lui","")
            line = line.split(",")
            rt = format(int(line[0]),'05b')
            imm = format(int(line[1]),'016b') if (int(line[1]) > 0) else format(65536 + int(line[1]),'016b')
            binary = str('001111') + str('00000') + str(rt) + str(imm)
            binaryInstructions[i * 4] = binary
            #f.write(binary + "\n")
            f.write("0x" + format(int(binary,2), "08x")  + "\n")



        elif(line[0:3] == "ori"): # ORI
            line = line.replace("ori","")
            line = line.split(",")
            imm = format(int(line[2]),'016b') if (int(line[2]) > 0) else format(65536 + int(line[1]),'016b')
            rs = format(int(line[1]),'05b')
            rt = format(int(line[0]),'05b')
            binary = str('001101') + str(rs) + str(rt) + str(imm)
            binaryInstructions[i * 4] = binary
            #f.write(binary + "\n")
            f.write("0x" + format(int(binary,2), "08x") + "\n")


        elif(line[0:4] == "andi"): # ANDI
            line = line.replace("andi","")
            line = line.split(",")
            imm = format(int(line[2]),'016b') if (int(line[2]) > 0) else format(65536 + int(line[2]),'016b')
            rs = format(int(line[1]),'05b')
            rt = format(int(line[0]),'05b')
            binary = str('001100') + str(rs) + str(rt) + str(imm)
            binaryInstructions[i * 4] = binary
            #f.write(binary + "\n")
            f.write("0x" + format(int(binary,2), "08x")  + "\n")


        elif(line[0:3] == "bne"): # BNE
            line = line.replace("bne", "")
            line = line.split(",")
            rs = format(int(line[0]),'05b')
            rt = format(int(line[1]),'05b')

            if (line[2].isdigit()):  # First,test to see if it's a label or a integer
                binary = str('000101') + str(rs) + str(rt) + str(format(int(line[2]), '016b'))
                binaryInstructions[i * 4] = binary
                #f.write(binary + "\n")
                f.write("0x" + format(int(binary,2), "08x")  + "\n")



            else:
                for j in range(len(labelName)):
                    if (labelName[j] == line[2]):
                        jumpDistance = (-1) * ((i - labelIndex[j])+1) ####
                        if(jumpDistance < 0):
                            binary = str('000101') + str(rs) + str(rt) + str(format(jumpDistance + (2**16), '016b'))
                            binaryInstructions[i * 4] = binary
                            #f.write(binary + "\n")
                            f.write("0x" + format(int(binary,2), "08x") + "\n")

                        else:
                            binary = str('000101') + str(rs) + str(rt) + str(format(jumpDistance, '016b'))
                            binaryInstructions[i * 4] = binary
                            #f.write(binary + "\n")
                            f.write("0x" + format(int(binary,2), "08x")  + "\n")


        elif(line[0:3] == "beq"): # BEQ
            line = line.replace("beq", "")
            line = line.split(",")
            rs = format(int(line[0]),'05b')
            rt = format(int(line[1]),'05b')

            if (line[2].isdigit()):  # First,test to see if it's a label or a integer
                binary = str('000100') + str(rs) + str(rt) + str(format(int(line[2]), '016b'))
                binaryInstructions[i * 4] = binary
                #f.write(binary + "\n")
                f.write("0x" + format(int(binary,2), "08x")  + "\n")



            else:
                for j in range(len(labelName)):
                    if (labelName[j] == line[2]):
                        jumpDistance = -1 * ((i - labelIndex[j]) +1)
                        if(jumpDistance < 0):
                            binary = str('000100') + str(rs) + str(rt) + str(format(jumpDistance + (2**16), '016b'))
                            binaryInstructions[i * 4] = binary
                            #f.write(binary + "\n")
                            f.write("0x" + format(int(binary,2), "08x") + "\n")

                        else:
                            binary = str('000100') + str(rs) + str(rt) + str(format(jumpDistance, '016b'))
                            binaryInstructions[i * 4] = binary
                            #f.write(binary + "\n")
                            f.write("0x" + format(int(binary,2), "08x")  + "\n")





        elif(line[0:1] == "j"): # JUMP
            line = line.replace("j","")
            line = line.split(",")

            # Since jump instruction has 2 options:
            # 1) jump to a label
            # 2) jump to a target (integer)
            # We need to save the label destination and its target location

            if(line[0].isdigit()): # First,test to see if it's a label or a integer
                binary = str('000010') + str(format(int(line[0]),'026b'))
                binaryInstructions[i * 4] = binary
                #f.write(binary + "\n")
                f.write("0x" + format(int(binary,2), "08x")  + "\n")


            else: # Jumping to label
                for j in range(len(labelName)):
                    if(labelName[j] == line[0]):
                        binary = str('000010') + str(format(int(labelIndex[j]),'026b'))
                        binaryInstructions[i * 4] = binary
                        #f.write(binary + "\n")
                        f.write("0x" + format(int(binary,2), "08x")  + "\n")

        i += 1


    #--Closing Files--#
    f.close()
    h.close()



    # We SHALL start the simulation!
    CpuType = input("What kind of MIPS CPU would you like? 'm' for multi-cyle, 'p' for pipelined, 'n' for none\n")
    if(CpuType == "n"):
        pass
    deBug = input("Want to enter debug mode, to step through every step? type y for yes \n")
    sim(binaryInstructions, deBug, CpuType)


if __name__ == "__main__":
    main()
