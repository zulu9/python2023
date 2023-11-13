import random
from hashlib import sha256
import time
import matplotlib.pyplot as plotme

# Aufgabe 1
print("\nAufgabe 1")
starttime = time.time()
x = random.randint(1, 100)
for x in range(x, x + 30):
    if x % 2 == 0:
        print(x)
endtime = time.time()
print("Laufzeit: ", endtime - starttime)

# Aufgabe 2
print("\nAufgabe 2")
starttime=time.time()
maximum = 100
x = 1
summe = 1
while x < maximum:
    summe = summe + x
    x += 1
    if summe >= 1000:
        break
print(x-1, summe-x)
endtime =  time.time()
print("Laufzeit: ", endtime - starttime)

# Aufagbe 3
print("\nAufgabe 3")
starttime = time.time()
x = 0
maximum = 20000
def fibo(n):
    if n == 1:
        return [1]
    if n == 2:
        return [1, 1]
    fibs = [1, 1]
    for n in range(2, n):
        fibs.append(fibs[-1] + fibs[-2])
    return fibs

fib = fibo(x)
while fib[-1] < maximum:
    x += 1
    fib = fibo(x)
    print(x, fibo(x))
print(fibo(x-1))
endtime = time.time()
print("Laufzeit: ", endtime - starttime)

# Aufgabe 4
print("\nAufgabe 4")
starttime = time.time()
x = 0
xstart = 0
xend = 100
primes = []
for x in range(xstart, xend):
    is_prime = True
    for i in range(2, x):
        if x % i == 0:
            is_prime = False
    if is_prime:
        primes.append(x)
print(primes)
endtime = time.time()
print("Laufzeit: ", endtime - starttime)

# Aufgabe 5
print("\nAufgabe 5")
starttime = time.time()
# hashed password (passwort)
secret = "33c5ebbb01d608c254b3b12413bdb03e46c12797e591770ccf20f5e2819929b2"
user_input = True
while user_input:
    user_input = input("Passwort eingeben: ")
    user_hash = sha256(user_input.encode('utf-8')).hexdigest()
    if user_hash == secret:
        print("Passwort richtig!")
        break
    else:
        print("Passwort falsch!")
endtime = time.time()
print("Laufzeit: ", endtime - starttime)

# Aufgabe 6
print("\nAufgabe 6")
starttime = time.time()
x = 1
times_list = []
for x in range(x, x + 30):
    starttime_loop = time.time()
    if x % 2 == 0:
        print(x)
    endtime_loop = time.time()
    times_list.append([x, endtime_loop-starttime_loop])
print(times_list)
x_list = []
y_list = []
for sublist in times_list:
    x_list.append(sublist[0])
    y_list.append(sublist[1])
print(x_list)
print(y_list)
plotme.plot(x_list, y_list)
plotme.show()
endtime = time.time()
print("Laufzeit: ", endtime - starttime)
