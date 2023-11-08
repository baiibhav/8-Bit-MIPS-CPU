#a comment
add $1 $2 $3 # comment
and $4 $1 $2 # comment
or $4 $1 $2
sub $4 $1 $2
slt $4 $1 $2
lw $4 1($1)
sw $4 1($1)
addi $0 $1 1
beq $0 $1 3
j 3
