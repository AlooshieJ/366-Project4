from math import *
from copy import deepcopy
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


class fifo:
    def __init__(self, size):

        self._keys = []
        self._values = []
        self.capacity = size

        for i in range(size): # creating w/ all size = 0
            self._keys.append(i)
            self._values.append(0)

    def pop (self): # removes first element

        del self._keys[0]
        del self._values[0]



    def update(self, key, value):

        keyIndex = self._keys.index(key)
        self._keys[keyIndex] = key
        self._values[keyIndex] = value

        self.move_to_end(key)


    def move_to_end(self,key):
        keyIndex = self._keys.index(key)
        value = self._values[keyIndex]

        del self._keys[keyIndex]
        del self._values[keyIndex]

        self._keys.append(key)
        self._values.append(value)

    def get(self,key): # returns key value pair
        try:
            keyIndex = self._keys.index(key)
            return keyIndex, self._keys[keyIndex] , self._values[keyIndex]
        except ValueError:
            return -1





    def print(self):

        print(f"keys: {self._keys}\nvalues: {self._values}\n")

    def checkWay(self): # returns *INDEX* of first instance of empty
        occupied = []
        empty = []
        keyNum = []
        key = 0
        while key < self.capacity:
            keyIndex = self._keys.index(key)
            keyNum.append(key)
            #print(f"checking way: {key}", end=" ")
            if self._values[keyIndex] == 0: # empty
                empty.append(keyIndex)
                #print(f"---Empty")
                break
            else:   # occupied
                #print(f"---Occupied")
                occupied.append(keyIndex)

            key += 1
        return empty,occupied,keyNum





