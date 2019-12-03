

file = open("toBin.txt",'r')

output = open("Hex.txt",'w')

for line in file.readlines():
    string = str( hex(int(line,2)) )
    output.write(string + '\n')