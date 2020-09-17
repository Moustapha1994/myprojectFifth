
"""Main file"""
from program import Interaction
from Class import Init

def main():
    """Main function"""
    try:
        interact= Interaction()
    except:
        print("Executez le fichier main.py utilisant un argument (- i ou --init) en premier")
        exit(1)

    run = True
    while run:
        interact.see_substitutes()
        interact.display_category()
        interact.display_product()
        interact.display_substitute()

        run = interact.continu()

Arg = None

try:
    INIT_database = Init()
    Arg = INIT_database.arg()
except AttributeError:
    pass

if __name__ == "__main__":
    if Arg is True:
        Arg
    else:
        main()
