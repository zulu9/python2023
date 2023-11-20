# Tag 11 Übungen
from functools import reduce
# Aufgabe 1
print("\nAufgabe 1")

with open("woerter.txt") as f:
    contents = f.read()
print(contents)
wordlist = str.split(contents)
print(wordlist)

# Aufgabe 2
print("\nAufgabe 2")

clean_wordlist = list(map(lambda s: s.strip(","), wordlist))
clean_wordlist = list(filter(None, clean_wordlist))
lower_wordlist = list(map(str.lower, clean_wordlist))
capitalized_wordlist = list(map(str.capitalize, lower_wordlist))
print(capitalized_wordlist)

with open("woerter_bereinigt.txt", 'w') as f:
    for wort in capitalized_wordlist:
        f.write(wort)
        f.write('\n')

# Aufgabe 3
print("\nAufgabe 3")
laengen = {wort: len(wort) for wort in capitalized_wordlist}
print(laengen)
matches = list(filter(lambda mywort: any(substr in mywort for substr in ["m", "fe", "dr"]), capitalized_wordlist))
print(matches)

# Aufgabe 4
print("\nAufgabe 4")
with open("buchstaben.txt") as f:
    contents = f.read()
print(contents)
contentlist = list(contents)
print(contentlist)
clean_contentlist = list(filter(lambda s: s.strip(","), contentlist))
print(clean_contentlist)
joined = "".join(clean_contentlist).split(" ")
print(joined)

# Aufgabe 5
print("\nAufgabe 5")


def lamesearch(keyword: str, inputstring: str) -> int:
    count = 0
    for word in inputstring.split():
        if keyword in word:
            count += 1
    return count


with open("zen.txt") as f:
    contents = f.read()

# search_for = input("Keyword: ")
search_for = "is"
print(lamesearch(search_for, contents))

# Aufgabe 6
print("\nAufgabe 6")
with open("zahlen.txt") as f:
    contents = f.read()
contentlist = list(contents)
clean_contentlist = list(filter(lambda s: s.strip(","), contentlist))
integer_contentlist = list(map(int, clean_contentlist))
print(integer_contentlist)


# Aufgabe 7
print("\nAufgabe 7")
# integer_contentlist[0]="pferd" # Cause Error


def mysumme(liste: list) -> int:
    summe = 0
    try:
        summe = reduce(lambda x, y: x + y, liste)
    except TypeError:
        summe = "Error"
    finally:
        return summe


def myproduct(liste: list) -> int:
    product = 1
    try:
        product = reduce(lambda x, y: x * y, liste)
    except TypeError:
        product = "Error"
    finally:
        return product


print(mysumme(integer_contentlist))
print(mysumme(integer_contentlist) / len(integer_contentlist))
print(myproduct(integer_contentlist))
print(myproduct(list(filter(lambda element: element != 0, integer_contentlist))))
