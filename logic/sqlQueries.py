import mysql.connector
from mysql.connector import Error

def create_connection(host_name, user_name, user_passwd, dm_name):
    connection = None
    
    try:
        connection = mysql.connector.connect(host=host_name,
                                             user=user_name,
                                             passwd=user_passwd,
                                              database=dm_name
                                            )
        print("connection to MySql DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    
    return connection

def create_database(connection, query):
    cursor = connection.cursor()
    
    try:
        cursor.execute(query)
        print("database created successfully")
    except Error as e:
        print(f"The error '{e}' occurred")
        
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

def query_companies(connection, query):
    cursor = connection.cursor()
    result = None
    
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")
    
def update_company_status(file_name):
    connection = create_connection("localhost", "root", "", "checkon") 
    
    update_company = f"""
        UPDATE
        companies
        SET
        found = 1
        where fileName = {file_name}
      """
    execute_query(connection, update_company)
   
  
db_query = "CREATE DATABASE checkon"
table_create = """
CREATE TABLE IF NOT EXISTS companies (
    company TEXT,
    fileName TEXT,
    found INT
)
"""
add_companies = """
    INSERT INTO companies(company, fileName, found)
    VALUES 
    ("Snapchat", "snap.py", 0),
    ("Addepar", "addepar.py", 0),
    ("Quora", "quora.py", 0),
    ("twoSigma", "twoSigma.py", 0),
    ("Yelp", "yelp.py", 0);
"""

def get_companies(): 
    connection = create_connection("localhost", "root", "", "checkon") 
    
    get_query = "SELECT * FROM companies WHERE found = 0"
    # return list of tuples
    return query_companies(connection, get_query)

    
def update_company(company):
    connection = create_connection("localhost", "root", "", "checkon") 
    update = f"""
    UPDATE
    companies
    SET
    found = 1
    WHERE
    company = '{company}'
    """
    execute_query(connection, update)


