import networkx as nx  
import numpy as np
import random


###################################################################################
############################# Clase para definir diferentes grafos ################



# Formato básico para contruir una clase
class Contagios:

    def __init__(self,N,steps):  #inicializamos el self, con parametros globales
        self.N = N           # numero de nodos
        self.steps = steps   # numero de pasos o frames
        return




    def Infectados_Iniciales(self,G,n):
        """ Funcion para definir los contagiados iniciales
            G     - grafo
            n     - numero de infectados con los que se quiere comenzar
    
            La funcion regresa la lista de infectados iniciales y una lista de suceptibles iniciales
            y el primer elemento de una linea de contagios de uno de los infectados iniciales
        """
        Infectados_Iniciales  = []   # Inicializamos el vector de infectados iniciales
        path = []                    # Inicializamos una linea de contagio de uno de los nodos de infectados iniciales
        Suceptibles = list(G.nodes())   # Inicializamos los suceptibles como todos los nodos
        for i in range(0,n):                       # recorremos un ciclo 'n' veces
            Infectados_Iniciales.append(np.random.choice(Suceptibles))  # elegimos un nodo al azar
            Suceptibles = list(set(Suceptibles)-set(Infectados_Iniciales))  # quitamos al infectado de la lista de suceptibles
        path.append(random.choice(Infectados_Iniciales))     # elegimos un nodo infectado para comenzar a obtener su linea de contagios
        return Infectados_Iniciales,Suceptibles,path
    
##########################################################################################
########################################################################################## 
    '''
    def Vacunados_Iniciales(self,G,n):
        """ Funcion para definir los vacunados iniciales
            G     - grafo
            n     - numero de vacunados con los que se quiere comenzar
    
        """
        G1 = G.copy()           # generamos una copia del grafo original trabajar con ella
        Vacunados_Iniciales = []
        Suceptibles = list(G.nodes())
        for i in range(0,n):                       # recorremos un ciclo 'n' veces
            vacunado = np.random.choice(Suceptibles)
            Vacunados_Iniciales.append(vacunado)  # elegimos un nodo al azar
            Suceptibles = list(set(Suceptibles)-set(Vacunados_Iniciales))  # quitamos al infectado de la lista de suceptibles
            G1.remove_node(vacunado) 
        return G1,Vacunados_Iniciales
    '''
##########################################################################################
########################################################################################## 

    '''
    def Contagio_en_un_tiempo(self,Infectados,Suceptibles,G,p,path):
        """ Funcion simular los contagios en un periododo de tiempo
                Infectados  - la lista de infectados al iniciar el periodo de tiempo
                Suceptibles - la lista de suceptibles al iniciar un periodo de tiempo
                G     - grafo
                p - probabilidad de contagio
                path - la linea de contagio hasta el periodo de tiempo en cuestion
                
            **La funcion regresa:
                * Infectados_Totales - la lista de infectados despues de los contagios en un periodo de tiempo
                * Suceptibles - la lista de infectados despues de los contagios en un periodo de tiempo
                * path - la linea de contagio despues del periodo de tiempo en cuestion
                * Enlaces_t - la lista de enlaces/contagios que ocurrieron en el periodo de tiempo
                
        """
        Infectados_Totales = []  # Inicializamos los infectados totales
        Infectados_Totales = Infectados_Totales + Infectados
        Enlaces_t = []  # Inicializamos la lista de contagios/enlaces
        
        for nodo_i in Infectados:  # ciclo que recorre los nodos infectados
            r = np.random.uniform(0,1)       # calculamos un numero aleatoriamente entre 0 y 1
            if r<p:                          # preguntar si r<p es equivalente a tomar la probabilidad de infectar a alguien
                vecinos =  list(G.neighbors(nodo_i))  # tenemos la lista de vecinos del infectado de la iteracion correspondiente
                vecinos_s = list(set(vecinos)-set(Infectados_Totales))   # tomamos la lista de vecinos del nodo que no esten infectados
                
                if len(vecinos_s)==0:      # si la lista es vacia, significa que todos los vecinos del nodo estan infectados
                    if nodo_i == path[len(path)-1]:   # la linea de contagios del nodo elegido se mantendra en el mismo nodo
                        path.append(nodo_i)
                    continue               # ya no se puede contagiar a otro vecino y se continua con el ciclo
               
                nuevo_contagio = np.random.choice(vecinos_s)
                Infectados_Totales.append(nuevo_contagio)   # elegimos uno de los vecinos para 'infectarlo'
                Enlaces_t.append((nodo_i,nuevo_contagio))   # agregamos el enlace/contagio a la lista de contagios
                
                if nodo_i == path[len(path)-1]:   # se actualiza la linea de contagio del nodo que se haya elegido en las funciones anteriores
                    path.append(nuevo_contagio)
            
            else:                                 # si no se contagia a nadie en ese periodo
                if nodo_i == path[len(path)-1]:   # la linea de contagios del nodo elegido se mantendra en el mismo nodo
                    path.append(nodo_i)
                    
                continue 
        Suceptibles = list(set(Suceptibles)-set(Infectados_Totales))  # a la lista de suceptibles le quitamos la lista de infectados despues de los contagios del periodo
        return Infectados_Totales,Suceptibles,path,Enlaces_t
    '''
    
