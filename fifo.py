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

    def checkWay(self): # returns list of *INDEX* of first instance of empty , list of occupied , list of keys
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



# class fifo:
#     def __init__(self, size):
#
#         self.index = collections.OrderedDict()
#         self.capacity = size
#
#         #for i in range(size): # creating w/ all size = 0
#          #   self.index.append(i)
#
#     def get(self,key):
#         if key in self.index:
#             value = self.index[key]
#             # store value , for removing
#             del self.index[key]
#             #now add it back, already sorting due to structure
#             self.index[key] = value
#             return value
#         else:
#             return -1
#
#     def set(self,key , value): # set the value of dictionary, given a key
#         #if key in self.index:
#          #   del self.index[key]
#         #elif len(self.index) >= self.capacity:
#         #    self.index.popitem(last= False)
#
#         tmp = self.index
#         print(f"before: {tmp} after:", end = '')
#         tmp.move_to_end(key)
#         tmp[key] = value
#         print(tmp)
#         self.index = tmp
#
#
#     def front(self):
#         front = [*self.index.keys()][0] # allows us to acces first index key , aka least used key
#         #print(f" in func{tmp} type: {ty} {tmp2}")
#         return front
#
#     def checkWay(self):
#         occupied = []
#         empty = []
#         # for key in self.index:
#         #     print(f"checking way: {key}",end = " ")
#         #     if self.index[key] == 0: # empty
#         #         empty.append(key)
#         #         print("---Empty")
#         #     else:   # occupied
#         #         print("---Occupied")
#         #         empty.append(key)
#         # return [empty,occupied]
#         key = 0
#         print(f"fifo.ceckWay {self.index}")
#         while key < self.capacity:
#             print(f"checking way: {key}", end=" ")
#             if self.index[key] == 0:  # empty
#                 empty.append(key)
#                 print("---Empty")
#                 break
#                 #return key
#             elif self.index[key] == 1:  # occupied
#                 print("---Occupied")
#                 occupied.append(key)
#
#             key += 1
#
#         print( empty, occupied)
#         if len(occupied) < self.capacity:
#             return key , occupied
#         else: return "full" #, occupied




lru = fifo(5)
lru.print()

for tmp in range(lru.capacity-1):
    lru.update(tmp, 1)
lru.print()

#lru.update(2,0)
print(lru.get(2))
lru.print()
t = lru.checkWay()
print(t)
print(t[0][0] , t[2][-1:][0])
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
