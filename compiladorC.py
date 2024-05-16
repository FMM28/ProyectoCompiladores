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

instrucciones = {'data':[],'bss':[],'text':[]}          #se van a ir guaradando las intrucciones para al final imprimirlas
variables = []
mensajes = 0

for i,linea in enumerate(lineas):
    # print(i)
    if len(linea)>0:
        if es_id(linea[0]):
            if es_palRes(linea[0]):
                if linea[0] == 'var':               #Declaracion de variables
                    if es_tipo(linea[1]):
                        if len(linea)==4:
                            if agregaVar(variables,linea[1],linea[2]):
                                error(f"La variable '{linea[2]}' ya ha sido declarada previamente",i) 
                        else:
                            for j in range(len(linea)):
                                
                                if linea[j]=='=':
                                    if (linea[j+1]=="'" and linea[j+3]=="'") or (linea[j+1]=='"' and linea[j+3]=='"'):
                                        if esDelTipo(linea[1],linea[j+2]):
                                            if agregaVar(variables,linea[1],linea[j-1],linea[j+2]):
                                                error(f"La variable '{linea[j-1]}' ya ha sido declarada previamente",i)
                                        else:
                                            error("El valor no es valido",i)
                                    elif esDelTipo(linea[1],linea[j+1]):
                                        if agregaVar(variables,linea[1],linea[j-1],linea[j+1]):
                                            error(f"La variable '{linea[j-1]}' ya ha sido declarada previamente",i)
                                    else:
                                        error("El valor no es valido",i)
                    else:
                        error("Falta tipo",i)
                elif linea[0] == 'print':
                    ins,da,mensajes = imprime(linea[2:-2],variables,i,mensajes)
                    instrucciones["text"].extend(ins)
                    instrucciones["data"].extend(da)
                elif linea[0] == 'read':
                    pass
                elif linea[0] == 'for':
                    pass
                elif linea[0] == 'println':
                    pass
                elif linea[0] == 'end':                             #guarda las varaibles resultantes y manda el archivo de salida
                    for var in variables:
                        if var.valor != None:
                            if var.tipo in ['string','char']:
                                instrucciones["data"].append(f'{var.nombre}: .ascii "{var.valor}"')
                            elif var.tipo == 'float':
                                instrucciones["data"].append(f'{var.nombre}: .float {var.valor}')
                            elif var.tipo == 'int':
                                instrucciones["data"].append(f'{var.nombre}: .word {var.valor}')
                        else:
                            instrucciones["bss"].append(f'{var.nombre}: .space 4')

                    salidaEnsablador("ensablador",instrucciones)
            else:
                op=0
                for token in linea:                                     #Cuenta cuantos operadores tiene para determinar si
                    if es_operador(token):                              # es operacion o una asignacion de valores
                        op+=1
                if op>1:                                                #Operacion
                    print(evalua_posfija(convertirInfijaAPostfija(linea[2:-1])))
                else:                                                   #Asigancion de valores
                    for var in variables:
                            if var.nombre == linea[0]:
                                if len(linea)==4:
                                    if esDelTipo(var.tipo,linea[2]) and var.tipo not in ["char","string"]:
                                        var.valor = linea[2]
                                    else:
                                        error("El valor no es valido",i)
                                else:
                                    if esDelTipo(var.tipo,linea[3]):
                                        var.valor = linea[3]
                                    elif es_palRes(linea[2]):               #aqui va la parte de seno,coseno,tangente
                                        pass
                                    else:
                                        error("El valor no es valido",i)
for v in variables:
    print(v.nombre,v.tipo,v.valor)