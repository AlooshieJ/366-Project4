from proj4Header import *
from simFunc import *
from mccpu import *
#-----MAIN-----#
def main():
    validInstructions = []  #list of valid instructions
    labelName= []           #list of label names
    labelIndex= []          #list of label indicies



    #----opening files----#
    f = open("output.txt","w+")
    h = open("A1.asm","r")                 # INPUT FILE NAME WITH ASM CODE HERE
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
            f.write("0x" + format(int(binary,2), "08x") + "\n")



        elif(line[0:4] == "addi"): # ADDI
            line = line.replace("addi","")
            line = line.split(",")
            imm = format(int(line[2]),'016b') if (int(line[2]) >= 0) else format(65536 + int(line[2]),'016b')
            rs = format(int(line[1]),'05b')
            rt = format(int(line[0]),'05b')
            binary = str('001000') + str(rs) + str(rt) + str(imm)
            binaryInstructions[i * 4] = binary
            f.write("0x" + format(int(binary,2), "08x") + "\n")


        elif(line[0:4] == "addu"): # ADDU
            line = line.replace("addu","")
            line = line.split(",")
            rd = format(int(line[0]),'05b')
            rs = format(int(line[1]),'05b')
            rt = format(int(line[2]),'05b')
            binary = str('000000') + str(rs) + str(rt) + str(rd) + str('00000100001')
            binaryInstructions[i * 4] = binary
            f.write("0x" + format(int(binary,2), "08x") + "\n")


        elif(line[0:3] == "add"): # ADD
            line = line.replace("add","")
            line = line.split(",")
            rd = format(int(line[0]),'05b')
            rs = format(int(line[1]),'05b')
            rt = format(int(line[2]),'05b')
            binary = str('000000') + str(rs) + str(rt) + str(rd) + str('00000100000')
            binaryInstructions[i * 4] = binary
            f.write("0x" + format(int(binary,2), "08x") + "\n")

        elif(line[0:3] == "sub"): # SUB
            line = line.replace("sub","")
            line = line.split(",")
            rd = format(int(line[0]),'05b')
            rs = format(int(line[1]),'05b')
            rt = format(int(line[2]),'05b')
            binary = str('000000') + str(rs) + str(rt) + str(rd) + str('00000100010')
            binaryInstructions[i * 4] = binary
            f.write("0x" + format(int(binary,2), "08x") + "\n")

        elif(line[0:4] == "fold"): # FOLD
            line = line.replace("fold","")
            line = line.split(",")
            rd = format(int(line[0]),'05b')
            rs = format(int(line[1]),'05b')
            rt = format(int(line[2]),'05b')
            binary = str('000000') + str(rs) + str(rt) + str(rd) + str('00000011111')
            binaryInstructions[i * 4] = binary
            f.write("0x" + format(int(binary,2), "08x") + "\n")


        elif(line[0:5] == "multu"): # MULTU
            line = line.replace("multu","")
            line = line.split(",")
            rs = format(int(line[0]),'05b')
            rt = format(int(line[1]),'05b')
            binary = str('000000') + str(rs) + str(rt) + str('0000000000011001')
            binaryInstructions[i * 4] = binary
            f.write("0x" + format(int(binary,2), "08x") + "\n")



        elif(line[0:4] == "mult"): # MULT
            line = line.replace("mult","")
            line = line.split(",")
            rs = format(int(line[0]),'05b')
            rt = format(int(line[1]),'05b')
            binary = str('000000') + str(rs) + str(rt) + str('0000000000011000')
            binaryInstructions[i * 4] = binary
            f.write("0x" + format(int(binary,2), "08x") + "\n")



        elif(line[0:4] == "sltu"): # SLTU
            line = line.replace("sltu","")
            line = line.split(",")
            rd = format(int(line[0]),'05b')
            rs = format(int(line[1]),'05b')
            rt = format(int(line[2]),'05b')
            binary = str('000000') + str(rs) + str(rt) + str(rd) + str('00000101011')
            binaryInstructions[i * 4] = binary
            f.write("0x" + format(int(binary,2), "08x")  + "\n")



        elif(line[0:3] == "slt"): # SLT
            line = line.replace("slt","")
            line = line.split(",")
            rd = format(int(line[0]),'05b')
            rs = format(int(line[1]),'05b')
            rt = format(int(line[2]),'05b')
            binary = str('000000') + str(rs) + str(rt) + str(rd) + str('00000101010')
            binaryInstructions[i * 4] = binary
            f.write("0x" + format(int(binary,2), "08x")  + "\n")



        elif(line[0:3] == "srl"): # SRL
            line = line.replace("srl","")
            line = line.split(",")
            imm = format(int(line[2]),'05b') if (int(line[2]) > 0) else format(65536 + int(line[2]),'05b')
            rs = format(int(line[1]),'05b')
            rt = format(int(line[0]),'05b')
            binary = str('00000000000') + str(rs) + str(rt) + str(imm) + str('000010')
            binaryInstructions[i * 4] = binary
            f.write("0x" + format(int(binary,2), "08x")+ "\n")

        elif(line[0:3] == "sll"): # SLL
            line = line.replace("sll","")
            line = line.split(",")
            imm = format(int(line[2]),'05b') if (int(line[2]) > 0) else format(65536 + int(line[2]),'05b')
            rs = format(int(line[1]),'05b')
            rt = format(int(line[0]),'05b')
            binary = str('00000000000') + str(rs) + str(rt) + str(imm) + str('000000')
            binaryInstructions[i * 4] = binary
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
            f.write("0x" + format(int(binary,2), "08x")  + "\n")


        elif(line[0:4] == "mfhi"): # MFHI
            line = line.replace("mfhi", "")
            rd = format(int(line), '05b')
            binary = str("0000000000000000") + str(rd) + str("00000010000")
            binaryInstructions[i * 4] = binary
            f.write("0x" + format(int(binary,2), "08x") + "\n")



        elif(line[0:4] == "mflo"): # MFLO
            line = line.replace("mflo", "")
            rd = format(int(line), '05b')
            binary = str("0000000000000000") + str(rd) + str("00000010010")
            binaryInstructions[i * 4] = binary
            f.write("0x" + format(int(binary,2), "08x") + "\n")


        elif(line[0:3] == "xor"): # XOR
            line = line.replace("xor", "")
            line = line.split(",")
            rd = format(int(line[0]),'05b')
            rs = format(int(line[1]),'05b')
            rt = format(int(line[2]),'05b')
            binary = str("000000") + str(rs) + str(rt) + str(rd) +str("00000100110")
            binaryInstructions[i * 4] = binary
            f.write("0x" + format(int(binary,2), "08x")  + "\n")


        elif(line[0:3] == "lui"): # LUI
            line = line.replace("lui","")
            line = line.split(",")
            rt = format(int(line[0]),'05b')
            imm = format(int(line[1]),'016b') if (int(line[1]) > 0) else format(65536 + int(line[1]),'016b')
            binary = str('001111') + str('00000') + str(rt) + str(imm)
            binaryInstructions[i * 4] = binary
            f.write("0x" + format(int(binary,2), "08x")  + "\n")



        elif(line[0:3] == "ori"): # ORI
            line = line.replace("ori","")
            line = line.split(",")
            imm = format(int(line[2]),'016b') if (int(line[2]) > 0) else format(65536 + int(line[1]),'016b')
            rs = format(int(line[1]),'05b')
            rt = format(int(line[0]),'05b')
            binary = str('001101') + str(rs) + str(rt) + str(imm)
            binaryInstructions[i * 4] = binary
            f.write("0x" + format(int(binary,2), "08x") + "\n")


        elif(line[0:4] == "andi"): # ANDI
            line = line.replace("andi","")
            line = line.split(",")
            imm = format(int(line[2]),'016b') if (int(line[2]) > 0) else format(65536 + int(line[2]),'016b')
            rs = format(int(line[1]),'05b')
            rt = format(int(line[0]),'05b')
            binary = str('001100') + str(rs) + str(rt) + str(imm)
            binaryInstructions[i * 4] = binary
            f.write("0x" + format(int(binary,2), "08x")  + "\n")


        elif(line[0:3] == "bne"): # BNE
            line = line.replace("bne", "")
            line = line.split(",")
            rs = format(int(line[0]),'05b')
            rt = format(int(line[1]),'05b')

            if (line[2].isdigit()):  # First,test to see if it's a label or a integer
                binary = str('000101') + str(rs) + str(rt) + str(format(int(line[2]), '016b'))
                binaryInstructions[i * 4] = binary
                f.write("0x" + format(int(binary,2), "08x")  + "\n")



            else:
                for j in range(len(labelName)):
                    if (labelName[j] == line[2]):
                        jumpDistance = (-1) * ((i - labelIndex[j])+1) ####
                        if(jumpDistance < 0):
                            binary = str('000101') + str(rs) + str(rt) + str(format(jumpDistance + (2**16), '016b'))
                            binaryInstructions[i * 4] = binary
                            f.write("0x" + format(int(binary,2), "08x") + "\n")

                        else:
                            binary = str('000101') + str(rs) + str(rt) + str(format(jumpDistance, '016b'))
                            binaryInstructions[i * 4] = binary
                            f.write("0x" + format(int(binary,2), "08x")  + "\n")


        elif(line[0:3] == "beq"): # BEQ
            line = line.replace("beq", "")
            line = line.split(",")
            rs = format(int(line[0]),'05b')
            rt = format(int(line[1]),'05b')

            if (line[2].isdigit()):  # First,test to see if it's a label or a integer
                binary = str('000100') + str(rs) + str(rt) + str(format(int(line[2]), '016b'))
                binaryInstructions[i * 4] = binary
                f.write("0x" + format(int(binary,2), "08x")  + "\n")



            else:
                for j in range(len(labelName)):
                    if (labelName[j] == line[2]):
                        jumpDistance = -1 * ((i - labelIndex[j]) +1)
                        if(jumpDistance < 0):
                            binary = str('000100') + str(rs) + str(rt) + str(format(jumpDistance + (2**16), '016b'))
                            binaryInstructions[i * 4] = binary
                            f.write("0x" + format(int(binary,2), "08x") + "\n")

                        else:
                            binary = str('000100') + str(rs) + str(rt) + str(format(jumpDistance, '016b'))
                            binaryInstructions[i * 4] = binary
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
                f.write("0x" + format(int(binary,2), "08x")  + "\n")


            else: # Jumping to label
                for j in range(len(labelName)):
                    if(labelName[j] == line[0]):
                        binary = str('000010') + str(format(int(labelIndex[j]),'026b'))
                        binaryInstructions[i * 4] = binary
                        f.write("0x" + format(int(binary,2), "08x")  + "\n")

        i += 1


    #--Closing Files--#
    f.close()
    h.close()



    # We SHALL start the simulation!
    CpuType = input("What kind of MIPS CPU would you like? 'm' for multi-cyle, 'p' for pipelined, or 'n' for none\n")


    if(CpuType == "n"):
        cache_MODE = input(f"Would you like to run $$CacheMoney Sim$$ ? 'y' 'n' ") == 'y'
    else:
        cache_MODE = False

    if cache_MODE == False:
        deBug = input("Want to enter debug mode, to step through every step? Type 'y' for yes, or 'n' for no\n")
    else:
        deBug = 'n'
    sim(binaryInstructions, deBug, CpuType,cache_MODE)


if __name__ == "__main__":
    main()
