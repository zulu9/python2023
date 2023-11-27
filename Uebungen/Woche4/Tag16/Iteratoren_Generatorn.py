mylist = ['a','b','c']
print(mylist)
mylist = iter(mylist)
print(mylist)
print(type(mylist))
print(next(mylist))
print(next(mylist))


# Iterator
class Durchzaehlen:
    # create the attributes -> an iterable variable
    def __init__(self, iterable_variable):
        self.iterable_variable = iterable_variable
        self.iterable_object = iter(self.iterable_variable)

    # definition of iteration (beginn of iteration)
    def __iter__(self):
        return self

    # definition on what should be the next element ot iterate
    def __next__(self):
        while True:
            try:
                next_obj = next(self.iterable_object)
                return next_obj
            except StopIteration:
                self.iterable_object = iter(self.iterable_variable)


beispiel = Durchzaehlen('abc')
for i in range(10):
    print(next(beispiel), end=' ')


# Generator
def counter(n):
    for i in range(n+1):
        yield i**2


for num in counter(10):
    print(num)


def counter_norm(n):
    out = []
    for i in range(n+1):
        out.append(i)
    return out


print()
for num in counter_norm(10):
    print(num)

