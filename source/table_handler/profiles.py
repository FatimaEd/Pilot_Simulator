from source.databaselib import write
from source.databaselib import read


# This functions takes some values using parameters and make a dictionary from it.
# Then it passes the dictionary to write.write_to_table using the table name "fuel_account"
# which saves the data.
def create_new_user(username, fullname, password):
    data = {
        "username": username,
        "full_name": fullname,
        "password": password
    }

    write.write_to_table("profiles", data)


# Cross-checks username and password with the table and returns true if record exists.
def check_user(username, password):
    result = read.read_all_from_table_with_filter("profiles", f"username = '{username}' and password = '{password}'")
    if len(result) > 0:
        return True
    else:
        return False
