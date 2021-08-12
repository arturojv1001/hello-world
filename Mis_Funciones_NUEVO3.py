 # -*- coding: utf-8 -*-
'''
EJEMPLO DE COMO HACER CLASES Y OBJETOS
FECHA: 18 DE ENERO DEL 2021
'''

# Importamos los paquetes que usaremos

import os, shutil, glob
import networkx as nx 
#import matplotlib.pyplot as plt 
import random as rd 
import numpy as np
#from numpy import linalg as LA
#import statistics
import pandas as pd
import random


###################################################################################
############################# Clase para definir diferentes grafos ################



# Formato básico para contruir una clase
class Modelos:

    def __init__(self,N,p,vecinos,m,n_inicial,enlaces_nuevo_nodo,nodos_anadidos):  #inicializamos el self, con parametros globales
        self.N = N #numero de nodos
        self.p = p #probabilidad 
        self.vecinos = vecinos
        self.m = m #numero de enlaces   (para grafos dado un numero de enlaces)
        self.n_inicial = n_inicial
        self.enlaces_nuevo_nodo = enlaces_nuevo_nodo
        self.nodos_anadidos = nodos_anadidos
        return

    # Ponemos todas las funciones que definen a este objeto llamado Modelos
    
    def Barabasi_Albert(self):
# n_inicial es un entero que representa el numero de nodos con los que queremos iniciar antes de agregar los demas nodos
# enlaces_nuevo es un entero que representa el numero de enlaces que se agregaran al nuevo nodo cuando aparezca
# nodos_anadidos es un entero que representa el numero de nodos que se agregan al numero de nodos incial
# NOTA: el numero de nodos total del grafo es igual a n_inicial+nodos_anadidos
    
    ####### se crea un grafo regular (todos conectados con todos) ###########################################################
        A = np.zeros((self.n_inicial,self.n_inicial)) # se crea una matriz de 0´s de tamano n_inicial
        V = int(self.n_inicial/2)  # el numero de vecinos que tendra cada nodo (para que todos esten conectados) 
            
        for i in range(0,self.n_inicial):      # ciclo que recorre todas las filas de la matriz de ceros
            for j in range(i+1,i+V+1):    # ciclo que recorre las diagonales a la derecha de la diagonal principal
                i,j = i,j%self.n_inicial       # se toman los modulos para que (i,j) no se salgan de rango de la matriz
                A[i][j] = A[j][i] = 1     # se vuelven 1 las entradas de la matriz para conectar los nodos i,j
        
        if self.enlaces_nuevo_nodo > len(A):   # si el numero de enlaces_nuevo_nodo es mayor que la cantidad de nodos inicial
            self.enlaces_nuevo_nodo = len(A)   # la cantidad de nodos de cada nuevo enlace sera igual que la cantidad de nodos incial
    
    ### ciclo para agregar el nodo correspondiente y agregar los enlaces al nuevo nodo##########################################
        for w in range(0,self.nodos_anadidos):
            caja = []                     # se crea un arreglo vacio
            N = len(A)                    # N es el tamano de la matriz actual, es decir la cantidad de nodos del grafo actual
        ### ciclo para crear el arreglo o "caja" donde iran los nodos dependiendo de su grado ###
            for h in range(0,N):                # se crea un ciclo que recorre todas las filas de la matriz (recorre los nodos)
                temp = A[h,:]                   # se guarda la fila correspondiente a la iteracion respectiva 'h'
                grado_nodo_h = int(sum(temp))   # se obtiene la suma de esta fila, que representa el grado de nodo del 'nodo_h'
    #el grado del nodo es igual a la suma de los elementos de su respectiva fila de la matriz ya que cada enlace se representa por 1
                for c in range(0,grado_nodo_h):    # se hace un ciclo de la longitud del grado del nodo de la respectiva iteracion
                    caja.append(h)                 # en cada iteracion se agrega el numero del nodo en el arreglo "caja"
            nueva_columna = np.zeros(N)         # se crea una columna de 0´s del tamano de la dimension de la matriz actual 
            A = np.hstack((A, np.atleast_2d(nueva_columna).T))  # se anade la nueva columna a la matriz 
                                                                # ( se obtiene una matriz de N*(N+1) )
            nueva_fila = np.zeros(N+1)          # se crea una fila de 0´s del tamano (N+1)
            A = np.vstack ((A, nueva_fila) )    # se anade la nueva fila a la matriz 
                                                # ( se obtiene una matriz de (N+1)*(N+1) )
            
            grado_nuevo_nodo = 0                              # inicializamos el grado del nuevo nodo como 0
        ### mientras el grado de nodo del nuevo nodo sea menor a 'enlaces_nuevo_nodo' se repite el ciclo
            while grado_nuevo_nodo < self.enlaces_nuevo_nodo:
                nodo_extremo = random.choice(caja)            # se elige un nodo del arreglo 'caja' al azar
    # la probabilidad de que el nodo a elegir sea el nodo_i es igual al tamano del arreglo 'caja' entre las veces que aparece el nodo_i
    # en otras palabras p_i = suma(grados de todos los nodos)/(grado del nodo_i) 
                A[N][nodo_extremo] = A[nodo_extremo][N] =1    # se agrega un enlace entre el nuevo nodo y el nodo elegido al azar 
                grado_nuevo_nodo = sum(A[N][:])       # se suma 1 al grado del nuevo nodo 
        G1 = nx.from_numpy_matrix(A)                      # se obtiene el grafo a partir de la matriz con networkx
        return G1     # la funcion regresa el grafo creado (grafo Barabasi_Albert)
    
    
    
    def WATTS_STROGATZ(self):
