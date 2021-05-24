import random
import sys

#leer las listas
def leer(fichero):
    with open(fichero, 'r') as f:

        texto = f.read()

        lineas = texto.splitlines()

        num_pers = int(lineas[0])
        lista = lineas[1:]

        for i in range(num_pers):
            lista[i] = lista[i].split()
            for j in range(len(lista[i])):
                lista[i][j] = int(lista[i][j]) - 1

    return num_pers, lista

#primera generación
def iniciar(tam,n_genes):
    P=[]
    for i in range(tam):
        ind=list(range(n_genes))
        random.shuffle(ind)
        P.append(ind)
    return P

#comprobar si la población ha convergido (95% de individuos iguales)
def convergido(P,n_genes,tam):
    b=True
    j=0
    while j<n_genes and b: #recorremos todos los genes
        L=[]
        for k in list(range(tam)): #recorremos todos los individuos
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
def maximo(L):
    m = 0
    elem = L[0]
    for i in range(1,len(L)):
        if L[i][0]>elem[0]:
            m = i
            elem = L[i]
        elif L[i][0]==elem[0]:
            if L[i][1]>=elem[1]:
                m = i
                elem = L[i]
    return m, elem

def nMinimos(L,n):
    M=list(range(n))
    N=L[:n]
    for j in range(n,len(L)):
        if L[j]<maximo(N)[1]:
            M.pop(maximo(N)[0])
            M.append(j)
            N.pop(maximo(N)[0])
            N.append(L[j])
        j+=1
    return M

#seleccion
def torneo(tam,Fitnesses):
    op1=random.randint(0, tam-1)
    op2=random.randint(0, tam-1)

    if Fitnesses[op1][0]<Fitnesses[op2][0]:
        return op1
    elif Fitnesses[op1][0]==Fitnesses[op2][0]:
        if Fitnesses[op1][1]<=Fitnesses[op2][1]:
            return op1
        else:
            return op2
    else:
        return op2

#cruce
def rotacion(n_genes,prog1,prog2):
    i=0
    while prog1[i]==prog2[i] and i<n_genes-1:
        i+=1
    if i==n_genes-1:
        R=list(range(n_genes))
    else:
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

def bloquea(m_mejores,h,M,ind):
    b=False
    i=0
    while not b and i<len(m_mejores):
        m=m_mejores[i]
        b=(M[m].index(h)<M[m].index(ind[m]))
        i+=1
    return b

def num_estables(n_genes,M,H,ind):
    #función que comprueba la estabilidad, devuelve el número de parejas no estables
    num=0
    for m in range(n_genes):#recorremos todas las parejas
        h = ind[m] #m es la mujer, h es el hombre pareja de m
        m_mejores=H[h][:H[h].index(m)] #mujeres mejores que m para el hombre h
        if bloquea(m_mejores,h,M,ind):
            num+=1

    return num

def sum_pos_m(n_genes,M,ind):
    f=0
    for i in range(n_genes):
        #posición del hombre que es pareja de la mujer i en la lista de esta
        f+=(M[i].index(ind[i]))
    return f

def sum_pos_h(n_genes,H,ind):
    f=0
    for i in range(n_genes):
        #posición de la mujer i en la lista del hombre con el que está emparejado
        f+=(H[ind[i]].index(i))
    return f

def eg_cost_fitness(n_genes,M,H,ind):
    return sum_pos_m(n_genes, M, ind) + sum_pos_h(n_genes, H, ind)

def sex_eq_cost_fitness(n_genes,M,H,ind):
    return sum_pos_m(n_genes, M, ind) - sum_pos_h(n_genes, H, ind)

def genetico(n_genes,n_generaciones,tam):
    #población aleatoria inicial
    #cada individuo de la población es una lista de longitud n_genes
    #cuyos elementos están comprendidos entre 0 y n_genes
    P=iniciar(tam,n_genes)
    Fitnesses=list(map(fitness,P))
    peor=nMinimos(Fitnesses, 1)[0]

    print("\nGeneración 0:")
    print("Mejor individuo",P[peor])
    print("con", list(map(num_est,P))[peor], "parejas no estables")
    print("y con felicidad equitativa", list(map(sex_eq,P))[peor])


    g = 0
    while g<n_generaciones:
        g += 1
        sig_P = []

        #elitismo (nos quedamos con los tres peores de la anterior población)
        peores=nMinimos(Fitnesses, 3)
        for j in peores:
            sig_P.append(P[j])

        while len(sig_P) < tam:
            if len(sig_P) == tam-1:#si solo queda 1 individuo
                #copiamos uno cualquiera
                sig_P.append(P[random.randint(0, n_genes-1)])
            else:
                #seleccionamos los progenitores
                prog1 = P[torneo(tam, Fitnesses)]
                prog2 = P[torneo(tam, Fitnesses)]

                #obtenemos la descendencia
                (des1,des2) = cruce(n_genes,prog1,prog2)

                #mutamos la descendencia (80% de probabilidad)
                mutacion(80, des1, n_genes)
                mutacion(80, des2, n_genes)

                #añadimos la descendencia a la sig generación
                sig_P.append(des1)
                sig_P.append(des2)

        P = sig_P
        Fitnesses=list(map(fitness,P))
        peor=nMinimos(Fitnesses, 1)[0]

        print(f"\nGeneración {g}:")
        print("Mejor individuo",P[peor])
        print("con", list(map(num_est,P))[peor], "parejas no estables")
        print("y con felicidad equitativa", list(map(sex_eq,P))[peor])

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print('La entrada debe ser: python3 me_genetico.py hombres.txt mujeres.txt num_generaciones tam_poblacion')
    else:
        ficheroH = sys.argv[1]
        ficheroM = sys.argv[2]
        n_generaciones = sys.argv[3]
        tam = sys.argv[4]

        nH, H = leer(ficheroH)
        nM, M = leer(ficheroM)

        if nH == nM:
            #definimos a la función fitness
            num_est = lambda ind: num_estables(nH,M,H,ind)
            eg = lambda ind: eg_cost_fitness(nH,M,H,ind)
            sex_eq = lambda ind: sex_eq_cost_fitness(nH,M,H,ind)
            fitness = lambda ind: (num_est(ind), abs(sex_eq(ind)))
            
            genetico(nH,n_generaciones,tam)
        else:
            print('Datos incorrectos')
