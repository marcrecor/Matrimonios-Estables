#leer las listas
import sys

def leer(fichero, t):
    with open(fichero, 'r') as f:

        texto = f.read()

        lineas = texto.splitlines()

        num = int(lineas[0])
        if t == 'h':
            c = lineas[1].split()
            lista = lineas[2:]
        else:
            c = []
            lista = lineas[1:]

        for i in range(num):
            lista[i] = lista[i].split()
            for j in range(len(lista[i])):
                lista[i][j] = int(lista[i][j])

    return num, lista, c

def hospitales(R,H,c,n,m):
    """
    la función hospitales resuelve el problema de los hospitales y los
    residentes, mediante el algoritmo de Gale-Shapley.

    ENTRADA:
    --------
    R : lista de listas de enteros.
        El elemento i-ésimo (la lista i-ésima) corresponde con el ranking
        de los hospitales para el residente i.
    H : lista de listas de enteros.
        El elemento j-ésimo (la lista j-ésima) corresponde con el ranking
        de los residentes para el hospital j.
    c : lista de enteros.
        El elemento j-ésimo corresponde con la capacidad del hospital j.
    n : entero.
        Número de residentes
    m : entero.
        Número de hospitales

    SALIDA:
    -------
    residentes : lista de listas de enteros.
        El elemento j-ésimo corresponde con la lista de los residentes
        que se les ha asignado el hospital j.
        Si algún hospital no llena su capacidad:None

    """
    rsolos = list(range(n))
    #rsolos es una lista que indica los residentes sin hospital
    #inicialmente todos los residentes no tienen hospital
    numres = [0]*m #número de residentes asignados por hospital
    siguiente = [0]*n #número de hospitales que ha propuesto cada residente

    residentes = []
    for i in list(range(m)):
        residentes+=[[None]*c[i]]
    #residentes es una lista de listas de enteros.
    #La lista j-ésima corresponde con los residentes del hospital j.
    #None significa que hay un puesto vacío en el hospital.

    while rsolos != []: #mientras algún residente no tenga hospital asignado
        r=rsolos[0] #tomamos un residente sin hospital, r
        h = R[r][siguiente[r]]
        #primer hospital del ranking de r de los que no le han rechazado
        if numres[h]<c[h]: #si el hospital no ha alcanzado la capacidad máxima
            residentes[h][numres[h]]=r #a r se le asigna h
            numres[h]+=1 #h tiene un residente más
            rsolos.pop(rsolos.index(r)) #r ya tiene hospital
        else: #si el hospital ya tiene el número máximo de residentes
            peor=rpeor(H[h],residentes[h])
            #residente peor de los que están en h (desde el punto de vista de h)
            if H[h].index(r) < H[h].index(peor):
                #si el hospital prefiere a r frente a peor
                residentes[h][residentes[h].index(peor)]=r #cambio de residente
                rsolos.pop(rsolos.index(r)) #r ya tiene hospital
                rsolos.append(peor) #el otro residente pasa a estar solo
        siguiente[r]+=1 #el residente ha agotado un hospital más
    return residentes


def rpeor(ranhos,res):
    """
    la función rpeor nos indica cual es el peor residente (desde el punto
    de vista del hospital) de los que hay actualmente en el hospital.

    ENTRADA:
    --------
    ranhos : lista de enteros.
        ranking de los residentes para el hospital.
    res : lista de enteros.
        residentes actuales del hospital.

    SALIDA:
    -------
    p : entero.
        peor residente (para el hospital) de los que hay ahora.

    """
    p = res[0]
    for i in list(range(1,len(res))): #recorremos todos los residentes del hospital
        if ranhos.index(res[i])>ranhos.index(p):
            #si el residente siguiente es peor que el que teníamos
            p=res[i] #cambiamos el residente
    return p

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('La entrada debe ser: python3 hospitales.py residentes.txt hospitales.txt')
    else:
        ficheroR = sys.argv[1]
        ficheroH = sys.argv[2]

        nR, R, _ = leer(ficheroR,'r')
        nH, H, c = leer(ficheroH,'h')

        parejas = hospitales(R,H,c,nR,nH)
        print(f'El emparejamiento obtenido es: {parejas}')
