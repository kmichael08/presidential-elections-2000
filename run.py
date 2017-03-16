from jinja2 import FileSystemLoader, Environment
from xlrd import open_workbook
from collections import OrderedDict
from json import dumps

CANDIDATES_NUM = 12

templateLoader = FileSystemLoader( searchpath="templates" )

env = Environment( loader=templateLoader )

TEMPLATE_FILE = "gmina.html"

template = env.get_template( TEMPLATE_FILE )


# outputText = template.render( templateVars )

sheet = open_workbook('dane/gm-kraj.xls').sheet_by_index(0)

candidates = [sheet.cell(0, i).value for i in range(10, 22)]

rubryki = ['Uprawnieni do głosowania', 'Wydane karty', 'Wyjęto z urny', 'Nieważne głosy', 'Ważne głosy', 'Frekwencja']

def generuj_gminy():
    for row in range(1, sheet.nrows):
        FILE = 'gmina' + sheet.cell(row, 1).value + '.html'

        votes = [ int(sheet.cell(row, i).value) for i in range(10, 22) ]

        res_dict = OrderedDict(zip(candidates, votes))

        gmina = sheet.cell(row, 2).value
        powiat = sheet.cell(row, 3).value

        wartosci = []

        for col in range(5, 10):
            wartosci.append(int(sheet.cell(row, col).value))

        wartosci.append("%.2f" % (wartosci[1] / wartosci[0] * 100))

        ogolne = OrderedDict(zip(rubryki, wartosci))

        diagram = [['Kandydat', 'Głosy']]

        for kandydat, glosy in zip(candidates, votes):
            diagram.append([kandydat, glosy])


        outputText = template.render({'res_dict' : res_dict, 'gmina' : gmina, 'powiat' : powiat, 'ogolne' : ogolne, 'diagram' : dumps(diagram)})


        with open('pages/gminy/' + FILE, 'w') as page:
            page.write(outputText)

class Powiat:

    def __init__(self, kod, nazwa):
        self.kod = kod
        self.nazwa = nazwa
        self.gminy = []
        self.votes = [0] * CANDIDATES_NUM
        self.ogolne = OrderedDict(zip(rubryki, [0] * 6))
        self.res_dict = OrderedDict(zip(candidates, self.votes))

    """ Update given a row. """
    def update(self, row):
        self.gminy.append(row[2].value)
        for g1, i in zip(row[10:22], range(CANDIDATES_NUM)):
            self.votes[i] += int(g1.value)

        for key, g1 in zip(self.res_dict.keys(), self.votes):
            self.res_dict[key] = g1

        wartosci = []

        for col in range(5, 10):
            wartosci.append(int(row[col].value))

        for rubryka, wartosc in zip(rubryki[:-1], wartosci):
            self.ogolne[rubryka] += wartosc

        self.ogolne['Frekwencja'] = "%.2f" % (self.ogolne['Wydane karty'] / self.ogolne['Uprawnieni do głosowania'] * 100)

def generuj_powiaty():
    powiaty = OrderedDict()
    for row in range(1, sheet.nrows):
        kod = sheet.cell(row, 1).value[:4]
        nazwa = sheet.cell(row, 2).value
        powiaty[kod] = Powiat(kod, nazwa)

    for row in range(1, sheet.nrows):
        kod = sheet.cell(row, 1).value[:4]
        powiaty[kod].update(sheet.row(row))


    for powiat in powiaty.values():
        FILE = 'powiat' + powiat.kod + '.html'


        diagram = [['Kandydat', 'Głosy']]

        for kandydat, glosy in zip(candidates, powiat.votes):
            diagram.append([kandydat, glosy])

        outputText = template.render({'res_dict' : powiat.res_dict, 'powiat' : powiat.nazwa, 'ogolne' : powiat.ogolne, 'diagram' : dumps(diagram)})

        with open('pages/powiaty/' + FILE, 'w') as page:
            page.write(outputText)










if __name__ == "__main__":
    generuj_gminy()
    generuj_powiaty()
    #print(outputText)