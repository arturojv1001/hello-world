from Clases_Contagios_2 import Contagios
#from Clases_Epidemia import Epidemia
from Mis_Funciones_NUEVO3 import Modelos
from Mis_Funciones_NUEVO3 import Medidas
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import statistics
import time
import pandas as pd

##########################################################################################
########################################################################################## 
####################### Inicializamos parametros  ########################################

N    = 15                 # numero de nodos del grafo 
t    = 30                  # cantidad de periodos de contagio que vamos a simular
p_i  = 0.2                # probabilidad de infeccion
p_r  = 0.4                 # probabilidad de recuperacion
p_m  = 0.5               # probabilidad de muerte
contagios_iniciales = 1   # numero de contagios iniciales
periodos_recuperacion = 5  # numero de periodos minimos para la recuperacion
periodos_m = 7
periodos_inmune = 2
incubacion = 4
steps = t     # el numero de pasos es igual al numero de periodos de contagio

G    = nx.erdos_renyi_graph(N,0.2)    # definimos el grafo
pos  = nx.circular_layout(G)          # definimos la posicion para la animacion
cntgs  = Contagios(N,steps)           # mandamos a llamar la clase de funciones de contagios
#Epi    = Epidemia(N,steps)
Med    = Medidas(N,steps)

Infectados_Iniciales,Suceptibles_Iniciales,path = cntgs.Infectados_Iniciales(G,contagios_iniciales)  # Inicializamos los contagios

Infectados_Totales  = Infectados_Iniciales    # Inicializamos los Infectados Totales antes del primer periodo de contagios
Suceptibles_Totales = Suceptibles_Iniciales   # Inicializamos los Suceptibles Totales
INFECTADOS = [Infectados_Iniciales]           # Inicializamos un vector en el que guardamos los infectados  en cada periodo de tiempo
SUCEPTIBLES = [Suceptibles_Iniciales]         # Inicializamos un vector en el que guardamos los suceptibles  en cada periodo de tiempo
RECUPERADOS = []        # Inicializamos un vector de recuperados generales, con todos los recuperados en cada periodo de tiempo
ENLACES     = []        # Inicializamos un vector de enlaces que representan los contagios en el tiempo t
MUERTES     = []
Muertes_Totales     = []

##########################################################################################
########################################################################################## 
####################### Simulacion de Contagios  ########################################


#RECUPERADOS, Suceptibles_Totales, SUCEPTIBLES, Infectados_Totales, path, Recuperados_Totales,  Muertes_Totales, INFECTADOS, ENLACES = Epi.Simulacion_Epidemia(t, RECUPERADOS, periodos_inmune, Suceptibles_Totales, SUCEPTIBLES, Infectados_Totales, G, p_i, path,  Muertes_Totales, INFECTADOS, incubacion, ENLACES, p_r, periodos_recuperacion, p_m, periodos_m, MUERTES)


Grados_de_Nodo = []
Coeficientes_Agrupamiento = []
Promedio_Caminos_Cortos = []
aux = []
for node in G.nodes():
    Promedio_Caminos_Cortos.append( Med.Promedio_Caminos_Single(G,node) )
    Coeficientes_Agrupamiento.append( nx.clustering(G, node) )
    Grados_de_Nodo.append( G.degree(node) ) 
    
    if node in Suceptibles_Totales:
        aux.append("0")
    elif node in Infectados_Totales:
        aux.append("1")
        
'''   
print( Grados_de_Nodo )
print("\n")
print( Coeficientes_Agrupamiento )
print("\n")
print( Promedio_Caminos_Cortos )
print("\n")
'''
claves = ["nodo_"+str(i) for i in range(1,len(Grados_de_Nodo)+1)]

df = pd.DataFrame( [claves, Grados_de_Nodo, Coeficientes_Agrupamiento, Promedio_Caminos_Cortos ]).transpose()
df.columns = [ "nodo", "grado_nodo", " coef_agr","caminos_cortos"]
master = df.copy()
#print(df)

temp = pd.DataFrame([claves,aux]).transpose()
temp.columns = ["nodo","estado_0"]
master = master.merge(temp,how="outer",on="nodo")






