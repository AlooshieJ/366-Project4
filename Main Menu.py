print("PC Control Signal")

PCControlSignal = {
"MemtoReg":(0,0,0,0),
"Branch":(0,0,0,0),
"ALUSrc":(0,0,0,0),
"RegDst":(0,0,0,0),
"RegWrite":(0,0,0,0)

}


def fetch(inst=None):
    print(f"fetch: for {inst}")
    for sig in PCControlSignal:
        print(f" {sig}  {PCControlSignal[sig]} ")





def decode(inst):
    print(f" decode {inst}")

def execute(inst):
    print(f" execute {inst}")

tmp = {

    "0": (fetch),
    "1": (decode),
    '2': (execute)

}
for key in tmp:
   tmp[key]("addi")


#
# def Fetch (ALL)
# IorD = 0
# AluSrcA = 0
# ALUOp = 00
# PCSrc = 0
# IRWrite = 1
# PCWrite = 1
#
# def Decode (ALL)
# ALUSrcA = 0
# ALUSrcB = 11
# ALUOp = 00
#
# def LSWExectution(self) # (LW, SW)
# ALUSrcA = 1
# ALUSrcB = 10
# ALUOp = 00
#
# def Execution-(R-type)
# ALUSrcA = 1
# ALUSrcB = 00
# ALUOp = 10
#
# def Execution-(BEQ)
# ALUSrcA = 1
# ALUSrcB = 00
# ALUOp = 01
# PCSrc = 1
# Branch = 1
#
# def Exectution - (I-type)
#
#
# def Memory-(LW)
# IorD = 1
#
# def WriteBack-(LW)
# RegDst = 0
# MemtoReg = 1
# RegWrite = 1
#
# def Memory (Addi)
# RegDst = 0
# MemtoReg = 0
# RegWrite = 1
#
#
#
# FINAL RESULTS
# ----------------------------------#Final output Statistics#--------------------------
#
# Total dynamic instruction count = Total
#
# Total cycle count= Total
#
# ----------------------------------#Total Cycle Count for#----------------------------
#
# 3 cycle = Total Count
#
# 4 cycle = Total Count
#
# 5 cycle = Total Count
#
# ----------------------------#value distribution of each control signals#--------------
# MemtoReg:
# 0 = Total
# 1 = Total
# X = Total
#
# MemWrite:
# 0 = Total
# 1 = Total
# X = Total
#
# Branch:
# 0 = Total
# 1 = Total
# X = Total
#
# ALUSrcA:
# 0 = Total
# 1 = Total
# X = Total
#
# ALUSrcB:
# 0 = Total
# 1 = Total
# X = Total
#
# RegDst:
# 0 = Total
# 1 = Total
# X = Total
