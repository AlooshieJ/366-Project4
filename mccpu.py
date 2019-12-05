from math import *


def bin_digits(n, bits):
    s = bin(n & int("1"*bits, 2))[2:]
    return ("{0:0>%s}" % bits).format(s)

def minBits(dec):
    if(dec == 0):
        numBits = 1
    elif(dec < 0):
        return "This is unsigned, no negative numbers"
    else:
        numBits = int(log(abs(dec), 2) + 1 )
    return numBits

class mem:
    def __init__(self, address, b3, b2, b1, b0):

        self.addr = address
        self.b0 = b0  # addr + 0
        self.b1 = b1  # addr + 1
        self.b2 = b2  # addr + 2
        self.b3 = b3  # addr + 3
        self.data = str(self.b3) + str(self.b2) + str(self.b1) + str(self.b0)

    def print_mem(self):  # b3 = msb , b0 = lsb
        print(" ", hex(self.addr), end=":  ")
        print("{0:02x}".format(self.b3), end="")
        print("{0:02x}".format(self.b2), end="")
        print("{0:02x}".format(self.b1), end="")
        print("{0:02x}".format(self.b0), end="")

        # print(hex(self.addr) + str(" ") + b3 + b2+ b1+ b0 + str(" | ")) #, end=" ")
#
# # def fetch( instruction , register ,memory ):
# #     # check insturction
# #     # update dictionary
# #     # print dictionary...
# #
# # def decode(instruciton):
# #     # prnit dictionary
#
#
# dict = {
#     # key     : [0] [1] [2]
#     "control1": 0
#
# }
# dict['control1'] = 'x'
# for x in dict:
#     print(dict[x])
# #-------------------- sim loop , so we have all info on instruction
# # x = # cycles for that intruction
# # for i in range( x):
# #     fetch( instruction)
# #     ddecode
# #
#



class fifo:
    def __init__(self, size):

        self.index = []
        self.size = size

        #for i in range(size): # creating w/ all size = 0
         #   self.index.append(i)



    def push(self,value):

        self.index.append(value)
        #if len(self.index) > self.size:
           # self.pop()

    def top (self): # my pop return  what it pops out
        return self.index[0]
        #
        # if len(self.index) > 0:
        #     tmp = self.index[0]
        #     self.index = self.index[1:]
        #     self.index.append(tmp)
        #     #self.index = self.index[1:]
        #     return tmp
        #
        # else:
        #
        #     print("fifo is empty")

   # def leastUsedSwap(self):
    def print(self):
        print(f"fetch: {self.top() }")







# note, doesnt not work with negatives
    def writeWordMem(self, value):

        tmp = str(format(int(value), '08x'))

        # 0|0|0|0|0|0|0|0
        # 0,1,2,3,4,5,6,7
        # -8,7,6,5,4,3,2,1
        # print(tmp)
        # print("infunc: ",tmp[-2:], tmp[-4:-2], tmp[-6:-4],tmp[-8:-6] )
        self.b0 = int(tmp[-2:],   16)
        self.b1 = int(tmp[-4:-2], 16)
        self.b2 = int(tmp[-6:-4], 16)
        self.b3 = int(tmp[-8:-6], 16)
        self.data = str(self.b3) + str(self.b2) + str(self.b1) + str(self.b0)




class Block:
    def __init__(self, size):

        self.valid = 0 # would have to check somehow
        self.tag = 0x0 # math to addr
        self. size = size
        self.usedCount = 0

        self.data  = []

        for i in range(size):
            self.data.append('$') # read from mem each index is a byte


   # def write_to_block(self,Memory):

    def write_to_blk(self, start, end):

        for i in range( self.size):

           self.data[i] =  Memory[ int(start,2) - 0x2000 + i]

    def read_byte(self,offset):

        return self.data[int(offset,2)]





        #print(f"{start} {end} ")



class CacheMoney:

    def __init__(self, option, addr,total_blocks,bytes):

        self.blk_size = bytes # input
        self.blk_offset = 0
        # self.blks = []
        self.totalblks = total_blocks
        self.memspace = 0 # ???
        self.type = option
        self.setNum = 0
        self.set = []
        self.way = []
        self.Hit = 0
        self.Miss = 0
        self.Count = 0
        self.leastUsed = fifo(total_blocks) # list size of total blocks, should incorporate a ways check too


        if self.type == 'DM':
            print(f"Creating Direct Map Cash | total blocks: {self.totalblks}  block size: {self.blk_size}")

            self.blk_offset = minBits(self.blk_size -1)
            self.setNum =     minBits(self.totalblks -1)
            self.tagsize = 32 - (self.setNum + self.blk_offset)
            print(f"tag size: {self.tagsize} set size: {self.setNum} in blk off: {self.blk_offset}")

            for i in range(self.totalblks): # creating 4 blocks
                self.set.append(Block(self.blk_size ))


        # if type == 'SA':

    def printCache (self):
        if self.type == 'DM':

            for i in range(self.totalblks): # these are sets..

                print(f"set: {bin_digits(i,self.setNum)} {cache.set[i].data}", end=" ")
                print(f"tag : {cache.set[i].tag} Valid: {cache.set[i].valid} ")
        print()

            # print("printing set:")
            # for i in self.set:
            #     print( i)
