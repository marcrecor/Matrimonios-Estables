import random
import sys

#leer las listas
def leer(fichero):
    with open(fichero, 'r') as f:

        texto = f.read()

        lineas = texto.splitlines()

        num_pers = int(lineas[0])
        lista = lineas[1:]

        LM = []
        for i in range(num_pers):
            LM.append(lista[i].split(' |'))
            for j in range(len(LM[i])):
                LM[i][j] = LM[i][j].split()
                for k in range(len(LM[i][j])):
                    LM[i][j][k] = int(LM[i][j][k])

        LH = []
        for i in range(num_pers):
            LH.append(lista[i+num_pers+1].split(' |'))
            for j in range(len(LH[i])):
                LH[i][j] = LH[i][j].split()
                for k in range(len(LH[i][j])):
                    LH[i][j][k] = int(LH[i][j][k])

    return num_pers, LH, LM

#crear una población inicial
def concat(L):
    M=[]
    for i in range(len(L)):
        M=M+L[i]
    return M

def elim_no_acep(n_genes,ind,M):
    L=list(map(concat, M))
    for i in range(n_genes):
        if not (ind[i] in L[i]):
            ind[i]=-1

def iniciar(n_genes,M,tam):
    P=[]
    for i in range(tam):
        ind=list(range(n_genes))
        random.shuffle(ind)
        elim_no_acep(n_genes,ind,M)
        P.append(ind)
    return P

#comprobar si una población ha convergido (95% de individuos iguales)
def convergido(P,n_genes):
    b = True
    j = 0
    while j < n_genes and b: #recorremos todos los genes
        L = []
        for k in list(range(n_genes)): #recorremos todos los individuos
            L.append(P[k][j])
        T = []
        for x in list(set(L)):
            T.append(L.count(x))
        s = sum(T)
        T = list(map(lambda x : x/s, T))
        b = (max(T) >= 0.95)
        j += 1
    return b

#elitismo
def nMaximos(L,n) :
    M=list(range(n))
    N=L[:n]
    for j in range(n,len(L)):
        if L[j]>min(N):
            M.pop(N.index(min(N)))
            M.append(j)
            N.pop(N.index(min(N)))
            N.append(L[j])
        j+=1
    return M

#seleccion
def torneo(tam,Fitnesses):
    op1 = random.randint(0, tam-1)
    op2 = random.randint(0, tam-1)

    if Fitnesses[op1] >= Fitnesses[op2]:
        return op1
    else:
        return op2

#cruce
def rotacion(n_genes,prog1,prog2):
    i=random.randint(0, n_genes-1)
    j = 0
    while prog1[i] == -1 and j < n_genes:
        i=random.randint(0, n_genes-1)
        j += 1

    R=[i]
    j=i
    while (prog2[j]!=prog1[i]) and (prog2[j] != -1) and (prog2[j] in prog1):
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
    correccion(des1)
    correccion(des2)
    return (des1,des2)

def correccion(des):
    for i in range(len(des)):
        if des[i] in des[i+1:]:#comprobamos si está repetido
            des[i] = -1


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
        elim_no_acep(n_genes, des, M)

#funcion fitness
def pos(p,P):#posición de p en P
    encontrado = False
    i,j=0,0
    while i<len(P) and not encontrado:
        if not(p in P[i]):
            j+=len(P[i])
        else:
            encontrado = True
        i+=1
    if encontrado:
        return j
    else:
        return -1

def cardinal(n_genes,ind): # número de parejas
    c=n_genes
    for i in range(n_genes):
        if ind[i] == -1:
            c-=1
    return c

def num_estables(n_genes,M,H,ind):
    #función que comprueba la estabilidad, devuelve el número de parejas estables
    num = n_genes

    for m in range(n_genes):#recorremos todas las mujeres
        h = 0
        b = False
        while h < n_genes and not b:#recorremos todos los hombres
            if pos(h, M[m]) != -1: #si (h,m) es aceptable
                if ind[m] == -1: #Si la mujer no tiene pareja
                    if not(h in ind): #si el hombre h no tiene pareja
                        b = True
                    else: #si el hombre h tiene pareja
                        b = pos(m,H[h]) < pos(ind.index(h),H[h])
                else:#si la mujer tiene pareja
                    if not(h in ind): #si el hombre h no tiene pareja
                        b = pos(h,M[m]) < pos(ind[m],M[m])
                        #compruebo si m prefiere a h sobre su pareja
                    else: #si el hombre h tiene pareja
                        b = (pos(h,M[m]) < pos(ind[m],M[m])) and (pos(m,H[h]) < pos(ind.index(h),H[h]))
                        #m y h se prefieren entre sí sobre sus actuales parejas
            h += 1

        if b:
            num -= 1

    return num

def genetico(M,n_genes,n_generaciones,tam):
    #población aleatoria inicial
    #cada individuo de la población es una lista de longitud n_genes
    #cuyos elementos son enteros que están comprendidos entre 0 y n_genes
    #si una mujer no tiene pareja lo indicamos con un -1

    P = iniciar(n_genes,M,tam)
    Fitnesses = list(map(fitness,P))
    mejor = Fitnesses.index(min(Fitnesses))

    print("\nGeneración 0:")
    print(f"Mejor individuo {P[mejor]}")
    print(f"Con {num_est(P[mejor])} parejas estables")
    print(f"y con cardinal {card(P[mejor])}")

    g = 0
    while g < n_generaciones:
        g += 1
        sig_P = []

        #elitismo (nos quedamos con los dos mejores de la anterior población)
        mejores = nMaximos(Fitnesses, 2)
        for j in mejores:
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

                #seleccionamos los dos mejores entre progenitores y descendientes
                aux = list(map(fitness,[des1,des2,prog1,prog2]))
                descendientes = nMinimos(aux,2)
                des1 = [des1,des2,prog1,prog2][descendientes[0]]
                des2 = [des1,des2,prog1,prog2][descendientes[1]]

                #añadimos la descendencia a la sig generación
                sig_P.append(des1)
                sig_P.append(des2)

        P = sig_P
        Fitnesses = list(map(fitness,P))
        mejor = Fitnesses.index(max(Fitnesses))

        print(f"\nGeneración {g}:")
        print(f"Mejor individuo {P[mejor]}")
        print(f"Con {num_est(P[mejor])} parejas estables")
        print(f"y con cardinal {card(P[mejor])}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print('La entrada debe ser: python3 me_genetico.py personas.txt num_generaciones tam_poblacion')
    else:
        fichero = sys.argv[1]
        n_generaciones = sys.argv[2]
        tam = sys.argv[3]

        n_genes, H, M = leer(fichero)

        #definimos a la función fitness
        num_est = lambda ind: num_estables(n_genes,M,H,ind)
        card = lambda ind: cardinal(n_genes,ind)
        fitness = lambda ind: card(ind)

        genetico(M,n_genes,n_generaciones,tam)