##########################################################################################
########################################################################################## 
    
    def Contagio_en_un_tiempo2(self,Infectados,Suceptibles,G,p,path,Recuperados_Totales,Muertes_Totales):
        """ Funcion simular los contagios en un periododo de tiempo
                Infectados  - la lista de infectados al iniciar el periodo de tiempo
                Suceptibles - la lista de suceptibles al iniciar un periodo de tiempo
                G     - grafo
                p - probabilidad de contagio
                path - la linea de contagio hasta el periodo de tiempo en cuestion
                
            **La funcion regresa:
                * Infectados_Totales - la lista de infectados despues de los contagios en un periodo de tiempo
                * Suceptibles - la lista de infectados despues de los contagios en un periodo de tiempo
                * path - la linea de contagio despues del periodo de tiempo en cuestion
                * Enlaces_t - la lista de enlaces/contagios que ocurrieron en el periodo de tiempo
                
        """
        Infectados_Totales = []  # Inicializamos los infectados totales
        Infectados_Totales = Infectados_Totales + Infectados
        Enlaces_t = []  # Inicializamos la lista de contagios/enlaces
        
        for nodo_i in Infectados:   # ciclo que recorre los nodos infectados
            vecinos =  list(G.neighbors(nodo_i))  # tenemos la lista de vecinos del infectado de la iteracion correspondiente
            vecinos_s = list(set(vecinos)-set(Infectados_Totales))   # tomamos la lista de vecinos del nodo que no esten infectados
            vecinos_s = list(set(vecinos_s)-set(Recuperados_Totales))
            vecinos_s = list(set(vecinos_s)-set(Muertes_Totales))
            #vecinos_s = list(set(vecinos_s)-set(Vacunados_Totales))
            
            if len(vecinos_s)==0: # si la lista es vacia, significa que todos los vecinos del nodo estan infectados
                continue               # ya no se puede contagiar a otro vecino y se continua con el ciclo
            
            num_vecinos_contagiados_i = np.random.binomial(len(vecinos_s), p)   # de todos lo vecinos suceptibles elegimos el numero de vecinos que contagia el nodo_i
                                                                                # para esto usamos una binomial
            if num_vecinos_contagiados_i == 0:         # si no se contagia a nadie en ese periodo
                if nodo_i == path[len(path)-1]:        # la linea de contagios del nodo elegido se mantendra en el mismo nodo
                    path.append(nodo_i)
                continue       # como no se cumple la probabilidad de contagiar, se continua con el ciclo
                
            vecinos_contagiados_i = random.sample(vecinos_s, num_vecinos_contagiados_i)   # elegimos una muestra aleatoria del tamano del numero de vecinos 
                                                                                          # que va a contagiar el nodo_i  
            Infectados_Totales = Infectados_Totales + vecinos_contagiados_i      # actualizamos la lista de infectados, agregando los nodos que infecta el nodo_i
            for nuevo_contagio in vecinos_contagiados_i:   # ciclo que recorre los nodos que acaba de contagiar el nodo_i
                Enlaces_t.append((nodo_i,nuevo_contagio))  # agregamos a la lista de enlaces/contagios cada enlace entre el nodo_i y los que contagio 
            
            if nodo_i == path[len(path)-1]:        # se actualiza la linea de contagio del nodo que se haya elegido en las funciones anteriores
                path.append(random.sample(vecinos_contagiados_i, 1))
            
        Suceptibles = list(set(Suceptibles)-set(Infectados_Totales)) # a la lista de suceptibles le quitamos la lista de infectados despues de los contagios del periodo
        Suceptibles = list(set(Suceptibles)-set(Recuperados_Totales))
        Suceptibles = list(set(Suceptibles)-set(Muertes_Totales))
        return Infectados_Totales,Suceptibles,path,Enlaces_t

