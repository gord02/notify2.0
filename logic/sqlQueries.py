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
        # print("connection to MySql DB successful")
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
    return result

def query_companies(connection, query):
    cursor = connection.cursor()
    result = None  
    try:
        cursor.execute(query)
        result = cursor.fetchall()
    except Error as e:
        print("the failed query: " , query)
        print(f"The error '{e}' occurred")
    return result
    
    
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


def add_company(company, fileName):
    connection = create_connection("localhost", "root", "", "checkon") 
    add=f""" INSERT INTO companies(company, fileName, found)
        VALUES ('{company}', '{fileName}', 0);
    """
    execute_query(connection, add)
    order_companies()
   
    
def reset_all_company_found():
    connection = create_connection("localhost", "root", "", "checkon") 
    
    update=""" UPDATE companies
        SET found = 0
        WHERE found = 1;
    """
    execute_query(connection, update)
    
    
def reset_company_found(company):
    connection = create_connection("localhost", "root", "", "checkon") 
    
    update=f""" UPDATE companies
        SET found = 0
        WHERE Company = "{company}";
    """
    execute_query(connection, update)
    
    
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
    execute_query(connection, companies)
    # order_companies()

# reset_all_company_found()
# add_company("Snowflake","snowflake.py")
# reset_company_found("LinkedIn")
# add_companies()


def get_companies(): 
    connection = create_connection("localhost", "root", "", "checkon") 
    
    get_query = " SELECT * FROM companies WHERE found = 0 ORDER BY company;"
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
    execute_query(connection, query)
   
    
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