# - N es un numero entero que representa la cantidad de nodos del grafo 
# - vecinos es un numero entero (par) que representa la cantidad total de vecinos que tiene cada nodo inicialmente
#   es decir, se tienen (vecinos/2) de cada lado
# - p es la probabilidad de reconectar cada enlace

        B = np.zeros((self.N,self.N))       # creamos una matriz de tamano N de ceros
        if self.vecinos > self.N:           # si el numero de vecinos ingresado es mayor a N
            V = int((self.N)/2)        # se asigna automaticamente el valor entero de N/2 a V
        else: 
            V = int(self.vecinos/2)    # V representa la cantidad de vecinos de cada lado del nodo
            
        for i in range(0,self.N):              # hacemos un ciclo que recorre cada fila de la matriz
            for j in range(i+1,i+V+1):    # hacemos otro ciclo que recorre las diagonales a ala derecha de la matriz principal
                i,j = i,j % self.N                # tomamos el modulo de los subindices para que no se salga del rango de la matriz
                B[i][j] = B[j][i] = 1        # creamos el enlace en esa entrada y en la entrada respectiva para que sea simetrica 
    ####################################################################################################3
    
    ###################################################################################################
    
        for i in range(0,self.N):             # hacemos un ciclo que recorre cada fila de la matriz
            for j in range(i+1,i+V+1):   # hacemos otro ciclo que recorre las diagonales a ala derecha de la matriz principal
                i,j = i,j%self.N                  # tomamos el modulo de los subindices para que no se salga del rango de la matriz
                temp = B[i,:]                # tomamos la fila de la iteracion respectiva de la matriz
                r = np.random.uniform(0,1)   # calculamos un numero aleatoriamente entre 0 y 1
                if r<self.p:                      # preguntar si r<p es equivalente a tomar la probabilidad de p para reconectar enlaces
                    donde_ceros = np.where(temp==0)[0]   # dentro de esa fila, creamos un arreglo con los subindices de las entradas
                                                         # que tengan un 0, es decir en las que no hay enlaces
                    donde_ceros = np.delete(donde_ceros,np.where(donde_ceros==i)[0])   # a ese arreglo, le quitamos el subindice de la diagonal
                    if len(donde_ceros)==0:  # si el arreglo que creamos es vacio, significa que ese nodo esta conectado con todos los demas nodos
                        break                # por lo que no podemos conectaro con otro nodo y nos salimos del ciclo para recorrer otra fila
                    nuevo_j = random.choice(donde_ceros) # si el arreglo no es vacio, elegimos un subindice que tenga un 0 de forma aleatoria
                    B[nuevo_j][i] = B[i][nuevo_j] = 1    # creamos un enlace entre el nodo_i y el nodo elegido aleatoriamente para reconectar
                    B[i][j] = B[j][i] = 0                # el enlace original es desconectado
                
        G = nx.from_numpy_matrix(B)     # convertimos la matriz en un grafo por medio de networkx
        return G            # la funcion regresa el grafo G despues de reconectar sus enlaces
    
    
    def WATTS_STROGATZ_NEWMAN(self):
        B = np.zeros((self.N,self.N))       # creamos una matriz de tamano N de ceros
        if self.vecinos > self.N:           # si el numero de vecinos ingresado es mayor a N
            V = int((self.N)/2)        # se asigna automaticamente el valor entero de N/2 a V
        else: 
            V = int(self.vecinos/2)    # V representa la cantidad de vecinos de cada lado del nodo
            
        for i in range(0,self.N):              # hacemos un ciclo que recorre cada fila de la matriz
            for j in range(i+1,i+V+1):    # hacemos otro ciclo que recorre las diagonales a ala derecha de la matriz principal
                i,j = i,j % self.N                # tomamos el modulo de los subindices para que no se salga del rango de la matriz
                B[i][j] = B[j][i] = 1        # creamos el enlace en esa entrada y en la entrada respectiva para que sea simetrica 
