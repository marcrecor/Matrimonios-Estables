import random
import sys


if __name__ == '__main__':
    if len(sys.argv)<2:
        print('La entrada debe ser: python3 crear_listas_me.py num_pers fichero.txt')
    else:
        num_pers = int(sys.argv[1])
        fichero = sys.argv[2]

        with open(fichero, 'w') as f:

            f.write(f'{num_pers}\n')

            for _ in range(num_pers):

                ranking = list(range(num_pers))

                random.shuffle(ranking)

                for i in range(len(ranking)):
                    f.write(str(ranking[i])+' ')
                f.write('\n')
