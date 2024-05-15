import string
from PyQt5.QtWidgets import QApplication, QFileDialog       #pip install PyQt5
import sys

# Funciones para contruir el compilador, funcionara como una libreria para importar las funciones  
# y que la logica sea mas facil de entender

class Variable:
    def __init__(self,tipo,nombre,valor) -> None:
        self.tipo = tipo
        self.nombre = nombre
        self.valor = valor

def abrirArchivo():
    lineas = []
    ventana = QApplication(sys.argv)
    nombre_archivo, _ = QFileDialog.getOpenFileName(None, "Seleccionar archivo")
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
    for var in lista:
        if var.nombre == nombre:
            return True
    lista.append(Variable(tipo,nombre,valor))

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

def salida(nombre,datos):
        
        with open(nombre+'.txt', 'w') as archivo:
            for lista in datos:
                linea = ' '.join(elemento for elemento in lista) + '\n'
                archivo.write(linea)