###################################################################################################
    
###################################################################################################
    
        for i in range(self.N):        # hacemos un ciclo que recorre todas las filas de la matriz
            for j in range(i+1,self.N):   # hacemos un ciclo que recorre lo elementos arriba de la diagonal principal de la matriz
                
                if B[i][j] == 0:            # si no hay un enlace entre los nodos i,j 
                    r = np.random.uniform(0,1)   # calculamos un numero aleatoriamente entre 0 y 1
                    if r<self.p:                      # preguntamos si es menor a nuestra probabilidad
                        B[j][i] = B[i][j] = 1       # en caso de que la probabilidad se cumpla, se une el enlace i,j
        G = nx.from_numpy_matrix(B)   # convertimos la matriz en un grafo
        return G
    
    
    def G_P(self): #genera un grafo dado un numero de nodos y la probabilidad de que haya un enlace entre sus nodos
    
        A = np.zeros((self.N,self.N))   # matriz de ceros de tamano nxn que tomaremos como la matriz adjunta de nuestro grafo

        for i in range(self.N):              # doble ciclo para recorrer la parte triangular superior de la matriz adjunta
            for j in range (i+1,self.N):     # (tampoco recorremos ningun elemento de la diagonal, ya que los dejaremos en 0 siempre)   
                r = np.random.uniform(0,1)  # calculamos un numero aleatoriamente entre 0 y 1

                if r<(self.p):         # preguntar si r<p es equivalente a tomar la probabilidad de p para unir nodos
                    A[i,j] = A[j,i] = 1  # unimos los nodos respectivos de la parte triangular superior de la matriz
                      # como la matriz es simetrica, igualamos la otra entrada respectiva de la matriz 

        G = nx.from_numpy_matrix(A) # convertimos la matriz adjunta en el grafo GP
        return G
    
    

    def G_E(self): #genera un grafo dados su numero de nodos y enlaces
        A = np.zeros((self.N,self.N))   # matriz de ceros de tamano nxn que tomaremos como la matriz adjunta de nuestro grafo

        enlaces_totales = self.N*(self.N-1)/2  #calculamos el numero de enlaces to3tales
    
        if self.m > enlaces_totales:  #si el numero de enlaces que queremos es mayor al numero de enlaces posibles 
            self.m = int(enlaces_totales/2)      # entonces automaticamente nuestro grafo tendra la mitad del numero de enlaces posibles
    
        enlaces = 0  # inicializamos el numero de enlaces como 0 
    
        while enlaces < self.m:   # mientras el numero de enlaces sea menor que el numero de enlaces que queremos que tenga la grafica
            i = np.random.randint(0,self.N)  # seleccionamos un nodo del grafo aleatoriamente
            temp = A[i][:]              # tomamos toda la fila correspondiente a 'nodo_i' 
    
            donde_ceros = np.where(temp==0)[0]         # creamos un arreglo con los subindices de las entradas que tienen 0
            donde_ceros = np.delete(donde_ceros,np.where(donde_ceros==i)[0])  # quitamos la entrada de la diagonal
            
            if len(donde_ceros)==0:  # si el arreglo de subindices de ceros es vacio, significa que ese nodo ya tiene N-1 enlaces
                enlaces = enlaces    # no agregamos valor al contador de enlaces
            else:
                nuevo_j = random.choice(donde_ceros)  # si el arreglo de subindices de ceros no es vacio, elegimos uno al azar
                enlaces = enlaces + 1                 # agregamos 1 al contador de enlaces
                A[nuevo_j][i] = A[i][nuevo_j] = 1     # unimos con un enlace el nodo_i y el nuevo nodo elegido aletoriamente
        G = nx.from_numpy_matrix(A)    # obtenemos el grafo correspondiente a nuestra matriz
        return G
    

    def Todos_los_Modelos(self,Nombre_del_Modelo):
        #También se puede llamar a las funciones que hemos creado en el objeto Modelos (con "self")
        if Nombre_del_Modelo == 'Erdos-Renyi':
            return self.ER()

        if Nombre_del_Modelo == 'NWS':
            return self.NWS()
        
        if Nombre_del_Modelo =='Grafo-Probabilidad':
            return self.G_P()
        
        if Nombre_del_Modelo =='Grafo-Enlaces':
            return self.G_E()




