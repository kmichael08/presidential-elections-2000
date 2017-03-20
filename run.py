from jinja2 import FileSystemLoader, Environment
from xlrd import open_workbook
from collections import OrderedDict
from json import dumps, load
import re

CANDIDATES_NUM = 12

templateLoader = FileSystemLoader( searchpath="templates" )

env = Environment( loader=templateLoader )

TEMPLATE_FILE = "gmina.html"

ROOT_PATH = '../../'

template = env.get_template( TEMPLATE_FILE )

sheet = open_workbook('dane/gm-kraj.xls').sheet_by_index(0)

candidates = [sheet.cell(0, i).value for i in range(10, 22)]

rubryki = ['Uprawnieni do głosowania', 'Wydane karty', 'Wyjęto z urny', 'Nieważne głosy', 'Ważne głosy', 'Frekwencja']

class Unit:

    def __init__(self, name, typ, full_type = None, full_name = None):
        self.subunits = OrderedDict()
        self.votes = [0] * CANDIDATES_NUM
        self.ogolne = OrderedDict()
        self.name = name
        self.typ = typ
        self.parent = None

        if full_type == None:
            self.full_type = typ
        else:
            self.full_type = full_type

        if full_name == None:
            self.full_name = name
        else:
            self.full_name = full_name

        self.destination = 'pages/' + self.typ + '/' + re.sub(r' ', '_', str(self.name)) + '.html'
        self.statystyki = [0] * 6
        self.diagram = [['Kandydat', 'Głosy']]

    """ Create (if not existing yet) the subunit and add to the list and return it. """
    def add_subunit(self, name, typ, full_type=None, full_name=None):
        if name not in self.subunits:
            self.subunits[name] = Unit(name, typ, full_type, full_name)
        self.subunits[name].parent = self
        return self.subunits[name]

    """ Calculate values based on subunits. """
    def update(self):
        for sub in self.subunits.values():
            for i in range(len(sub.votes)):
                self.votes[i] += sub.votes[i]
            for i in range(5):
                self.statystyki[i] += sub.statystyki[i]

    """ Generate the page for this unit. """
    def generate(self):
        for sub in self.subunits.values():
            sub.generate()
        if self.typ not in ['gmina', 'obwod']:
            self.update()
        self.res_dict = OrderedDict(zip(candidates, self.votes))

        for cand, support in self.res_dict.items():
            self.diagram.append([cand, support])

        self.statystyki[5] = 100 * self.statystyki[1] / self.statystyki[0]
        self.ogolne = OrderedDict(zip(rubryki, self.statystyki))

        outputText = template.render({'res_dict' : self.res_dict, 'ogolne' : self.ogolne, 'subunits' : self.subunits, 'subnames' : sorted(self.subunits.keys()),
                                      'root' : ROOT_PATH, 'diagram' : self.diagram, 'ancestors' : self.ancestors() })

        with open(self.destination, 'w') as page:
            page.write(outputText)


    def ancestors(self):
        if self.parent == None:
            return [(str(self.full_type) + ' ' + str(self.full_name), self.destination)]
        else:
            return self.parent.ancestors() + [( str(self.full_type) + ' ' + str(self.full_name), self.destination)]


polska = Unit('Polska', 'kraj', full_type='')
okregi_dict = OrderedDict()
gminy_dict = OrderedDict()


""" Add the row from the sheet with units. """
def add_row(row):
    okr_num = int(row[0].value)
    gmina = str(row[0].value) + str(row[1].value)
    gmina_name = row[2].value
    powiat = row[3].value
    gminy_dict[gmina] = okregi_dict[okr_num].add_subunit(powiat, 'powiat').add_subunit(gmina, 'gmina', full_name=gmina_name)

""" Generate the tree of all units. """
def make_tree():
    with open('dane/wojewodztwa.json', 'r') as woj:
        woj_dict = load(woj)

    for woj, okregi in woj_dict.items():
        wojewodztwo = polska.add_subunit(woj, 'woj', full_type='województwo')
        for okreg in okregi:
            okr_obj = wojewodztwo.add_subunit(okreg, 'okr', full_type='okręg')
            okregi_dict[okreg] = okr_obj

    for row in list(sheet.get_rows())[1:]:
        add_row(row)

""" Print the tree of units. """
def dfs_print(unit):
    print(unit.destination, unit.name)
    for sub in unit.subunits.values():
        dfs_print(sub)


LICZBA_OKREGOW = 68

""" Generate directly pages for obwody. """
#TODO typy w xls
def generuj_obwody_i_gminy():
    for num in range(1, LICZBA_OKREGOW + 1):
        sheet_obwod = open_workbook('dane/obwody/obw' + ("%02d" % num) + '.xls').sheet_by_index(0)
        for obw in range(1, sheet_obwod.nrows):
            name = str(sheet_obwod.cell(obw, 1).value) + str(int(sheet_obwod.cell(obw, 4).value))
            gmina = str(sheet_obwod.cell(obw, 0).value) + str(sheet_obwod.cell(obw, 1).value)
            obwod_name = sheet_obwod.cell(obw, 6).value
            obw_obj = gminy_dict[gmina].add_subunit(name, 'obwod', full_type='obwód', full_name=obwod_name)
            obw_obj.votes = [int(sheet_obwod.cell(obw, i).value) for i in range(12, 24)]
            obw_obj.statystyki = [int(sheet_obwod.cell(obw,i).value) for i in range(7, 12)]
            toll = 100 * obw_obj.statystyki[1] / obw_obj.statystyki[0]
            obw_obj.statystyki.append(toll)

    for num in range(1, sheet.nrows):
        gmina = str(sheet.cell(num, 0).value) + str(sheet.cell(num, 1).value)
        gmina_obj = gminy_dict[gmina]
        gmina_obj.votes =  [int(sheet.cell(num, i).value) for i in range(10, 22)]
        gmina_obj.statystyki = [int(sheet.cell(num, i).value) for i in range(5, 10)]
        toll = 100 * gmina_obj.statystyki[1] / gmina_obj.statystyki[0]
        gmina_obj.statystyki.append(toll)


if __name__ == "__main__":
    make_tree()
    generuj_obwody_i_gminy()
    polska.generate()