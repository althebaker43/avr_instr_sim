; This is a simple routine to add two numbers
; Inputs:
;  R16: operand 1
;  R17: operand 2
; Outputs:
;  R18: sum of operands 1 and 2
.global add2
add2:
    push r16

    add r16,r17
    mov r18,r16

    pop r16

    ret
