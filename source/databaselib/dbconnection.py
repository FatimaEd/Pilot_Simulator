import mysql.connector


# This function is mysql connection based on connection parameter.
# This is a single point in the total project through which the
# project is communicating with the database. Changing the database
# connection string below we can chance the project database. This
# makes the code non-duplicate in multiple places.
def get_connection():
    return mysql.connector.connect(
             host='127.0.0.1',
             port=3306,
             database='pilot_simulator',
             user='root',
             password='2358',
             autocommit=True
             )


# To avoid writing multiple lines during running each query
# this function is created. It takes the query string as a parameter
# and returns the result of the query.
def execute(sql):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


# The execute(sql) works fine for any queries, however; when
# we wanted to get the newly created auto-incremented id execute(sql)
# function was returning blank. So we found it here:
# https://stackoverflow.com/questions/2548493/how-do-i-get-the-id-after-insert-into-mysql-database-with-python
def execute_insert(sql):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(sql)
    cursor.fetchall()
    return cursor.lastrowid

