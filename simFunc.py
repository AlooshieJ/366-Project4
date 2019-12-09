from proj4Header import *
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
        if(CpuType == "m" ):
            cycleStop = cycle['count'] + cycle['length']
            cycleStart = cycle['count']

            #updateCounters according to cycle length#
            if(cycle['length'] == 3):
                # counter.updateCounters(cycInfo.c1)
                # counter.updateCounters(cycInfo.c2)
                # counter.updateCounters(cycInfo.c3)
                counter.threeCycles += 1
            elif(cycle['length'] == 4):
                # counter.updateCounters(cycInfo.c1)
                # counter.updateCounters(cycInfo.c2)
                # counter.updateCounters(cycInfo.c3)
                # counter.updateCounters(cycInfo.c4)
                counter.fourCycles += 1
            elif(cycle['length'] == 5):
                # counter.updateCounters(cycInfo.c1)
                # counter.updateCounters(cycInfo.c2)
                # counter.updateCounters(cycInfo.c3)
                # counter.updateCounters(cycInfo.c4)
                # counter.updateCounters(cycInfo.c5)
                counter.fiveCycles += 1


            while(cycle['count'] < cycleStop):
                cycle['count'] += 1

                #When Skip destintion is landed  on
                if(userStop == cycle['count']):
                    m_cyclePrint = False
                    userStop == "n"

                #updating Counters#
                if( (cycleStop - cycle.get('count')) == (cycle.get('length') -1 ) ):
                    counter.updateCounters(cycInfo.c1)
                elif((cycleStop - cycle.get('count')) == (cycle.get('length') -2 ) ):
                    counter.updateCounters(cycInfo.c1)
                elif((cycleStop - cycle.get('count')) == (cycle.get('length') -3 ) ):
                    counter.updateCounters(cycInfo.c3)
                elif((cycleStop - cycle.get('count')) == (cycle.get('length') -4 ) ):
                    counter.updateCounters(cycInfo.c4)
                elif((cycleStop - cycle.get('count')) == (cycle.get('length') -5 ) ):
                     counter.updateCounters(cycInfo.c5)


                #MultiCycle-Debug
                if( (m_cyclePrint == True and type(userStop) == int)  or (userStop == "n" and deBug == "y")  or userStop == 1 or userStop == cycle['count'] ):
                    print(f"inst = {cycInfo.instruction},     C.L = {cycle.get('length')},    C.S-C.L = {cycleStop - cycle.get('length')},    C.L-1 = {cycle.get('length') -1 },  DIC = {DIC-1}  ")
                    #print(f"Cycle : {cycle.get('count')}\n")
                    if( (cycleStop - cycle.get('count')) == (cycle.get('length') -1 ) ):
                        print(f"\t\tDIC = {DIC-1}")
                        print(f"\t\tPC = {PC}")
                        print(f"\t\tInstruction's Cycle: {cycInfo.instruction}'s Cycle 1")
                        print(f"\t\tCurrent Cycle = #{cycle.get('count')}")
                        print(f"----Control Signals----")
                        cycInfo.c1.printCycle()
                        #counter.updateCounters(cycInfo.c1)
                        counter.printCounters()
                    elif((cycleStop - cycle.get('count')) == (cycle.get('length') -2 ) ):
                        print(f"\t\tDIC = {DIC-1}")
                        print(f"\t\tPC = {PC}")
                        print(f"\t\tInstruction and Cycle: {cycInfo.instruction}'s Cycle 2")
                        print(f"\t\tCurrent Cycle = #{cycle.get('count')}")
                        print(f"----Control Signals----")
                        cycInfo.c2.printCycle()
                        #counter.updateCounters(cycInfo.c2)
                        counter.printCounters()
                    elif((cycleStop - cycle.get('count')) == (cycle.get('length') -3 ) ):
                        print(f"\t\tDIC = {DIC-1}")
                        print(f"\t\tPC = {PC}")
                        print(f"\t\tInstruction and Cycle: {cycInfo.instruction}'s Cycle 3")
                        print(f"\t\tCurrent Cycle = #{cycle.get('count')}")
                        print(f"----Control Signals----")
                        cycInfo.c3.printCycle()
                        #counter.updateCounters(cycInfo.c3)
                        counter.printCounters()
                    elif((cycleStop - cycle.get('count')) == (cycle.get('length') -4 ) ):
                        print(f"\t\tDIC = {DIC-1}")
                        print(f"\t\tPC = {PC}")
                        print(f"\t\tInstruction and Cycle: {cycInfo.instruction}'s Cycle 4")
                        print(f"\t\tCurrent Cycle = #{cycle.get('count')}")
                        print(f"----Control Signals----")
                        cycInfo.c4.printCycle()
                        #counter.updateCounters(cycInfo.c4)
                        counter.printCounters()
                    elif((cycleStop - cycle.get('count')) == (cycle.get('length') -5 ) ):
                        print(f"\t\tDIC = {DIC-1}")
                        print(f"\t\tPC = {PC}")
                        print(f"\t\tInstruction and Cycle: {cycInfo.instruction}'s Cycle 5")
                        print(f"\t\tCurrent Cycle = #{cycle.get('count')}")
                        print(f"----Control Signals----")
                        cycInfo.c5.printCycle()
                        #counter.updateCounters(cycInfo.c5)
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
    print('')
    if(CpuType == "m" ):
        counter.printCounters()

    m.close()
    outMem.close()

    # for state in states:
    #     state.printState()
    # print(f"length of states: {len(states)}")
