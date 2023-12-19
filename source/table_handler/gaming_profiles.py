from source.databaselib import write
from source.databaselib import dbconnection

from typing import Dict


# This function brings a list of profile id and profile name under a specific user.
# We have created a dictionary mapping the profile name against profile id and
# returned it for later use.
def list_profiles(username) -> Dict:
    profile_list = {}

    result = dbconnection.execute(f"select profile_id, profile_name from game_profile where username = '{username}'")

    for row in result:
        profile_list[row[0]] = str(row[1])

    return profile_list


# This function bring one specific gaming profile from game_profile table based on profile_id.
# To make it easier to use later we put it into a dictionary and Returning the dictionary.
def get_profile_info(profile_id) -> Dict:
    profile_info = {}

    result = dbconnection.execute(
        f"select profile_id, profile_name, aeroplane_model, consumption_fullload, consumption_base from game_profile where profile_id = '{profile_id}'")

    for row in result:
        profile_info["profile_id"] = row[0]
        profile_info["profile_name"] = row[1]
        profile_info["aeroplane_model"] = row[2]
        profile_info["consumption_fullload"] = row[3]
        profile_info["consumption_base"] = row[4]

    return profile_info

# This functions takes some values using parameters and make a dictionary from it.
# Then it passes the dictionary to write.write_to_table using the table name "game_profile"
# which saves the data to the database and returns auto-incremented id
def create_new_profile(username, profile_name, aeroplane_model, consumption_fullload,
                       consumption_base):
    data = {
        "username": username,
        "profile_name": profile_name,
        "aeroplane_model": aeroplane_model,
        "consumption_fullload": consumption_fullload,
        "consumption_base": consumption_base,
    }

    return write.write_to_table("game_profile", data)
