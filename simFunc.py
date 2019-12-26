from proj4Header import *
from mccpu import *
import xlsxwriter
#--------------------------------------------------------------------------------SIM------------------------------------------------------------------------------------------------------------------#
def sim(program, deBug, CpuType,cache_mode = False ):
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
    cache_created = False
    #m = open("memAddr.txt","w+") #outPut File for cash

    # --------------------------------------------------------------------------------------------------- For Cache -----------------------------------------------------------------------------#
    cacheName = ""
    blocks = 0
    bytesize = 0
    numWays = 1 # by default
    numSets = 0

    if cache_mode == True:
        if cache_created == False:
            print("$$$ Cash $$$")
            print(f" Welcome to DataCache sim ! how would you like your $CACHE$?")
            cacheType = input("(1) for Direct Memory (2) Set-Associative (3) Fully Associative ")
            if cacheType == '1':
                cacheName = 'DM'
                blocks = int(input(" How many Blocks? "))
                bytesize = int(input(" How many Bytes per block (size in B)?"))
                # cache = CacheMoney('DM',blocks,bytesize)
            elif cacheType == '2':
                cacheName = 'SA'
                numWays = int(input(" How many Ways?"))
                numSets = int(input(" How many Sets? "))
                bytesize = int(input(" How many Bytes per block (size in B)?"))
                blocks = numSets
            elif cacheType == '3':
                cacheName = 'FA'
                blocks = int(input(" How many Blocks? "))
                bytesize = int(input(" How many Bytes per block (size in B)?"))

            cache_debug = input("would you like to debug? y/n") == 'y'

            cache_CORE =CacheMoney(cacheName, blocks,bytesize,numWays,cache_debug) # type of cache , mem? , sets, bytes
            cache_created = True



    #------------------------For MultiCycle Mode--------------------------#
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



    #----------------------------------------------------------------------------------------------------------SIMULATOR LOOP--------------------------------------------------------------------------------------------------------------------------#
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





        #--------------------------------------------------------Begining to simulate instruction---------------------------------------------------#

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
            #For the pipe
            states[DIC].inst = {"instruction":"Addi", "rd":None, "rs":s,  "rt":t,  "imm":imm,  "type":"I"}




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
            #ForThePipe
            states[DIC].inst = {"instruction":"Addu", "rd":d, "rs":int(fetch[6:11],2),  "rt":int(fetch[11:16],2),  "imm":None,  "type":"R"}

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
            #ForThePipe
            states[DIC].inst = {"instruction":"Add", "rd":d, "rs":s,  "rt":t,  "imm":None,  "type":"R"}

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
            #ForThePipe
            states[DIC].inst = {"instruction":"Sub", "rd":d, "rs":s,  "rt":t,  "imm":None,  "type":"R"}

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
            #ForThePipe
            states[DIC].inst = {"instruction":"Srl", "rd":d, "rs":None,  "rt":int(fetch[11:16],2),  "imm":h,  "type":"R"}

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
            #ForThePipe
            states[DIC].inst = {"instruction":"Sll", "rd":d, "rs":None,  "rt":int(fetch[11:16],2),  "imm":h,  "type":"R"}

        elif fetch[0:6] == '000100':  #<--------------------------------#    # BEQ
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            imm = -(65536 - int(fetch[16:],2)) if fetch[16]=='1' else int(fetch[16:],2)
            #For Multi-Cycle
            cycle.update({"length": 3})
            cycInfo.instruction = "BEQ"
            cycInfo.Type = 'Branch'
            # Compare the registers and decide if jumping or not
            if register[s] == register[t]:
                PC += imm*4
                cycInfo.taken = True
            else:
                cycInfo.taken = False
            #For the pipe
            states[DIC].inst = {"instruction":"Beq", "rd":None, "rs":s,  "rt":t,  "imm":imm,  "type":"I"}


        elif fetch[0:6] == '000101':        #<--------------------------------BNE
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            imm = -(65536 - int(fetch[16:],2)) if fetch[16]=='1' else int(fetch[16:],2)
            #For Multi-Cycle
            cycle.update({"length": 3})
            cycInfo.instruction = "BEQ"
            cycInfo.Type = 'Branch'
            # Compare the registers and decide if jumping or not
            if register[s] != register[t]:
                PC += imm*4
                cycInfo.taken = True
            else:
                cycInfo.taken = False
            #For the pipe
            states[DIC].inst = {"instruction":"Bne", "rd":None, "rs":s,  "rt":t,  "imm":imm,  "type":"I"}


        elif fetch[0:6] == '001101':      #<--------------------------------# ORI
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            imm = int(fetch[16:],2)
            register[t] = register[s] | imm
            #for multi-cycle#
            cycle.update({'length':4})
            cycInfo.Type = "I"
            cycInfo.instruction = "ORI"
            #For the pipe
            states[DIC].inst = {"instruction":"Ori", "rd":None, "rs":s,  "rt":t,  "imm":imm,  "type":"I"}


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
            #For the pipe
            states[DIC].inst = {"instruction":"Andi", "rd":None, "rs":s,  "rt":t,  "imm":imm,  "type":"I"}

        elif fetch[0:6] == '101011':    #<--------------------------------# SW
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            offset = -(65536 - int(fetch[16:],2)) if fetch[16]=='1' else int(fetch[16:],2)
            offset = offset + register[s]-0x2000
            #Writing to Cache File
            #m.write(f"SW @ dic:, {DIC - 1}, {format((offset + 0x2000), '08x')}  \n")
            #Storing a word to memory
            if (offset % 4) == 0:
                mem[offset+3] = (register[t] >> 24) & 0x000000ff  # +3
                mem[offset+2] = (register[t] >> 16) & 0x000000ff # +2
                mem[offset+1] = (register[t] >> 8) & 0x000000ff # +1
                mem[offset+0] = register[t] & 0x000000ff  # +0
            #For Cache
            # updatedMem = mem[:]
            #For Multi-Cycle
            cycle.update({"length": 4})
            cycInfo.instruction = "SW"
            cycInfo.Type = 'SW'
            #For the pipe
            states[DIC].inst = {"instruction":"Sw", "rd":None, "rs":s,  "rt":t,  "imm":'0x'+format(offset-register[s]+0x2000, "04x"),  "type":"I"}

        elif fetch[0:6] == '100011': #<--------------------------------# LW
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            offset = -(65536 - int(fetch[16:],2)) if fetch[16]=='1' else int(fetch[16:],2)
            offset = offset + register[s]-0x2000
            #Writing to Cache File
            #m.write(f"LW @ dic:, {DIC - 1}, {format((offset + 0x2000), '08x')}  \n")
            #Loading a word from memory
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
            #For the pipe
            states[DIC].inst = {"instruction":"Lw", "rd":None, "rs":s,  "rt":t,  "imm":'0x'+format(offset- register[s] +0x2000, "04x"),  "type":"I"}

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
            #ForThePipe
            states[DIC].inst = {"instruction":"Slt", "rd":d, "rs":s,  "rt":t,  "imm":None,  "type":"R"}

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
            #For the pipe
            states[DIC].inst = {"instruction":"Lui", "rd":None, "rs":s,  "rt":t,  "imm":imm,  "type":"I"}

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
            #ForThePipe
            states[DIC].inst = {"instruction":"Xor", "rd":d, "rs":s,  "rt":t,  "imm":None,  "type":"R"}

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



        DIC += 1

        #------------------------------------------------------------------------------------------------Simulation Part Done-----------------------------------------------------------------------------------------------------------------------------------#



        #---------------------------------------------------------------------- Cases sim logic ----------------------------------------------------------------------------------------#

        if cache_mode == True:

            if fetch[0:6] == '100011':
                cache_CORE.write_cache(offset + 0x2000,mem)

            elif fetch[0:6] == '101011' : # opcode for lw
                cache_CORE.write_cache(offset + 0x2000,mem)
                #printMemory(mem)
            #elif :
               # cache_CORE.write_cache(offset + 0x2000,mem)
            else:
                print("Instruction does not acces Memory")




        #---------------------------------------------------------------------------------------------------------Multi-Cycle------------------------------------------------------------------------------------------------------------------------------------#
        cycInfo.cycleUpdate()  #Update cycles based on instruction
        if(CpuType == "m" ):
            cycleStop = cycle['count'] + cycle['length']
            cycleStart = cycle['count']

            #updateCounters according to cycle length#
            if(cycle['length'] == 3):
                counter.threeCycles += 1
            elif(cycle['length'] == 4):
                counter.fourCycles += 1
            elif(cycle['length'] == 5):
                counter.fiveCycles += 1

            #Loop that does cycle by cycle
            while(cycle['count'] < cycleStop):
                cycle['count'] += 1

                #When Skip destintion is landed  on
                if(userStop == cycle['count']):
                    m_cyclePrint = False
                    userStop == "n"

                #Updating Counters#
                if( (cycleStop - cycle.get('count')) == (cycle.get('length') -1 ) ):
                    counter.updateCounters(cycInfo.c1)
                elif((cycleStop - cycle.get('count')) == (cycle.get('length') -2 ) ):
                    counter.updateCounters(cycInfo.c2)
                elif((cycleStop - cycle.get('count')) == (cycle.get('length') -3 ) ):
                    counter.updateCounters(cycInfo.c3)
                elif((cycleStop - cycle.get('count')) == (cycle.get('length') -4 ) ):
                    counter.updateCounters(cycInfo.c4)
                elif((cycleStop - cycle.get('count')) == (cycle.get('length') -5 ) ):
                     counter.updateCounters(cycInfo.c5)


                #MultiCycle-Debug
                if( (m_cyclePrint == True and type(userStop) == int)  or (userStop == "n" and deBug == "y")  or userStop == 1 or userStop == cycle['count'] ):
                    #print(f"inst = {cycInfo.instruction},     C.L = {cycle.get('length')},    C.S-C.L = {cycleStop - cycle.get('length')},    C.L-1 = {cycle.get('length') -1 },  DIC = {DIC-1}  ")
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
                    #print('')

                #UserInput
                if( (  (deBug == "y")  and (userStop != "n")  and (m_cyclePrint == False) and (userStop == cycle['count'])  ) or nextCycle == True):
                    userStop = input("Want to skip to a certain cycle? Type 'n' for NO, or type the cycle number you wish to skip to\n")
                    if(userStop != "n"):
                        userStop = int(userStop)
                        multiSkip = input("Want to print along the way? Type 'y' for yes, or 'n' for no\n")
                        nextCycle = False
                        if(multiSkip == "y"):
                            m_cyclePrint = True
                        else:
                            m_cyclePrint = False



                if(userStop == "n" and deBug == "y"):
                    deBug = input("Next Cycle? Type 'y' for yes, or 'n' for no\n")
                    if(deBug == "y"):
                        nextCycle = True
                    else:
                        nextCycle = False


        #----------------------------------------------------------------------------------------------------For Regular Debug Mode---------------------------------------------------------------------------------------------------------------------------#
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

                userInput = input("Want to skip to a certain DIC? Type 'n' for NO, or type the DIC number you wish to skip to\n")
                if(userInput == "n"):
                    userInput = input("Next Step? Type 'y' for yes, or 'n' for no \n")
                    if(userInput == "y"):
                        deBug = "y"
                    else:
                        deBug = "n"
                else:
                    skip = True
                    skipCount = int(userInput)
                    printDicInput = input("Want to print along the way? Type 'y' for yes, or 'n' for no\n")

        if(DIC == skipCount - 1):
            skip = False
    print("")



    currentState = State(mem, register, format(int(fetch,2), '08x'),DIC)
    states.append(currentState)


