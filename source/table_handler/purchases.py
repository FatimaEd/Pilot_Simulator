from source.databaselib import write
from source.databaselib import dbconnection
from source.table_handler import money_fuel_account


def create_new_purchase(profile_id, fuel, saf_fuel, euro, remarks):
    fuel_transaction_id = money_fuel_account.add_fuel_transaction(fuel, saf_fuel)
    euro_transaction_id = money_fuel_account.add_money_transaction(euro)

    data = {
        "profile_id": str(profile_id),
        "fuel_transaction_id": str(fuel_transaction_id),
        "euro_transaction_id": str(euro_transaction_id),
        "remarks": str(remarks)
    }

    return write.write_to_table("purchases", data)


def get_purchase_information(profile_id):
    sql = ("select purchases.purchase_id,  purchases.remarks, fuel_account.normal_fuel, fuel_account.saf_fuel, euro_balance.amount from purchases " +
            "inner join fuel_account on fuel_account.fuel_transaction_id= purchases.fuel_transaction_id " +
            "inner join euro_balance on  euro_balance.euro_transaction_id=purchases.euro_transaction_id " +
            f"where purchases.profile_id = '{profile_id}' order by purchase_id")

    return dbconnection.execute(sql)
