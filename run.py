from jinja2 import FileSystemLoader, Environment
from xlrd import open_workbook
from collections import OrderedDict
from json import dumps


templateLoader = FileSystemLoader( searchpath="templates" )

env = Environment( loader=templateLoader )

TEMPLATE_FILE = "gmina.html"

template = env.get_template( TEMPLATE_FILE )


# outputText = template.render( templateVars )

sheet = open_workbook('dane/gm-kraj.xls').sheet_by_index(0)

candidates = [sheet.cell(0, i).value for i in range(10, 22)]

def generuj_gminy():
    for row in range(1, sheet.nrows):
        FILE = 'gmina' + sheet.cell(row, 1).value + '.html'

        votes = [ int(sheet.cell(row, i).value) for i in range(10, 22) ]

        res_dict = OrderedDict(zip(candidates, votes))

        gmina = sheet.cell(row, 2).value
        powiat = sheet.cell(row, 3).value

        rubryki = ['Uprawnieni do głosowania', 'Wydane karty', 'Wyjęto z urny', 'Nieważne głosy', 'Ważne głosy', 'Frekwencja']
        wartosci = []

        for col in range(5, 10):
            wartosci.append(int(sheet.cell(row, col).value))

        wartosci.append("%.2f" % (wartosci[1] / wartosci[0] * 100))

        ogolne = OrderedDict(zip(rubryki, wartosci))

        lista = [['Kandydat', 'Głosy']]

        for kandydat, glosy in zip(candidates, votes):
            lista.append([kandydat, glosy])


        outputText = template.render({'res_dict' : res_dict, 'gmina' : gmina, 'powiat' : powiat, 'ogolne' : ogolne, 'lista' : dumps(lista)})


        with open('pages/gminy/' + FILE, 'w') as page:
            page.write(outputText)


def generuj_powiaty():
    pass












if __name__ == "__main__":
    generuj_gminy()
    generuj_powiaty()
    #print(outputText)