
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

        self.data  = []

        for i in range(size):
            self.data.append('$') # read from mem


class CacheMoney:

    def __init__(self, option, addr,total_blocks= 4):

        self.blk_size = 16 # input
        self.blk_offset = 0
        self.blks = []
        self.totalblks = total_blocks
        self.memspace = 0 # ???
        self.type = option
        self.set = []
        self.way = []


        if self.type == 'DM':
            print(f"Creating Direct Map Cash | total blocks: {self.totalblks}  block size: {self.blk_size}")
            for i in range(self.totalblks): # creating 4 blocks
                self.blks.append(Block(self.blk_size ))

            self.set.append(self.blks)

        # if type == 'SA':

    def printCache (self):
        if self.type == 'DM':

            for i in range(self.totalblks): # these are sets..

                print("set: ",i, cache.blks[i].data, end=" ")
                print(f"tag : {cache.blks[i].tag} Valid: {cache.blks[i].valid} ")
            print(cache.blks)

            # print("printing set:")
            # for i in self.set:
            #     print( i)


# a. a directly-mapped cache, block size of 16 Bytes, a total of 4 blocks (b=16; N=1; S=4)
# b. a fully-associated cache, block size of 8 Bytes, a total of 8 blocks (b=8; N=8; S=1)
# c. a 2-way set-associative cache, block size of 8 Bytes, 4 sets (b=8; N=2; S=4)
# d. a 4-way set-associative cache, block size of 8 Bytes, 2 sets (b=8; N=4; S=2)


t1 = 4
Memory = []
print("$$$ Cash $$$")


for i in range(20):
    Memory.append(mem(0x2000 + 4*i, 0, 0 , 0, 0))
cache = CacheMoney('DM',0x2000, t1)

cache.printCache()

count = 0
for addr in Memory:
    addr.writeWordMem(count)
    count += 1

    if addr.addr % (4 * 8) == 0:
        print('\n', end=" ")
    addr.print_mem()
