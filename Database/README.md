# Database Folder

## Overview and explanation

### Part I:
* Data Source:
  * To use the yelp databases, go to `yelp_dbs` folder:
    * `yelp_db_1_6.sql` contains information of the following cities:
		+-----------------------+
		| Tables_in_yelp_db_1_6 |
		+-----------------------+
		| yelp_fresno           |
		| yelp_los_angeles      |
		| yelp_sacramento       |
		| yelp_san_diego        |
		| yelp_san_francisco    |
		| yelp_san_jose         |
		+-----------------------+
		6 rows in set (0.00 sec)
 
	* `yelp_db_7_12.sql` contains information of the following cities:
 		+------------------------+
		| Tables_in_yelp_db_7_12 |
		+------------------------+
		| yelp_Anaheim           |
		| yelp_Bakersfield       |
		| yelp_Long_Beach        |
		| yelp_Oakland           |
		| yelp_Riverside         |
		| yelp_Santa_Ana         |
		+------------------------+
		6 rows in set (0.00 sec)

### Part II:
* Usage:

  * Export .sql files from mysql server:

    Use `mysqldump --add-drop-table -u root -p name_of_your_db > export_dn_name.sql` for dumping database.
	**Note: make sure to run this command after exit mysql.** 

  * Improt .sql files to mysql server:

    Use `source your_sql_file_path` for importing database.**
	**Note: run this command im mysql cmd.**
 
