# Tag 15 Tests
def my_decorator(fkt):
    def fkt_wrapper():
        print("Before funcion call")
        fkt()
        print("After function call")
    return fkt_wrapper


@my_decorator
def myfkt():
    print("Inside the function")


myfkt()
