from math import *
import collections

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

        self.index = collections.OrderedDict()
        self.capacity = size

        #for i in range(size): # creating w/ all size = 0
         #   self.index.append(i)

    def get(self,key):
        if key in self.index:
            value = self.index[key]
            # store value , for removing
            del self.index[key]
            #now add it back, already sorting due to structure
            self.index[key] = value
            return value
        else:
            return -1

    def set(self,key , value): # set the value of dictionary, given a key
        if key in self.index:
            del self.index[key]
        elif len(self.index) >= self.capacity:
            self.index.popitem(last= False)
        self.index[key] = value

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
    #data = []
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

    def __init__(self, option,total_blocks,bytes):

        self.blk_size = bytes # input
        self.totalblks = total_blocks
        self.blk_offset = 0
        # self.blks = []

        self.memspace = 0 # ???
        self.type = option
        self.setNum = 0
        self.set = []
        self.way = []
        self.Hit = 0
        self.Miss = 0
        self.Count = 0
        self.lru = fifo(total_blocks) # list size of total blocks, should incorporate a ways check too


        if self.type == 'DM':
            print(f"Creating Direct Map Cash | total blocks: {self.totalblks}  block size: {self.blk_size} B")

            self.blk_offset = minBits(self.blk_size -1)
            self.setNum =     minBits(self.totalblks -1)
            self.tagsize = 32 - (self.setNum + self.blk_offset)
            print(f"tag size: {self.tagsize} set size: {self.setNum} in blk off: {self.blk_offset}")

            for i in range(self.totalblks): # creating 4 blocks
                self.set.append(Block(self.blk_size ))

        # b. a fully-associated cache, block size of 8 Bytes, a total of 8 blocks (b=8; N=8; S=1)

        elif self.type == "FA":
            print(f"Creating Fully Associative Cash| total blocks: {self.totalblks} block size: {self.blk_size}")

            self.blk_offset = minBits(self.blk_size - 1)
            self.ways = self.totalblks
            self.tagsize = 32 - self.blk_offset
            print(f"tag size: {self.tagsize} total ways: {self.ways} in blk off: {self.blk_offset}")

            for i in range(self.totalblks):
                self.way.append(Block(self.blk_size))


    def printCache (self):
        if self.type == 'DM':

            for i in range(self.totalblks): # these are sets..

                print(f"set: {bin_digits(i,self.setNum)} {self.set[i].data}", end=" ")
                print(f"tag : {self.set[i].tag} Valid: {self.set[i].valid} ")
                # print(f" used : {cache.set} times")
        print()

        if self.type == "FA":

            for i in range(self.totalblks):  # these are sets..
                print(f"way: {i} {cache.way[i].data}", end=" ")
                print(f"tag : {cache.way[i].tag} Valid: {cache.way[i].valid} ")
            for i in range(self.totalblks):
                self.lru.index[i] = 0




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
            #self.leastUsed = int(set,2)
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
                    print(f"--FULL-- access tag: {tag} ",end=" ")
                    print(f"loading blk fom Mem  [0x{format(int(strtBlk, 2), '04x')}] - M[0x{format(int(endBlk, 2), '04x')}] into set {set}  ")

                    # add swap with memory

                    self.set[int(set, 2)].tag = tag

            print(f"updated blk | set: {set}  tag  : {self.set[i].tag} valid: {self.set[i].valid}")
            print("")


        elif self.type == "FA":
            self.Count += 1
            addr = bin_digits(addr, 32)
            tag = addr[:self.tagsize]

            tag = hex(int(tag, 2))

            off = addr[-self.blk_offset:]
            strtBlk = addr[:self.tagsize ]  # memory range
            endBlk = strtBlk[:]
            for i in range(self.blk_offset):
                strtBlk += '0'
                endBlk += '1'

            print(f"({self.Count}) addr: {hex(int(addr,2))} \ntag: {tag}  off: {off} ")
           # print(f"M  [0x{format(int(strtBlk, 2), '04x')}] - M[0x{format(int(endBlk, 2), '04x')}] into way [ ]  ")
            """"
            # for each way - > loop through lru , check for empty, if full check tag of last used
            # check valid
                if valid , then check tag
                    if tag match 
                        hit , update lru
                        
                    else miss 
                
                
                if not valid, then empty , load into block instant miss, update lru
            #
            """
            wayNum = 0
            full = False
            for key in self.lru.index:
                if self.lru.index[key] == 0: # empty
                    wayNum = key
                else:
                    wayNum = self.lru.get()
                    full = True

            print(f"way: {wayNum} full:{full}")
            #
            # count = 0
            # for ways in self.way:
            #     if ways.valid == 0: # if empty
            #             self.Miss += 1
            #             print(f"({self.Count}) ---MISS--- addr: {addr}\n| tag: {tag} way: {count} ")
            #             ways.valid = 1
            #             break
            #
            #
            #
            #     else: # not empty then check tag
            #         if ways.tag == tag:
            #             self.Hit += 1
            #             print(f"({self.Count}) ---Hit--- addr: {addr}\n| tag: {tag} way: {count} ")
            #             ways.valid = 1
            #             break
            #
            #     count += 1


                #print(ways.data)


    def output(self):

        print(f"| total memory Accesses: {self.Count} Last used set: {self.lru.index}\n| Hits: {self.Hit} Miss: {self.Miss}")
        print(f"| Hit %  {( self.Hit / (self.Hit + self.Miss) )* 100}")


# a. a directly-mapped cache, block size of 16 Bytes, a total of 4 blocks (b=16; N=1; S=4)
# b. a fully-associated cache, block size of 8 Bytes, a total of 8 blocks (b=8; N=8; S=1)
# c. a 2-way set-associative cache, block size of 8 Bytes, 4 sets (b=8; N=2; S=4)
# d. a 4-way set-associative cache, block size of 8 Bytes, 2 sets (b=8; N=4; S=2)



Memory = [ ] # each index is a byte
cacheName = ""
blocks = 0
bytesize = 0
print("$$$ Cash $$$")
print(f" Welcome to DataCache sim ! how would you like your $CACHE$?")
cacheType = input("(1) for Direct Memory (2) Set-Associative (3) Fully Associative ")

if cacheType == '1':
    cacheName = 'DM'
    blocks = int(input( " How many Blocks? "))
    bytesize  = int( input( " How many Bytes per block (size in B)?"))
    #cache = CacheMoney('DM',blocks,bytesize)

elif cacheType == '3':
    cacheName = 'FA'
    blocks = int(input(" How many Blocks? "))
    bytesize = int(input(" How many Bytes per block (size in B)?"))

#elif cacheType == 3:


debug = input("would you like to debug? y/n")

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
#print(m)

cache = CacheMoney(cacheName, blocks,bytesize) # type of cache , mem? , sets, bytes
cache.printCache()
#
for mems in m:
    cache.write_cache(int(mems,16))
    if debug == 'y':
        input("")
cache.printCache()
cache.output()

#printMemory(Memory)
#print(Memory)
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
