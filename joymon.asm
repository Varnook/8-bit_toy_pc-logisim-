; Programa para mover un punto en pantalla con el joystick.

joyValue: 0xF0
monLow: 0xF1
monHig: 0xF2
monCol: 0xF3

main:
CALL clrscr
JOY 	 joyValue
SETR R0, joyValue
MOV  R0, R1
SHR  R0, 0x04     ; Se obtiene la pos X en R0.
AND  R1, 0x0F     ; Se obtiene la pos Y en R1.
SUB  R1, 0x01


; Convertir R0 y R1 a algo que el monitor pueda leer. 		DISP  					+--------+
				  ;											low = 01 high = 00 		|00xxxxxx|
SETM R0, monCol   ; X no necesita nada más que el SHR.		col = 1					|01xxxxxx|
				  ;																	|00xxxxxx|
MOV  R0, 0x06 	  ;	Para Y se hace uso del SHL, pero		DISP  					|10xxxxxx|
SUB  R0, R1       ; se termina expresando un número de		low = 00 high = 01 		+--------+
MOV  R1, 0x01	  ; 15 bits.								col = 2			
JN   esLow        ;
				  ; si Y > 6 (maximo shift para high que es de 7 bits) entonces
SHL  R1, R0		  ;		1 << [(6 - Y) and 7]  primero hay que invertir Y para poder correr a 1
SETM R1, monHig   ; sino 1 << (6 - Y)         según los últimos 3 bits de Y. Si no se invierte
JMP  loadDisp     ;							  antes del << el bit se va a correr al revés, por
				  ; 						  ejemplo el punto que tendría que quedar abajo en
esLow:			  ;							  la pantalla queda arriba (siempre con respecto a
AND  R0, 0x07	  ;							  la mitad del low o high que corresponda.
SHL  R1, R0
SETM R1, monLow

loadDisp:
DISP monLow
JMP main

clrscr:
	MOV  R0, 0x00
	SETM R0, monLow
	SETM R0, monHig

	MOV  R1, 0x0F

	iterarCol:
	SETM R1, monCol
	DISP monLow
	SUB  R1, 0x01
	JZ   finIterarCol
	JMP  iterarCol

	finIterarCol:
RET
