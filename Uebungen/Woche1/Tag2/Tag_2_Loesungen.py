# Musterlösungen Tag 2

print('============= Aufgabe 1 =============')
x = 2/4 #float
print(type(x))
print(x)
print(int(x))


print('============= Aufgabe 2 =============')
schlecht_les = 1000000
gut_les = 1_000_000
print(schlecht_les)
print(gut_les)
print(type(schlecht_les), type(gut_les))

print('============= Aufgabe 3 =============')
print(3 > 2)
print(5 != 6)
print(5 == 2)
print(3 < 2 or 2 > 1)
print(5 != 9 and 7 < 10)
print(not 5 != 9 and not 7 < 10)
print((not 5 != 9 and 7 < 10) or 2*3 > 7)
print(not (5 != 9 and 7 < 10) or 2*3 > 7)

print('============= Aufgabe 5 =============')
import math as m
print(m.sqrt(9))

print('============= Aufgabe 6 =============')
x_inf = m.inf
x_minf = -m.inf

print(x_inf, x_minf)

print('============= Aufgabe 7 =============')
print(m.pi*m.e)

print('============= Aufgabe 8 =============')
print(m.log(3,10))
print(m.log10(3))
print(m.log(3, m.e))
print(m.log(3)) # e ist die Standardbasis

print('============= Aufgabe 9 =============')
import numpy as np
mylist = [1, 2, 3, 4]
print(np.mean(mylist))
print(np.sum(mylist))
print(np.std(mylist, ddof=1))
# ddof = Means Delta Degrees of Freedom = Freiheitsgrade, default ist 0, ein array hat allerdings 1 ;)
# Statistik ist was tolles :D
