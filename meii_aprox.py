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

def concat(L):
    M=[]
    for i in range(len(L)):
        M=M+L[i]
    return M

# romper las indiferencias de una lista de manera aleatoria
def romper_indif(Lista): 
    Lista_mod = Lista
    for i in range(len(Lista)):
        for j in range(len(Lista[i])):
            random.shuffle(Lista_mod[i][j])

    return list(map(concat, Lista_mod))

# posición de p en P
def pos(p,P):
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

def sub_score(n,M,M_mod,h):
    for m in range(n):
        if h in M_mod[m] != -1: #si h aparece en la lista de m
            j = pos(h,M[m]) #puesto del ranking
            i = M_mod[m].index(h)
            M_mod[m][j], M_mod[m][i] = M_mod[m][i], M_mod[m][j]

#2-aproximación de Gale-Shapley
def meii(M,H,n):
    """
    La función meii resuelve el problema de los matrimonios estables en el
    caso del mismo número de hombres que de mujeres (heterosexuales), con
    indiferencias y listas incompletas, mediante el algoritmo de Gale–Shapley.

    ENTRADA:
    --------
    M : lista de listas de listas de enteros.
        El elemento i-ésimo (la lista i-ésima) corresponde con el ranking
        de los hombres para la mujer i.
    H : lista de listas de listas de enteros.
        El elemento i-ésimo (la lista i-ésima) corresponde con el ranking
        de las mujeres para el hombre i.

    SALIDA:
    -------
    parejas : lista de enteros.
        El elemento i-ésimo corresponde con el hombre emparejado con la mujer i.

    """
    h_activos = list(range(n))
    #lista que indica los hombres que están activos
    #inicialmente todos los hombres están activos

    h_solos = list(range(n))
    #lista que indica los hombres que están solos
    #inicialmente todos los hombres están solos

    parejas = [-1]*n
    #-1 significa que la mujer no tiene pareja
    siguiente = [0]*n
    #siguiente es una lista tal que si m es el i-ésimo elemento de la lista,
    #entonces el hombre i ha hecho m propuestas y por tanto la siguiente
    #propuesta que realice tiene que ser a la mujer en el puesto m de su ranking
    #Inicialmente no ha habido propuestas, luego para todos es 0


    while h_activos != []: #mientras exista algún hombre activo
        h1 = h_activos[0] #tomamos un hombre activo, h1
        if siguiente[h1] == len(H[h1]): #si no le queda ninguna mujer para proponer
            h_activos.pop(h_activos.index(h1)) #h1 deja de estar activo
        else:
            m = H[h1][siguiente[h1]]
            #primera mujer del ranking de las que aún no le ha propuesto h1
            if parejas[m] == -1: #si m no tiene pareja
                parejas[m] = h1 #si m está sola tiene que aceptar a h1
                h_activos.pop(h_activos.index(h1)) #h1 deja de estar activo
                h_solos.pop(h_solos.index(h1)) #h1 deja de estar solo
            else: #si m ya tenía pareja
                h2=parejas[m] #pareja de m
                if (M[m].index(h1))<(M[m].index(h2)):#m prefiere a h1 frente a h2
                    parejas[m]=h1 #cambiamos la pareja
                    h_activos.pop(h_activos.index(h1)) #eliminamos a h1 de los hombres activos
                    h_solos.pop(h_solos.index(h1)) #eliminamos a h1 de los hombres solos
                    h_activos.append(h2) #añadimos a h2 a los hombres activos
                    h_solos.append(h2) #añadimos a h2 a los hombres solos
            siguiente[h1]+=1 #el hombre h1 ha hecho una nueva propuesta
    return parejas, h_solos

