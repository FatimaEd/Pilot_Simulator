from source.databaselib import write
from source.databaselib import dbconnection
from source.table_handler import money_fuel_account
from source.table_handler import purchases


def create_new_trip(profile_id, from_airport, to_airport, passenger, fuel, saf_fuel, distance, euro, remarks):
    fuel_transaction_id = money_fuel_account.add_fuel_transaction(fuel, saf_fuel)
    euro_transaction_id = money_fuel_account.add_money_transaction(euro)

    data = {
        "profile_id": str(profile_id),
        "from_airport": str(from_airport),
        "to_airport": str(to_airport),
        "passenger": str(passenger),
        "fuel_transaction_id": str(fuel_transaction_id),
        "distance": str(distance),
        "euro_transaction_id": str(euro_transaction_id),
        "remarks": str(remarks)
    }

    return write.write_to_table("trips", data)


# This function runs a sql query
def get_trip_information(profile_id):
    sql = ("select trips.trip_id, trips.from_airport, trips.to_airport , trips.distance, trips.remarks," +
           " fuel_account.normal_fuel, fuel_account.saf_fuel, euro_balance.amount, trips.passenger from trips " +
           "inner join fuel_account on fuel_account.fuel_transaction_id= trips.fuel_transaction_id " +
           "inner join euro_balance on  euro_balance.euro_transaction_id=trips.euro_transaction_id " +
           f"where profile_id = '{profile_id}' order by trip_id")

    return dbconnection.execute(sql)


# This function runs a sql query
def get_statistics():
    sql = """
            SELECT
                game_profile.profile_name,
                SUM(trips.distance) AS total_distance,
                SUM(euro_balance.amount) AS total_euro_balance,
                SUM(IF(fuel_account.saf_fuel > 0, 0, fuel_account.saf_fuel * -1)) AS saf_fuel_used,
                SUM(IF(fuel_account.normal_fuel > 0, 0, fuel_account.normal_fuel * -1)) AS normal_fuel_used,
                ROUND((
                    (SUM(IF(fuel_account.saf_fuel > 0, 0, fuel_account.saf_fuel * -1)) *  0.803 * 2.68 * 0.2) +
                    (SUM(IF(fuel_account.normal_fuel > 0, 0, fuel_account.normal_fuel * -1)) *  0.803 * 2.68)
                ) / SUM(trips.distance)) AS CO2_emission_kilometer
            FROM
                trips
                INNER JOIN game_profile ON trips.profile_id = game_profile.profile_id
                INNER JOIN fuel_account ON trips.fuel_transaction_id = fuel_account.fuel_transaction_id
                INNER JOIN euro_balance ON trips.euro_transaction_id = euro_balance.euro_transaction_id
            GROUP BY
                profile_name
            HAVING
                total_distance != 0
            ORDER BY
                CO2_emission_kilometer, total_euro_balance DESC
        """

    return dbconnection.execute(sql)


#  This function calculates all the fuel , saf fuel
#  and euro transactions and returns three summaries.
def get_account_balance(profile_id):
    trip_result = get_trip_information(profile_id)
    purchase_result = purchases.get_purchase_information(profile_id)

    fuel_balance_normal = 0
    fuel_balance_saf = 0
    euro_balance = 0

    for row in trip_result:
        fuel_balance_normal = fuel_balance_normal + int(row[5])
        fuel_balance_saf = fuel_balance_saf + int(row[6])
        euro_balance = euro_balance + int(row[7])

    for row in purchase_result:
        fuel_balance_normal = fuel_balance_normal + int(row[2])
        fuel_balance_saf = fuel_balance_saf + int(row[3])
        euro_balance = euro_balance + int(row[4])

    return fuel_balance_normal, fuel_balance_saf, euro_balance
