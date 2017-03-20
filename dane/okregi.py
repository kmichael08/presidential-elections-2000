from json import dump
from collections import OrderedDict

keys = ['dolnośląskie', 'kujawsko-pomorskie', 'lubelskie', 'lubuskie', 'łódzkie',
        'małopolskie', 'mazowieckie', 'opolskie', 'podkarpackie', 'podlaskie',
        'pomorskie', 'śląskie', 'świętokrzyskie', 'warmińsko-mazurskie', 'wielkopolskie',
        'zachodnio-pomorskie']

thresholds = [0, 4, 7, 12, 14, 19, 27, 36, 38, 42, 45, 48, 54, 56, 59, 64, 68]

okregi = [ list(range(i + 1, j + 1)) for i, j in zip(thresholds[:-1], thresholds[1:])]

okregi = [[str(okr) for okr in woj] for woj in okregi]

wojewodztwa = OrderedDict(zip(keys, okregi))

with open('wojewodztwa.json', 'w') as res_file:
    dump(wojewodztwa, res_file)