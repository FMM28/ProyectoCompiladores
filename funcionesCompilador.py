import string
import sys
import tkinter as tk
from tkinter import filedialog

try:
    from PyQt5.QtWidgets import QApplication, QFileDialog       #pip install PyQt5
except:
    pass

# Funciones para contruir el compilador, funcionara como una libreria para importar las funciones  
# y que la logica sea mas facil de entender

class Variable:
    def __init__(self,tipo,nombre,valor) -> None:
        self.tipo = tipo
        self.nombre = nombre
        self.valor = valor

def abrirArchivo():
    lineas = []
    try:
        ventana = QApplication(sys.argv)
        nombre_archivo, _ = QFileDialog.getOpenFileName(None, "Seleccionar archivo")
    except:
        root = tk.Tk()
        root.withdraw()
        nombre_archivo = filedialog.askopenfilename()
    try:
        with open(nombre_archivo, 'r') as archivo:
            for linea in archivo:
                lineas.append(linea.strip())  
    except FileNotFoundError:
        print(f"El archivo '{nombre_archivo}' no fue encontrado.")
    return lineas

def quita_comentarios(cad):
    cad2=""
    estado="z"
    for c in cad:
        if estado=='z':
            if c=='/':
                estado='a'
            else:
                cad2+=c
        elif estado=='a':
            if c=='*':
                estado='b'
            else:
                estado='z'
                cad2+='/'+c
        elif estado=='b':
            if c=='*':
                estado=='c'
        elif estado=='c':
            if c=='/':
                estado='z'
            else:
                estado='b'
    
    return cad2

def es_separador(c):
    return c==' ' or c=='\t' or c=='\n'

def es_simEsp(c):
    return c in string.punctuation

def separa_token(cad):
    lista = []
    dentro=False
    token=''
    for c in cad:
        if dentro:
            if es_separador(c) or es_simEsp(c):
                lista.append(token)
                token=''
                dentro=False
                if es_simEsp(c):
                    lista.append(c)
            else:
                token+=c
        else:
            if es_simEsp(c):
                lista.append(c)
            elif not(es_separador(c)):
                dentro=True
                token=c
    return lista

def es_id(cad):
    return cad[0] in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_'

def es_palRes(cad):
    return cad in [
        "var", "string", "int", "float", "char", "read", "print", "println", "for", "sin", "cos", "tan", "end"
    ]

def es_tipo(cad):
    return cad in ["string", "int", "float", "char"]

def es_operador(cad):
    return cad in [
        '+', '-', '*', '/', '%', '='
    ]

def es_numero(cad):
    cad=str(cad)
    cad2=''
    estado='z'
    for c in cad:
        if estado=='z':
            if c in string.digits:
                cad2+=str(c)
                estado='a'
            else:
                return False
        if estado=='a':
            if c in string.digits:
                cad2+=str(c)
            elif c == '.':
                cad2+=c
            elif c=='e':
                cad2+=c
            else:
                return False
    return True

def obtenerPrioridadOperador(o):
    # Función que trabaja con convertirInfijaA**.
    return {'(':1, ')':2, '+': 3, '-': 3, '*': 4, '/':4, '^':5}.get(o)

def obtenerListaInfija(cadena_infija):
    '''Devuelve una cadena en notación infija dividida por sus elementos.'''
    infija = []
    cad = ''
    for i in cadena_infija:
       if i in['+', '-', '*', '/', '(', ')', '^']:
           if cad != '':
               infija.append(cad)
               cad = ''
           infija.append(i)
       elif i == chr(32): # Si es un espacio.
           cad = cad
       else:
           cad += i
    if cad != '':
       infija.append(cad)
    return infija


def convertirInfijaAPostfija(expresion_infija):
    '''Convierte una expresión infija a una posfija, devolviendo una lista.'''
    infija = obtenerListaInfija(expresion_infija)
    pila = []
    salida = []
    for e in infija:
        if e == '(':
            pila.append(e)
        elif e == ')':
            while pila[len(pila) - 1 ] != '(':
                salida.append(pila.pop())
            pila.pop()
        elif e in ['+', '-', '*', '/', '^']:
            while (len(pila) != 0) and (obtenerPrioridadOperador(e)) <= obtenerPrioridadOperador(pila[len(pila) - 1]):
                salida.append(pila.pop())
            pila.append(e)
        else:
            salida.append(e)
    while len(pila) != 0:
        salida.append(pila.pop())
    return salida

