# Musterloesungen fuer Tag 6: for, if and while

import random
import time
import matplotlib.pyplot as plt
import statistics

print('============= Aufgabe 1 =============')
for num in range(1, 30):
    if num % 2 == 0:
        print(num)

# oder
even_num = [x for x in range(1, 30) if x % 2 == 0]
print(even_num)

rnd_num = random.randint(6, 1000)
for i in range(rnd_num, rnd_num+30):
    if i % 2 == 0:
        print(i)

# oder
even_num = [x for x in range(rnd_num, rnd_num+30) if x % 2 == 0]
print(even_num)

print('============= Aufgabe 2 =============')
num = 1
max_sum = 1000
while num <= 100:
    if num == 1:
        sum_num = num
    else:
        sum_num += num
    if sum_num + num - 1 > max_sum:
        break
    num += 1
print('Sum:', sum_num)
print('Last added number: ', num)

# mit kontrolle
num = 1
counter = 1
max_sum = 100
while num <= 100:
    counter += 1
    if num == 1:
        sum_num = num
    else:
        sum_num += num
    num += 1
    if sum_num > max_sum:
        sum_num = sum_num - num + 1
        num -= 2
        break
    # Control statement:
    #print(t)
    if counter > 10000:
        print('Infinity loop, Wuhu!')
        break

print('Sum:', sum_num)
print('Last added number: ', num)

print('============= Aufgabe 3 =============')
stop_point = 600
fib_out = [0, 1]
while fib_out[-1] < stop_point:
    print(fib_out)
    fib_out.append(fib_out[-1] + fib_out[-2])

# oder

fib_out = [0, 1]
stop_point = 20
i = 0
while i < stop_point:
    fib_out.append(fib_out[i] + fib_out[i + 1])
    i += 1

print(fib_out)

print('============= Aufgabe 4 =============')
prim_num = []
prim = False
for num in range(1, 500):
    if num > 1:
        for i in range(2, num):
            if (num % i) == 0:
                prim = True
        if prim:
            prim = False
        else:
            prim_num.append(num)


print(prim_num)

print('============= Aufgabe 5 =============')
if input(('Give me your password!')) == 'myPassword':
    print('The password is correct!')
else:
    print('The password is incorrect')

print('============= Aufgabe 6 =============')
run_ex_time = []
run_ex_loops = []
test = []
for j in range(20, 10000, 10):
    start = time.time()
    for i in range(0, j):
        if i % 2 == 0:
            print(i)
            x = i + j
            test.append(x)
    end = time.time()
    run_ex_loops.append(len(range(0, j)))
    run_ex_time.append(end-start)
print(run_ex_loops)
print(run_ex_time)


plt.plot(run_ex_time, run_ex_loops, color='b')
plt.show()

print(statistics.mean(run_ex_time))
