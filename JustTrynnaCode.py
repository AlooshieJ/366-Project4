from JustTrynnaCodeFuncs import *


def main():
    columns = 3
    rows = 4
    list2D = [[0] * columns for i in range(rows)]

    list2D[1][0] = 2

    num = 5
    numCopy = num
    numCopy = 6

    print(f"num:{num}  copy:{numCopy}")
    for row in list2D:
        print(row)



if __name__ == '__main__':
    main()
