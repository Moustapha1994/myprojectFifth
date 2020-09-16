"""Class which allow the creation of the database with an argument"""
import argparse
import mysql.connector
from data_collect import CollectData
from conf import CHAMP, db



class Sql:
    """Creating and using the database"""
    def __init__(self, user, password, host):
        self.user = str(user)
        self.password = str(password)
        self.host = str(host)

    def create_db(self, database):
        """Create the database"""
        cnx = self.connect_db()
        mycursor = cnx.cursor()
        self.database = str(database)
        try:
            mycursor.execute(
                "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(db))
            print("Database {} created successfully.".format(db))
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            exit(1)

    def connect_db(self):
        """make the connection to the database"""
        try:
            cnx = mysql.connector.connect(
                user=self.user,
                password=self.password,
                host=self.host
                )
            return cnx
        except mysql.connector.errors.ProgrammingError:
            return False

    def create_tables(self):
        """Create the tables in database"""
        cnx = self.connect_db()
        mycursor = cnx.cursor()
        use_db = ("USE {}".format(db))
        mycursor.execute(use_db)
        try:
            with open('createdb.sql', 'r') as file:
                query = file.read()
            mycursor.execute(query)
            mycursor.close()
        except:
            pass



class Init:
    """Help us to create and fill the database"""
    def __init__(self):
        pass

    def init_db(self):
        """Uses class methods to create and fill the DB"""
        try:
            sql = Sql(**CHAMP)
            sql.create_db(db)
            sql.create_tables()
            data = CollectData()
            data.insert_category()
            data.obtain_food(20)
        except:
            print("check your your file conf.py something is rong")
            exit(1)

    def arg(self):
        """ADD the --init argument"""
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--init", "-i", action="store_true", help="Initialise the DB with -i or --init"
        )
        args = parser.parse_args()

        if args.init:
            self.init_db()
            return True

"""
def main():
    # Initialize the data collect

    # Download the response
    sql = Sql()

    connect = sql.insert_category()
    sql.obtain_food(connect)


if __name__ == "__main__":
    main()
"""