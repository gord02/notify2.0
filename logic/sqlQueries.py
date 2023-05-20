import mysql.connector
from mysql.connector import Error

import os
# try:
#     connection = mysql.connector.connect(host='localhost',
#                                          database='checkon',
#                                          user='root',
#                                          password='')
#     if connection.is_connected():
#         db_Info = connection.get_server_info()
#         print("Connected to MySQL Server version ", db_Info)
#         cursor = connection.cursor()
#         cursor.execute("select database();")
#         record = cursor.fetchone()
#         print("You're connected to database: ", record)

# except Error as e:
#     print("Error while connecting to MySQL", e)

def create_connection(host_name, user_name, user_passwd, dm_name):
    connection = None
    # try:
    #     connection = mysql.connector.connect(host=host_name,
    #                                          user=user_name,
    #                                          passwd=user_passwd,
    #                                           database=dm_name
    #                                         )
    #     # print("connection to MySql DB successful")
    # except Error as e:
    #     print(f"The error '{e}' occurred")
    
    db_user = os.environ.get('CLOUD_SQL_USERNAME')
    # db_password = os.environ.get('CLOUD_SQL_PASSWORD')
    db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
    db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')
    
       # When deployed to App Engine, the `GAE_ENV` environment variable will be
    # set to `standard`
    if os.environ.get('GAE_ENV') == 'standard':
        # If deployed, use the local socket interface for accessing Cloud SQL
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        connection =  mysql.connector.connect(user=db_user, password=None, unix_socket=unix_socket, db=db_name)
    else:
        # If running locally, use the TCP connections instead
        # Set up Cloud SQL Proxy (cloud.google.com/sql/docs/mysql/sql-proxy)
        # so that your application can use 127.0.0.1:3306 to connect to your
        # Cloud SQL instance
        host = '127.0.0.1'
        db_user = 'root'
        db_name = 'checkon'
        db_connection_name = 'notify-3441:us-central1:checkon'
        # print(db_user, db_password, host, db_name)
        connection =  mysql.connector.connect(user=db_user, password=None, host=host, db=db_name)
    return connection

def create_database(connection, query):
    cursor = connection.cursor()
    
    try:
        cursor.execute(query)
        print("database created successfully")
    except Error as e:
        print(f"The error '{e}' occurred")
        
def execute_query(connection, query):
    result = None
    cursor = connection.cursor(buffered=True)
    try:
        cursor.execute(query)
        connection.commit()
        # print("query executed successfully")
        result = cursor.fetchall()
    except Error as e:
        print("the failed query: " , query)
        print(f"The error '{e}' occurred")
    print()
    return result

def execute_query_update(connection, query):
    cursor = connection.cursor(buffered=True)
    try:
        cursor.execute(query)
        connection.commit()
        # print("query executed successfully")
    except Error as e:
        print("the failed query: " , query)
        print(f"The error '{e}' occurred")


def update_company(company):
    connection = create_connection("localhost", "root", "", "checkon") 
    update = f"""
    UPDATE
    companies
    SET
    found = 1
    WHERE
    company = '{company}';
    """
    execute_query_update(connection, update)


def add_company(company, fileName):
    connection = create_connection("localhost", "root", "", "checkon") 
    add=f""" INSERT INTO companies(company, fileName, found)
        VALUES ('{company}', '{fileName}', 0);
    """
    execute_query_update(connection, add)
    order_companies()
   
    
def reset_all_company_found():
    connection = create_connection("localhost", "root", "", "checkon") 
    
    update=""" UPDATE companies
        SET found = 0
        WHERE found = 1;
    """
    execute_query_update(connection, update)
    
    
def reset_company_found(company):
    connection = create_connection("localhost", "root", "", "checkon") 
    
    update=f""" UPDATE companies
        SET found = 0
        WHERE Company = "{company}";
    """
    execute_query_update(connection, update)
    
    
def order_companies():
    connection = create_connection("localhost", "root", "", "checkon") 
    order="SELECT * FROM companies ORDER BY company;"
    execute_query(connection, order)


def add_companies():
    connection = create_connection("localhost", "root", "", "checkon") 
    
    companies = """
    INSERT INTO companies(company, fileName, found)
    VALUES 
    ("PathAi", "pathAi.py", 0),
    ("Rippling", "rippling.py", 0);
    """
    execute_query_update(connection, companies)


def get_companies(): 
    connection = create_connection("localhost", "root", "", "checkon") 
    
    get_query = " SELECT * FROM companies WHERE found = 0 ORDER BY company;"
    # return list of tuples
    return execute_query(connection, get_query)


def isUser(email):
    connection = create_connection("localhost", "root", "", "checkon") 
    query = f"""
        SELECT email FROM users WHERE email = '{email}';
    """
    res = execute_query(connection, query)
    if(len(res) == 0 ):
        return False
    return True
   
    
def createUser(email, jobTypes):
    connection = create_connection("localhost", "root", "", "checkon") 
    query = f"""
        INSERT INTO users (email, preferences) VALUES ('{email}', '{jobTypes}');
    """
    execute_query(connection, query)
    
    
def updateUser(email, jobTypes):
    connection = create_connection("localhost", "root", "", "checkon") 
    query = f"""
        UPDATE users SET preferences = '{jobTypes}' WHERE email = '{email}';
    """
    execute_query_update(connection, query)
   
    
def getUsers():
    connection = create_connection("localhost", "root", "", "checkon") 
    query = f"""
        SELECT email, preferences FROM users;
    """
    return execute_query(connection, query)


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
# tests to:

# that user is added, seen in db
# test checking for user, there not there

# res = get_companies()
# print(res)
# print(res[0][1])


# tests:

# print(get_companies())
# print(getUsers())
# print(isUser("gordon.hamilton1110@gmail.com"))
# print(isUser("gordon@gmail.com"))

# update_company("Addepar")
# reset_all_company_found()
# add_company("Snowflake","snowflake.py")
# reset_company_found("LinkedIn")
# add_companies()
# reset_all_company_found()

