from source.table_handler import profiles
from source.table_handler import airports

from source.table_handler import gaming_profiles
from source.table_handler import trips
from source.table_handler import purchases
from geopy.distance import geodesic

from typing import Dict
import random

current_user = ""
current_profile = ""
current_profile_info = Dict
fuel_price_per_L = 1.21
max_passenger = 833
min_passenger = 530

consumption_full_load = 25  # per kilo
consumption_base = 16


def hold():
    input("Press enter to continue ...")
    print("")
    print("")


def command():
    str_num = input()
    if str_num.strip() == "":
        num = -1
    else:
        num = int(str_num)
    print("")
    print("")
    return num


def print_welcome_screen():
    print("=====================================")
    print("Welcome to Pilot simulator")
    print("--------------------------")
    print("")
    print("Please select an option below")
    print("")
    print("\t 1. Register")
    print("\t 2. Login")
    print("\t 3. Exit")
    print("")

    option = command()
    if option == 1:
        print_registration_screen()
    elif option == 2:
        print_login_screen()
    elif option == 3:
        return 0


def print_registration_screen():
    print("=====================================")
    print("Register a new user")
    print("--------------------------")
    print("")
    username = input("Username: ")
    full_name = input("Full name: ")
    password = input("Password: ")
    profiles.create_new_user(username, full_name, password)
    print("New user has been created successfully!")
    hold()


def print_login_screen():
    print("=====================================")
    print("Login")
    print("--------------------------")
    print("")
    username = input("Username: ")
    password = input("Password: ")
    if profiles.check_user(username, password):
        print("Login successfully!")
        global current_user
        current_user = username
        hold()
    else:
        print("Invalid username or password!")
        hold()


def print_profile_list_screen():
    global current_user
    global current_profile
    print("==============================================================")
    print("Profile selection")
    print("--------------------------")
    print("")
    print("Please select a profile to continue or create a new profile.")
    print("")
    profile_list = gaming_profiles.list_profiles(current_user)

    count = 1
    id_list = []
    for key, value in profile_list.items():
        print(f"{count}. {value}")
        id_list.append(key)
        count += 1
    print(f"{count}. [ New Profile ]")
    print(f"{count + 1}. [ Logout ]")
    print("")

    num = int(input(": "))

    if num == count:
        create_new_profile_screen()
    elif num == count + 1:
        current_user = ""
    elif num < count:
        current_profile = id_list[num - 1]


def create_new_profile_screen():
    print("=====================================")
    print("Create new profile")
    print("--------------------------")
    print("")
    global current_user
    profile_name = input("Profile name: ")
    aeroplane_model, consumption_fullload, consumption_base = create_random_aircraft()

    profile_id = gaming_profiles.create_new_profile(current_user, profile_name, aeroplane_model, consumption_fullload,
                                                    consumption_base)

    random_airport = airports.get_initial_airport_info()

    trips.create_new_trip(profile_id, random_airport.get("id"), random_airport.get("id"), "0", "24000", "18000", "0",
                          "50000", "Initial fuel and euros. Enough for flying 2000km distance.")

    print("New profile created successfully!")
    hold()


def create_random_aircraft():
    # Will be randomized in later implementation
    # Airbus A380 consumes 3liter/ 100 kilo for a passenger.
    # Airbus max capacity 853 people
    # So for 100 kilo 853*3 = 2559 liter per 100 kilo
    # So 2559/100 = 25.59 per kilo on full load.
    # We are rounding that to 25 to make it easier.
    # So our max passenger will be 833

    return "Airbus A380", str(consumption_full_load), str(consumption_base)


def game_screen():
    global current_profile
    global current_profile_info
    print("===============================================================")
    print("Aeroplane Console")
    print("")
    print("---------------------------------------------------------------")
    print("Profile Info")
    print("---------------------------------------------------------------")

    current_profile_info = gaming_profiles.get_profile_info(current_profile)

    print(f"Profile name            : {current_profile_info.get('profile_name')}")
    print(f"Aeroplane model         : {current_profile_info.get('aeroplane_model')}")
    print(f"Consumption (base)      : {current_profile_info.get('consumption_base')} litre/km")
    print(f"Consumption (full load) : {current_profile_info.get('consumption_fullload')} litre/km")
    print("")

    current_airport_info = print_trip_status(current_profile_info.get("profile_id"))
    print("")
    print("")

    print("Choose an option from below:")
    print("")

    print("\t1. Make a trip")
    print("\t2. Purchase fuel")
    print("\t3. Game Statistics")
    print("\t4. Exit from profile")

    num = command()

    if num == 1:
        trip_screen(current_airport_info.get("id"), current_airport_info.get("latitude_deg"),
                    current_airport_info.get("longitude_deg"))
    elif num == 2:
        purchase_screen(current_profile)
    elif num == 3:
        print("showing game statistics")
    elif num == 4:
        current_profile = ""


