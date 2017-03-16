from jinja2 import FileSystemLoader, Environment
from xlrd import open_workbook

templateLoader = FileSystemLoader( searchpath="templates" )

env = Environment( loader=templateLoader )

TEMPLATE_FILE = "gmina.html"

template = env.get_template( TEMPLATE_FILE )


# outputText = template.render( templateVars )






def generuj_gminy():
    pass

def generuj_powiaty():
    pass












if __name__ == "__main__":
    generuj_gminy()
    generuj_powiaty()
    print(outputText)