import random
import sys

def puesto(p,P):#puesto de p en el ranking de P
    encontrado = False
    i = 0
    while i<len(P) and not encontrado:
        if (p in P[i]):
            encontrado = True
        i += 1
    if encontrado:
        return i - 1
    else:
        return -1

def indiferencias(ranking,n):
    p = 0
    rank = []
    while p < n:
        q = random.randint(p, n)
        if p != q:
            ind = []
            for i in range(p,q):
                ind.append(ranking[i])
            rank.append(ind)
            p = q
    return rank

def incompletas(m, ranking, LH, n):
    n_elim = random.randint(0, n-1)
    #número de personas que se eliminan del ranking
    for i in range(n_elim):
        p = random.randint(0, n-i-1) #posición del ranking que vamos a eliminar
        h = ranking[p] #hombre correspondiente a esa posición
        puestom = puesto(m,LH[h])
        if len(LH[h][puestom]) == 1:
            if puestom == 0:
                LH[h] = LH[h][1:]
            elif puestom == len(LH[h])-1:
                LH[h] = LH[h][:len(LH[h])-1]
            else:
                LH[h] = LH[h][:puestom] + LH[h][puestom+1:]
        else:
            LH[h][puestom].pop(LH[h][puestom].index(m))
        ranking.pop(p)
    return n-n_elim

def listas(n):
    #si la mujer m no está en la lista del hombre h, entonces el hombre h
    #no está en la lista de la mujer m.
    LM, LH = [], []

    #creamos las listas de los hombres
    for _ in range(n):
        ranking = list(range(n))
        random.shuffle(ranking)
        ranking = indiferencias(ranking, n)
        LH.append(ranking)

    #creamos las listas de las mujeres
    for m in range(n):
        ranking = list(range(n))
        random.shuffle(ranking)
        num = incompletas(m, ranking, LH, n)
        ranking = indiferencias(ranking, num)
        LM.append(ranking)
    return LM, LH

if __name__ == '__main__':
    if len(sys.argv)<2:
        print('La entrada debe ser: python3 crear_listas_meii.py num_pers fichero.txt')
    else:
        num_pers = int(sys.argv[1])
        fichero = sys.argv[2]

        with open(fichero, 'w') as f:

            f.write(f'{num_pers}\n')

            LM, LH = listas(num_pers)

            for i in range(num_pers):
                ranking = LM[i]
                for j in range(len(ranking)):
                    indif = ranking[j]
                    for k in range(len(indif)):
                        f.write(str(indif[k])+' ')

                    if j != len(ranking) -1 :
                        f.write('|')
                f.write('\n')

            f.write('\n')

            for i in range(num_pers):
                ranking = LH[i]
                for j in range(len(ranking)):
                    indif = ranking[j]
                    for k in range(len(indif)):
                        f.write(str(indif[k])+' ')

                    if j != len(ranking) -1 :
                        f.write('|')
                f.write('\n')