def purchase_screen(profile_id):
    print("---------------------------------------------------------------")
    print("Purchase fuels")
    print("---------------------------------------------------------------")

    normal_fuel = int(input("How much normal fuel you want to buy in liters? : "))
    saf_fuel = int(input("How much SAF fuel you want to buy in liters? : "))

    total_fuel_cost_in_euro = int(normal_fuel_cost(normal_fuel) + saf_fuel_cost(saf_fuel))

    previous_normal_fuel, previous_saf_fuel, previous_euro = trips.get_account_balance(profile_id)



    print(
        f"For {normal_fuel} liter normal fuel and {saf_fuel} liter SAF fuel "
        f"you will be charged {total_fuel_cost_in_euro} euros")

    remarks = (f"{normal_fuel} liter normal fuel and {saf_fuel} liter SAF fuel "
               f"are purchased with {total_fuel_cost_in_euro} euros")
    if previous_euro < total_fuel_cost_in_euro:
        print("But you do not have enough money in your account.")
        print(f"You currently have {previous_euro} euro in your account.")
        hold()
    else:
        affirmative = str(input("Do you want to proceed? [Y/N (or any)] ")).upper()
        if affirmative == "Y":
            purchases.create_new_purchase(str(profile_id),
                                          str(normal_fuel),
                                          str(saf_fuel),
                                          str(total_fuel_cost_in_euro * -1),
                                          remarks)
            print(remarks)
            hold()
        else:
            print("Purchase canceled.")
            hold()


# FUEL CONSUMPTION RANDOM NUMBER OF PASSENGERS
def normal_fuel_cost(fuel_to_buy):
    return fuel_to_buy * fuel_price_per_L


def saf_fuel_cost(fuel_to_buy):
    return normal_fuel_cost(fuel_to_buy) * 2.3


def trip_screen(current_airport_id, current_lat, current_lang):
    print("---------------------------------------------------------------")
    print("Please select an airport from below")
    print("---------------------------------------------------------------")

    ident_id_dic = {}
    ident_distance_dic = {}

    result = airports.get_random_airport_list(current_airport_id)

    for row in result:
        distance = calc_distance(current_lat, current_lang, row[3], row[4])
        print(f" {row[1]} : {row[2]} ({distance} km)")
        ident_id_dic[str(row[1])] = str(row[0])
        ident_distance_dic[str(row[1])] = int(distance)

    selected_ident = str(input(": ")).upper()

    random_passenger = str(random.randint(min_passenger, max_passenger))

    fuel_consumption = calc_fuel_consumption(int(random_passenger))

    if selected_ident in ident_id_dic.keys():
        fuel_consumption_normal = 0
        fuel_consumption_saf = 0

        total_fuel_consumption = (int(ident_distance_dic.get(selected_ident)) * fuel_consumption) * -1

        earning = int(total_fuel_consumption * -1 * 2 * 3 * int(random_passenger) / max_passenger)

        is_saf_fuel = str(input("Use SAF fuel? [Y/N (or any)] ")).upper()

        if is_saf_fuel == "Y":
            fuel_consumption_saf = total_fuel_consumption
        else:
            fuel_consumption_normal = total_fuel_consumption

        remarks = (f"This trip collected {earning} euro revenue while traveling "
                   f"{ident_distance_dic.get(selected_ident)} km consuming"
                   f" {int(total_fuel_consumption * -1)} liter fuel")

        trips.create_new_trip(current_profile, str(current_airport_id), str(ident_id_dic.get(selected_ident)),
                              random_passenger, str(fuel_consumption_normal), str(fuel_consumption_saf),
                              str(ident_distance_dic.get(selected_ident)),
                              str(earning), remarks)

        co2_emissions_total, co2_emissions_per_passenger = calculate_co2_emissions((total_fuel_consumption * -1),
                                                                                   int(random_passenger))

        co2_emissions_total_saf = int(co2_emissions_total * .2)
        co2_emissions_per_passenger_saf = int(co2_emissions_per_passenger * .2)

        if is_saf_fuel == "Y":
            print("Thank you! You have used SAF which reduces carbon emissions by 80%")
            print(f"Total CO2 emission               : {co2_emissions_total_saf} kg")
            print(f"Total CO2 emission per passenger : {co2_emissions_per_passenger_saf} kg")
        else:
            print("You have used normal fuel")
            print(f"Total CO2 emission               : {int(co2_emissions_total)} kg")
            print(f"Total CO2 emission per passenger : {int(co2_emissions_per_passenger)} kg")
            print(f"You could have reduced total carbon emissions to {co2_emissions_total_saf}"
                  f" kg if you would have used SAF fuel which is better for the planet.")

        print("")
        print(remarks)
        hold()
    else:
        print("Invalid airport ident.")
        hold()