for i in range(0,t):
    
    
    Suceptibles_Totales = cntgs.Inmunes(RECUPERADOS,i,periodos_inmune,Suceptibles_Totales)
    SUCEPTIBLES.append(Suceptibles_Totales)
    
    Recuperados_Totales = []
    if i>=periodos_inmune:
        for r in range(0,periodos_inmune):
            for K in RECUPERADOS[i-r-1]:
                Recuperados_Totales.append(K)
    
    # en cada iteracion, obtenemos:
    #   *el numero de infectados en el tiempo i
    #   *el numero de suceptibles al terminar el tiempo i
    #   *una linea de contagio del primer nodo infectado
    #   *la lista de enlaces/contagios que se dieron en el tiempo i
    Infectados_i, Suceptibles_i, path, Enlaces_t = cntgs.Contagio_en_un_tiempo3(Infectados_Totales,Suceptibles_Totales,G,p_i,path,Recuperados_Totales,Muertes_Totales,INFECTADOS,i,incubacion)
    
    ENLACES.append(Enlaces_t)  # actualizamos el vector de enlaces/contagios 
    
    
    
    Recuperados = []    # en cada iteracion generamos un arreglo para guardar los recuperados en el tiempo i
    Recuperados = cntgs.Recuperacion_t(INFECTADOS,i,p_r,periodos_recuperacion,RECUPERADOS,Muertes_Totales) 
    
    RECUPERADOS.append(Recuperados)      # guardamos los recuperados del tiempo i en el arreglo de recuperados generales


    Infectados_Totales  = (Infectados_i)              # Actualizamos la lista de infectados totales al finalizar el tiempo i
    Infectados_Totales = list(set(Infectados_Totales)-set(Recuperados))  # a la lista de infectados totales al finalizar el tiempo i
                                                                         # le quitamos aquellos nodos que se recuperan en ese periodo
    Suceptibles_Totales = (Suceptibles_i) #+ Recuperados   # agregamos los recuperados a la lista de suceptibles
    INFECTADOS.append(Infectados_Totales)                 # agregamos los infectados totales del tiempo i al vector de infectados en cada periodo
   
    
    muertes_i = cntgs.Muertes(INFECTADOS,i,p_m,periodos_m,Infectados_Totales,Recuperados)
    Muertes_Totales = Muertes_Totales + muertes_i
    MUERTES.append(Muertes_Totales)
    Infectados_Totales = list(set(Infectados_Totales)-set(MUERTES[i]))

    aux = []
    for nodo in G.nodes():
        if nodo in Suceptibles_Totales:
            aux.append("0")
        elif nodo in Infectados_Totales:
            aux.append("1")
        elif nodo in (Recuperados_Totales or Recuperados):
            aux.append("2")
        elif nodo in Muertes_Totales:
            aux.append("3")
        else: aux.append("-1")
        
    temp = pd.DataFrame([claves,aux]).transpose()
    temp.columns = ["nodo","estado_"+str(i+1)]
    master = master.merge(temp,how="outer",on="nodo")
    

#print(master)
master.to_csv("OUTPUT.csv")
num_inf = []
T = []
for i in range(len(INFECTADOS)):
    num_inf.append(len(INFECTADOS[i]))
    T.append(i)

plt.figure()
plt.plot(T,num_inf)
plt.title('Numero de Infectados a traves del Tiempo' )
plt.xlabel('tiempo')
plt.ylabel('Numero de Infectados')
plt.show()


'''
Grados_de_Nodo = []
Coeficientes_Agrupamiento = []
Promedio_Caminos_Cortos = []
for node in G.nodes():
    Promedio_Caminos_Cortos.append( Med.Promedio_Caminos_Single(G,node) )
    Coeficientes_Agrupamiento.append( nx.clustering(G, node) )
    Grados_de_Nodo.append( G.degree(node) ) 
    
print( Grados_de_Nodo )
print("\n")
print( Coeficientes_Agrupamiento )
print("\n")
print( Promedio_Caminos_Cortos )
print("\n")

claves = ["nodo_"+str(i) for i in range(1,len(Grados_de_Nodo)+1)]

df = pd.DataFrame( [claves, Grados_de_Nodo, Coeficientes_Agrupamiento, Promedio_Caminos_Cortos ]).transpose()
df.columns = [ "nodo", "grado_nodo", " coef_agr","caminos_cortos"]

print(df)
'''       
