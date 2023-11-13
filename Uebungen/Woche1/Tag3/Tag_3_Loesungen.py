# Musterlösungen Tag 3

import datetime as dt
print(dt.time(10,5,8,10))
print('============= Aufgabe 1 =============')
now_time = dt.datetime.now()
print(now_time)

print('============= Aufgabe 2 =============')
# str() uebersetzt ein datetime-Objekt zu string, damit es zusammen im Output geprinted werden kann
print('Nur das Jahr: ' + str(now_time.year))
print('Nur der Monat: ' + str(now_time.month))
print('Nur die Stunde: ' + str(now_time.hour))
print('Nur die Minute: ' + str(now_time.minute))
print('Nur die Sekunde: ' + str(now_time.second))
print('Nur die Milisekunde: ' + str(now_time.microsecond))
# str() ubersetzt nur genau so das Format -> fuer Formatsanderungen muss strptime() verwendet werden

print('============= Aufgabe 3 =============')
# io ist fuer I/O (Input/Output) streams, d.h. hiermit kann der String aus import this gelesen werden
# contextlib ist fuer context managment mit with
# Die Packages werden in der Kombination benoetigt, weil das eine ermoeglicht den String aus this zu lesen (io)
# und contextlib es ermoeglicht den String in einem Objekt im Script zu hinterlegen
import io, contextlib
with contextlib.redirect_stdout(zen := io.StringIO()): # hier wird in das Objekt zen der String aus this mithilfe von io hinterlegt
    import this
print(type(zen)) # zen ist erstmal in io.string, also eine bestimmte Form von string
pythonZen = zen.getvalue() # getvalue liest den tatsaechlichen string aus
print(pythonZen)


print('============= Aufgabe 4 =============')
print(pythonZen.replace('P', ''))

print('============= Aufgabe 5 =============')
print(pythonZen.split('y'))

print('============= Aufgabe 6 =============')
print(pythonZen.split('.'))

print('============= Aufgabe 7 =============')
print(pythonZen.replace('y', 'Y'))

print('============= Aufgabe 8 =============')
print(pythonZen.index('Complex'))
# index() ist hier der Befehl, weil ein String auch nur eine list ist

print('============= Aufgabe 9 =============')
print(pythonZen.count('than'))


print('============= Aufgabe 10 =============')
# Ersetzten von . durch {}
pythonZen_2 = pythonZen.replace('.', '{}')
# Zaehlen von {}
print(pythonZen_2.count('{}'))

print(tuple(range(0, pythonZen_2.count('{}'))))

pythonZen_2 = pythonZen_2.format(*tuple(range(0, pythonZen_2.count('{}'))))
# es kann hier ein tuple oder eine list sein, da nur gelesen wird ist es egal
# der * ist dafuer da um das Argument (die list oder das tuple) zu entpacken, d.h. es wird benoetigt, damit python auf die einzelnen Elemente zugreift
# und nicht die gesamte list/tuple als ein Argument sieht
#pythonZen_2 = pythonZen_2.format(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17)

print(pythonZen_2)

print('============= Aufgabe 11 =============')
# Ob mit oder ohne Ersetzung ueberprueft wird ist hier egal (laenge unterscheidet sich, aber Sie sollen nur den richtigen Befehl verwenden ;))
print(len(pythonZen_2))

print('============= Aufgabe 12 =============')
print(pythonZen_2.count(' '))

print('============= Aufgabe 13 =============')
pythonZen_3 = pythonZen_2.replace(' ', '')
pythonZen_3.replace('.', '')
print(pythonZen_3)

print('============= Aufgabe 14 =============')
myname = 'Christina Meyer'

print('============= Aufgabe 15 =============')
myname_short = myname.replace(' ', '')
print(myname_short)

print('============= Aufgabe 16 =============')
print(myname.upper())
print(myname.lower())
print(myname.title()) # capitalize() mach geanu das selbe
print(myname.title().swapcase())

print('============= Aufgabe 17 =============')
myname = myname + ' ' + '31'
print(myname)

print('============= Aufgabe 18 =============')
print(myname.zfill(3 + len(myname)))
