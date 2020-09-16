"""Class that retrieves the data from the API and insert them into the db"""
import mysql.connector
import requests
from conf import CHAMP, db


class CollectData:
    """Takes care of recovering data from OpenFoodFact and inserting them into the database"""
    def __init__(self):
        self.cnx = mysql.connector.connect(**CHAMP, database=db)

    def insert_category(self):
        """Take 10 categories from API and insert them in db"""
        res = requests.get("https://fr.openfoodfacts.org/categories&json=1")
        data_json = res.json()
        data_tags = data_json.get('tags')
        data_cat = [d.get('name') for d in data_tags]
        i = 2
        while i < 12:
            mycursor = self.cnx.cursor()
            add_category = ("INSERT INTO Category" "(name)" "VALUES('{}')".format(data_cat[i]))
            try:
                print("Category created: {}.".format(data_cat[i]))
                mycursor.execute(add_category)
                self.cnx.commit()
                mycursor.close()
                i = i+1
            except:
                print("An error occurred while creating categories")

    def obtain_food(self, nb_fd):
        """Recovers the number of products given in parameter"""
        for i in range(1, 11):
            nb_ini_cat = i
            nb_food = nb_fd
            mycursor = self.cnx.cursor(buffered=True)
            cat_nb_1 = str(nb_ini_cat)
            selec_cat = ("SELECT name FROM Category WHERE id = "+cat_nb_1)
            mycursor.execute(selec_cat)
            cat_saved = str(mycursor.fetchone()[0]) #indexation
            payload = {
                'action': 'process',
                'tagtype_0': 'categories', #which subject is selected (categories)
                'tag_contains_0': 'contains',
                'tag_0': '{}'.format(cat_saved),
                'sort_by': 'unique_scans_n',
                'page_size': '{}'.format(nb_food),
                'countries': 'France',
                'json': 1,
                'page': 1
            }

            r_food = requests.get('https://fr.openfoodfacts.org/cgi/search.pl', params=payload)
            food_json = r_food.json()
            food = food_json.get('products')
            food_id = ("SELECT id FROM Category WHERE id = "+cat_nb_1)
            mycursor.execute(food_id)
            nb_food=5

            for j in range(nb_food):
                prod_name_saved = [d.get('product_name_fr') for d in food]
                name = str(prod_name_saved[j])
                store_saved = [d.get('stores') for d in food]
                store = str(store_saved[j])
                link_saved = [d.get('url') for d in food]
                link = str(link_saved[j])
                nutri_grd_saved = [d.get('nutrition_grade_fr') for d in food]
                nutri_grd = str(nutri_grd_saved[j])
                add_food = (
                    "INSERT INTO Product"
                    "(name, store, link, nutriscore, category)"
                    "VALUES (%s, %s, %s, %s, %s)")
                data = (name, store, link, nutri_grd, cat_nb_1)
                mycursor.execute(add_food, data)
                self.cnx.commit()
            mycursor.close()
        print("Products added.")
"""
def main():
     #Initialize the data collect

    # Download the response
    CD = CollectData()
    
    connect = CD.insert_category()
    CD.obtain_food(connect)


if __name__ == "__main__":
    main()
"""