@ Pruebo una suma
suma ES 4 MAS 5
IMPRIMIR suma

@ Pruebo una multiplicación
multiplicacion ES suma POR 3
IMPRIMIR multiplicacion

@ Pruebo una división dentro de la misma impresión
IMPRIMIR multiplicacion DIVIDIDO 9 @ Imprimiría 3

@ Pruebo un string
texto ES "Este es un texto 'ejemplo' (con simbolos pero sin acentos)."
IMPRIMIR texto

@ Pruebo una suma con decimales
suma ES 3.8 MAS 3.7
IMPRIMIR suma

@ Pruebo una multiplicación con decimales
multiplicacion ES 3 POR suma
IMPRIMIR multiplicacion

@ Pruebo una división con decimales
division ES multiplicacion DIVIDIDO 5
IMPRIMIR division

@ Pruebo encadenar varias operaciones
resultado ES 8 MAS 4.5 POR 3 MENOS 500.432
IMPRIMIR resultado

@ Pruebo un valor booleano
booleano ES 2 IGUAL 3
IMPRIMIR booleano

@ Pruebo un valor asignado según condición
booleano ES "A" SI 2 IGUAL 3 NO "B"
IMPRIMIR booleano

@ Pruebo una comparación por mayor
IMPRIMIR 105 MAYOR 57

@ Pruebo una comparación por menor
IMPRIMIR 105 MENOR 57

@ Pruebo una comparación con decimales
IMPRIMIR 108.855 MAYOR 108.6774

@ Pruebo una comparación de strings por igual
IMPRIMIR "BUENO" IGUAL "BUENO"

@ Pruebo una comparación de strings por diferente
IMPRIMIR "BUENO" DIFERENTE "BUENO"

@ Pruebo una comparación de strings por mayor
IMPRIMIR "BUENO" MAYOR "AVANZAR"

@ Pruebo una comparación de strings por menor
IMPRIMIR "BUENO" MENOR "AVANZAR"

@ Pruebo un y entre verdadero y verdadero
IMPRIMIR VERDADERO Y VERDADERO

@ Pruebo un y entre verdadero y falso
IMPRIMIR VERDADERO Y FALSO

@ Pruebo un o entre verdadero y verdadero
operador_uno ES "BUENO" IGUAL "BUENO"
operador_dos ES 5 IGUAL 5
operador_tres ES 5 IGUAL 3
IMPRIMIR operador_uno
IMPRIMIR operador_dos
IMPRIMIR operador_tres
IMPRIMIR operador_uno O operador_dos
IMPRIMIR operador_uno O operador_tres

@ Pruebo concatenar strings
variable ES " -- "
IMPRIMIR "AA" MAS "BB" MAS variable MAS "CC"

@ Pruebo una suma inválida
@ IMPRIMIR 3 MAS "AA"

@ Pruebo una resta inválida
@ IMPRIMIR 3 MENOS "AA"

@ Pruebo una multiplicación inválida
@ IMPRIMIR 3 POR "AA"

@ Pruebo una división inválida
@ IMPRIMIR 3 DIVIDIDO "AA"

@ Pruebo una comparación inválida
@ IMPRIMIR "ASD" MAYOR 3
