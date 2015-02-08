; This is a simple routine to multiply two numbers
; Inputs:
;  R16: operand 1
;  R17: operand 2
; Outputs:
;  R18: product of operands 1 and 2
.global mult2
mult2:
    push r16
    push r17
    ; TODO: clear R18

mult2_loop:

    tst     r17
    breq    mult2_end
    dec     r17

    add     r18,r16

    rjmp    mult2_loop

mult2_end:

    mov r16,r18
    pop r17
    pop r16

    ret
