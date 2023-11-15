# Musterloesungen Tag 7
import math
import numpy as np

print('============= Aufgabe 1 =============')
def mySum(beginn, end):
    """
    Calculated the sum from param beginn to param end and returns it
    :param beginn: first number
    :param end: last number
    :return: sum from first to last number
    """
    out = 0
    for i in range(beginn, end + 1):
        out = out + i
    return out


print(mySum(3,25))

print('============= Aufgabe 2 =============')
def aOfSquare(kante):
    """
    Calculates the area of a square
    :param kante: edge of square
    :return: area of the square in unit^2 of kante
    """
    return kante**2

print(aOfSquare(5))

print('============= Aufgabe 3 =============')
def nice(text, size):
    """
        prints box:\n
        +-------------+\n
        |    text     |\n
        +-------------+
    :param text: - str: Input converted to string for inside the box
    :param size: - int: width of the box: number of '-'
    :return: None
    """

    text = str(text)
    text_lenght = len(text)
    spaces = size - text_lenght - 2
    spaces_L = math.floor(spaces / 2)
    spaces_R = math.ceil(spaces / 2)

    print('+' + (size - 2) * '-' + '+')
    print('|' + spaces_L * ' ' + text + spaces_R * ' ' + '|')
    print('+' + (size - 2) * '-' + '+')


nice('Juhu', 25)

print('============= Aufgabe 4 =============')
def mixer(wort, zahl):
    """
    Checks if wort is a string and zahl is a int or float
    :param wort: - str: word to check
    :param zahl: - int/float: number to check
    :return: - dict: {word: zahl}
    """
    if type(wort) == str:
        e1 = wort
    else:
        e1 = str(wort)
    if type(zahl) == int or type(zahl) == float:
        e2 = zahl**2
    else:
        e2 = np.nan
        print('Second Element not a number!')
    return {e1: e2}


print(mixer('Juhu', 3))
print(mixer('Juhu', '3'))

print('============= Aufgabe 5 =============')
def fakulaet(zahl):
    """
    Calculates factual of zahl
    :param zahl: - int
    :return: - int: zahl!
    """
    if type(zahl) == int or type(zahl) == float:
        out = 1
        for i in range(1, zahl + 1):
            out = out * i
    else:
        print(zahl, ' is not a number!')
        out = None # Damit out immer gegeben ist!
    return out


print(fakulaet(4))

print('============= Aufgabe 6 =============')
# Tag 6 Aufgabe 1:
def daySixExOne(begin, end):
    """
    Creates a list of even numbers from begin to end
    :param begin: - int: beginn of range
    :param end: - int: end of range(+1)
    :return: - list: list of even numbers
    """
    out = []
    for i in range(begin, end + 1):
        if i % 2 == 0:
            out.append(i)
    return out


print(daySixExOne(4,90))

# Tag 6 Aufgabe 2:
def daySixExTwo(first, last, max_sum):
    """
    Adds numbers from first to last
    :param first: - int: first number to add
    :param last: - int: last number to add
    :param max_sum: - int: maximal sum
    :return: - dict: {Sum, Last added number}
    """
    stopp_counter = 0
    out = 0
    while first <= last:
        stopp_counter += 1
        if first == 1:
            out = first
        else:
            out = out + first
        first += 1
        if out > max_sum:
            out = out - first
            first -= 1
            break
        # Control statement:
        if stopp_counter > 10000:
            print('Infinity loop, Wuhu!')
            break
    return {'Sum:': out, 'Last added number: ': first}


print(daySixExTwo(first=1, last=50, max_sum=111))

# Tag 6 Aufgabe 4:
def daySixExFour(beginn, end):
    """
    Creates a list of prim numbers between beginn and end
    :param beginn: - int: Start prime number
    :param end: - int: End prime number
    :return: - list: list of prim numbers
    """
    prim_num = []
    prim = False
    for num in range(beginn, end):
        if num > 1:
            for i in range(2, num):
                if (num % i) == 0:
                    prim = True
            if prim:
                prim = False
            else:
                prim_num.append(num)
    return prim_num


print(daySixExFour(2,60))

# Tag 6 Aufgabe 5:
def daySixPW():
    """
    Checks a password through input
    :return: - None
    """
    if input('Give me your password! ') == 'myPassword':
        print('The password is correct!')
    else:
        print('The password is incorrect')


daySixPW()

print('============= Aufgabe 7 =============')

def checkBool(statement):
    """
    Bruteforce function to test a boolean statement in a sting
    Accepts: <,>,>=,<=,!=,==,not
    :param statement: - str: boolean statement as string
    :return: - boolean
    """
    if type(statement) == str:
        out = False
        statement = statement.lstrip()
        marker_not = False
        if statement[:3].lower() == 'not':
            marker_not = True
            statement = statement[3:]

        info = ''
        for key, element in enumerate(statement):
            if element == ' ':
                continue
            if not element.isdigit():
                info = info + element
                if not statement[key + 1].isdigit():
                    info = info + '='
            if not info == '':
                numberleft = int(statement[:key])
                break
        length_operator = len(info)
        numberright = int(statement[key + length_operator:])
        # Brute force! Alles wird überprüft
        if info == '==':
            if numberleft == numberright:
                out = True
        if info == '!=':
            if numberleft != numberright:
                out = True
        if info == '>=':
            if numberleft >= numberright:
                out = True
        if info == '<=':
            if numberleft <= numberright:
                out = True
        if info == '>':
            if numberleft > numberright:
                out = True
        if info == '<':
            if numberleft < numberright:
                out = True
        if marker_not:
            out = not out
        return out
    else:
        print('Statement is not a string!')
        return None


print(checkBool('4 >= 3'))
print(checkBool(' Not 4>=3'))
print(checkBool(4>=3))
