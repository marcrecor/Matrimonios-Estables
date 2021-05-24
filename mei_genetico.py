import random

#leer las listas
def leer(fichero):    
    with open(fichero, 'r') as f:
    
        texto = f.read()
        
        lineas = texto.splitlines()
    
        num_pers = int(lineas[0])
        lista = lineas[1:]
    
        for i in range(num_pers):
            lista[i] = lista[i].split(' |')
            for j in range(len(lista[i])):
                lista[i][j] = lista[i][j].split()
                for k in range(len(lista[i][j])):
                    lista[i][j][k] = int(lista[i][j][k])
        
    return num_pers, lista

#primera generación
def iniciar(n_genes):
    P=[]
    for i in range(n_genes):
        ind=list(range(n_genes))
        random.shuffle(ind)
        P.append(ind)
    return P

#comprobar si una población ha convergido (95% de individuos iguales)
def convergido(P,n_genes):
    b=True
    j=0
    while j<n_genes and b: #recorremos todos los genes
        L=[]
        for k in list(range(n_genes)): #recorremos todos los individuos
            L.append(P[k][j])
        T=[]
        for x in list(set(L)):
            T.append(L.count(x))
        s=sum(T)
        T=list(map(lambda x : x/s, T))
        b=max(T)>=0.95
        j+=1
    return b

#elitismo
def nMinimos(L,n) :
    if n>=len(L):
        M=list(range(len(L)))
    elif n==0:
        M=[]
    else:
        M=list(range(n))
        N=L[:n]
        j=n
        while j<len(L):
            if L[j]<max(N):
                M.pop(N.index(max(N)))
                M.append(j)
                N.pop(N.index(max(N)))
                N.append(L[j])
            j+=1
    return M

#seleccion
def torneo(n_genes, Fitnesses):
    op1 = random.randint(0, n_genes-1)
    op2 = random.randint(0, n_genes-1)
    
    if Fitnesses[op1] <= Fitnesses[op2]:
        return op1
    else:
        return op2

#cruce
def rotacion(n_genes,prog1,prog2):
    i=random.randint(0, n_genes-1)
    R=[i]
    j=i
    while prog2[j]!=prog1[i]:
        j=prog1.index(prog2[j])
        R.append(j)
    return R
        
def cruce(n_genes,prog1,prog2):
    rot=rotacion(n_genes,prog1,prog2)    
    des1,des2=[],[]
    for i in range(n_genes):
        if i in rot:
            des1.append(prog1[i])
            des2.append(prog2[i])
        else:
            des1.append(prog2[i])
            des2.append(prog1[i])
    return (des1,des2)

#mutacion
def mutacion(prob,des,n_genes):
    #intercambio de los valores de dos genes
    q=random.uniform(0, 100)
    if q<=prob:
        punto1=random.randint(1, n_genes-1)
        punto2=random.randint(1, n_genes-1)
        while punto2==punto1:#tienen que ser dos puntos diferentes
            punto2=random.randint(1, n_genes-1)
        des[punto1],des[punto2]=des[punto2],des[punto1]

#funcion fitness 
def pos(p,P):
    b=False
    i,j=0,0
    while i<len(P) and not b:
        if not(p in P[i]):
            j+=len(P[i])
        else:
            b=True
        i+=1
    return j

def concat(L):
    M=[]
    for i in range(len(L)):
        M=M+L[i]
    return M

#numero de parejas estables
def bloquea(m_mejores,h,M,ind):
    b=False
    i=0
    while not b and i<len(m_mejores):
        m = m_mejores[i]
        b = (pos(h,M[m]) > pos(ind[m],M[m]))
        i += 1
    return b 

def num_estables(n_genes,M,H,ind):
    #función que comprueba la estabilidad, devuelve el número de parejas estables
    num=n_genes
    for i in range(n_genes):#recorremos todas las parejas
    #i es la mujer, ind[i] es el hombre pareja de i
        #mujeres mejores que i para el hombre ind[i]
        m_mejores=concat(H[ind[i]][:pos(i,H[ind[i]])])
        if bloquea(m_mejores,ind[i],M,ind):
            num-=1                 
    return num       

#suma de las posiciones         
def sum_pos_m(n_genes,M,ind):
    f=0
    for i in range(n_genes):
        #posición del hombre que es pareja de la mujer i en la lista de esta
        f+=(pos(ind[i],M[i]))
    return f

