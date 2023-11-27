## Decorators in functions
def myDecorator(fkt):
    def fktWrapper():
        print("Before function call")
        fkt()
        print("After function call")
    return fktWrapper


@myDecorator
def myFkt():
    print("Inside the function")

myFkt()


## Decorators in classes
def myDecorator(aclass):
    class MyWrapper:
        def __init__(self, *args, **kwargs):
            self.wrapped = aclass(*args, **kwargs)
            # Attribute wrapped ist ein Objekt
            # der Klasse aclass

        def decorated_method(self):
            print("Before method call")
            self.wrapped.original_method()
            print("After method call")

    return MyWrapper


@myDecorator
class MyClass:
    def __init__(self, name):
        self.name = name

    def original_method(self):
        print(f"Hello, {self.name}!")


test = MyClass('Shiva')
test.decorated_method()
