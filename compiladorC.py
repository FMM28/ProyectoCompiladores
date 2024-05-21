from funcionesCompilador import *

lineas = abrirArchivo()                                     #abre un archivo
lineasTMP = []
for i,linea in enumerate(lineas):                           #lee linea por linea
    a = quita_comentarios(linea)                            #quita comentarios
    if a != '':
        if a[-1] not in [";","{","}"]: 
            error("Falta ';'",i)
    lineasTMP.append(separa_token(a))               #Separa en tokens
lineas = lineasTMP                                          #guarda la lista temporal y despues la elimina
del lineasTMP

# print (lineas)
salida("Sin Comentarios",lineas)

instrucciones = {'data':set(),'bss':set(),'text':[],'funciones':set()}          #se van a ir guaradando las intrucciones para al final imprimirlas
variables = []
mensajes = 0
saltosFor = 0
entraFor = False

try:
    for i,linea in enumerate(lineas):
        # print(i)
        if entraFor:
            if linea[-1]=='}':
                instrucciones["text"].extend(['\taddi x30, x30, 1','\tsw x29, 0(x30)',f'\tj for{saltosFor}',f'\nfinFor{saltosFor}:'])
                entraFor = False
                saltosFor+=1
        if len(linea)>1:
            if es_id(linea[0]):
                if es_palRes(linea[0]):
                    if linea[0] == 'var':               #Declaracion de variables
                        if es_tipo(linea[1]):
                            if len(linea)==4:
                                if agregaVar(variables,linea[1],linea[2]):
                                    error(f"La variable '{linea[2]}' ya ha sido declarada previamente",i) 
                            else:        
                                if linea[3]=='=':
                                    if (linea[4]=="'" and linea[6]=="'") or (linea[4]=='"' and linea[6]=='"'):
                                        if esDelTipo(linea[1],linea[5]):
                                            if agregaVar(variables,linea[1],linea[2],linea[5]):
                                                error(f"La variable '{linea[2]}' ya ha sido declarada previamente",i)
                                        else:
                                            error("El valor no es valido",i)
                                    elif esDelTipo(linea[1],linea[4]):
                                        if agregaVar(variables,linea[1],linea[2],linea[4]):
                                            error(f"La variable '{linea[2]}' ya ha sido declarada previamente",i)
                                    else:
                                        error("El valor no es valido",i)
                        else:
                            error("Falta tipo",i)
                    elif linea[0] == 'print':
                        if linea[1] == "(" and linea[-2] == ")":
                            ins,fu,da,mensajes = imprime(linea[2:-2],variables,i,mensajes)
                            instrucciones["text"].extend(ins)
                            instrucciones['funciones'].update(fu)
                            instrucciones["data"].update(da)
                        else:
                            error("Falta un parentesis",i)
                    elif linea[0] == 'read':
                        if existerVar(variables,linea[2]):
                            if linea[1] == "(" and linea[-2] == ")":
                                instrucciones['text'].extend(["\n\t#Leyendo","\tli a0, 0",f"\tla a1, {linea[2]}","\tli a2, 100","\tli a7, 63","ecall"])
                            else:
                                error("Falta un parentesis",i)
                        else:
                            error(f"La variable {linea[2]} no ha sido declarada",linea)
                    elif linea[0] == 'for':
                        if linea[1]=='(' and linea[-2] == ')':
                            entraFor = True
                            instrucciones["text"].append('\n\t#Ejecutando For')
                            if existerVar(variables,linea[2]):
                                instrucciones["text"].extend([f'\tli t1, {linea[4]}',f'\tla t0, {linea[2]}','\tsw t1, 0(t0)'])
                            else:
                                agregaVar(variables,'int',linea[2],linea[4])
                            instrucciones["text"].extend([f'\tla x29, {linea[2]}','\tlw x30, x29',f'\tli x31, {linea[4]}',f'\nfor{saltosFor}:',f'\tbge x30, x31, finFor{saltosFor}'])
                        else:
                            error("Falta un parentesis",i)
                    elif linea[0] == 'println':
                        pass
                    elif linea[0] == 'end':                             #guarda las varaibles resultantes y manda el archivo de salida
                        for var in variables:
                            if var.valor != None:
                                if var.tipo in ['string','char']:
                                    instrucciones["data"].add(f'{var.nombre}: .ascii "{var.valor}"')
                                elif var.tipo == 'float':
                                    instrucciones["data"].add(f'{var.nombre}: .float {var.valor}')
                                elif var.tipo == 'int':
                                    instrucciones["data"].add(f'{var.nombre}: .word {var.valor}')
                            else:
                                instrucciones["bss"].add(f'{var.nombre}: .space 4')
                        instrucciones["text"].extend(['\n\t# Salida del programa','\tli a7, 93','\tli a0, 0','\tecall'])

                        salidaEnsablador("ensablador",instrucciones)

                elif existerVar(variables,linea[0]):
                    op=0
                    for token in linea:                                     #Cuenta cuantos operadores tiene para determinar si
                        if es_operador(token):                              # es operacion o una asignacion de valores
                            op+=1
                    if op>1:                                                #Operacion
                        for c in linea[2:-1]:
                            if es_id(c):
                                if not existerVar(variables,c):
                                    error(f"La variable {c} no ha sido declarada",i)
                        ins,bs,fun = opera(evalua_posfija(convertirInfijaAPostfija(linea[2:-1])),linea[0])
                        instrucciones["text"].extend(ins)
                        instrucciones["bss"].update(bs)
                        instrucciones["funciones"].update(fun)
                    else:                                                   #Asigancion de valores
                        for var in variables:
                            if var.nombre == linea[0]:
                                if len(linea)==4:
                                    if esDelTipo(var.tipo,linea[2]) and var.tipo not in ["char","string"]:
                                        instrucciones["text"].extend([f'\n\t# Se actualiza la variable {var.nombre}',f'\tli t0 {linea[2]}',f'\tla t1 {var.nombre}','\tsw t0, 0(t1)'])
                                    else:
                                        error("El valor no es valido",i)
                                else:
                                    if es_palRes(linea[2]):               #aqui va la parte de seno,coseno,tangente
                                        pass
                                    elif esDelTipo(var.tipo,linea[3]):
                                        instrucciones['funciones'].add('copiaCadena')
                                        instrucciones['data'].add(f'mensaje{mensajes}: .ascii "{linea[3]}"')
                                        instrucciones['text'].extend([f'\n\t# Se actualiza la variable {var.nombre}',f'\tla t0, mensaje{mensajes}',f'\tla t1, {var.nombre}','\tjal ra, copiar_cadena'])
                                        mensajes+=1
                                    else:
                                        error("El valor no es valido",i)
                                break
                else:
                    error(f"'{linea[0]}' no es una palabra reservada o variable",i)
except:
    error("Sintaxis incorrecta",i)
# for v in variables:
#     print(v.nombre,v.tipo,v.valor)
print("El programa se ha compilado exitosamente")