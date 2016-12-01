#  -*- coding: 850 -*-
# -*- coding: utf-8 -*-

from Tkinter import *

## DEFINICIÓN DE FUNCIONES

#### Funciones principales ####

# Crea la sub-ventana del programa utilizando el módulo Tkinter para
# interfaces gráficas.
# Entrada: String con la expresion booleana y la variable de la ventana principal.
# Salida: Muestra y mantiene activa la sub-ventana.

def subVentana(stringExpresionBooleana, ventanaPrincipal):
    ventanaHija = Toplevel(ventanaPrincipal)
    ventanaHija.geometry ("300x250")
    ventanaHija.title("Mapa de Karnaugh")

    matrizExpresionBooleana, variables = generarMatrizExpresionBooleana(stringExpresionBooleana.get())
    mapaKarnaugh = llenarMapaKarnaugh(matrizExpresionBooleana)

    # print mapa
    if len(variables) == 4:
        mapa1 = str(mapaKarnaugh[0])
        mapa2 = str(mapaKarnaugh[1])
        mapa3 = str(mapaKarnaugh[2])
        mapa4 = str(mapaKarnaugh[3])
        Label(ventanaHija, text = "Mapa de Karnaugh").grid(row=2, column=2)
        Label(ventanaHija, text = mapa1).grid(row=4, column=2)
        Label(ventanaHija, text = mapa2).grid(row=5, column=2)
        Label(ventanaHija, text = mapa3).grid(row=6, column=2)
        Label(ventanaHija, text = mapa4).grid(row=7, column=2) 
    else:
        mapa1 = str(mapaKarnaugh[0])
        mapa2 = str(mapaKarnaugh[1])
        Label(ventanaHija, text = "Mapa de Karnaugh").grid(row=2, column=2)
        Label(ventanaHija, text = mapa1).grid(row=4, column=2)
        Label(ventanaHija, text = mapa2).grid(row=5, column=2) 

    #print expresion
    gruposDe1 = leerMapaKarnaugh(mapaKarnaugh)
    matrizCambioDeEstados = identificarEstados(gruposDe1, len(variables))
    expresionSimplificada = generarExpresionSimplificada(matrizCambioDeEstados, variables)
    Label(ventanaHija, text = "expresion: "+expresionSimplificada).grid(row=8, column=2) 

    ventanaHija.mainloop()

# Genera una matriz con los estados lógicos de cada término de
# la expresión booleana.
# Entrada: Un string de la expresión booleana bien formulada.
# Salida: Una matriz con los estados lógicos de la expresión booleana.

def generarMatrizExpresionBooleana(stringExpresionBooleana):
    stringExpresionBooleana = stringExpresionBooleana.replace(' ','')
    row = []
    matrizExpresionBooleana = []
    guardarVaribles = True
    variables = []
    i = 0
    while i < len(stringExpresionBooleana):
        if i+1 < len(stringExpresionBooleana):
            if stringExpresionBooleana[i+1] == '\'':
                row.append(0)
                i += 2
                if guardarVaribles:
                    variables.append(stringExpresionBooleana[i-2])
            elif stringExpresionBooleana[i] == '+':
                i += 1
                matrizExpresionBooleana.append(row)
                row = []
                guardarVaribles = False
            else:
                row.append(1)
                i += 1
                if guardarVaribles:
                    variables.append(stringExpresionBooleana[i-1])
        else:
            row.append(1)
            i += 1

    matrizExpresionBooleana.append(row)
    return matrizExpresionBooleana, variables

# Genera y llena el mapa de karnaugh.
# Entrada: Matriz expresión booleana.
# Salida: Matriz mapa de karnaugh llena.

def llenarMapaKarnaugh(matrizExpresionBooleana):
    cantidadVariables = len(matrizExpresionBooleana[0])
    matrizMapaKarnaugh = crearMapaKarnaugh(cantidadVariables)
    if cantidadVariables == 2:
        for i in range(len(matrizExpresionBooleana)):

            matrizMapaKarnaugh[matrizExpresionBooleana[i][1]][matrizExpresionBooleana[i][0]] = 1
    elif cantidadVariables == 3:
        for i in range(len(matrizExpresionBooleana)):
            posicionColumna = posicionMapaKarnaugh(matrizExpresionBooleana[i], 'Columna')

            matrizMapaKarnaugh[matrizExpresionBooleana[i][2]][posicionColumna] = 1
    else:
        for i in range(len(matrizExpresionBooleana)):
            posicionColumna = posicionMapaKarnaugh(matrizExpresionBooleana[i], 'Columna')
            posicionFila = posicionMapaKarnaugh(matrizExpresionBooleana[i], 'Fila')

            matrizMapaKarnaugh[posicionFila][posicionColumna] = 1
    return matrizMapaKarnaugh

# Lee el mapa de karnaugh lleno e identifica grupos de unos lógicos.
# Entrada: Matriz mapa karnaugh lleno.
# Salida: Lista con conjuntos de 1s en el mapa.

