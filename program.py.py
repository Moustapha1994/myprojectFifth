"""Manages interaction with user and parse data"""
import mysql.connector
from conf import CHAMP, db
from math import fabs

class Interaction:
    """This Class manages the interaction between the user and the console """
    def __init__(self):
        self.cnx = mysql.connector.connect(**CHAMP, database=db)
        self.cat_id = None
        self.nutri_prod_chosen = None
        self.id_prod_chosen = None
        self.id_prod_substitute = None
        self.response = ['Y', 'N']

    def display_category(self):
        """Show the category"""
        mycursor = self.cnx.cursor()
        dict_category = {}
        category = ("SELECT id, name FROM Category;")
        mycursor.execute(category)
        rows = mycursor.fetchall()
        print("\n\nListes des categories: \n")
        for i, row in rows:
            print('{} : {}'.format(i, row))
            dict_category[i] = row

        while True:
            try:
                self.cat_id = int(input("\n\nChoisissez un numero de categorie : \n"))
                cat_choose = dict_category[self.cat_id]
                break
            except ValueError:
                print("Le numero choisi doit etre un nombre")
            except KeyError:
                print("Vous devez choisir un bon numero de categorie")
        print("Vous avez choisi {} category\n\n".format(cat_choose))

    def display_product(self):
        """Show the products of the chosen category"""
        print("Ici la liste des produits pour cette categorie: \n")

        mycursor = self.cnx.cursor()
        get_product = ("SELECT id, name FROM Product WHERE category={}".format(self.cat_id))
        mycursor.execute(get_product)
        result = mycursor.fetchall()
        coef = (self.cat_id-1)*20
        for i in range(len(result)):
            map_id = result[i][0] - coef
            print("{}. {}".format(map_id, result[i][1]))

        while True:
            try:
                self.id_prod_chosen = int(input("\nChoisissez un numero de produit: \n"))
                self.id_prod_chosen = self.id_prod_chosen + coef
                get_nutriscore = ("SELECT nutriscore \
                	FROM Product WHERE id={} \
                	AND category={}".format(self.id_prod_chosen, self.cat_id))
                mycursor.execute(get_nutriscore)
                self.nutri_prod_chosen = mycursor.fetchall()[0][0]
                break
            except ValueError:
                print("Il doit etre un nombre")
            except IndexError:
                print("Veuillez choisir un bon numero de produits")

        mycursor.close()
        print("\nLe produit que vous avez choisi a pour nutriscore : {} \n\n".format(
            self.nutri_prod_chosen
        ))

    def display_substitute(self):
        """Show the substitutes"""
        mycursor = self.cnx.cursor()
        query = ("SELECT id, name, nutriscore, store, link \
            FROM Product WHERE nutriscore <= '{}' \
            AND category={} AND id !={}".format(
                self.nutri_prod_chosen,
                self.cat_id,
                self.id_prod_chosen
                )
                )
        mycursor.execute(query)
        result = mycursor.fetchall()

        coef = (self.cat_id-1)*20
        print("Ici la liste de produits avec avec un meilleur ou equivalent nutriscore :\n")
        for i in range(len(result)):
            map_id = result[i][0] - coef
            if result[i][0] is None:
                print('Il n y a pas de substitut')
            else:
                print(
                    "{}. {} avec nutriscore: {}. \n"
                    " Peut être acheté {} plus d'informations sur le lien : \n{}\n"
                    .format(
                        map_id, result[i][1],
                        result[i][2],
                        result[i][3],
                        result[i][4]
                        )
                    )

        while True:
            try:
                self.id_prod_substitute = int(input("\n Choisissez l'id du produit: \n"))
                self.id_prod_substitute = self.id_prod_substitute + coef
                break
            except ValueError:
                print("Il doit être un nombre")
            except IndexError:
                print("Vous devez devez choisir un bon nombre pour choisir un produit")

        save = ()
        while save not in ['Y', 'N']:
            save = input('\nVoulez vous enregistrer ce substitut ?\n"Y" or "N"\n').upper()

        if save == "Y":
            query = ("INSERT INTO Substitute \
                    (id_product_to_substitute, id_substitute_product) VALUES ({}, {})".format(
                        self.id_prod_chosen,
                        self.id_prod_substitute)
                    )
            mycursor.execute(query)
            self.cnx.commit()
        mycursor.close()

    def see_substitutes(self):
        """Display registered susbtitutes"""
        while True:
            try:
                response = ()
                while response not in [1, 2]:
                    response = int(
                        input(
                            "\n1 - Selectionner une catégorie à remplacer.\n"
                            "2 - Consulter les substitués ?\n"
                        ).upper()
                    )
                    if response not in [1, 2]:
                        print("\n Vous devez choisir 1 ou 2.")
                break
            except ValueError:
                print("\n Il doit être un nombre")

        if response == 2:
            query = ("SELECT name, nutriscore, store, link \
                    FROM Product \
                    INNER JOIN Substitute \
                    ON Substitute.id_substitute_product = Product.id")

            mycursor = self.cnx.cursor()
            mycursor.execute(query)
            results = mycursor.fetchall()

            i = 1
            print('\n\nVoici la liste de vos substitutions : \n')
            for result in results:
                print(
                    "{}. {} avec nutriscore : {}.\n"
                    "peut être acheté {} plus d'informations sur le lien : \n{}\n"
                    .format(
                        i, result[0], result[1], result[2], result[3]
                    )
                )
                i += 1
            self.continu()

    def continu(self):
        """Return to the beginning"""
        answer = ()
        while answer not in self.response:
            answer = str(input('\nVoulez vous contitnuer ?\n"Y" or "N"\n').upper())

        if answer == "Y":
            print("\nBien, maintenant choisissez une catégorie de produit que tu veux remplacer : ")
            return True

        if answer == "N":
            print("\nAu revoir Merci de votre patience !.\n")
            exit(1)

        return False

