import datetime as dt
print('~~~======================================~~~')
print('~~~~~~~====== Stadt Land Fluss ======~~~~~~~')
print('~~~======================================~~~')
print()

print('Let\'s beginn!')
print()
# In Version 1 wird jede Antwort, die eingegeben wird als seperate Variable abgespeichert und am Ende zusammengefuegt
name = input('What\'s your name? >> ')
letter = input('Chose a letter to play: >> ')
print()
print('                 ~~~ START ~~~')
start = dt.datetime.now() # Startzeit definieren
city = input('City: >> ')
country = input('Country: >> ')
river = input('River: >> ')
color = input('Color: >> ')
animal = input('Animal: >> ')
end = dt.datetime.now() # Endzeit definieren
diff = end - start #Differenz berechnen fuer Ausgabe
print('                 ~~~ END ~~~')
print('Your time: ', diff.seconds, ' s') # diff.seconds gibt nur den Sekundenanteil raus, macht die Darstellung schoener

#Output schreiben: mit \ am Ende wird die naechste Zeile (mit Einrueckung!) zum String gezaehlt, dies macht die Output Erstellung besser lesbar
out = '~~~======================================~~~\n' + \
      '~~~~~~~====== Stadt Land Fluss ======~~~~~~~\n' + \
      '~~~======================================~~~' + '\n\n' + \
    'Name: ' + name + '\n' + \
    'Letter: ' + letter + '\n' + \
    '~~~======================================~~~' + '\n' + \
    'City: ' + city + '\n' + \
    'Country: ' + country + '\n' + \
    'River: ' + river + '\n' + \
    'Color: ' + color + '\n' + \
    'Animal: ' + animal + '\n' + \
    '~~~======================================~~~' + '\n' + \
    'Your time: ' + str(diff.seconds) + ' s'

open('StadtLandFluss_v1.txt', 'w').write(out)
