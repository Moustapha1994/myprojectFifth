#!/usr/bin/python3
# -*-coding:utf-8 -

import mysql.connector as MC
import requests


Champ= {
    "host":"localhost",
    "user":"root",
    "password":"Moustapha.94"
}


class CollectData:
    """collection of datas from OpenFoodFacts to mydatabase"""

    def __init__(self):
        self.con = mysql.connector.connect(**Champ,database="MyDatabase")

    def insert_category(self):
        """choose 10 categories from OFF"""
        payload = {'page':10
                   }
        rech = requests.get('https://fr.openfoodfacts.org/categories&json=1',payload)
        jsonData = rech.json()
        tagData= jsonData.get('tags')
        cat = [d.get('name') for d in tagData]
        i=1
        while i< 11:
            mycursor = self.con.cursor()
            add_category = ("INSERT INTO Category" "(name)" "VALUES('{}')".format(cat[i]))
            try:
                print("Category created: {}".format(cat[i]))
                mycursor.execute(add_category)
                self.con.close()
                i=i+1
            except:
                print("There is an error for creating category")









