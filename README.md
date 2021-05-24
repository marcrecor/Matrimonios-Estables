# Matrimonios-Estables
Este repositorio contiene implementaciones para resolver las distintas variantes del problema de los matrimonios estables

Descripción de los ficheros
===========================

1.- me.py
---------

Este fichero resuelve el problema de los matrimonios estables en el caso básico, mediante el algoritmo de Gale-Shapley. Los datos de las listas de los hombres y las mujeres deben pasarse como unos ficheros que sean un parámetro al ejecutar el script. Estos ficheros deben tener la siguiente estructura: su primera línea debe ser el número de personas y las líneas siguientes deben ser cada una la lista de una persona. Cada lista debe contener los números del 0 al (número de personas -1), sin repeticiones.


2.- hospitales.py
-----------------

Este fichero resuelve el problema de los hospitales y los médicos residentes, mediante el algortimo de Gale-Shapley. Los datos de las listas de los hospitales y los residentes deben pasarse como unos ficheros que sea un parámetro al ejecutar el script. El fichero de los hospitales debe tener la siguiente esctructura: su primera línea debe ser el número de hospitales, la segunda línea debe ser la capacidad de cada hospital y el resto de líneas debe ser cada una la lista de un hospital. El fichero de los residentes debe tener la siguiente estructura: su primera línea debe ser el número de residentese y las líneas siguientes debe ser cada una la lista de un residente. Cada lista de hospitales (respectivamente residentes) debe contener los núneros del 0 al (número de residentes -1) (respectivamente al (número de hospitales -1)), sin repeticiones.


3.- meii.py
-----------

Este fichero resuelve el problema de los matrimonios estables en el caso del mismo número de hombres que de mujeres, con indiferencias en sus listas de preferencias, mediante el algoritmo de Gale-Shapley. Los datos de las listas de los hombres y las mujeres deben pasarse como un fichero que sea un parámetro al ejecutar el script. Este fichero debe tener la siguiente estructura: su primera línea debe ser el número de personas, las (número de personas) líneas siguientes se corresponden con las listas de las mujeres mientras que las líneas restantes se corresponden con las listas de los hombres. Cada una de las listas debe contener los números del 0 al (número de personas -1) sin repeticiones, además para marcar la indiferencia se pone el símbolo | .


4.- habitaciones.py
-------------------

Este fichero resuelve el problema de los compañeros de habitación, mediante el algoritmo de Irving. Los datos de las listas de cada persona deben pasarse como un fichero que sea un parámetro al ejecutar el script. El fichero debe tener la siguiente estructura: su primera línea debe ser el número de personas, el resto de líneas debe ser cada una la lista de un residente. Cada lista debe contener los números del 0 al (número de personas -1), sin repeticiones y sin incluir su propio número.

5.- meii_aprox.py
-----------------

Este fichero resuelve el problema de los matrimonios estables con indiferencias y listas incompletas mediante un algoritmo de aproximación. Se trata de una 5/3-aproximación. Los datos de las listas de los hombres y las mujeres deben pasarse como un fichero que sea un parámetro al ejecutar el script. El fichero debe tener la siguiente estructura: su primera línea debe ser el número de personas, las (número de personas) líneas siguientes se corresponden con las listas de las mujeres mientras que las líneas restantes se corresponden con las listas de los hombres. Cada una de las listas debe contener los números del 0 al (número de personas -1) sin repeticiones y pueden no estar todos, además para marcar la indiferencia se pone el símbolo | .

Autor
=====
Marta Crespo Cordero, marcre05@ucm.es
