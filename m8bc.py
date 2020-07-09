import sys
import os

from microcoder import crearROM
from assembler  import crearPrograma
#import minilanguage

extensiones = [".ops", ".asm", ".lmg"]

def main(archivo, nombreSalida):
    salida = ""

    try:
        with open(archivo) as a:
            texto = a.read()
    except FileNotFoundError:
        print("No se ha encontrado el archivo")
        exit()
    
    if archivo[-4:] == ".ops":
        salida = crearROM(texto)
         
        if not nombreSalida:
            f= open("ROM", "w")
            f.write(salida)
            f.close()        

    if archivo[-4:] == ".asm":
        salida = crearPrograma(texto)
        
        if not nombreSalida:
            f= open("RAM", "w")
            f.write(salida)
            f.close()     
       
    if nombreSalida:
        f = open(nombreSalida+".mem", "w")
        f.write(salida)
        f.close()
    

if sys.argv[1][-4:] in extensiones:
    if len(sys.argv) == 2:
        main(sys.argv[1], "")

    elif len(sys.argv) == 4 and sys.argv[2] == "-o":
        main(sys.argv[1], sys.argv[3])

    else:
        print("Uso: m8bc.py archivoEntrada -o archivoSalida")
else:
    print("Uso: m8bc.py nombreArchivo(.ops/.asm/.lmg)")