##########################################################################################
########################################################################################## 
    
    def Contagio_en_un_tiempo3(self,Infectados,Suceptibles,G,p,path,Recuperados_Totales,Muertes_Totales,INFECTADOS,i,incubacion):
        """ Funcion simular los contagios en un periododo de tiempo
                Infectados  - la lista de infectados al iniciar el periodo de tiempo
                Suceptibles - la lista de suceptibles al iniciar un periodo de tiempo
                G     - grafo
                p - probabilidad de contagio
                path - la linea de contagio hasta el periodo de tiempo en cuestion
                
            **La funcion regresa:
                * Infectados_Totales - la lista de infectados despues de los contagios en un periodo de tiempo
                * Suceptibles - la lista de infectados despues de los contagios en un periodo de tiempo
                * path - la linea de contagio despues del periodo de tiempo en cuestion
                * Enlaces_t - la lista de enlaces/contagios que ocurrieron en el periodo de tiempo
                
        """
        if i<incubacion:
            Infectados_Totales = Infectados
            path.append(path[i-1])
            Enlaces_t = []
            return Infectados_Totales,Suceptibles,path,Enlaces_t
        else:
            Infectados_Totales = []  # Inicializamos los infectados totales
            Infectados_Totales = Infectados_Totales + Infectados
            Enlaces_t = []  # Inicializamos la lista de contagios/enlaces
            
            for nodo_i in INFECTADOS[i-incubacion]:   # ciclo que recorre los nodos infectados
                vecinos =  list(G.neighbors(nodo_i))  # tenemos la lista de vecinos del infectado de la iteracion correspondiente
                vecinos_s = list(set(vecinos)-set(Infectados_Totales))   # tomamos la lista de vecinos del nodo que no esten infectados
                vecinos_s = list(set(vecinos_s)-set(Recuperados_Totales))
                vecinos_s = list(set(vecinos_s)-set(Muertes_Totales))
                #vecinos_s = list(set(vecinos_s)-set(Vacunados_Totales))
                
                if len(vecinos_s)==0: # si la lista es vacia, significa que todos los vecinos del nodo estan infectados
                    continue               # ya no se puede contagiar a otro vecino y se continua con el ciclo
                
                num_vecinos_contagiados_i = np.random.binomial(len(vecinos_s), p)   # de todos lo vecinos suceptibles elegimos el numero de vecinos que contagia el nodo_i
                                                                                    # para esto usamos una binomial
                if num_vecinos_contagiados_i == 0:         # si no se contagia a nadie en ese periodo
                    if nodo_i == path[len(path)-1]:        # la linea de contagios del nodo elegido se mantendra en el mismo nodo
                        path.append(nodo_i)
                    continue       # como no se cumple la probabilidad de contagiar, se continua con el ciclo
                    
                vecinos_contagiados_i = random.sample(vecinos_s, num_vecinos_contagiados_i)   # elegimos una muestra aleatoria del tamano del numero de vecinos 
                                                                                              # que va a contagiar el nodo_i  
                Infectados_Totales = Infectados_Totales + vecinos_contagiados_i      # actualizamos la lista de infectados, agregando los nodos que infecta el nodo_i
                for nuevo_contagio in vecinos_contagiados_i:   # ciclo que recorre los nodos que acaba de contagiar el nodo_i
                    Enlaces_t.append((nodo_i,nuevo_contagio))  # agregamos a la lista de enlaces/contagios cada enlace entre el nodo_i y los que contagio 
                
                if nodo_i == path[len(path)-1]:        # se actualiza la linea de contagio del nodo que se haya elegido en las funciones anteriores
                    path.append(random.sample(vecinos_contagiados_i, 1))
                
            Suceptibles = list(set(Suceptibles)-set(Infectados_Totales)) # a la lista de suceptibles le quitamos la lista de infectados despues de los contagios del periodo
            Suceptibles = list(set(Suceptibles)-set(Recuperados_Totales))
            Suceptibles = list(set(Suceptibles)-set(Muertes_Totales))
        return Infectados_Totales,Suceptibles,path,Enlaces_t
    