#--------------------------------------------------------------------------------------------------GIRL YOU GON GET THIS PIPE-------------------------------------------------------------------------------------------------------------------------------#

    if(CpuType == 'p'):         #Checking if in Pipeline mode
        row = []
        stalls = 0
        totalCycles = DIC + 4 + stalls
        for i in range(DIC):
            row.append(Row(0,["-"] * totalCycles))


        i = 0 #iterator for whie loop        #------------------IDEAL PIPELINE
        while( i < len(row)):
            row[i].column[i+0] = 'F'
            row[i].column[i+1] = 'D'
            row[i].column[i+2] = 'E'
            row[i].column[i+3] = 'M'
            row[i].column[i+4] = 'W'
            row[i].instNum = i
            i += 1


        # for rows in row:              #Row List printout
        #     print("")
        #     for columns in rows.column:
        #             print(columns, end = " ")

        #---------------------------------------------------------Excel file creation----------------------------------------#
        pipeOutput = xlsxwriter.Workbook("pipeOutput.xlsx")
        outSheet =  pipeOutput.add_worksheet()


        for state in states:    #---------------------------ADDING HAZADS AND STALLS                #LW use,  Computation before branch, branch taken, LW-Branch:2 Stalls
            if(state.stateNum == len(states)-1):        #breaks if last state- Last state is after last instruction is executed, no attached dictionary for state
                break
            print(f"type:{state.inst['type']},   instruction: {state.inst['instruction']},   rd: {state.inst['rd']},   rs: {state.inst['rs']},   rt: {state.inst['rt']},   stateNum: {state.stateNum}")


            if(state.inst['type'] == 'R'):      #-----checks if instruction i is an R-type
                if(state.stateNum < len(states)-2):       #i+1 instruction, making sure not on last instruction
                    if(state.inst['rd'] == states[state.stateNum + 1].inst['rs'] ): #checking for i+1 RS-Hazard
                        if(states[state.stateNum + 1].inst['type'] == 'I'): #checking if i+1 is an I type
                            #if I type, check if rs is used or updated
                            if(states[state.stateNum + 1].inst['instruction'] == 'Beq' or states[state.stateNum + 1].inst['instruction'] == 'Bne' or states[state.stateNum + 1].inst['instruction'] == 'Lw' or states[state.stateNum + 1].inst['instruction'] == 'Sw'):
                                print("RS-HAZARD,   i+1 : I  and doesn't update rs")
                        else:#i+1 is a R type
                            print('RS-HAZARD i+1 : R')
                    if(state.inst['rd'] == states[state.stateNum + 1].inst['rt'] ): #checking for i+1 RT-Hazard
                        print(f"RT-HAZARD,   i+1:{states[state.stateNum + 1].inst['type']}")


                if(state.stateNum < len(states)-3): #i+2 instruction  , making sure not on second to last instruction       #####################i=R, i+2
                    if(state.inst['rd'] == states[state.stateNum + 2].inst['rs'] ): #checking for i+2 RS-Hazard
                        if(states[state.stateNum + 2].inst['type'] == 'I'): #checking if i+2 is an I type
                            #if I type, check if rs is used or updated
                            if(states[state.stateNum + 2].inst['instruction'] == 'Beq' or states[state.stateNum + 2].inst['instruction'] == 'Bne' or states[state.stateNum + 2].inst['instruction'] == 'Lw' or states[state.stateNum + 2].inst['instruction'] == 'Sw'):
                                print("RS-HAZARD,   i+2 : I  and doesn't update rs")
                        else:#i+2 is a R type
                            print('RS-HAZARD i+2 : R')
                    if(state.inst['rd'] == states[state.stateNum + 2].inst['rt'] ): #checking for i+2 RT-Hazard
                        print(f"RT-HAZARD,   i+2:{states[state.stateNum + 2].inst['type']}")



        #------------checks if instruction i is an I-type--------------#
            elif(state.inst['type'] == 'I'):
                pass
                #print(f"rt:{state.inst['rt']},  rs: {state.inst['rs']}")  #,  imm: {state.inst['imm']}
                #if():
           # print('-------------------------------------------------------------------------------------------')
            #input()
        # totalCycles += stalls
        # for rows in row:
        #     rows.addColumn(stalls)


        #-#-#-#-----------------------Writing to Excel File--------------------#-#-#-#
        outSheet.write(0,0, "     Cycles:")
        for i in range(totalCycles):
            outSheet.write(0, i+1, i+1)


        for x, rows in enumerate(row):  #-----------------DATA INPUT
            print("")
            for y, columns in enumerate(rows.column):
                #print(f"(x{x+1}, y{y+1})")
                outSheet.write(x+1, y+1, columns)       #inserting cycle data into excel sheet


        for rows in row:   #---------------Adding instruction printout before Fetch
            #j = 0       #iterator
            columnIndex = rows.column.index('F')        #returns index where instruction begins to be fetched
            outString = "N.A.A.T.M"                     #out going string to excel sheet
            #print(type(states[rows.instNum].inst))

            if(type(states[rows.instNum].inst) == dict):        #cheking if variable is a dict in order to print out instruction
                outString = ""
                print("")
                for key, value in states[rows.instNum].inst.items():        #adding keys and values to string
                    outString += f"{key} : {value},   "

                print(f"going into sheet: {outString[:-4]},  cycle:{columnIndex + 1}")
                outSheet.write(rows.instNum + 1, columnIndex, outString[:-4])           #Writing to excel, removed unnecessary characters at the end

            else:
                print(outString)
                outSheet.write(rows.instNum + 1, columnIndex, outString)         #Writing to excel



        pipeOutput.close()     #----------------------------Closing Excel File


#--------------------------------------------------------------------------------------------------------Final Print Out Stats----------------------------------------------------------------------------------------------------------------------------------#
    print('\n***Simulation finished***')
    print("PC: {}, HI: {}, LO:{}".format(PC, HI, LO))
    print('Dynamic Instr Count: ', DIC)
    print('Registers: $8 - $23')
    printRegisters(register)
    print('\nMemory contents 0x2000 - 0x2100 ')
    printMemory(mem)
    print('')



    if(CpuType == "m" ):      #-----------Multi Cycle Printout
        counter.printCounters()


    if cache_mode == True:       #-----------Cache Sim Printout
        cache_CORE.output()


    for state in states:
        print(f"state:{state.stateNum} ,    inst:{state.inst}")
        state.printState
    printMemory(states[210].mem)



    #print(len(states))
