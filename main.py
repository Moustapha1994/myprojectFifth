
"""Main file"""
from program import Program
from Class import Init

def main():
    """Main function"""
    try:
        programme = Program()
    except:
        print("Executez le fichier main.py utilisant un argument (- i ou --init) en premier")
        exit(1)

    run = True
    while run:
        programme.see_substitutes()
        programme.display_category()
        programme.display_product()
        programme.display_substitute()

        run = programme.continu()

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