##########################################################################################
##########################################################################################    

    def Recuperacion_t(self,INFECTADOS,i,p_r,periodos_recuperacion,RECUPERADOS,Muertes_Totales):
        """ Funcion simular los recuperados en un periodo de tiempo
                INFECTADOS            - Arreglo de arreglos con infectados en cada tiempo hasta el periodo actual
                i                     - tiempo o iteracion actual
                p_r                   - probabilidad de recuperacion
                periodos_recuperacion - numero minimo de periodos de la enfermedad antes de que un individuo se pueda recuperar
                RECUPERADOS           - Arreglo de arreglos con recuperados en cada tiempo hasta el periodo actual
                
                
            **La funcion regresa:
                * Recuperados         - la lista de recuperados en un periodo de tiempo
                
        """
        Recuperados = []
        if i>=periodos_recuperacion:    # definimos un numero minimo de periodos de enfermedad antes de poder recupuerarse
            # en cada iteracion generamos un arreglo para guardar los recuperados en el tiempo i
            posibles_recuperados = list(set(INFECTADOS[i-periodos_recuperacion])-set(Muertes_Totales))
            #posibles_recuperados = list(set(INFECTADOS[i-periodos_recuperacion])-set(Vacunados_Totales))
            for infectado in posibles_recuperados:    # recorremos todos los infectados en el tiempo i
                r = np.random.uniform(0,1)             # calculamos un numero aleatoriamente entre 0 y 1
                if r<p_r:                              # si se cumple la probabilidad de recuperacion
                    Recuperados.append(infectado)      # agregamos el infectado a la lista de recuperados
            Recuperados = list(set(Recuperados)-set(RECUPERADOS[i-1]))  # a los recuperados, le quitamos los de la lista anterior para no repetirlos
        return Recuperados
    