def evalua_posfija(posfija):
    pila=[]
    cod_int=[]
    cont = 1
    for e in posfija:
        if es_operador(e):
            op2 = pila.pop()
            op1 = pila.pop()
            if e=='+':
                resultado = 't'+str(cont) + "=" + op1 +'+' + op2 + ';'
            elif e=='-':
                resultado = 't'+str(cont) + "=" + op1 +'-' + op2 + ';'
            elif e=='/':
                resultado = 't'+str(cont) + "=" + op1 +'/' + op2 + ';'
            elif e=='*':
                resultado = 't'+str(cont) + "=" + op1 +'*' + op2 + ';'
            pila.append('t'+str(cont))
            cod_int.append(resultado)
            cont+=1
        else:
            pila.append(e)
    return cod_int

def error(mensaje,linea):
    print(f"Error en la linea {(linea+1)}:",mensaje)
    exit()

def agregaVar(lista,tipo,nombre,valor=None):
    if existerVar(lista,nombre):
        return True
    lista.append(Variable(tipo,nombre,valor))

def existerVar(lista,nombre):
    for var in lista:
        if var.nombre == nombre:
            return True
    return False

def esDelTipo(tipo,valor):
    try:
        if tipo=='int':
            int(valor)
        elif tipo=='float':
            float(valor)
        elif tipo=='char':
            if len(valor)>1:
                return False
    except:
        return False
    return True

def imprime(datos,listaVariables,linea,mensajes):
    instrucciones = ["\n\t#Imprimiendo"]
    funciones = {'copiaCadena','obtenerLongitud'}
    data = ["mensaje_concatenado: .space 20"]
    estado = 'a'
    tmp=''
    for dato in datos:
        if estado == 'a':
            if dato == '"' or dato == "'":
                estado = 'b'
            else:
                if dato == ',':
                    data.append('espacio: .ascii " "')
                    instrucciones.extend(["\tla t0, espacio","\tla t1, mensaje_concatenado","\tjal ra, copiar_cadena","\tla t0, espacio","\tjal ra, obtener_longitud","\tadd t1, t1, t3"])
                else:
                    if existerVar(listaVariables,dato):
                        for var in listaVariables:
                            if var.nombre == dato:
                                instrucciones.extend([f"\tla t0, {dato}","\tla t1, mensaje_concatenado","\tjal ra, copiar_cadena",f"\tla t0, {dato}","\tjal ra, obtener_longitud","\tadd t1, t1, t3"])
                                break
                    else:
                        error(f"La variable {dato} no ha sido declarada",linea)
        elif estado == 'b':
            if dato== '"' or dato == "'":
                data.append(f'mensaje{mensajes}: .ascii "{tmp}"')
                instrucciones.extend([f"\tla t0, mensaje{mensajes}","\tla t1, mensaje_concatenado","\tjal ra, copiar_cadena",f"\tla t0, mensaje{mensajes}","\tjal ra, obtener_longitud","\tadd t1, t1, t3"])
                mensajes+=1
                estado = 'a'
            else:
                tmp = dato
    instrucciones.extend(["\tli a0, 1","\tla a1, mensaje_concatenado","\tjal ra, obtener_longitud","\tmv a2, a1","\tli a7, 64","\tecall"])
    
    return instrucciones,funciones,data,mensajes

def salida(nombre,datos):
        
        with open(nombre+'.txt', 'w') as archivo:
            for lista in datos:
                linea = ' '.join(elemento for elemento in lista) + '\n'
                archivo.write(linea)

def salidaEnsablador(nombre,datos):
    with open(nombre+'.txt','w') as archivo:
        archivo.write(".data\n")
        for linea in datos["data"]:
            archivo.write(linea+'\n')

        archivo.write("\n.bss\n")
        for linea in datos["bss"]:
            archivo.write(linea+'\n')

        archivo.write("\n.text\n.global _start\n\n_start:\n")
        for linea in datos["text"]:
            archivo.write(linea+'\n')

        archivo.write("\n#Funciones utilizadas")
        for linea in datos['funciones']:
            if linea == 'copiaCadena':
                archivo.write('\n\ncopiar_cadena:\n\tcopiar_loop:\n\t\tlb t2, 0(t0)\n\t\tsb t2, 0(t1)\n\t\taddi t0, t0, 1\n\t\taddi t1, t1, 1\n\t\tbnez t2, copiar_loop\n\tret')
            elif linea == 'obtenerLongitud':
                archivo.write('\n\nobtener_longitud:\n\tlongitud_loop:\n\t\tlb t2, 0(t0)\n\t\tbeqz t2, longitud_fin\n\t\taddi t0, t0, 1\n\t\taddi t3, t3, 1\n\t\tj longitud_loop\n\tlongitud_fin:\n\tret')