from source.databaselib import dbconnection
from typing import Dict


# This function is used for making the insert command easier.
# This function takes Dictionary. The dictionary maps field
# names and their values. This method reads the dictionary and
# creates an insert statement from it and then executes the
# insert statement. At the end returns the auto-incremented id if
# the table has an auto-incremented column.
def write_to_table(table_name, data: Dict):
    fields = ""
    values = ""

    for key, value in data.items():
        if fields != "":
            fields = fields + ", "
        if values != "":
            values = values + ", "

        fields = fields + key

        values = values + "'" + value + "'"

    sql = f"insert into {table_name} ({fields}) values ({values})"

    return dbconnection.execute_insert(sql)
