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
                lista[i][j] = int(lista[i][j])

    return num_pers, lista

def habitacion(P, n):
    """
    La función habitacion resuelve el problema de los compañeros de habitación
    (tiene que haber 2n personas).

    ENTRADA:
    --------
    P : lista de listas de enteros.
        El elemento i-ésimo (la lista i-ésima) corresponde con el ranking
        de las demás personas para la persona i.
    n : entero.
        Número de personas.
    """
    propuestas = [None]*n
    #elemento i es la persona que ha aceptado la propuesta de la persona i
    nprop = [0]*n
    #el elemento i es el número de propuetas que ha hecho la persona i

    fase1(P,0,0,propuestas,nprop)

    if (None) in propuestas : #una persona ha sido rechazada por todas
        print('Una persona ha sido rechazada por todas, no existe emparejamiento estable')
    else: #todos han aceptado alguna propuesta
        #reducimos la tabla de H actual
        k=0
        while k<n:
            reducir(P,k,propuestas[k])
            k+=1
        w=fase2(P)
        print(f'El emparejamiento obtenido es: {w}')

def fase1(P,p,r,propuestas,nprop):
    if p < len(P) and not((len(P)-1) in nprop):
    #si Pay personas que aún no han propuesto y no hay ninguna
    #que haya sido rechazada por todas las demás
        sig = P[p][nprop[p]] #persona que le toca proponer a p
        nprop[p]+=1 #p va a hacer una propuesta
        if sig in propuestas:
        #sig ya había aceptado una propuesta
            ant=propuestas.index(sig) #persona a la que había aceptado sig
            if P[sig].index(p) < P[sig].index(ant):
            #p es mejor que ant para sig
                propuestas[p]=sig #sig acepta a p
                propuestas[ant]=None #sig rechaza a ant
                p=ant #ant es el próximo en proponer
            #si p es peor que ant para sig: p sigue proponiendo

            fase1(P,p,r,propuestas,nprop)
        else:
        #sig no había aceptado ninguna propuesta
            propuestas[p]=sig #sig acepta a p
            fase1(P,r+1,r+1,propuestas,nprop)
            #propone la siguiente persona que nunca haya propuesto

def reducir(P,p,q):
    #q aceptó a p
    puestop=P[q].index(p) #puesto de p en el ranking de q
    if puestop != len(P)-1: #si p no está en último lugar
        sucp = P[q][puestop +1:] #sucesores de p en el ranking de q
        for x in sucp:
            P[x].pop(P[x].index(q))
            #eliminamos q del ranking de cada sucesor de p
        P[q]=P[q][:puestop+1]
        #eliminamos los sucesores de p del ranking de q

def num(P):
    #numero de personas de cada ranking
    b=[]
    for i in list(range(len(P))):
        b.append(len(P[i]))
    return b

def fase2(P):
    while not([] in P) and num(P)!=[1]*(len(P)):
    #mientras todos los rankings tienen al menos un elemento y existe algún
    #ranking con más de una persona
        rot = buscarrot(P) #buscamos una rotación
        eliminarrot(rot,P) #eliminamos esa rotación

    if ([] in P): #si hay algun ranking vacío
        print('No existe emparejamiento estable')
    else: #si todos los rankings tienen una única persona
        return formarparejas(P)

def formarparejas(P):
    #dada la lista de rankings con un solo elemento calcula las parejas
    #que se forman
    x=[]
    y=[]
    L=list(range(len(P)))
    for i in L:
        x.append(P[i][0])
    while L != []:
        i=L[0]
        y.append((i,x.index(i)))
        L.pop(L.index(i))
        L.pop(L.index(x.index(i)))
    return y


def primer(num):
    #devuelve primera persona cuyo ranking tiene más de dos personas
    b=True
    i=0
    while b and i<len(num):
        b=(num[i]==1)
        i+=1
    return i-1

def buscarrot(H):
    #busca una rotación
    longs=num(H)
    x=primer(longs) #primera persona cuyo ranking tiene más de una persona
    q=H[x][1] #segunda persona del ranking de x
    Q=[q]
    P=[H[q][longs[q]-1]] #ultima persona del ranking de q
    i=0

    while (P[i] != x):
        q = H[P[i]][1]
        #q es la segunda persona del ranking de P[i]
        Q.append(q)
        p=H[q][longs[q]-1]
        #p es la última persona del ranking de q
        P.append(p)
        i+=1

    P=[P.pop(len(P)-1)]+P #movemos el último elemento al primer puesto
    Q=[Q.pop(len(Q)-1)]+Q #movemos el último elemento al primer puesto

    return list(zip(P,Q))


def eliminarrot(rot,H):
    #dada una rotación y una lista de rankings, reduce la última
    i=0
    while i < len(rot)-1:
        x=rot[i][0]
        y=rot[i+1][1]
        reducir(H,x,y)
        i+=1
    x=rot[i][0]
    y=rot[0][1]
    reducir(H,x,y)

if __name__ == '__main__':
    if len(sys.argv) < 1:
        print('La entrada debe ser: python3 habitaciones.py personas.txt')
    else:
        fichero = sys.argv[1]

        n, P = leer(fichero)

        habitacion(P, n)