def leerMapaKarnaugh(matrizMapaKarnaugh):
    gruposDe1 = []
    for i in range(len(matrizMapaKarnaugh)):
        for j in range(len(matrizMapaKarnaugh[i])):
            if matrizMapaKarnaugh[i][j] == 1:
                grupo = {(i,j)}
                grupo = duplicarGrupo(grupo, matrizMapaKarnaugh)
                if grupo not in gruposDe1:
                    gruposDe1.append(grupo)
    return gruposDe1

# Identifica las variables que no cambian de estado en cada conjunto de 1s.
# Entrada: Lista conjunto de 1s y entero con la cantidad de variables del la expresión.
# Salida: Matriz con los cambios de estado de las variables.

def identificarEstados(grupos,cantidadVariables):
    estados = { 0:[0,0], 1:[0,1], 2:[1,1], 3:[1,0] }
    matrizCambioDeEstados = []
    for grupo in grupos:
        terminoBooleano = []
        sumaEstados = [0,0,0,0]
        for posicion in grupo:
            fila = posicion[0]
            columna = posicion[1]
            if cantidadVariables == 2:
                sumaEstados[0] = sumaEstados[0] + columna
                sumaEstados[1] = sumaEstados[1] + fila
            elif cantidadVariables == 3:
                sumaEstados[0] = sumaEstados[0] + estados[columna][0]
                sumaEstados[1] = sumaEstados[1] + estados[columna][1]
                sumaEstados[2] = sumaEstados[2] + fila
            else:
                sumaEstados[0] = sumaEstados[0] + estados[columna][0]
                sumaEstados[1] = sumaEstados[1] + estados[columna][1]
                sumaEstados[2] = sumaEstados[2] + estados[fila][0]
                sumaEstados[3] = sumaEstados[3] + estados[fila][1] 
        for i in range(cantidadVariables):
            if sumaEstados[i] == len(grupo) or sumaEstados[i] == 0:
                terminoBooleano.append(sumaEstados[i]/len(grupo))
            else:
                terminoBooleano.append(2)
        matrizCambioDeEstados.append(terminoBooleano)
    return matrizCambioDeEstados


# Genera el string con la expresión booleana simplificada.
# Entrada: Matriz cambio de estados y lista con los strings que representan las variables.
# Salida: String expresión simplificada.

def generarExpresionSimplificada(matrizCambioDeEstados, variables):
    expresion=""
    for i in range(len(matrizCambioDeEstados)):
        for j in range(len(matrizCambioDeEstados[i])):
            if j==0:  
                if matrizCambioDeEstados[i][j]==1:
                    expresion=expresion + variables[0]
                elif matrizCambioDeEstados[i][j]==0:
                    expresion=expresion + variables[0]+'\''
            elif j==1:
                if matrizCambioDeEstados[i][j] == 1:
                    expresion=expresion + variables[1]
                    
                elif matrizCambioDeEstados[i][j]==0:
                    expresion=expresion + variables[1]+'\''  
            elif j==2:
                if matrizCambioDeEstados[i][j]== 1:
                    expresion=expresion + variables[2]
        
                elif matrizCambioDeEstados[i][j]==0:
                    expresion=expresion + variables[2] +'\''      
            elif j==3:
                if matrizCambioDeEstados[i][j] == 1:
                  expresion=expresion + variables[3]
                 
                elif matrizCambioDeEstados[i][j]==0:
                    expresion=expresion + variables[3]+'\''
        if  i!= (len(matrizCambioDeEstados)-1 ):
            expresion = expresion + " + "    
    return expresion



#### Funciones Auxiliares ####

# Duplica un conjunto de 1s en direcciones adyacentes.
# Entrada: Conjunto con las posiciones de los 1s y matriz mapa karnaugh.
# Salida: Conjunto de 1s más grande posible.

def duplicarGrupo(grupo, matrizMapaKarnaugh):
    puedeDuplicar = True
    nuevaPosicionH = 1
    nuevaPosicionV = 1
    while puedeDuplicar:
        grupo, puedeDuplicar, nuevaPosicionH = duplicarDerecha(grupo, matrizMapaKarnaugh, nuevaPosicionH)
        grupo, puedeDuplicar, nuevaPosicionV = duplicarAbajo(grupo, matrizMapaKarnaugh, nuevaPosicionV)
        grupo, puedeDuplicar, nuevaPosicionH = duplicarIzquerda(grupo, matrizMapaKarnaugh, nuevaPosicionH)
        grupo, puedeDuplicar, nuevaPosicionV = duplicarArriba(grupo, matrizMapaKarnaugh, nuevaPosicionV) 
    return grupo

# Duplica un conjunto de 1s hacia arriba (de manera cíclica).
# Entrada: Conjunto de 1s, matriz mapa karnaugh y entero contador de duplicaciones verticales.
# Salida: Conjunto duplicado (si es posible), booleano (indica si puede seguir duplicandose 
# y entero contador de duplicaciones verticales).

