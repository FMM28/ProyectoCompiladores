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

instrucciones = []
variables = []

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
                    pass
                elif linea[0] == 'read':
                    pass
                elif linea[0] == 'for':
                    pass
                elif linea[0] == 'println':
                    pass
                elif linea[0] == 'end':
                    pass
            else:
                op=0
                for token in linea:                                     #Cuenta cuantos operadores tiene para determinar si
                    if es_operador(token):                              # es operacion o una asignacion de valores
                        op+=1
                if op>1:                                                #Operacion
                    pass
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
                                    else:
                                        error("El valor no es valido",i)
for v in variables:
    print(v.nombre,v.tipo,v.valor)