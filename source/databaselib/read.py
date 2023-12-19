from source.databaselib import dbconnection


# To write long query in every place in the code was painful
# So we implemented these two methods in this file so that
# by passing the table name we get the query result.
# Although we could not use it for complex cases. In that case
# we used dbconnection.execute directly.
def read_from_table(table_name):
    return dbconnection.execute(f"select * from {table_name}")


# Same as read_from_table, but we can also pass filter value to this function.
def read_all_from_table_with_filter(table_name, filter):
    if str(filter).strip() == "":
        return dbconnection.execute(f"select * from {table_name}")
    else:
        return dbconnection.execute(f"select * from {table_name} where {filter}")