def duplicarArriba(grupo, matrizMapaKarnaugh, nuevaPosicionV):
    nuevoGrupo = set()
    for elemento in grupo:
        fila = elemento[0] - nuevaPosicionV
        columna = elemento[1]
        if fila < 0:
            fila = len(matrizMapaKarnaugh) + fila
            if fila == elemento[0]:
                return grupo, False, nuevaPosicionV
        if matrizMapaKarnaugh[fila][columna] == 1:
            nuevoGrupo.add((fila,columna))
        elif matrizMapaKarnaugh[fila][columna] == 0:
            return grupo, False, nuevaPosicionV
    return (nuevoGrupo | grupo), True, nuevaPosicionV+1

# Duplica un conjunto de 1s hacia abajo (de manera cíclica).
# Entrada: Conjunto de 1s, matriz mapa karnaugh y entero contador de duplicaciones verticales.
# Salida: Conjunto duplicado(si es posible), booleano (indica si puede seguir duplicandose 
# y entero contador de duplicaciones verticales).

def duplicarAbajo(grupo, matrizMapaKarnaugh, nuevaPosicionV):
    nuevoGrupo = set()
    for elemento in grupo:
        fila = elemento[0] + nuevaPosicionV
        columna = elemento[1]
        if fila >= len(matrizMapaKarnaugh):
            fila = (elemento[0]+nuevaPosicionV)%nuevaPosicionV
            if fila == elemento[0]:
                return grupo, False, nuevaPosicionV
        if matrizMapaKarnaugh[fila][columna] == 1:
            nuevoGrupo.add((fila,columna))
        elif matrizMapaKarnaugh[fila][columna] == 0:
            return grupo, False, nuevaPosicionV
    return (nuevoGrupo | grupo), True, (nuevaPosicionV+1)

# Duplica un conjunto de 1s hacia la derecha (de manera cíclica).
# Entrada: Conjunto de 1s, matriz mapa karnaugh y entero contador de duplicaciones horizontales.
# Salida: Conjunto duplicado(si es posible), booleano (indica si puede seguir duplicandose 
# y entero contador de duplicaciones horizontales).

def duplicarDerecha(grupo, matrizMapaKarnaugh, nuevaPosicionH):
    nuevoGrupo = set()
    for elemento in grupo:
        fila = elemento[0]
        columna = elemento[1] + nuevaPosicionH
        if columna >= len(matrizMapaKarnaugh[0]):
            columna = (elemento[1]+nuevaPosicionH)%nuevaPosicionH
            if columna == elemento[1]:
                return grupo, False, nuevaPosicionH
        if matrizMapaKarnaugh[fila][columna] == 1:
            nuevoGrupo.add((fila,columna))
        elif matrizMapaKarnaugh[fila][columna] == 0:
            return grupo, False, nuevaPosicionH
    return (nuevoGrupo | grupo), True, nuevaPosicionH+1

# Duplica un conjunto de 1s hacia la izquerda (de manera cíclica).
# Entrada: Conjunto de 1s, matriz mapa karnaugh y entero contador de duplicaciones horizontales.
# Salida: Conjunto duplicado(si es posible), booleano (indica si puede seguir duplicandose 
# y entero contador de duplicaciones horizontales).

def duplicarIzquerda(grupo, matrizMapaKarnaugh, nuevaPosicionH):
    nuevoGrupo = set()
    for elemento in grupo:
        fila = elemento[0]
        columna = elemento[1] - nuevaPosicionH
        if columna < 0:
            columna = len(matrizMapaKarnaugh[0]) + columna
            if columna == elemento[1]:
                return grupo, False, nuevaPosicionH
        if matrizMapaKarnaugh[fila][columna] == 1:
            nuevoGrupo.add((fila,columna))
        elif matrizMapaKarnaugh[fila][columna] == 0:
            return grupo, False, nuevaPosicionH
    return (nuevoGrupo | grupo), True, nuevaPosicionH+1
    
# Suma los estados lógicos de un término booleano para hallar su ubicaión en el mapa.
# Entrada: Lista término booleano y string (indica si la coordenada es de fila o columna).
# Salida: Entero suma de estados lógicos. 

def posicionMapaKarnaugh(terminoBooleano, filaColumna):
    suma = 0
    if filaColumna == 'Columna':
        suma = terminoBooleano[0] + terminoBooleano[1]
        if terminoBooleano[0] == 1 and terminoBooleano[1] == 0:
            suma = 3
    else:
        suma = terminoBooleano[2] + terminoBooleano[3]
        if terminoBooleano[2] == 1 and terminoBooleano[3] == 0:
            suma = 3
    return suma

# Crea matriz para el mapa de karnaugh, por defecto lleno de 0s.
# Entrada: Entero con la cantidad de variables de la expresión.
# Salida: Matriz mapa de karnaugh, llena de 0s.

def crearMapaKarnaugh(cantidadVariables):
    matrizMapaKarnaugh = []
    row = []
    if cantidadVariables == 2:
        for i in range(2):
            for j in range(2):
                row.append(0)
            matrizMapaKarnaugh.append(row)
            row = []
    elif cantidadVariables == 3:
        for i in range(2):
            for j in range(4):
                row.append(0)
            matrizMapaKarnaugh.append(row)
            row = []
    else:
        for i in range(4):
            for j in range(4):
                row.append(0)
            matrizMapaKarnaugh.append(row)
            row = []
    return matrizMapaKarnaugh
