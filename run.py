from jinja2 import FileSystemLoader, Environment
from xlrd import open_workbook
from collections import OrderedDict
from json import dumps, load

CANDIDATES_NUM = 12

templateLoader = FileSystemLoader( searchpath="templates" )

env = Environment( loader=templateLoader )

TEMPLATE_FILE = "gmina.html"

template = env.get_template( TEMPLATE_FILE )

# outputText = template.render( templateVars )

sheet = open_workbook('dane/gm-kraj.xls').sheet_by_index(0)

candidates = [sheet.cell(0, i).value for i in range(10, 22)]

rubryki = ['Uprawnieni do głosowania', 'Wydane karty', 'Wyjęto z urny', 'Nieważne głosy', 'Ważne głosy', 'Frekwencja']

class Unit:

    def __init__(self, name, typ):
        self.subunits = OrderedDict()
        self.votes = []
        self.ogolne = OrderedDict()
        self.name = name
        self.typ = typ
        self.destination = 'pages/' + self.typ + '/' + str(self.name)

    def add_subunit(self, name, typ):
        if name not in self.subunits:
            self.subunits[name] = Unit(name, typ)
        return self.subunits[name]

    # calculate based on the lowest
    def update(self):
        pass

    def generate(self):
        self.res_dict = OrderedDict(zip(candidates, self.votes))
        outputText = template.render({'res_dict' : self.res_dict, 'ogolne' : self.ogolne})
        with open(self.destination, 'w') as page:
            page.write(outputText)



polska = Unit('Polska', 'kraj')
okregi_dict = OrderedDict()
gminy_dict = OrderedDict()

def add_row(row):
    okr_num = int(row[0].value)
    gmina = row[2].value
    powiat = row[3].value
    gminy_dict[gmina] = okregi_dict[okr_num].add_subunit(powiat, 'powiat').add_subunit(gmina, 'gmina')


def make_tree():
    with open('dane/wojewodztwa.json', 'r') as woj:
        woj_dict = load(woj)

    for woj, okregi in woj_dict.items():
        wojewodztwo = polska.add_subunit(woj, 'woj')
        for okreg in okregi:
            okr_obj = wojewodztwo.add_subunit(okreg, 'okr')
            okregi_dict[okreg] = okr_obj

    for row in list(sheet.get_rows())[1:]:
        add_row(row)


def dfs_print(unit):
    print(unit.destination, unit.name)
    for sub in unit.subunits.values():
        dfs_print(sub)


def generate_page(unit):
    for sub in unit.subunits:
        sub.update()
    sub.generate()


LICZBA_OKREGOW = 68

#TODO typy w xls, pilnować nrows + 1?
def generuj_obwody():
    for num in range(1, LICZBA_OKREGOW + 1):
        sheet_obwod = open_workbook('dane/obwody/obw' + ("%02d" % num) + '.xls').sheet_by_index(0)
        for obw in range(1, sheet_obwod.nrows):
            name = str(sheet_obwod.cell(obw, 1).value) + str(int(sheet_obwod.cell(obw, 4).value))
            gmina = sheet_obwod.cell(obw, 2).value
            obw_obj = gminy_dict[gmina].add_subunit(name, 'obwod')
            obw_obj.votes = [int(sheet_obwod.cell(obw, i).value) for i in range(12, 24)]






if __name__ == "__main__":
    #generuj_gminy()
    #generuj_powiaty()
    make_tree()
    generuj_obwody()
    dfs_print(polska)