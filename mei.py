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

def indiferencia(M,H,n):
    """
    La función indiferencia resuelve el problema de los matrimonios estables
    en el caso del mismo número de hombres que de mujeres (heterosexuales)
    con indiferencias, calculando una solución débilmente-estable.

    ENTRADA:
    --------
    M : lista de listas de listas de enteros.
        El elemento i-ésimo (la lista i-ésima) corresponde con el ranking
        de los hombres para la mujer i. Cada elemento del ranking es a su
        vez una lista con los hombres con indiferencia para ese puesto.
    H : lista de listas de listas de enteros.
        El elemento i-ésimo (la lista i-ésima) corresponde con el ranking
        de las mujeres para el hombre i. Cada elemento del ranking es a su
        vez una lita con las mujeres con indiferencia para ese puesto.
    n : entero.
        Número de hombres / mujeres

    SALIDA:
    -------
    parejas : lista de enteros.
        El elemento i-ésimo corresponde con el hombre emparejado con la mujer i.
    """
    hsolos = list(range(n)) #todos los hombres estan sin pareja
    parejas = [None]*n #el elemento i corresponde con la pareja de la mujer i
    #None significa que la mujer no tiene pareja
    siguiente = [[0]*n,[0]*n]
    #primera lista: elemento i corresponde con el siguiente puesto del ranking
    #al que tiene que proponerse el hombre i.
    #segunda lista: elemento i corresponde con el siguiente puesto dentro del
    #puesto del ranking (dentro de la indiferencia) al que tiene que proponerse
    #el hombre i.

    while hsolos != []: #mientras exista algun hombre sin pareja
        for h in hsolos: #tomamos un hombre, h, sin pareja

            m = H[h][siguiente[0][h]][siguiente[1][h]]
            #primera mujer del ranking a la que aun no ha propuesto h

            if parejas[m] != None: #si m teni�a pareja
                h2 = parejas[m] #h2 es la pareja actual de m
                hsolos.append(h2) #h2 vuelve a estar solo

            parejas[m]=h #h es pareja de m
            hsolos.pop(hsolos.index(h)) #h deja de estar solo

            if puesto(h,M[m]) != (len(M[m])-1):#si h no esta en el ultimo puesto
                eliminar(M,H,m,h,siguiente)
            #si esta en el ultimo puesto no tiene sucesores y por tanto
            #no hay que eliminar nada

            mod_siguiente(H,h,siguiente) #h ha hecho una propuesta
    return parejas

def eliminar(M,H,m,h,siguiente):
    ph=puesto(h,M[m]) #puesto de h en el ranking de m

    suc=M[m][ph+1:] #sucesores de h para m (lista de listas)
    M[m]= M[m][:ph+1] #eliminamos los sucesores del ranking de m

    for i in list(range(len(suc))):
        for j in list(range(len(suc[i]))):
            s=suc[i][j] #s es sucesor de h en el ranking de m
            pm=puesto(m,H[s]) #puesto de m para s

            #modificamos siguiente
            if (pm < siguiente[0][s]) and (len(H[s][pm])==1):
            #si s hab�a propuesto a m y no hay indiferencia con m
                siguiente[0][s]-=1
            elif (pm == siguiente[0][s]) and (H[s][pm].index(m)<siguiente[1][s]):
            #si s ya ha propuesto a m y est� proponiendo en puesto que est� m
                siguiente[1][s]-=1
            #si s hab�a propuesto a m, hab�a indiferencia y ahora estaba
            #proponiendo en un puesto diferente o si a�n no hab�a propuesto
            #no es necesario modificar siguiente

            #eliminamos m del ranking de s
            if len(H[s][pm])==1: #si no hay indiferencia con m
                H[s].pop(pm) #eliminamos el puesto entero del ranking
            else: #si hay indifernecia con m
                H[s][pm].pop(H[s][pm].index(m)) #eliminamos solo m en el puesto

def mod_siguiente(H,h,siguiente):
    if siguiente[1][h]==(len(H[h][siguiente[0][h]])-1):
    #si h ya se ha propuesto a todas las mujeres del mismo puesto del ranking
        siguiente[1][h]=0 #tiene que pasar al siguiente puesto del ranking
        siguiente[0][h]+=1 #y la primera mujer dentro de la indiferencia
    else: #si aun quedan mujeres en ese puesto del ranking
        siguiente[1][h]+=1


def puesto(p,ranking):
    #indica el puesto de p dentro del ranking
    i = 0
    while i<(len(ranking)) and (not(p in ranking[i])):
        i+=1
    return i

if __name__ == '__main__':
    if len(sys.argv) < 1:
        print('La entrada debe ser: python3 mei.py personas.txt')
    else:
        fichero = sys.argv[1]

        n, H, M = leer(fichero)

        parejas = indiferencia(M,H,nH)
        print(f'El emparejamiento obtenido es: {parejas}')