# addr[-self.blk_offset:]
    def write_cache(self,addr, Memory =None): # keeping track of blk addressing

        if self.type == 'DM':
            self.Count += 1
            #addr = addr + 0x2000
            addr =  bin_digits(addr,32)
            tag = addr[:self.tagsize]

            tag = hex(int(tag,2))

            set = addr[-self.setNum - self.blk_offset: -self.blk_offset]
            off = addr[-self.blk_offset:]
            strtBlk = addr[:self.tagsize + self.setNum] # memory range
            endBlk =  strtBlk[:]
            self.leastUsed = int(set,2)
            for i in range(self.blk_offset):
                strtBlk += '0'
                endBlk += '1'
            print(f"({self.Count}) addr: {hex(int(addr,2))} \ntag: {tag} set: {set} off: {off} ")
            # need a range for addr

            if self.set[int(set,2)].valid == 0: # cold miss
                self.Miss +=1


                print(f"cold miss with addr : {hex(int(addr,2))} \nin blk info for set {set}:   tag : {self.set[int(set,2)].tag}  Valid : {self.set[int(set,2)].valid}")
                self.set[int(set, 2)].tag = tag
                self.set[int(set, 2)].valid = 1
                print(f"loading blk fom Mem  [0x{format(int(strtBlk,2),'04x')}] - M[0x{format(int(endBlk,2),'04x')}] into set {set}  ")
                self.set[int(set,2)].write_to_blk(strtBlk,endBlk)
            else: # valid bit, check tag
                if self.set[int(set,2)].tag == tag: # valid tag , hit load write blk
                    self.Hit += 1
                    print(f"Hit with addr: {hex(int(addr,2))}\nin blk info for set {set}: tag : {self.set[int(set,2)].tag} Valid : {self.set[int(set,2)].valid}")
                    print(f"No update to cache, loading from blk ")

                    ##ADD CACHE ACCESS


                else: # not the same tag , overwite set
                    self.Miss += 1
                    print(f"Miss with addr {hex(int(addr,2))}\n in blk info for set {set}: tag: {self.set[int(set,2)].tag} Valid: {self.set[int(set,2)].valid}")
                    print(f"access tag: {tag} updating blk with Memory FIX THIS!!!!")

                    # add swap with memory

                    self.set[int(set, 2)].tag = tag

            print(f"updated blk | set: {i}  tag  : {self.set[i].tag} valid: {self.set[i].valid}")
            print("")

    def outputDM(self):

        print(f"Hits: {self.Hit} Miss: {self.Miss} | total memory Accesses: {self.Count} Last used set: {self.leastUsed}")


# a. a directly-mapped cache, block size of 16 Bytes, a total of 4 blocks (b=16; N=1; S=4)
# b. a fully-associated cache, block size of 8 Bytes, a total of 8 blocks (b=8; N=8; S=1)
# c. a 2-way set-associative cache, block size of 8 Bytes, 4 sets (b=8; N=2; S=4)
# d. a 4-way set-associative cache, block size of 8 Bytes, 2 sets (b=8; N=4; S=2)

def printMemory(memory):
    memory = memory[:]
    k = 0
    a = 0
    # memory[0] = format(memory[0], '08b')
    # memory[1] = format(memory[1], '08b')
    # memory[2] = format(memory[2], '08b')
    # memory[3] = format(memory[3], '08b')
    print("\nAddress\t\tValue(+0)\tValue(+4)\tValue(+8)\tValue(+c)\tValue(+10)\tValue(+14)\tValue(+18)\tValue(+1c)", end = "")
    for i in range(0,len(Memory)): # 9
        print("")
        address = '0x' + format(a , '08x')
        print(f"{address}\t", end = "")
        a += 32
        for j in range(0,8):
            memory[k+0] = format(memory[k+0], '08b')
            memory[k+1] = format(memory[k+1], '08b')
            memory[k+2] = format(memory[k+2], '08b')
            memory[k+3] = format(memory[k+3], '08b')
            byte0 = format(int(str(memory[k + 0]), 2), "02x")
            byte1 = format(int(str(memory[k + 1]), 2), "02x")
            byte2 = format(int(str(memory[k + 2]), 2), "02x")
            byte3 = format(int(str(memory[k + 3]), 2), "02x")
            print(f"0x{byte3.upper()}{byte2.upper()}{byte1.upper()}{byte0.upper()}", end = "\t")
            k = k + 4
        if(k > len(Memory)):
                break

Memory = [ ] # each index is a byte
print("$$$ Cash $$$")
for i in range (1024):
    Memory.append(i)

f = open('memAddr.txt',"r")
addrs = []
m = []
for x in f.readlines():
    addrs.append(x)

for line in addrs:
    line = line.split(',')
    m.append(line[2][1:-3])
print(m)
cache = CacheMoney('DM',0x2000, 4, 16) # type of cache , mem? , sets, bytes
cache.printCache()

for mems in m:
    cache.write_cache(int(mems,16))
cache.printCache()
cache.outputDM()

#printMemory(Memory)
print(Memory)
#print(cache.set[3].read_byte('01'))
# pq = fifo(4)
#
# print(pq.index)
# pq.push(1)
# print(pq.index)
#
# pq.push(2)
# print(pq.index)
#
# pq.push(3)
# print(pq.index)
#
# pq.push(4)
# print(pq.index)
# print( pq.top())
# print(pq.index)
#
# pq.push(3)
# print(pq.index)
#
# pq.pop()
#
# print(pq.index)