def calc_fuel_consumption(passenger):
    return 16 / min_passenger * passenger


def calc_distance(current_lat, current_long, target_lat, target_long):
    start_coord = (current_lat, current_long)
    end_coord = (target_lat, target_long)

    distance_in_km = geodesic(start_coord, end_coord).kilometers
    return int(distance_in_km)


def print_trip_status(profile_id):
    result = trips.get_trip_information(profile_id)

    fuel_balance_normal, fuel_balance_saf, euro_balance = trips.get_account_balance(profile_id)

    last_airport_from = 0
    last_airport_to = 0
    last_trip_distance = 0
    last_trip_remarks = ""
    last_trip_consumption_normal = 0
    last_trip_consumption_saf = 0
    last_trip_earning = 0
    last_trip_passenger = 0

    # also need to add purchase fuels and euro transactions
    for row in result:
        last_airport_from = int(row[1])
        last_airport_to = int(row[2])
        last_trip_distance = int(row[3])
        last_trip_remarks = str(row[4])
        last_trip_consumption_normal = int(row[5]) * -1
        last_trip_consumption_saf = int(row[6]) * -1
        last_trip_earning = int(row[7])
        last_trip_passenger = int(row[8])

    airport_info_from = airports.get_airport_info(last_airport_from)
    airport_info_to = airports.get_airport_info(last_airport_to)

    print("---------------------------------------------------------------")
    print("Current Status ")
    print("---------------------------------------------------------------")
    print(f"Current Airport     : {airport_info_to.get('name')}")
    print(f"Euro Balance        : {euro_balance}")
    print(f"Normal Fuel Balance : {fuel_balance_normal}")
    print(f"SAF Fuel Balance    : {fuel_balance_saf}")

    print("")
    print("")
    if last_airport_from != last_airport_to:
        print("---------------------------------------------------------------")
        print("Last trip info ")
        print("---------------------------------------------------------------")
        print(f"From                      : {airport_info_from.get('name')}")
        print(f"To                        : {airport_info_to.get('name')}")
        print(f"Passenger on-board        : {last_trip_passenger} people")
        print(f"Distance covered          : {last_trip_distance} km")
        print(f"Fuel consumption (normal) : {last_trip_consumption_normal} liter")
        print(f"Fuel consumption (saf)    : {last_trip_consumption_saf} liter")
        print(f"Earning                   : {last_trip_earning} euro")
        print(f"Remarks                   : {last_trip_remarks}")

    return airport_info_to


# CO2 emission
fuel_density_kg_per_l = 0.803
CO2_emission_kg_per_l = 2.68


def calculate_co2_emissions(fuel_consumption_total_in_liters, passengers_count):
    # fuel consumption
    fuel_consumption_kg = fuel_consumption_total_in_liters * fuel_density_kg_per_l

    # CO2 emissions
    co2_emissions_kg = fuel_consumption_kg * CO2_emission_kg_per_l

    # CO2 emissions/passenger
    co2_emissions_per_passenger = co2_emissions_kg / passengers_count

    return co2_emissions_kg, co2_emissions_per_passenger


while True:
    if current_user != "":
        if current_profile != "":
            game_screen()
        else:
            print_profile_list_screen()
    elif print_welcome_screen() == 0:
        print("Good bye!")
        break
