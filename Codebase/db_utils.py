import sys
import csv
import pandas as pd
sys.path.insert(0, '/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages')
import pymysql


class YelpDb:
    """ Yelp Database Configurations and database utilities
    """

    def __init__(self, db_name):
        """ db connection
        """
        self.host = "localhost"
        self.user = "root"
        self.password = "skrskr220"
        self.db = db_name
        self.charset = 'utf8'
        self.conn = pymysql.connect(host=self.host,
                                    user=self.user,
                                    password=self.password,
                                    db=self.db,
                                    charset=self.charset)
        self.cursor = self.conn.cursor()  # set a cursor object
        
    def execute(self, sql):
        """ sql execution
        """
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except pymysql.Error:
            self.conn.rollback()
            print(sql)

    def fetch_all(self):
        """ fetch all documents
        """
        return self.cursor.fetchall()

    def fetch_one(self):
        """ fetch single document
        """
        return self.cursor.fetchone()

    def db_to_df(self, table_name):
        """ read dbs into Pandas DataFrame
        """
        yelp_df = pd.read_sql(f"SELECT * FROM {table_name};", self.conn)
        return yelp_df
    
    def close(self):
        """ disconnect from server
        """
        self.cursor.close()
        self.conn.close()
        


# keep this class temperary
class YelpDb_backup:
    """ Yelp Database Configurations
    """

    def __init__(self, ):
        """ db connection
        """
        self.host = "localhost"
        self.user = "root"
        self.password = "skrskr220"
        self.db = "yelp_info_db"
        self.charset = 'utf8'
        self.conn = pymysql.connect(host=self.host,
                                    user=self.user,
                                    password=self.password,
                                    db=self.db,
                                    charset=self.charset)
        self.cursor = self.conn.cursor()  # set a cursor object

    def create_yelp_table(self, table_name):
        """ Create table in the yelp_info_db based on properties
        """
        self.cursor.execute("DROP TABLE IF EXISTS " + table_name)
        sql = f"""CREATE TABLE {table_name} (
              `Address` char(255),
              `Amenities` varchar(2000),
              `Category` char(255),
              `Highlights` char(255),
              `Name` char(255),
              `Open_hours` varchar(500),
              `Phone` char(20),
              `Price` char(20),
              `Rating` char(20),
              `Reviews` char(20))"""
        self.cursor.execute(sql)
        print("Created table Successfully.")

    def csv_to_db(self, csv_path, table_name):
        """ Convert .csv files into database
        """
        with open(csv_path) as csv_file:
            csv_data = csv.reader(csv_file, delimiter=',')
            next(csv_data)
            for row in csv_data:
                # print(row)
                self.cursor.execute(f'INSERT INTO {table_name} (Address, \
                  Amenities, Category, Highlights, Name, Open_hours, \
                               Phone, Price, Rating, Reviews) \
                                    VALUES("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")', row)
            self.conn.commit()
            print("Finsihed read csv into db.")

    def execute(self, sql):
        """ Test sql execution
        """
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except pymysql.Error:
            self.conn.rollback()
            print(sql)

    def fetch_all(self):
        return self.cursor.fetchall()

    def fetch_one(self):
        return self.cursor.fetchone()

    def close(self):
        self.cursor.close()
        self.conn.close()  # disconnect from server