def sum_pos_h(n_genes,H,ind):
    f=0
    for i in range(n_genes):
        #posición de la mujer i en la lista del hombre con el que está emparejado
        f+=(pos(i,H[ind[i]]))
    return f

def regret_cost_fitness(n_genes,M,H,ind):
    r = 0
    for i in range(n_genes):
        r = max(r,(max(pos(i,H[ind[i]]),pos(ind[i],M[i]))))
    return r
    
def eg_cost_fitness(n_genes,M,H,ind):
    return sum_pos_m(n_genes, M, ind) + sum_pos_h(n_genes, H, ind)

def sex_eq_cost_fitness(n_genes,M,H,ind):
    return sum_pos_h(n_genes, H, ind) - sum_pos_m(n_genes, M, ind)
    
def principal(M,H,n_genes,num_est,eg,sex_eq,reg,fitness,n_generaciones):
    #población aleatoria inicial
    #cada individuo de la población es una lista de longitud n_genes
    #cuyos elementos son enteros que están comprendidos entre 0 y n_genes
    
    it = 30 #numero de iteraciones
    sol = [] #lista con las soluciones obtenidas
    
    for _  in range(it):
        P = iniciar(n_genes)
        Fitnesses = list(map(fitness,P))
        mejor = Fitnesses.index(min(Fitnesses))
    
        print("\nGeneración 0:")
        print("Mejor individuo",P[mejor])
        print("con", list(map(num_est,P))[mejor], "parejas estables")
        print("Arrepentimiento", list(map(reg,P))[mejor])
        print("Coste", list(map(eg,P))[mejor])
        print("Coste equitativo", list(map(sex_eq,P))[mejor])
    
    
        g = 0 
        while g<n_generaciones and not convergido(P, n_genes):
            g += 1
            sig_P = []
        
            #elitismo (nos quedamos con los dos peores de la anterior población)
            peores=nMinimos(Fitnesses, 2)
            for j in peores:
                sig_P.append(P[j])
        
            while len(sig_P) < n_genes:
                if len(sig_P) == n_genes-1:#si solo queda 1 individuo
                    #copiamos uno cualquiera
                    sig_P.append(P[random.randint(0, n_genes-1)])
                else:
                    #seleccionamos los progenitores
                    prog1 = P[torneo(n_genes, Fitnesses)]
                    prog2 = P[torneo(n_genes, Fitnesses)]
                
                    #obtenemos la descendencia
                    (des1,des2) = cruce(n_genes,prog1,prog2)
                
                    #mutamos la descendencia (80% de probabilidad)
                    mutacion(80, des1, n_genes)
                    mutacion(80, des2, n_genes)
                
                    #añadimos la descendencia a la sig generación
                    sig_P.append(des1)
                    sig_P.append(des2)
            
            P = sig_P
            Fitnesses = list(map(fitness,P))
            mejor = Fitnesses.index(min(Fitnesses))
    
            print(f"\nGeneración {g}:")
            print("Mejor individuo",P[mejor])
            print("con", list(map(num_est,P))[mejor], "parejas estables")
            print("Arrepentimiento", list(map(reg,P))[mejor])
            print("Coste", list(map(eg,P))[mejor])
            print("Coste equitativo", list(map(sex_eq,P))[mejor])
        
        sol.append(P[mejor])
        
    return sol


#función principal
if __name__ == "__main__":
    #fichero con las listas de preferencia de los hombres
    fich_hom = 'listas1H.txt'
    n_genes, H = leer(fich_hom)
    
    #fichero con las listas de preferencia de las mujeres
    fich_muj = 'listas1M.txt'
    n, M = leer(fich_muj)
    
    if n_genes == n:
        #definimos a la función fitness
        num_est = lambda ind: num_estables(n_genes,M,H,ind)
        fit_est = lambda ind: (n_genes - num_est(ind))*2*n_genes
        eg = lambda ind: eg_cost_fitness(n_genes,M,H,ind)
        sex_eq = lambda ind: sex_eq_cost_fitness(n_genes,M,H,ind)
        reg = lambda ind: regret_cost_fitness(n_genes, M, H, ind)
        fit_cost = lambda ind: 0.5*eg(ind)+0.5*sex_eq(ind)
        fitness = lambda ind: fit_est(ind)+0.5*fit_cost(ind)
    
        #número de generaciones
        n_generaciones=100
    
        sol = principal(M,H,n_genes,num_est,eg,sex_eq,reg,fitness,n_generaciones)
    
        print(sol)