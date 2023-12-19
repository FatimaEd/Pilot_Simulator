from source.databaselib import write


# This functions takes some values using parameters and make a dictionary from it.
# Then it passes the dictionary to write.write_to_table using the table name "fuel_account"
# which saves the data to the database and returns auto-incremented id
def add_fuel_transaction(normal_fuel, saf_fuel):
    data = {
        "normal_fuel": normal_fuel,
        "saf_fuel": saf_fuel
    }

    return write.write_to_table("fuel_account", data)


# This functions takes some values using parameters and make a dictionary from it.
# Then it passes the dictionary to write.write_to_table using the table name "euro_balance"
# which saves the data to the database and returns auto-incremented id
def add_money_transaction(money):
    data = {
        "amount": money
    }
    return write.write_to_table("euro_balance", data)

