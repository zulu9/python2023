# Musterlösungen Tag 4

import datetime as dt

print('============= Aufgabe 1 =============')
birth_shiva = dt.date(2016, 3, 23)
age_shiva = dt.date.today() - birth_shiva
print('Shiva is ' + str(age_shiva.days) + 'days old')

print('============= Aufgabe 2 =============')
date_chaos = open('Datumsspass.txt', 'r')
date_clean = date_chaos.readlines()
print(date_clean) # Einmal betrachten wie die Formate aussehen

print('============= Aufgabe 3 =============')
date_clean[0] = 'Datums Ordnung:\n'

temp = date_clean[1]
temp = dt.datetime.strptime(temp, '%d.%m.%y\n')
date_clean[1] = temp.strftime('%A, %d.%B %Y')
temp = date_clean[2]
temp = dt.datetime.strptime(temp, '%A, the %d. %B %Y\n') # Hier ist pyton nicht casesenitive! monday und Monday ist fuer den interpreter hier das Selbe
date_clean[2] = temp.strftime('%A, %d.%B %Y')
temp = date_clean[3]
temp = dt.datetime.strptime(temp, '%d-%m-%Y\n')
date_clean[3] = temp.strftime('%A, %d.%B %Y')
temp = date_clean[4]
temp = dt.datetime.strptime(temp, '%m/%d/%Y\n')
date_clean[4] = temp.strftime('%A, %d.%B %Y')
temp = date_clean[5]
temp = dt.datetime.strptime(temp, '%d-%m/%y')
date_clean[5] = temp.strftime('%A, %d.%B %Y')
print(date_clean)
# Datumsumwandlungen sind immer eine Konzentrationsarbeit! Die hat weniger damit zu tun, ob Sie programmieren koennen und mehr
# damit zu tun, ob Sie sich gerade konzentrieren koennen. Mir passieren dort auch schnell Fehler, wenn es geht umgehe ich das immer

print('============= Aufgabe 4 =============')
date_save = date_clean[0] + \
            date_clean[1] + '\n' + \
            date_clean[2] + '\n' + \
            date_clean[3] + '\n' + \
            date_clean[4]
open('Datumsordnung.txt', 'w').write(date_save)

print('============= Aufgabe 5 =============')
name = input('What\'s your name? >>')
color = input('What\'s your favorite color? >>')
animal = input('What\'s your favorite animal? >>')

out_txt = 'Some Questions:' + '\n' + \
          'Name: ' + name + '\n' + \
          'Favorite color: ' + color + '\n' + \
          'Favorite animal: ' + animal
out_csv = 'Some Questions:' + ',' + 'Some Anwers:' + '\n' \
          'Name: ' + ',' + name + '\n' + \
          'Favorite color: ' + ',' + color + '\n' + \
          'Favorite animal: ' + ',' + animal
open('Questions.txt', 'w').write(out_txt)
open('Questions.csv', 'w').write(out_csv)

# im .csv erzeugt '\n' eine neue Zeile und ',' eine neue Spalte

# Stadtlandfluss ist in Stadtlandfluss.py
