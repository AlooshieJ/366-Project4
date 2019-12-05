from math import *
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

def printList(list):
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




#-----SIM-----#
def sim(program, deBug):
    finished = False      # Is the simulation finished? 
    PC = 0                # Program Counter
    HI = 0                
    LO = 0
    register = [0] * 32   # Let's initialize 32 empty registers
    mem = [0] * 0x1000     # Let's initialize 0x3000 or 12288 spaces in memory. I know this is inefficient...
    DIC = 0               # Dynamic Instr Count
    skip = False
    skipCount = 0
    printDicInput = "n"

    while(not(finished)):
        if PC == len(program) :
            finished = True
            break
        fetch = program[PC]

        DIC += 1
        register[0] = 0 # keep $0 = 0

        if fetch[0:6] == '001000': # ADDI
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            imm = -(65536 - int(fetch[16:],2)) if fetch[16]=='1' else int(fetch[16:],2)
            register[t] = register[s] + imm



        elif fetch[0:6] == '000000' and fetch[21:32] == '00000100001': # ADDU
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

        elif fetch[0:6] == '000000' and fetch[21:32] == '00000100000': # ADD
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            d = int(fetch[16:21],2)
            register[d] = register[s] + register[t]

        elif fetch[0:6] == '000000' and fetch[21:32] == '00000100010': # SUB
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            d = int(fetch[16:21],2)
            register[d] = register[s] - register[t]


        elif fetch[0:6] == '000000' and fetch[26:32] == '000010': # SRL
            PC += 4
            t = int(fetch[11:16],2)
            d = int(fetch[16:21],2)
            h = int(fetch[21:26],2)
            register[d] = register[t] >> h

        elif fetch[0:6] == '000000' and fetch[26:32] == '000000': # SLL
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
            
        elif fetch[0:6] == '000100':  # BEQ
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            imm = -(65536 - int(fetch[16:],2)) if fetch[16]=='1' else int(fetch[16:],2)
            # Compare the registers and decide if jumping or not
            if register[s] == register[t]:
                PC += imm*4

        elif fetch[0:6] == '000101':  # BNE
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            imm = -(65536 - int(fetch[16:],2)) if fetch[16]=='1' else int(fetch[16:],2)
            # Compare the registers and decide if jumping or not
            if register[s] != register[t]:
                PC += imm*4
        
        elif fetch[0:6] == '001101':   # ORI
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            imm = int(fetch[16:],2)
            register[t] = register[s] | imm

        elif fetch[0:6] == '001100':   # ANDI
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            imm = int(fetch[16:],2)
            register[t] = register[s] & imm            

        elif fetch[0:6] == '101011':  # SW
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            offset = -(65536 - int(fetch[16:],2)) if fetch[16]=='1' else int(fetch[16:],2)
            offset = offset + register[s]-0x2000
            if (offset % 4) == 0:
                mem[offset+3] = (register[t] >> 24) & 0x000000ff  # +3
                mem[offset+2] = (register[t] >> 16) & 0x000000ff # +2
                mem[offset+1] = (register[t] >> 8) & 0x000000ff # +1
                mem[offset+0] = register[t] & 0x000000ff  # +0

        elif fetch[0:6] == '101000':  # SB
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            offset = -(65536 - int(fetch[16:],2)) if fetch[16]=='1' else int(fetch[16:],2)
            offset = offset + register[s]-0x2000
            mem[offset] = register[t]

        elif fetch[0:6] == '100000':  # LB
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            offset = -(65536 - int(fetch[16:],2)) if fetch[16]=='1' else int(fetch[16:],2)
            offset = offset + register[s]-0x2000
            register[t] = mem[offset]         

        elif fetch[0:6] == '100011':  # LW
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            offset = -(65536 - int(fetch[16:],2)) if fetch[16]=='1' else int(fetch[16:],2)
            offset = offset + register[s]-0x2000
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

        elif fetch[0:6] == '000000' and fetch[21:32] == '00000101010': # SLT
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            d = int(fetch[16:21],2)
            if (register[s] < register[t]): 
                register[d] = 1
            else:
                register[d] = 0

        elif fetch[0:6] == '001111': # LUI
            PC += 4
            t = int(fetch[11:16],2)
            imm = int(fetch[16:],2)
            imm = imm << 16
            register[t] = imm

        elif fetch[0:6] == '000000' and fetch[21:32] == '00000011001': # MULTU
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            result = register[s] * register[t]
            result = format(result,'064b')    
            HI = int(result[0:32],2)
            LO = int(result[32:64],2)

        elif fetch[0:6] == '000000' and fetch[21:32] == '00000011111': # FOLD 5 TIMES
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            d = int(fetch[16:21],2)
            result = register[s]
            for i in range(0,5):
                result = result * register[t]
                result = format(result,'064b')    
                high32 = int(result[0:32],2)
                low32 = int(result[32:64],2)
                result = high32 ^ low32
            result = format(result,'032b')   
            high16 = int(result[0:16],2)
            low16 = int(result[16:32],2)
            result = high16 ^ low16
            result = format(result,'016b')   
            high8 = int(result[0:8],2)
            low8 = int(result[8:16],2)
            result = high8 ^ low8
            register[d] = result

        elif fetch[0:6] == '000000' and fetch[21:32] == '00000100110': # XOR
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            d = int(fetch[16:21],2)
            register[d] = register[s] ^ register[t]
            #print(register[d])

        elif fetch[0:6] == '000000' and fetch[21:32] == '00000010000': # MFHI
            PC += 4
            d = int(fetch[16:21],2)
            register[d] = HI

        elif fetch[0:6] == '000000' and fetch[21:32] == '00000010010': # MFLO
            PC += 4
            d = int(fetch[16:21],2)
            register[d] =  LO            

        else:
            # This is not implemented on purpose
            PC += 4
            print('Not implemented')

        bit32Mem = []*0x400
        for i in range (0,0x400,4):
            bits32 = hex((mem[i+3]<<24) + (mem[i+2]<<16) + (mem[i+1]<<8) + (mem[i]))
            bit32Mem.append(("%08X" % int(bits32, 16)))

        if(printDicInput == "y" and (skip == True)):
            print("-----------------------")
            print("PC: {}, HI: {}, LO:{}".format(PC, HI, LO))
            print('Dynamic Instr Count: ', DIC)
            print('Registers: $8 - $23')
            printList(register)
            print("\nAddress Value(+0)\tValue(+4)\tValue(+8)\tValue(+c)\tValue(+10)\tValue(+14)\tValue(+18)\tValue(1c)", end = "")
            for z in range(0,9):   # j is a row of 0x20 addresses in Mars (can be from 0 to 32 - but need at least 9 to show all addresses for project1)
                print(hex(z*32+0x2000), end = "\t")
                for y in range(0,8):        # i is the column in MARS such that: address + value(i*4)
                    print ("0x" +bit32Mem[z*8+y], end="\t")
                print("\n", end = "")
            print('')

        if(skip == False):
            printDicInput = "n"
            if(deBug == "y"):
                print("-----------------------")
                print("PC: {}, HI: {}, LO:{}".format(PC, HI, LO))
                print('Dynamic Instr Count: ', DIC)
                print('Registers: $8 - $23')
                printList(register)
                print('\nMemory contents 0x2000 - 0x2100 ', mem[0:256], end = "")
                for z in range(0,9):   # j is a row of 0x20 addresses in Mars (can be from 0 to 32 - but need at least 9 to show all addresses for project1)
                    print(hex(z*32+0x2000), end = "\t")
                    for y in range(0,8):        # i is the column in MARS such that: address + value(i*4)
                        print ("0x" +bit32Mem[z*8+y], end="\t")
                    print("\n", end = "")
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



    DIC = DIC +1

    # Finished simulations. Let's print out some stats
    print('***Simulation finished***')
    print("PC: {}, HI: {}, LO:{}".format(PC, HI, LO))
    print('Dynamic Instr Count: ', DIC)
    print('Registers: $8 - $23')
    printList(register)
    print('\nMemory contents 0x2000 - 0x2100 ', mem[0:256], end = "")
    print("")


    outMem = open('outputMemory.txt', "w+")

    print("Address Value(+0)\tValue(+4)\tValue(+8)\tValue(+c)\tValue(+10)\tValue(+14)\tValue(+18)\tValue(1c)\n", end = "")
    outMem.write("Address Value(+0)\tValue(+4)\tValue(+8)\tValue(+c)\tValue(+10)\tValue(+14)\tValue(+18)\tValue(1c)\n")
    for j in range(0,9):   # j is a row of 0x20 addresses in Mars (can be from 0 to 32 - but need at least 9 to show all addresses for project1)
        print(hex(j*32+0x2000), end = "\t")
        outMem.write(hex(j*32+0x2000)+"\t")
        for i in range(0,8):        # i is the column in MARS such that: address + value(i*4)
            print ("0x" +bit32Mem[j*8+i], end="\t")
            outMem.write(("0x" +bit32Mem[j*8+i]))
            outMem.write("\t")
        outMem.write("\n")
        print("\n", end = "")
        
    outMem.close()

        # print(hex(mem[i+3]<<24) + hex(mem[i+2]<<16) + hex(mem[i+1]<<8) + hex(mem[i]) )


#-----MAIN-----#
def main():
    validInstructions = []  #list of valid instructions
    labelName= []           #list of label names
    labelIndex= []          #list of label indicies



    #----opening files----#
    f = open("output.txt","w+")
    h = open("TestCase24.asm","r")                 # INPUT FILE NAME WITH ASM CODE HERE
    #h = open("Hash-MIPS-plus.asm","r")
    #h = open("TestCase.asm","r")
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
            imm = format(int(line[1]),'016b') if (int(line[1]) > 0) else format(65536 + int(line[1]),'016b')
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
            imm = format(int(line[1]),'016b') if (int(line[1]) > 0) else format(65536 + int(line[1]),'016b')
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
    deBug = input("Want to enter debug mode, to step through every step? type y for yes \n")
    sim(binaryInstructions, deBug)


if __name__ == "__main__":
    main()