###################################################################################################################
############################# Clase para guardar medidas del grafo ###############################################



class Medidas(Modelos,):  #clase que hereda las funciones de la clase Modelos
    
    def __init__(self,N,p): #no hereda los parametros globales de Modelos,
        self.N = N          # por lo que los volvemos a inicializar
        self.p = p 
        return
    
    
    def promedio_caminos_cortos2(self,G): #funcion para encontrar el promedio de los caminos mas cortos entre los nodos de un grafo G
        #Nodos = G.number_of_nodes()  #Nodos es el numero de nodos del grafo
        #Nodos = self.N
        if nx.is_connected(G): #si todos los nodos de la grafica estan conectados (por lo menos por un camino)
            pm = nx.average_shortest_path_length(G) #se calcula el promedio de los caminos mas cortos con la funcion
                                                            # nx.average_shortest_path_length
        else:   #si la grafica no esta conectada (es decir, existen al menos dos nodos entre los cuales no existe un camino) 
            DISTANCIAS = [] 

            for c in nx.connected_components(G): #c va tomando los valores de las subgraficas del grafo
                subG = G.subgraph(c).copy()  #guardamos una copia de la subgrafica en la iteracion respectiva
                for NODO1 in subG.nodes():
                    for NODO2 in subG.nodes():
                        dist_camino_i = nx.shortest_path_length(subG,source=NODO1,target=NODO2) #calculamos los caminos mas cortos para esa subgrafica
                        DISTANCIAS.append(dist_camino_i)
            D = sum(DISTANCIAS)
            pm = D/(self.N*(self.N-1)) #tomamos el promedio de los promedios de los caminos mas cortos de todas las subgraficas
            #pm = pm/2

        return pm
    
    def Promedio_Caminos_Single(self,G,nodo):
        length = nx.single_source_shortest_path_length(G, nodo)

        sum = 0
        for i in length:
        #    print(length[i])
            sum = sum + int(length[i])
        prom = float(sum)/ float(len(length))
        return prom
    
    def Clustering_C(self,G): #funcion para encontrar el promedio del coeficiente de agrupamiento de los nodos de un grafo G
        coeficiente_agrupamiento = float(nx.average_clustering(G))
        return coeficiente_agrupamiento
    
    def dist_grado_por_grafo(self,G):
        grado = [G.degree(n) for n in G.nodes()]
        return grado

    def frequencias(self,G):
        #N = G.number_of_nodes()
        rows = []
        for i in range(self.N):
            rows.append([i,0])
        df = pd.DataFrame(rows, columns=["Grado de Nodo", "Cantidad de Nodos"])
        
        for nodo in G.nodes():
            grado_n = G.degree(nodo)
            fila = df.loc[df['Grado de Nodo'] == grado_n]
            index = df.index
            FILA = index[fila][0][0]
            df.at[FILA,"Cantidad de Nodos"] += 1 
        return df    
    
    def suma_columna_df(self,master,frecuencia):
        df_add = master.add(frecuencia, fill_value=0)
        df_add['Grado de Nodo'] = df_add['Grado de Nodo'].div(2)
        return df_add




###################################################################################################################
############################# Clase para guardar informacion del archivo ###########################################
    

class Save_Info(object):
    """ docstring for Save_Info"""

    def __init__(self):     #inicializamos self
        return

    def MakeDir(self,path_name):       #funcion para crear un directorio (carpeta)

    	if not os.path.exists(path_name):  #si la carpeta con el nombre 'path_name' no existe
    		os.makedirs(path_name)         # se crea una carpeta con el nombre deseado 'path_name'
    	else:
    		shutil.rmtree(path_name)       # si existe, entonces se usa ese directorio ya creado
    		os.makedirs(path_name)

    	return

    def SaveFiles(self,path_name,make_dir=False,file_format='*.hdf5'):
    
        """
          Routine to Copy all the files with a given format into the folder path_name

          path_name: The destination folder
          format:    the files format that will be copy to path_name

        """
    
        if make_dir == True:
            self.MakeDir(path_name)
        else: pass

        #formato1 = '*.hdf5'
        #files1 = glob.iglob(os.path.join(file_format))
        #for ifile in files1: shutil.move(ifile,path_name)

        # Copy  the files in format file_format to path_name
        for ifile in glob.iglob(os.path.join(file_format)):
            # Si el archivo for formato 'file_format' ya existe, lo elimina y guarda el nuevo
            if os.path.isfile(ifile):
                try:
                    shutil.move(ifile,path_name)
                except:
                    os.remove(path_name+'/'+ifile)
                    shutil.move(ifile,path_name)

        return

