controles = {
        "PC_load"          :  0,
        "PC_inc"           :  1,
        "PC_setStack"      :  2,
        "PC_stackInc"      :  3,
        "PC_loadFromStack" :  4,
        "PC_stackDec"      :  5,
        "PC_enOut"         :  6,
        "deco_load1"       :  7,
        "deco_load2"       :  8,
        "deco_enOpC"       :  9,
        "deco_enInxX"      : 10,
        "deco_enInxY"      : 11,
        "deco_enNum"       : 12,
        "mem_setAddr"      : 13,
        "mem_enIn"         : 14,
        "mem_enOut"        : 15,
        "reg_enIn"         : 16,
        "reg_enOut"        : 17,
        "en_A"             : 18,
        "en_B"             : 19,
        "w_flag"           : 20,
        "ALU_enOut"        : 25,
        "mon_setMost"      : 26,
        "mon_setLeast"     : 27,
        "mon_enIn"         : 28,
        "joy_enOut"        : 29,
        "CU_load"          : 30,
        "CU_reset"         : 31
        }

ALU_op = {
        "ADD" : 1,
        "SUB" : 2,
        "INC" : 3,
        "DEC" : 4,          # Todo el programa se basa en traducir
        "SHR" : 5,          # texto a números que están directamente
        "SHL" : 6,          # en el procesador en la forma de salidas
        "OR"  : 7,          # de la unidad de control.
        "XOR" : 8,
        "AND" : 9,
        
        "cte00" : 10,
        "cte01" : 11,
        "cte02" : 12,
        "cteff" : 13
}                   
                    
def crearROM(texto):
    resultado = "" 

    sinComentarios  = borrarComentarios('0:\n'+texto ) # Se borran comentarios, espacios y tabs. El '0:\n' se explica en separarDirecc.
    direccSeparadas = separarDirecc(sinComentarios   ) # Se separan las posiciones de la ROM del código y se crea una lista de strings.
    lineasSeparadas = separarLineas(direccSeparadas  ) # Se separa cada enter y ahora la lista de strings tiene [dir, renglon1, renglon2...] .
    memoriaEnLista  = poblarListaCero(lineasSeparadas) # Se genera una lista de 256 posiciones iguales con el string '00000000'.
                                                       # y luego se puebla con los strings de los renglones traducidos.
    i = 1
    while i <= 256:
        if not i % 8:
            resultado += memoriaEnLista[i-1] + '\n'
        else:
            resultado += memoriaEnLista[i-1] + ' '
        i += 1

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

    return resultado

                                    # La idea acá es buscar ':' que separa a las posiciones de memoria de las instrucciones.
def separarDirecc(texto):           # Una vez que se encuentra se va para atrás hasta el último '\n' (enter) y se separa ese
    resultado = []                  # pedazo de string de el resto. Ese resto se determina encontrando, delante de ':' hasta
    tamT = len(texto)               # encontrar los próximos ':' y de ahí retroceder un poco hasta el '\n'.
    iter_texto = 0                  # La función ignora todo el texto hasta encontrar los primeros ':', por eso se agregan en
                                    # borrarComentarios. La alternativa eran muchas lineas de código más.
    while iter_texto < tamT:
        
        if texto[iter_texto] == ':':

            dir_micro = iter_texto
            while dir_micro > 0 and texto[dir_micro] != '\n': dir_micro -= 1

            if dir_micro:
                resultado.append(texto[dir_micro:iter_texto])
            else:
                resultado.append(texto[0:iter_texto])

            iter_texto += 1
            ini_micro = iter_texto
            while iter_texto < tamT and texto[iter_texto] != ':' and texto[iter_texto] != '': iter_texto += 1

            if iter_texto < tamT and texto[iter_texto]:
                fin_micro = iter_texto
                while fin_micro > 0 and texto[fin_micro] != '\n': fin_micro -= 1 
                resultado.append(texto[ini_micro:fin_micro])
            else:
                resultado.append(texto[ini_micro:iter_texto])

        else:
            iter_texto += 1

    return resultado


def separarLineas(lista_texto):
    resultado = [] 

    for i in lista_texto:
        resultado += i.split('\n')

    return [i for i in resultado if i]


def poblarListaCero(lista_texto):
    listaCero = ['00000000' for i in range(256)]
    pos_lista = 0                                   # Se arma la lista cero y se la sobrescribe con
                                                    # Las instrucciones traducidas y ubicadas en
    for i in lista_texto:                           # las posiciones de memoria separadas en separarDirecc
        if i[0] in '01':                            # y calculadas en obtenerPosROM
            pos_lista = obtenerPosROM(i)
        elif [j for j in list(controles.keys())+list(ALU_op.keys()) if j in i]:
            listaCero[pos_lista] = instAHexa(i)
            pos_lista += 1
    return listaCero


# Se alargan los números binarios de las etiquetas para 
# llegar a 8 bits y se tiene en cuenta que las etiquetas
# marcan la posición por los bits más significativos

def obtenerPosROM(bin_corto_texto):
    while len(bin_corto_texto) < 8:
        bin_corto_texto += '0'

    return int(bin_corto_texto, 2)


def instAHexa(linea):

    instrucciones = {clave:(1<<valor) for clave,valor in controles.items()}
    instrucciones.update({clave:(valor<<21) for clave,valor in ALU_op.items()})

    numerosInst = [valor for clave,valor in instrucciones.items() if clave in linea]

    instABin = 0
    for i in numerosInst: instABin += i    # Tomando el número de las palabras clave (ver los diccionarios),
                                           # se hace el shift de bits correspondiente y después se suma el
    hexa_crudo = hex(instABin)[2:]         # resultado dentro de un mismo renglón

    resultado = hexa_crudo
    while len(resultado) < 8:
        resultado = '0' + resultado

    return resultado
