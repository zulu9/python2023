import datetime as dt
print('~~~======================================~~~')
print('~~~~~~~====== Stadt Land Fluss ======~~~~~~~')
print('~~~======================================~~~')
print()

results = {'name': ['What\'s your name? ', 'nothing'],
           'letter': ['Chose a letter to play: ', 'nothing'],
           'city': ['City: ', 'nothing'],
           'country': ['Country: ', 'nothing'],
           'river': ['River: ', 'nothing'],
           'color': ['Color: ', 'nothing'],
           'animal': ['Animal: ', 'nothing'],
           'time': ['Your time: ', 'nothing']}

num_wrong = 0

print('Let\'s beginn!')
print()
results['name'][1] = input(results['name'][0])
results['letter'][1] = input(results['letter'][0])
letter = results['letter'][1]
print()
print('                 ~~~ START ~~~')
start = dt.datetime.now()
results['city'][1] = input(results['city'][0])
if results['city'][1][0].lower() != letter.lower():
    results['city'][1] = 'Wrong Letter!'
    num_wrong += 1

results['country'][1] = input(results['country'][0])
if results['country'][1][0].lower() != letter.lower():
    results['country'][1] = 'Wrong Letter!'
    num_wrong += 1

results['river'][1] = input(results['river'][0])
if results['river'][1][0].lower() != letter.lower():
    results['river'][1] = 'Wrong Letter!'
    num_wrong += 1

results['color'][1] = input(results['color'][0])
if results['color'][1][0].lower() != letter.lower():
    results['color'][1] = 'Wrong Letter!'
    num_wrong += 1

results['animal'][1] = input(results['animal'][0])
if results['animal'][1][0].lower() != letter.lower():
    results['animal'][1] = 'Wrong Letter!'
    num_wrong += 1

end = dt.datetime.now()
diff = end - start
print('                 ~~~ END ~~~')
print('Your time: ', diff)
results['time'][1] = str(diff)

out = '~~~======================================~~~\n' + \
      '~~~~~~~====== Stadt Land Fluss ======~~~~~~~\n' + \
      '~~~======================================~~~' + '\n\n' + \
    results['name'][0] + results['name'][1].title() + '\n' + \
    results['letter'][0] + letter.title() + '\n' + \
    '~~~======================================~~~' + '\n' + \
    results['city'][0] + results['city'][1].title() + '\n' + \
    results['country'][0] + results['country'][1].title() + '\n' + \
    results['river'][0] + results['river'][1].title() + '\n' + \
    results['color'][0] + results['color'][1].title() + '\n' + \
    results['animal'][0] + results['animal'][1].title() + '\n' + \
    '~~~======================================~~~' + '\n' + \
    results['time'][0] + results['time'][1] + ' s' + '\n' + \
    'Number of wrong letters: ' + num_wrong

open(f'StadtLandFluss_{results["name"][1]}_{letter.title()}_{str(start.time().hour) + "_" + str(start.time().minute)}.txt', 'w').write(out)
