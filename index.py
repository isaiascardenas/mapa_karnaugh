# -*- coding: 850 -*-
# -*- coding: utf-8 -*-

# Descripción: El programa, a partir de una expresión booleana bien
# formulada, genera la expresión simplificada 
# utilizando el mapa de karnaugh.

# Autores:
# Isaías Cárdenas
# Neldy Montecinos
# Sebastián Fuentes
# Ignacio Gavilán
# Álvaro Saavedra
# José Herrera
# Versión 0.1 ~ Fecha: 21/10/16
#--------------------------------------------------------------

# IMPORTACIÓN

from Tkinter import Tk, Label, StringVar, Entry, Button
from functions import subVentana

# ###############   Main  ###############################

ventana = Tk()
ventana.title ('Team Karnaugh')
ventana.geometry ("300x210")
ventana.maxsize(280,210)
 
expresion = Label(ventana, text = "1) Ingresa la expresion booleana y presiona enter").grid(row = 1, column = 1)
expresion2 = Label(ventana, text = "Ej: A'BC'+ ABC + A'BC + A'B'C'", fg = 'red', font = "Times 11" ).grid(row = 7, column=1)
expresion3 = Label(ventana, text = "2) Presiona el boton 'DALE' ").grid(row = 12, column = 1)

text = StringVar()
entry = Entry(ventana, textvariable=text).grid(row=3, column=1)

Button(ventana,text="DALE", command=lambda: subVentana(text, ventana)).grid(row=13,column=1)

ventana.mainloop()
