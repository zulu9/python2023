''' 4 Methods to calculate the fibonacci sequenz '''

print('''As recursiv function''')
def fib_recu(n):
   if n <= 1:
       return n
   else:
       return(fib_recu(n-1) + fib_recu(n-2))

for i in range(14):
    print(fib_recu(i))


print(''' As iterator ''')
class fib_iter():
    def __init__(self, howMany):
        self.counter = howMany
        self.curFib = -1
        self.nextFib = 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.counter == 0:
            raise StopIteration

        self.counter -= 1

        nextFib = self.curFib + self.nextFib
        self.curFib = self.nextFib
        self.nextFib = nextFib

        return self.curFib


for fib in fib_iter(14):
    print(fib)

print(""''' As generator '''"")
stop_point = 600
fib_out = [0, 1]
while fib_out[-1] < stop_point:
    print(fib_out)
    fib_out.append(fib_out[-1] + fib_out[-2])


print(''' As generator function ''')
def fib_fkt():
    a = 0
    b = 1
    while True:
        yield a
        a, b = b, a + b


counter = 0
stop_counter = 14
for x in fib_fkt():
    print(x, " ", end="")
    counter += 1
    if counter > stop_counter:
        break
