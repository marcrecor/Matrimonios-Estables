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

def matrimonios_estables(M,H,n):
    """
    La función matrimonios_estables resuelve el problema de los matrimonios
    estables en el caso del mismo número de hombres que de mujeres
    (heterosexuales), mediante el algoritmo de Gale–Shapley.

    ENTRADA:
    --------
    M : lista de listas de enteros.
        El elemento i-ésimo (la lista i-ésima) corresponde con el ranking
        de los hombres para la mujer i.
    H : lista de listas de enteros.
        El elemento i-ésimo (la lista i-ésima) corresponde con el ranking
        de las mujeres para el hombre i.
    n : entero.
        Número de hombres / mujeres

    SALIDA:
    -------
    parejas : lista de enteros.
        El elemento i-ésimo corresponde con el hombre emparejado con la mujer i.

    """
    hsolos = list(range(n))
    #lista que indica los hombres que no tienen pareja
    #inicialmente todos los hombres están solos
    parejas = [None]*n
    #None significa que la mujer no tiene pareja
    siguiente = [0]*n
    #siguiente es una lista tal que si m es el i-ésimo elemento de la lista,
    #entonces el hombre i ha hecho m propuestas y por tanto la siguiente
    #propuesta que realice tiene que ser a la mujer en el puesto m de su ranking
    #Inicialmente no ha habido propuestas, luego para todos es 0


    for h1 in hsolos: #mientras exista algún hombre sin pareja, tomamos uno h1
        m = H[h1][siguiente[h1]]
        #primera mujer del ranking de las que aún no le ha propuesto h1
        if parejas[m]==None: #si m no tiene pareja
            parejas[m]=h1 #si m está sola tiene que aceptar a h1
            hsolos.pop(hsolos.index(h1)) #h1 deja de estar solo
        else: #si m ya tenía pareja
            h2=parejas[m] #pareja de m
            if (M[m].index(h1))<(M[m].index(h2)):#m prefiere a h1 frente a h2
                parejas[m]=h1 #cambiamos la pareja
                hsolos.pop(hsolos.index(h1)) #eliminamos a h1 de los hombres solos
                hsolos.append(h2) #añadimos a h2 a los hombres solos
        siguiente[h1]+=1 #el hombre h1 ha hecho una nueva propuesta
    return parejas

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('La entrada debe ser: python3 me.py hombres.txt mujeres.txt')
    else:
        ficheroH = sys.argv[1]
        ficheroM = sys.argv[2]

        nH, H = leer(ficheroH)
        nM, M = leer(ficheroM)

        if nH == nM:
            parejas = matrimonios_estables(M,H,nH)
            print(f'El emparejamiento obtenido es: {parejas}')
        else:
            print('Datos incorrectos')