class Block:
    #data = []
    def __init__(self, size):

        self.valid = 0 # would have to check somehow
        self.tag = 0x0 # math to addr
        self. size = size
        self.Count = 0

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

    def __init__(self, option,total_blocks,bytes,total_ways = 1):

        self.blk_size = bytes # input
        self.totalblks = total_blocks
        self.blk_offset = 0
        # self.blks = []
        self.total_ways = total_ways
        self.set_Bits = 0
        self.total_sets = total_blocks

        self.memspace = 0 # ???
        self.type = option
        self.setNum = 0
        self.set = []
        self.way = []
        self.Hit = 0
        self.Miss = 0
        self.Count = 0
        self.lru = fifo(total_blocks) # list size of total blocks, should incorporate a ways check too
        self.allLRU = []#[deepcopy(fifo(self.total_ways))] * self.total_sets


        if self.type == 'DM':
            print(f"Creating Direct Map Cash | total blocks: {self.totalblks}  block size: {self.blk_size} B")

            self.blk_offset = minBits(self.blk_size -1)
            self.setNum =     minBits(self.totalblks -1)
            self.tagsize = 32 - (self.setNum + self.blk_offset)
            print(f"tag size: {self.tagsize} set size: {self.setNum} in blk off: {self.blk_offset}")

            for i in range(self.totalblks): # creating 4 blocks
                self.set.append(Block(self.blk_size ))


        elif self.type == "FA":
            print(f"Creating Fully Associative Cash| total blocks: {self.totalblks} block size: {self.blk_size} B")

            self.blk_offset = minBits(self.blk_size - 1)
            self.ways = self.totalblks
            self.tagsize = 32 - self.blk_offset
            print(f"tag size: {self.tagsize} total ways: {self.ways} in blk off: {self.blk_offset}")

            for i in range(self.totalblks):
                self.way.append(Block(self.blk_size))

        # c. a 2-way set-associative cache, block size of 8 Bytes, 4 sets (b=8; N=2; S=4)
        elif self.type == 'SA':

            self.blk_offset = minBits(self.blk_size - 1)
            total_blocksA = self.total_sets * self.total_ways
            # self.total_sets = int(self.totalblks / self.total_ways)
            self.set_Bits = minBits( self.total_sets  - 1)
            self.tagsize = 32 - (self.set_Bits + self.blk_offset)
            print(f"Creating {self.total_ways}-way Set Associative Cash| total sets:{self.total_sets} | total blocks: {total_blocksA} | block size: {self.blk_size} B")

            print(f"tag size: {self.tagsize} | bits for set: {self.set_Bits} | in blk off: {self.blk_offset}")

        # for i in range(self.total_sets):
        #     for j in range(self.total_ways):
        #         self.way.append(deepcopy(Block(self.blk_size)))
        #     self.set.append(self.way)

        # creating sets that have individual ways in them
        for i in range(self.total_ways):
           self.way.append(Block(self.blk_size))

        for i in range(self.total_sets):
           self.set.append(deepcopy(self.way))
           self.allLRU.append(deepcopy(fifo(self.total_ways)))

        # creating lru for each set
        #for i in range(self.)




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
            #for i in range(self.totalblks):
            #    self.lru.index[i] = 0

        if self.type == "SA":
            s = 0
            w = 0

            for set in self.set:
                print(f" set: {bin_digits(s, self.set_Bits)} ")
                for way in set:
                    print(f" way: {w} {way.data} tag: {way.tag} Valid: {way.valid} ")
                    w += 1
                print('')
                print(f"lru for set {s} : ") # lru printing for each set
                self.allLRU[s].print()

                s +=1


                #print(f" tag:")





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

            wayNum = self.lru.checkWay() # returns index of key to empty way , and list of occupied ways , keysNumber
            emptyIndex  = wayNum[0]
            occupyIndex = wayNum[1]
            keyNums     = wayNum[2]
            match       = 0
            wayCounter  = 0
            print (f" way: {wayNum} ")
            for numWays in self.way:
                print(f"Checking way: {wayCounter} tag {numWays.tag} ",end = '')
                if numWays.valid == 0:
                    print('---Empty')
                if numWays.valid == 1:
                    print('---Occupied')
                    if numWays.tag == tag: # check tag
                        print(f"---Hit on way {wayCounter} tag {numWays.tag}")
                        numWays.valid = 1
                        self.Hit += 1
                        self.lru.update(wayCounter , 1)
                        match = 1
                        break
                wayCounter += 1

            if len(emptyIndex) == 1 and match != 1: # use empty
                print(f"---MISS using empty , way {keyNums[-1:][0]}")
                self.way[self.lru._keys[emptyIndex[0]]].tag = tag
                self.way[self.lru._keys[emptyIndex[0]]].valid = 1
                self.lru.update(self.lru._keys[emptyIndex[0]],1)
                self.Miss += 1
                #have to print which memory access ...
            elif len(emptyIndex) == 0 and match != 1: # if no empty check lru, update lru
                print(f"Miss due to FULL SET --- LRU replace way {self.lru._keys[0]}")
                self.way[self.lru._keys[0]].tag = tag
                self.way[self.lru._keys[0]].valid = 1
                self.lru.update(self.lru._keys[0],1)
                self.Miss += 1

            if debug == 'y':
                self.printCache()
            #self.lru.print()

        elif self.type == 'SA':
            self.Count += 1
            addr = bin_digits(addr, 32)
            tag = addr[:self.tagsize]

            tag = hex(int(tag, 2))

            set = addr[-self.set_Bits - self.blk_offset: -self.blk_offset]
            off = addr[-self.blk_offset:]
            strtBlk = addr[:self.tagsize + self.setNum]  # memory range
            endBlk = strtBlk[:]
            # self.leastUsed = int(set,2)
            for i in range(self.blk_offset):
                strtBlk += '0'
                endBlk += '1'

            print(f"({self.Count}) addr: {hex(int(addr,2))} \ntag: {tag} set: {set} off: {off} ")


            # for each set, check each way, within that way check the tag and valid , one address has N options

            wayResult       = self.allLRU[int(set,2)].checkWay()
            emptyIndex      = wayResult[0]
            occupiedIndex   = wayResult[1]
            keyNum          = wayResult[2]
            wayCounter = 0
            match = 0
            print(f"trying set :{set} ")
            for way in self.set[int(set,2)]:
                print(f"way : {wayCounter} tag: {way.tag} valid : {way.valid}",end = " ")
                if way.valid == 0: # miss first miss
                    print( " --- Empty")
                    break

                if way.valid == 1:
                    print("---Occupied, checking tag...", end = " ")
                    if way.tag == tag:
                        print(f"---Hit on tag {way.tag}")
                        way.valid = 1
                        self.Hit += 1
                        self.allLRU[int(set,2)].update(wayCounter,1)
                        match = 1
                        break
                wayCounter  += 1

            if len(emptyIndex) == 1 and match != 1: # use empty
                print(f"---Miss using empty, way {keyNum[-1:][0]}")
                self.set[int(set,2)][wayCounter].valid = 1
                self.set[int(set,2)][wayCounter].tag = tag
                #self.way[self.allLRU[int(set,2)]._keys[0]].tag = tag
                #self.way[self.allLRU[int(set,2)]._keys[0]].valid = 1
                #self.allLRU[int(set,2)].update(keyNum[-1:][0],1)
                self.allLRU[int(set,2)].update(self.allLRU[int(set,2)]._keys[emptyIndex[0]],1)
                self.Miss += 1
            elif len(emptyIndex) == 0 and match != 1:
                print(f"---Miss due to FULL SET -- LRU replace  way {self.allLRU[int(set,2)]._keys[0]}")
                self.set[int(set,2)][self.allLRU[int(set,2)]._keys[0]].valid = 1
                self.set[int(set, 2)][self.allLRU[int(set, 2)]._keys[0]].tag = tag
                self.allLRU[int(set,2)].update(self.allLRU[int(set,2)]._keys[0],1)
                self.Miss += 1

            #tag: {self.set[int(set,2)][0].data} valid : {self.set[int(set,2)][0]}\n lruInfo: ")
            #print(wayResult,self.set,"\n" ,self.allLRU)
            if debug == 'y':
                self.allLRU[int(set,2)].print()
                self.printCache()

                #print(wayResult)



    def output(self):

        print(f"| total memory Accesses: {self.Count} \n| Hits: {self.Hit} Miss: {self.Miss}")
        print(f"| Hit %  {( self.Hit / (self.Hit + self.Miss) )* 100}")


# a. a directly-mapped cache, block size of 16 Bytes, a total of 4 blocks (b=16; N=1; S=4)
# b. a fully-associated cache, block size of 8 Bytes, a total of 8 blocks (b=8; N=8; S=1)
# c. a 2-way set-associative cache, block size of 8 Bytes, 4 sets (b=8; N=2; S=4)
# d. a 4-way set-associative cache, block size of 8 Bytes, 2 sets (b=8; N=4; S=2)



Memory = [ ] # each index is a byte
cacheName = ""
blocks = 0
bytesize = 0
numWays = 1 # by default
numSets = 0
print("$$$ Cash $$$")
print(f" Welcome to DataCache sim ! how would you like your $CACHE$?")
cacheType = input("(1) for Direct Memory (2) Set-Associative (3) Fully Associative ")

if cacheType == '1':
    cacheName = 'DM'
    blocks = int(input( " How many Blocks? "))
    bytesize  = int( input( " How many Bytes per block (size in B)?"))
    #cache = CacheMoney('DM',blocks,bytesize)
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

cache = CacheMoney(cacheName, blocks,bytesize,numWays) # type of cache , mem? , sets, bytes
cache.printCache()
#
for mems in m:
    cache.write_cache(int(mems,16))
    if debug == 'y':
        input(" press enter to step")
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