##########################################################################################
##########################################################################################


    def Muertes(self,INFECTADOS,i,p_m,periodos_m,Infectados_Totales,Recuperados):
        """ Funcion simular los recuperados en un periodo de tiempo
                INFECTADOS            - Arreglo de arreglos con infectados en cada tiempo hasta el periodo actual
                i                     - tiempo o iteracion actual
                p_m                   - probabilidad de muerte por la enfermedad
                periodos_m            - numero minimo de periodos de la enfermedad antes de que un individuo se ponga grave y pueda morir
                Infectados_Totales    - Lista de Infectados hasta el tiempo actual
                Recuperados           - Lista de Recuperados
                G1                    - Grafo actualizado con los nodos que no esten muertos ni vacunados
                
                
            **La funcion regresa:
                * Muertes             - lista de muertes en el periodo t
                * G11                 - El grafo que se ingresa a la funcion, menos los nodos de los que mueren en el periodo t
                
        """
        Muertes = []
        #G11 = G1.copy()
        if i>=periodos_m:    # definimos un numero minimo de periodos de enfermedad antes de que la enfermedad sea grave
            # nos quedamos con la lista de individuos que llevan enfermos desde hace #periodos_m etapas
            Inf_en_Riesgo = list(set(INFECTADOS[i-periodos_m]).intersection(set(Infectados_Totales)))  
                                                             
            for j in range(0,periodos_m):   # recorremos los ultimos #periodos_m etapas
                Inf = list(set(INFECTADOS[i-j]).intersection(set(Infectados_Totales))) 
                Inf_en_Riesgo = list(set(Inf).intersection(set(Inf_en_Riesgo)))  # nos quedamos unicamente con los enfermos que lleven desde el periodo elegido enfermos
                
            Inf_en_Riesgo = list(set(Inf_en_Riesgo)-set(Recuperados))    # a nuestra lista de enfermos en riesgo, le quitamos la lista de recuperados
            for infectado in Inf_en_Riesgo:    # recorremos todos los infectados en riesgo en el tiempo i
                r = np.random.uniform(0,1)             # calculamos un numero aleatoriamente entre 0 y 1
                if r<p_m:                              # si se cumple la probabilidad de muerte
                    Muertes.append(infectado)      # agregamos el infectado a la lista de muertes
                    #G11.remove_node(infectado)     # eliminamos el nodo del grafo
        return Muertes#,G11
    
    
##########################################################################################
##########################################################################################


    def Muertes2(self,INFECTADOS,i,periodos_m,Infectados_Totales,Recuperados,P,R):
        """ Funcion simular los recuperados en un periodo de tiempo
                INFECTADOS            - Arreglo de arreglos con infectados en cada tiempo hasta el periodo actual
                i                     - tiempo o iteracion actual
                p_m                   - probabilidad de muerte por la enfermedad
                periodos_m            - numero minimo de periodos de la enfermedad antes de que un individuo se ponga grave y pueda morir
                Infectados_Totales    - Lista de Infectados hasta el tiempo actual
                Recuperados           - Lista de Recuperados
                G1                    - Grafo actualizado con los nodos que no esten muertos ni vacunados
                
                
            **La funcion regresa:
                * Muertes             - lista de muertes en el periodo t
                #G11                 - El grafo que se ingresa a la funcion, menos los nodos de los que mueren en el periodo t
                
        """
        poblacion_riesgo_bajo  = P[0]
        poblacion_riesgo_medio = P[1] + poblacion_riesgo_bajo
        
        prob_riesgo_bajo  = R[0]
        prob_riesgo_medio = R[1]
        prob_riesgo_alto  = R[2]
        
        Muertes = []
        #G11 = G1.copy()
        if i>=periodos_m:    # definimos un numero minimo de periodos de enfermedad antes de que la enfermedad sea grave
            # nos quedamos con la lista de individuos que llevan enfermos desde hace #periodos_m etapas
            Inf_en_Riesgo = list(set(INFECTADOS[i-periodos_m]).intersection(set(Infectados_Totales)))  
                                                             
            for j in range(0,periodos_m):   # recorremos los ultimos #periodos_m etapas
                Inf = list(set(INFECTADOS[i-j]).intersection(set(Infectados_Totales))) 
                Inf_en_Riesgo = list(set(Inf).intersection(set(Inf_en_Riesgo)))  # nos quedamos unicamente con los enfermos que lleven desde el periodo elegido enfermos
                
            Inf_en_Riesgo = list(set(Inf_en_Riesgo)-set(Recuperados))    # a nuestra lista de enfermos en riesgo, le quitamos la lista de recuperados
            for infectado in Inf_en_Riesgo:    # recorremos todos los infectados en riesgo en el tiempo i
                riesgo = np.random.uniform(0,1)             # calculamos un numero aleatoriamente entre 0 y 1
                if riesgo<=poblacion_riesgo_bajo:
                    p_m = prob_riesgo_bajo
                elif poblacion_riesgo_bajo < riesgo <= poblacion_riesgo_medio:
                    p_m = prob_riesgo_medio
                else:
                    p_m = prob_riesgo_alto
                r = np.random.uniform(0,1)             # calculamos un numero aleatoriamente entre 0 y 1
                if r<p_m:                              # si se cumple la probabilidad de muerte
                    Muertes.append(infectado)      # agregamos el infectado a la lista de muertes
                    #G11.remove_node(infectado)     # eliminamos el nodo del grafo
        return Muertes#,G11
    
