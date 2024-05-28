import mysql.connector
import configparser


class MySQL(object):

    def __init__(self, db_name: str):
        # Initialising DB with configs loaded from import_config,
        # once a table has been created set_current_table should be executed
        self.host = ""
        self.user = ""
        self.password = ""
        self.import_config()
        self.db_name = db_name
        self.db_connection = self.connect_to_database()
        self.cursor = self.db_connection.cursor()
        self.current_table = ""
        self.current_table_columns = ""

    def import_config(self):
        # Importing configuration from config.ini
        config = configparser.ConfigParser(interpolation=None)
        config.read('../.config/config.ini')
        self.host = config["mysql"]["host"]
        self.user = config["mysql"]["user"]
        self.password = config["mysql"]["password"]

    def connect_to_database(self):
        # Using the mysql module to connect to the DBMS and returning the db_connection
        db_connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.db_name)
        return db_connection

    def create_new_database(self, db_name: str):
        # Creating new DB if not already exists
        db_list = self.get_all_databases()
        if db_name in db_list:
            print(f"DB {db_name} already exists")
        else:
            sql_query = f"""CREATE DATABASE {db_name}"""
            self.cursor.execute(sql_query)
            print(f"DB {db_name} has been created")

    def get_all_databases(self):
        # Requesting all DB from DBMS and returning a list of DBs
        db_list = []
        sql_query = """SHOW DATABASES"""
        self.cursor.execute(sql_query)
        for item in self.cursor:
            db_list.append(list(item)[0])
        return db_list

    def get_all_tables_from_database(self):
        # Requesting all tables from DB and returning a list of tables
        table_list = []
        sql_query = """SHOW TABLES"""
        self.cursor.execute(sql_query)
        for item in self.cursor:
            table_list.append(list(item)[0])
        return table_list

    def get_all_column_names_from_table(self):
        # Requesting all column names from current_table and returning a tuple of column names exec. PRIMARY KEY
        column_list = []
        sql_query = f"""SELECT column_name,column_key
                        FROM INFORMATION_SCHEMA.COLUMNS
                        WHERE table_name = '{self.current_table}'
                        ORDER BY ordinal_position;
                        """
        self.cursor.execute(sql_query)
        for item in self.cursor:
            if 'PRI' not in item:
                column_list.append(list(item)[0])
        column_tuple = tuple(column_list)
        return column_tuple

    def drop_database(self, db_name: str):
        # Dropping specified DB from DBMS
        sql_query = f"""DROP DATABASE {db_name}"""
        self.cursor.execute(sql_query)
        print(f"DB {db_name} has been dropped")

    def switch_to_database(self, db_name: str):
        # Switching used DB
        sql_query = f"""USE {db_name}"""
        self.cursor.execute(sql_query)
        self.db_name = db_name
        print(f"Switched to DB {db_name} database")

    def create_new_table_from_dict(self, table_name: str, col_dict: dict):
        # Creating new table if not exists, taking a dictionary as input with the keys:
        # "col_name": column name
        # "col_type": column type
        # "col_add": column additional parameter
        db_tables = self.get_all_tables_from_database()
        if table_name in db_tables:
            print(f"Table {table_name} already exists")
        else:
            column_list = []
            col_length = len(col_dict["col_name"])
            for entry in range(col_length):
                column = f'{col_dict["col_name"][entry]} {col_dict["col_type"][entry]} {col_dict["col_add"][entry]}'
                column_list.append(column)

            column_string = str(column_list).replace("'", "").replace("[", "").replace("]", "")
            sql_query = f"""CREATE TABLE {table_name} ({column_string})"""
            self.cursor.execute(sql_query)
            print(f"{table_name} has been created")

    def set_current_table(self, table_name: str):
        # Set current table for simplified further usage
        db_tables = self.get_all_tables_from_database()
        if table_name in db_tables:
            self.current_table = table_name
            self.current_table_columns = self.get_all_column_names_from_table()
            print(f"Switched to {table_name} table")
            print(f"Table columns: {self.current_table_columns}")
        else:
            print("ERROR: Table not in DB")

    def insert_row_into_table(self, row_values: tuple):
        # Insert single row into table, taking a tuple as input
        col_names = str(self.current_table_columns).replace("'", "")
        sql_query = f"""INSERT INTO {self.current_table}{str(col_names)}
                        Values {str(row_values)};
                        """
        self.cursor.execute(sql_query)
        self.db_connection.commit()
        print(f"{row_values} have been inserted into {self.current_table}")
        last_row_id = self.cursor.lastrowid
        print("1 record inserted, ID:", last_row_id)

    def insert_multiple_rows_into_table(self, row_values: list):
        # Insert multiple rows into table, taking a list of tuples as input
        col_names = str(self.current_table_columns).replace("'", "")
        row_values = str(list(row_values)).replace("[", "").replace("]", "")
        sql_query = f"""INSERT INTO {self.current_table}{str(col_names)}
                                Values {str(row_values)};
                                """
        self.cursor.execute(sql_query)
        self.db_connection.commit()
        print(f"{row_values} have been inserted into {self.current_table}")

    def select_from_table(self, col_selection: str = '*'):
        # Selecting specified content from table with default value all and printing them
        col_selection = str(list(col_selection)).replace("'", "").replace("[", "").replace("]", "")
        sql_query = f"""SELECT {col_selection} FROM {self.current_table}"""
        self.cursor.execute(sql_query)
        results = self.cursor.fetchall()

        for item in results:
            print(item)

    def select_from_table_where(self, search_query: str, col_selection: str = '*'):
        # Selecting specified content from table, where search query is matched,
        # with default value all and printing them
        col_selection = str(list(col_selection)).replace("'", "").replace("[", "").replace("]", "")
        sql_query = f"""SELECT {col_selection} FROM {self.current_table} WHERE {search_query}"""
        self.cursor.execute(sql_query)
        results = self.cursor.fetchall()

        for item in results:
            print(item)

    def select_from_table_order_by(self, column: str, col_selection: str = '*', descending: bool = False):
        # Selecting specified content from table, ordered ascending by specified column,
        # with default value all and printing them
        col_selection = str(list(col_selection)).replace("'", "").replace("[", "").replace("]", "")
        if descending:
            column += " DESC"
        sql_query = f"""SELECT {col_selection} FROM {self.current_table} ORDER BY {column}"""
        self.cursor.execute(sql_query)
        results = self.cursor.fetchall()

        for item in results:
            print(item)

    def delete_from_table_where(self, del_query: str):
        # Delete row from current table where query is matched
        sql_query = f"""DELETE FROM {self.current_table} WHERE {del_query}"""
        self.cursor.execute(sql_query)
        self.db_connection.commit()
        print(f"{del_query} have been deleted form {self.current_table}")
        print(self.cursor.rowcount, "record(s) deleted")

    def delete_table(self, table_name: str):
        # Deleting table from DB
        sql_query = f"""DROP TABLE {table_name}"""  # sql_query = """DROP TABLE IF EXISTS {table_name}"""
        self.cursor.execute(sql_query)
        print(f"{table_name} have been deleted form {self.db_name}")

    def update_table(self, old_data: str, new_data: str):
        # Update row in table with new data where old data has a match
        sql_query = f"""UPDATE {self.current_table} SET {new_data} WHERE {old_data}"""
        self.cursor.execute(sql_query)
        self.db_connection.commit()
        print(f"{new_data} have been updated at {old_data}")
        print(self.cursor.rowcount, "record(s) deleted")


if __name__ == '__main__':
    print('### TEST ###')
