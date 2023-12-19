from source.databaselib import dbconnection
from typing import Dict


# This function brings one random airport information from airports table.
# To make it easier to use later we put it into a dictionary and Returning the dictionary.
def get_initial_airport_info() -> Dict:
    profile_info = {}

    result = dbconnection.execute(
        "SELECT id, ident, name, latitude_deg, longitude_deg FROM airports ORDER BY RAND() LIMIT 1")

    for row in result:
        profile_info["id"] = row[0]
        profile_info["ident"] = row[1]
        profile_info["name"] = row[2]
        profile_info["latitude_deg"] = row[3]
        profile_info["longitude_deg"] = row[4]

    return profile_info


# This function bring one specific airport information from airports table based on airport_id.
# To make it easier to use later we put it into a dictionary and Returning the dictionary.
def get_airport_info(airport_id) -> Dict:
    profile_info = {}

    result = dbconnection.execute(
        f"SELECT id, ident, name, latitude_deg, longitude_deg FROM airports  where id = {airport_id}")

    for row in result:
        profile_info["id"] = row[0]
        profile_info["ident"] = row[1]
        profile_info["name"] = row[2]
        profile_info["latitude_deg"] = row[3]
        profile_info["longitude_deg"] = row[4]

    return profile_info


def get_airport_info_by_ident(airport_ident) -> Dict:
    profile_info = {}

    result = dbconnection.execute(
        f"SELECT id, ident, name, latitude_deg, longitude_deg FROM airports  where ident = '{airport_ident}'")

    for row in result:
        profile_info["id"] = row[0]
        profile_info["ident"] = row[1]
        profile_info["name"] = row[2]
        profile_info["latitude_deg"] = row[3]
        profile_info["longitude_deg"] = row[4]

    return profile_info


# This function brings 25 random airport information from airports table.
# We have directly returned the result of sql command.
def get_random_airport_list(current_airport_id):
    sql = f"SELECT id, ident, name, latitude_deg, longitude_deg FROM airports WHERE id != {current_airport_id} ORDER BY RAND() LIMIT 25"
    return dbconnection.execute(sql)