##########################################################################################
##########################################################################################    


    def Inmunes(self,RECUPERADOS,i,periodos_inmune,Suceptibles_Totales):
        '''Funcion para retener los elementos recien recuperados como inmunes
            RECUPERADOS         - lista de recuperados en cada tiempo hasta el tiempo actual
            i                   - numero de iteracion o tiempo
            periodos_inmune     - numero de periodos que se vuelve inmune un recuperado
            Suceptibles_Totales - lista de suceptibles hasta el tiempo actual
            
            **regresa:
             * Suceptibles Totales despues de sumar aquellos individuos que dejan de ser inmunes
        '''
        if i>=periodos_inmune:    # definimos un numero minimo de periodos de inmunidad a a la enfermedad
            Suceptibles_Totales = Suceptibles_Totales + RECUPERADOS[i-periodos_inmune] # agregamos los elementos que dejan de ser inmunes a los suceptibles
        return Suceptibles_Totales

##########################################################################################
##########################################################################################

'''
    def Vacunados_t(self,Suceptibles_Totales,Recuperados_Totales,i,periodos_v,num_vacunados_periodo):
            Funcion para vacunar individuos suceptibles o recuperados cada cierto tiempo 'periodos_v'
            Suceptibles_Totales    - lista de suceptibles hasta el tiempo actual
            Recuperados_Totales    - lista de recuperados hasta el tiempo actual
            i                      - numero de iteracion o tiempo
            periodos_v             - numero de periodos que ocurren antes de volver a vacunar individuos
            G1                     - Grafo actualizado con los nodos que no esten muertos ni vacunados
            num_vacunados_periodo  - numero de vacunados en los periodos en los que se vacunan individuos
            
            **regresa:
             * G11                 - El grafo que se ingresa a la funcion, menos los nodos de los que se vacunan en el periodo 
             * Suceptibles Totales despues de la vacunacion
             * Recuperados Totales despues de la vacunacion
             *Vacunados_i          - Lista de elementos vacunados en el periodo
        
        #G111 = G1.copy()           # generamos una copia del grafo original trabajar con ella
        Vacunados_i= []            # empezamos con un arreglo vacio
        if (i%periodos_v == 0) and (i>0):   # condicion para ver cada cuando hay vacunas, excluyendo la vacuna inicial
            for i in range(0,num_vacunados_periodo):     # recorremos un ciclo el numero de veces de los vacunados ingresados
                Posibles_Vacunados = Suceptibles_Totales + Recuperados_Totales
                if len(Posibles_Vacunados)==0:
                    break
                vacunado = np.random.choice(Posibles_Vacunados)
                Vacunados_i.append(vacunado)  # elegimos un nodo al azar
                if vacunado in Suceptibles_Totales:
                    Suceptibles_Totales = list(set(Suceptibles_Totales)-set(Vacunados_i))  # quitamos al infectado de la lista de suceptibles
                else:
                    Recuperados_Totales = list(set(Recuperados_Totales)-set(Vacunados_i))
                #G111.remove_node(vacunado)
        return Suceptibles_Totales,Recuperados_Totales,Vacunados_i
'''
