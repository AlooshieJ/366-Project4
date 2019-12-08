import collections

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
            print(f"checking way: {key}", end=" ")
            if self._values[keyIndex] == 0: # empty
                empty.append(keyIndex)
                print(f"---Empty")
                break
            else:   # occupied
                print(f"---Occupied")
                occupied.append(keyIndex)
            keyNum.append(key)
            key += 1
        return empty,occupied,keyNum







lru = fifo(5)
lru.print()

for tmp in range(lru.capacity):
    lru.update(tmp, 1)
lru.print()

lru.update(2,0)
print(lru.get(2))
lru.print()
print(lru.checkWay())
#for key , value in lru.index:
 #   print( key, value)
#print(lru.index)
lru.print()
E1 = (40 / 50) * 100
E2 = (23/34) * 100
E3 = (35/40) * 100
Hw = 95.5
# final = replace lowest exam
grade = (.3 * E1) + (.3 * E2 )+ (.3 * E3) + (.1 * Hw)
print(f"grade {grade}")
#
# class fifo:
#     def __init__(self, size):
#
#         self.index = []
#         self.size = size
#
#         #for i in range(size): # creating w/ all size = 0
#          #   self.index.append(i)
#
#
#
#     def push(self,value):
#
#         self.index.append(value)
#
#
#     # def order(self,setb):
#     #
#     #     self.index.
#
#     def top (self): # my pop return  what it pops out
#         return self.index[0]
#         #
#         # if len(self.index) > 0:
#         #     tmp = self.index[0]
#         #     self.index = self.index[1:]
#         #     self.index.append(tmp)
#         #     #self.index = self.index[1:]
#         #     return tmp
#         #
#         # else:
#         #
#         #     print("fifo is empty")
#
#    # def leastUsedSwap(self):
#
#
#
#
#
#