#3/2-aproximación (solo permitidas indiferencias en uno de los dos sexos)
def meii_p(L1,L2,L1_mod,L2_mod,n,solos,parejas,sexo):
    #inicialmente el extra score es 0 para todos
    scores = [0]*n

    #inicialmente todos están inactivos
    activos = []
    #esta intersección será el conjunto de los solos con score 0
    interseccion = solos

    while interseccion != []:
        for p in interseccion:
            scores[p] = 0.5
            if sexo=='h':
                sub_score(n,L2,L2_mod,p)
            #eliminamos p de la intersección
            interseccion.pop(interseccion.index(p))
            activos.append(p) #reactivamos p

        siguiente = [0]*n
        #los activos comienzan proponiendo desde el principio de su lista
        while activos != []: #mientras exista algún activo
            p1 = activos[0] #tomamos un activo, p1
            if siguiente[p1] == len(L1_mod[p1]):
            #si no le queda ninguno para proponer
                    activos.pop(activos.index(p1)) #p1 deja de estar activo
            else:
                q = L1_mod[p1][siguiente[p1]]
                #q es el primero del ranking de los que aún no se ha propuesto p1
                if (sexo=='h' and parejas[q] == -1) or (sexo=='m' and not(q in parejas)):
                    #si q no tiene pareja
                    parejas[q] = p1 #tiene que aceptar a p1
                    activos.pop(activos.index(p1)) #p1 deja de estar activo
                    solos.pop(solos.index(p1)) #p1 deja de estar solo
                    if p1 in interseccion: #si p1 estaba en la intersección
                        interseccion.pop(interseccion.index(p1))
                        #p1 deja de estar en la intersección
                else: #si q ya tenía pareja
                    if sexo=='h':
                        p2=parejas[q] #pareja de q
                    else: #sexo=='m'
                        p2=parejas.index(q)

                    if pos(p1,L2[q]) + scores[p1] < pos(p2,L2[q]) + scores[p2]:
                        #si m prefiere a p1 frente a p2
                        if sexo=='h':
                            parejas[q]=p1
                        else: #sexo=='m'
                            parejas[p1] = q
                            parejas[p2] = -1
                        #cambiamos la pareja

                        activos.pop(activos.index(p1)) #eliminamos a h1 de los activos
                        solos.pop(solos.index(p1)) #eliminamos a h1 de los solos
                        if p1 in interseccion: #si h1 estaba en la intersección
                            interseccion.pop(interseccion.index(p1))
                            #h1 deja de estar en la intersección
                        activos.append(p2) #añadimos a h2 a los hombres activos
                        solos.append(p2) #añadimos a h2 a los hombres solos
                        if scores[p2]==0:
                            interseccion.append(p2)
                siguiente[p1]+=1 #el p1 ha hecho una nueva propuesta

#algoritmo principal
def aprox_meii(M,H,n):
    """
    La función meii resuelve el problema de los matrimonios estables en el
    caso del mismo número de hombres que de mujeres (heterosexuales), con
    listas incompletas para los dos sexos y con indiferencias solo para las
    mujeres, mediante el algoritmo de Gale–Shapley.

    ENTRADA:
    --------
    M : lista de listas de listas de enteros.
        El elemento i-ésimo (la lista i-ésima) corresponde con el ranking
        de los hombres para la mujer i.
    H : lista de listas de enteros.
        El elemento i-ésimo (la lista i-ésima) corresponde con el ranking
        de las mujeres para el hombre i.

    SALIDA:
    -------
    parejas : lista de enteros.
        El elemento i-ésimo corresponde con el hombre emparejado con la mujer i.

    """

    #rompemos los enlaces arbitrariamente
    M_mod = romper_indif(M)
    H_mod = romper_indif(H)

    #aplicamos una vez el algoritmo normal
    parejas, h_solos = meii(M_mod,H_mod,n)


    ########################## TURNO DE LOS HOMBRES
    meii_p(H,M,H_mod,M_mod,n,h_solos,parejas,'h')

    ########################## TURNO DE LAS MUJERES
    m_solas = []
    for i in range(n):
        if parejas[i] == -1:
            m_solas.append(i)

    meii_p(M,H,M_mod,H_mod,n,m_solas,parejas,'m')

    return parejas


#función que comprueba la estabilidad, devuelve el número de parejas estables
def num_estables(n_genes,M,H,ind):
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

if __name__ == "__main__":
    if len(sys.argv) < 1:
        print('La entrada debe ser: python3 meii_aproximación.py personas.txt')
    else:
        fichero = sys.argv[1]

    n, M, H = leer(fichero)


    parejas = aprox_meii(M, H, n)
    print(f'El emparejamiento obtenido es: {parejas}')
    print(f'Número de parejas estables: {num_estables(n,M,H,parejas)}')
