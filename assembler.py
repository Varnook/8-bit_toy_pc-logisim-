import re


instrucciones = {
        "ADD"  :  2,
        "SUB"  :  4,
        "NEG"  :  6,
        "SHR"  :  8,
        "SHL"  : 10,
        "OR"   : 12,
        "XOR"  : 14,      # Misma idea que en microcoder. Ahora cada instrucción
        "AND"  : 16,      # tiene un valor que se mueve 3 bits a la izquierda y
        "CMP"  : 18,      # se traduce a hexa.
        "MOV"  : 20,
        "SETM" : 22,
        "SETR" : 23,
        "JC"   : 24,
        "JZ"   : 25,
        "JN"   : 26,
        "JMP"  : 27,
        "CALL" : 28,
        "RET"  : 29,
        "DISP" : 30,
        "JOY"  : 31
}


formatoDinamico = [clave for clave,valor in instrucciones.items() if valor < 21]


def crearPrograma(texto):
    resultado = ""

    sinComentarios = borrarComentarios(texto)          # Igual a la de microcoder pero ahora no es necesario modificar el string original.
    lineasSeparadas = separarLineas(sinComentarios)           # Usando regex se separa por linea y etiqueta.
    etiquetasTraducidas = traducirEtiquetas(lineasSeparadas)         # Se pasan las etiquetas a valores en hexa.
    instruccionesTraducidas = traducirInstrucciones(etiquetasTraducidas)    # Se traducen instrucciones y números de registros.
    
    for i in instruccionesTraducidas:
        resultado += i + '\n'

    return "v2.0 raw\n" + resultado

#también borra espacios
def borrarComentarios(texto):
    resultado = ""
    esComentario = False

    for c in texto:
        if c == ';' and not esComentario:
            esComentario = True
        elif c == '\n' and esComentario:
            esComentario = False
 
        if not esComentario and c not in ' \t':
            resultado += c

    return resultado;

def separarLineas(texto):
    return [i for i in re.split(':|\n', texto) if i]

def traducirEtiquetas(lineas_texto):
    etiquetas = encontrarEtiquetas(lineas_texto)        # Se genera un diccionario con los valores de cada etiqueta. Esos valores
    resultado = []                                      # se obtienen con una función auxiliar. Después se reemplazan los strings
                                                        # de las etiquetas por estos valores y, siempre que la instrucción no sea
    for linea in lineas_texto:                          # seguida por un registro, se agrega al final de la instrucción: una ','.
        
        instr = [clave for clave in instrucciones.keys() if clave in linea]
        etiqueta = [clave for clave in etiquetas.keys() if clave in linea]

        if instr:
            cantL = len(instr[0])       # Cantidad Letras
            
            if etiqueta:
                aReemplazar = linea
                
                while etiqueta:
                    et = max(etiqueta, key=len)
                    aReemplazar = aReemplazar.replace(et, hex(etiquetas[et]))
                    etiqueta.remove(et)

                if aReemplazar[cantL] not in ',R':
                    aReemplazar = aReemplazar[:cantL] + ',' + aReemplazar[cantL:]
                
                resultado.append(aReemplazar)

            else:
                if len(linea) > cantL and linea[cantL] == '0':
                    resultado.append(linea[:cantL] + ',' + linea[cantL:])
                else:
                    resultado.append(linea)

    return resultado;

def encontrarEtiquetas(lineas_texto):
    nro_inst  = 0                             # Se buscan las posiciones de memoria de las etiquetas marcadas
    etiquetas = {}                            # con ':'. Además el programa tiene la capacidad de asignar una
                                              # posición definida manualmente si después de los ':' hay algún
    for i in range(len(lineas_texto)):        # número (en hexa).
        linea = lineas_texto[i]
        
        if [clave for clave in instrucciones.keys() if clave in linea]:
            
            if "RET" in linea:
                nro_inst += 1
            else:
                nro_inst += 2

        else:
            if '0x' not in linea:
                siguiente = lineas_texto[i + 1]

                if len(siguiente) == 4 and '0x' in siguiente:
                    etiquetas[linea] = int(lineas_texto[i + 1], 16)
                else:
                    etiquetas[linea] = nro_inst

    return etiquetas;

def traducirInstrucciones(lineas_texto):
                                                        # Esta función reemplaza cada palabra clave por su valor según
    resultado = []                                      # el diccionario. Para las instrucciones que tienen un formato
    for i in lineas_texto:                              # variable, se asigna el código de operación sin necesitar que
       resultado += i.split(",")                        # se indique en assembler el formato a usar, como se indica en
                                                        # la rama true del segundo if con "R" not in resultado[i + 1].
    for i in range(len(resultado)):
        clave = [clave for clave in instrucciones.keys() if clave in resultado[i]]

        if clave:
            clave = clave[0]

            if clave in formatoDinamico:
                resultado[i] = hex((instrucciones[clave] + ("R" not in resultado[i + 1]) << 3) + int(resultado[i][-1]))[2:]
            else:
                if resultado[i][-2] == "R" :
                    resultado[i] = hex((instrucciones[clave] << 3) + int(resultado[i][-1]))[2:]
                else:
                    resultado[i] = hex( instrucciones[clave] << 3)[2:]
        else:
            if "R" in resultado[i]:
                resultado[i] = hex(int(resultado[i][1]) << 5)[2:]
            else:
                if len(resultado[i]) == 3:
                    resultado[i] = "0" + resultado[i][-1]
                else:
                    resultado[i] = resultado[i][2:]

    return resultado;
