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
            print(f"checking way: {key}", end=" ")
            if self._values[keyIndex] == 0: # empty
                empty.append(keyIndex)
                print(f"---Empty")
                break
            else:   # occupied
                print(f"---Occupied")
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
            #for i in range(self.totalblks):
            #    self.lru.index[i] = 0




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


            print (f" way: {wayNum} ")
            if len(emptyIndex) == 0 and len(occupyIndex) == self.lru.capacity: # no empty, all full
                print(f" all occupied{occupyIndex}")

            else:
                print(f" 1 empty index {emptyIndex}")

            # if wayNum[0] != "full": # update tag / valid bit, also need to check tag given a key
            #     if len(wayNum[1])  == 0: #all are empty, miss
            #         self.way[wayNum[0]].valid = 1
            #         self.way[wayNum[0]].tag = tag
            #         self.lru.set(wayNum[0], 1)
            #     else: # all are not empty, loop through occupied, chck tag
            #         for inway in wayNum[1]: # its not full , but occupied, check tag
            #             if self.way[inway].valid == tag:
            #                 #self.way[inway].valid = 1
            #                 self.way[inway].tag = tag
            #                 self.lru.set(inway,1)
            #             else: # if not the same tag, then update empty index
            #                 print('not matching tag, fill empty slot')
            #
            # else: # all sets a full,
            #     print(f"FULL.... what now")

            self.printCache()


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
