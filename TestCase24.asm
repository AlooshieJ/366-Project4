ori $8, $0, 2
addi $9, $0, 0x60
sw_loop:
sw $8, 0x2000($9)
addi $9, $9, -4
beq $9, $0, sw_done
addu $8, $8, $8
sub $8, $0, $8
addi $8, $8, -3
beq $0, $0, sw_loop
sw_done:
addi $8, $0, 0x2078
addi $10, $0, 0x2060
addi $9, $0, 0x2000
outer_loop:
addi $14, $0, 3
lw $11, 0($9)
inner_loop:
addi $9, $9, 4
lw $12, 0($9)
slt $13, $12, $11
beq $13, $0, skip
addu $11, $0, $12
skip:
addi $14, $14, -1
bne $14, $0, inner_loop
sw $11, 0($8)
addi $8, $8, 4
slt $13, $9, $10
bne $13, $0, outer_loop