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
    
    def import_sql(self, sql_file_path):
        """import sql file into database
        """
        file = open(sql_file_path, encoding="utf8")
        sqls = " ".join(file.readlines())
        for sql in sqls.split(";"):
            self.cursor.execute(sql)
        self.conn.commit()

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
        