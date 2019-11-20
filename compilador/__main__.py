from lexer import Lexer
from parce import Parser
from parce import int_to_hex_16
from rply import token as TokenClass
import regex
import sys

def main():
    fname = sys.argv[1]
    with open(fname) as f:
        text_input = f.read()
    
    lexer = Lexer().get_lexer()
    tokens = lexer.lex(text_input)
    
    list_tokens=list(tokens)
    dic_lineas_direcciones={}
    dic_variables={}
    dic_etiquetas={}
    contador=0
    #############Cambiar etiquetas por direcciones###############################Cambiar variables por direcciones##################
    # Asignamos a cada linea significativa un espacio en memoria
    for item in list_tokens:
        if contador > 256:
            raise Exception("Error: No hay suficiente espacio en memoria para compilar este programa.")
        else:
            contador_hex=int_to_hex_16(contador)
            if not (item.source_pos.lineno in dic_lineas_direcciones):
                dic_lineas_direcciones[item.source_pos.lineno] = contador_hex
                contador= contador+1
    # Llenamos un diccionario con los tokens de tipo VARIABLE
    for item in list_tokens:
        if item.gettokentype()=='VARIABLE' and item.value not in dic_variables :
            dic_variables[item.value]=""
    # Asociamos a cada variable un valor de memoria restante si hay espacio de memoria
    if (len(dic_lineas_direcciones)+len(dic_variables)) <= 256:
        for item in dic_variables:
            contador_hex=int_to_hex_16(contador)
            dic_variables[item]=contador_hex
            contador= contador+1
    else:
        raise Exception("Error: No hay suficiente espacio en memoria para compilar este programa.")
    #############Encontrar la dirección de cada etiqueta##################
    text_lines=text_input.splitlines()
    print("----------ASSEMBLY CODE-------------")
    for i in range(0,len(text_lines)): 
        print(text_lines[i])
        x=regex.search("^\s*(\@[A-Za-z]\w*)",text_lines[i])
        if x is not None: 
            dic_etiquetas[x.group(1)]=dic_lineas_direcciones[i+1]
    pg = Parser(dic_variables, dic_etiquetas)
    pg.parse()
    parser = pg.get_parser()
    print("-----------BINARY CODE--------------")
    f = open(sys.argv[1][:len(sys.argv[1])-4]+" - binary code.txt", "w")
    
    for line in text_lines:
        espaciosenblanco=regex.search("^\s*$", line)
        comentarios=regex.search("^\s*\%.*$", line)
        if espaciosenblanco is None and comentarios is None:
            f.write(parser.parse(lexer.lex(line)).eval()+"\n")
            print(parser.parse(lexer.lex(line)).eval())
    f.close()
    f = open(sys.argv[1][:len(sys.argv[1])-4]+" - initRam.coe", "w")
    cabecera="""; Sample memory initialization file for Single Port Block Memory, 
; v3.0 or later.
;
; This .COE file specifies initialization values for a block 
; memory of depth=256, and width=16. In this case, values are 
; specified in hexadecimal format.
memory_initialization_radix=16;
memory_initialization_vector=
"""
    f.write(cabecera)
    for line in text_lines:
        espaciosenblanco=regex.search("^\s*$", line)
        comentarios=regex.search("^\s*\%.*$", line)
        if espaciosenblanco is None and comentarios is None:
            f.write(parser.parse(lexer.lex(line)).eval()+"\n")
            print(parser.parse(lexer.lex(line)).eval())
    f.close()
    print("\n\n ¡Proceso terminado exitosamente!")

#main()
