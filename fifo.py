import collections

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




lru = fifo(5)
for tmp in range(lru.capacity):
    lru.set(tmp, 0)
#lru.set(1,0)
#for key , value in lru.index:
 #   print( key, value)
print(lru.index)

#print(lru.get(1))
print(lru.index[0])
#print(lru.get(2))
#lru.index.pop()
print(lru.index)

for i in range(5):
    if lru.index[i] == 0:
        print("empty, key :",i)

print(lru.index)

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
