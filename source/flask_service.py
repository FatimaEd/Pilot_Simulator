import random

from flask import Flask, request, render_template, jsonify, session, make_response, redirect, url_for
import secrets
from source.table_handler import profiles, gaming_profiles, trips, airports, purchases
from geopy.distance import geodesic

app = Flask(__name__)

app.secret_key = secrets.token_hex(16)

fuel_price_per_L = 1.21
max_passenger = 833
min_passenger = 530

consumption_full_load = 25  # per kilo
consumption_base = 16

# CO2 emission
fuel_density_kg_per_l = 0.803
CO2_emission_kg_per_l = 2.68


def generate_information(profile_id):
    current_profile_info = gaming_profiles.get_profile_info(profile_id)
    to_return = {}
    profile_info = {"profile_name": current_profile_info.get('profile_name'),
                    "aeroplane_model": current_profile_info.get('aeroplane_model'),
                    "consumption_base": current_profile_info.get('consumption_base'),
                    "consumption_fullload": current_profile_info.get('consumption_fullload')}

    to_return["profile_info"] = profile_info

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

    current_status = {"current_airport_id": airport_info_to.get('id'),
                      "latitude_deg": airport_info_to.get('latitude_deg'),
                      "longitude_deg": airport_info_to.get('longitude_deg'),
                      "airport_info_to": airport_info_to.get('name'),
                      "euro_balance": euro_balance,
                      "fuel_balance_normal": fuel_balance_normal,
                      "fuel_balance_saf": fuel_balance_saf}

    to_return["current_status"] = current_status

    if last_airport_from != last_airport_to:
        last_trip_info = {"airport_info_from": airport_info_from.get('name'),
                          "airport_info_to": airport_info_to.get('name'),
                          "last_trip_passenger": last_trip_passenger,
                          "last_trip_distance": last_trip_distance,
                          "last_trip_consumption_normal": last_trip_consumption_normal,
                          "last_trip_consumption_saf": last_trip_consumption_saf,
                          "last_trip_earning": last_trip_earning,
                          "last_trip_remarks": last_trip_remarks}

        to_return["last_trip_info"] = last_trip_info

    return to_return


# FUEL CONSUMPTION RANDOM NUMBER OF PASSENGERS
def normal_fuel_cost(fuel_to_buy):
    return fuel_to_buy * fuel_price_per_L


def saf_fuel_cost(fuel_to_buy):
    return normal_fuel_cost(fuel_to_buy) * 2.3


def buy_fuel_internal(amount, is_saf):
    profile_id = session["profileId"]
    total_fuel_cost_in_euro = 0
    remarks = ""
    if is_saf:
        total_fuel_cost_in_euro = int(saf_fuel_cost(amount))
        remarks = f"{amount} liter SAF fuel has been purchased with {total_fuel_cost_in_euro} euros"
    else:
        total_fuel_cost_in_euro = int(normal_fuel_cost(amount))
        remarks = f"{amount} liter normal fuel has been purchased with {total_fuel_cost_in_euro} euros"

    previous_normal_fuel, previous_saf_fuel, previous_euro = trips.get_account_balance(profile_id)

    return_list = []
    if previous_euro < total_fuel_cost_in_euro:
        saf_text = " "
        if is_saf:
           saf_text = f"SAF "
        return_list.append(f"For {amount} liter {saf_text}fuel you will be charged {total_fuel_cost_in_euro} euros")
        return_list.append("But you do not have enough money in your account.")
        return_list.append(f"You currently have {previous_euro} euro in your account.")
        return {"error": return_list}
    else:
        if is_saf:
            purchases.create_new_purchase(str(profile_id),
                                          str(0),
                                          str(amount),
                                          str(total_fuel_cost_in_euro * -1),
                                          remarks)
        else:
            purchases.create_new_purchase(str(profile_id),
                                          str(amount),
                                          str(0),
                                          str(total_fuel_cost_in_euro * -1),
                                          remarks)
        return_list.append(remarks)

    return {"output": return_list}


def calculate_co2_emissions(fuel_consumption_total_in_liters, passengers_count):
    # fuel consumption
    fuel_consumption_kg = fuel_consumption_total_in_liters * fuel_density_kg_per_l

    # CO2 emissions
    co2_emissions_kg = fuel_consumption_kg * CO2_emission_kg_per_l

    # CO2 emissions/passenger
    co2_emissions_per_passenger = co2_emissions_kg / passengers_count

    return co2_emissions_kg, co2_emissions_per_passenger


def calc_fuel_consumption(passenger):
    return 16 / min_passenger * passenger


def calc_distance(current_lat, current_long, target_lat, target_long):
    start_coord = (current_lat, current_long)
    end_coord = (target_lat, target_long)

    distance_in_km = geodesic(start_coord, end_coord).kilometers
    return int(distance_in_km)


def get_random_destination_list():
    status_information = generate_information(session['profileId'])

    result = airports.get_random_airport_list(status_information["current_status"]["current_airport_id"])

    destination_list = {}

    for row in result:
        distance = calc_distance(status_information["current_status"]["latitude_deg"],
                                 status_information["current_status"]["longitude_deg"],
                                 row[3], row[4])

        airport_info = {}
        airport_info["latitude_deg"] = status_information["current_status"]["latitude_deg"]
        airport_info["longitude_deg"] = status_information["current_status"]["longitude_deg"]
        airport_info["distance"] = distance
        airport_info["name"] = row[2]

        destination_list[row[1]] = airport_info

    to_return = {}

    to_return["destination_list"] = destination_list
    to_return["current_status"] = status_information["current_status"]

    return to_return



def get_Statistics():
    result = trips.get_statistics()

    list = []

    for row in result:
        record = {}
        record["profile_name"] = row[0]
        record["total_distance"] = row[1]
        record["total_euro_balance"] = row[2]
        record["saf_fuel_used"] = row[3]
        record["normal_fuel_used"] = row[4]
        record["CO2_emission_kilometer"] = row[5]
        list.append(record)

    return list


##########################---HTML---################################

@app.route('/login')
def login_page():
    if is_logged_in():
        return redirect(url_for('index_page'))
    else:
        return render_template("login.html")


@app.route('/registration')
def registration_page():
    if is_logged_in():
        return redirect(url_for('index_page'))
    else:
        return render_template("registration.html")


@app.route('/')
def index_page():
    if is_logged_in():
        return render_template("index.html")
    else:
        return redirect(url_for('login_page'))


##########################---API---################################

def is_logged_in():
    if 'username' in session:
        return True
    else:
        return False


@app.route('/api/login', methods=['POST'])
def login_api():
    data = request.get_json()

    if profiles.check_user(data["username"], data["password"]):
        session['username'] = data["username"]
        return make_response('', 200)
    else:
        return make_response('', 401)


@app.route('/api/logout', methods=['DELETE'])
def logout_api():
    print("working")
    session.pop('username', None)
    session.pop('profileId', None)
    return make_response('', 200)


@app.route('/api/registration', methods=['POST'])
def registration_api():
    data = request.get_json()

    try:
        profiles.create_new_user(data["username"], data["full_name"], data["password"])
        session['username'] = data["username"]
        return make_response('', 200)
    except:
        return make_response('', 409)


@app.route('/api/profiles', methods=['POST'])
def create_profile_api():
    data = request.get_json()

    try:
        profile_id = gaming_profiles.create_new_profile(session['username'], data["profile_name"], "Airbus A380",
                                                        str(consumption_full_load),
                                                        str(consumption_base))

        session['profileId'] = profile_id

        random_airport = airports.get_initial_airport_info()

        trips.create_new_trip(profile_id, random_airport.get("id"), random_airport.get("id"), "0", "24000", "18000",
                              "0",
                              "50000", "Initial fuel and euros. Enough for flying 2000km distance.")
        return make_response('', 200)
    except:
        return make_response('', 409)


@app.route('/api/profiles/current', methods=['GET'])
def get_current_profile_api():
    if 'profileId' in session:
        to_return = {
            "profileId": session['profileId']
        }
        return jsonify(to_return), 200
    else:
        return make_response('', 404)


@app.route('/api/profiles', methods=['GET'])
def get_profiles_api():
    try:
        profile_list = gaming_profiles.list_profiles(session['username'])
        return jsonify(profile_list), 200
    except:
        return make_response('', 409)


@app.route('/api/current_status', methods=['GET'])
def get_current_status_api():
    # try:
    toStr = jsonify(generate_information(session['profileId']))
    return toStr, 200
    # except:
    #     return make_response('', 409)


@app.route('/api/profiles/current', methods=['POST'])
def get_random_airport_list():
    data = request.get_json()

    try:
        gaming_profiles.get_profile_info(data["profileId"])
        session['profileId'] = data["profileId"]
        return make_response('', 200)
    except:
        return make_response('', 400)


def make_a_trip_internal(selected_ident, is_saf_fuel):
    profile_id = session['profileId']
    status_information = generate_information(profile_id)
    current_status = status_information["current_status"]

    current_airport_id = current_status["current_airport_id"]

    current_latitude_deg = current_status["latitude_deg"]
    current_longitude_deg = current_status["longitude_deg"]

    random_passenger = str(random.randint(min_passenger, max_passenger))

    fuel_consumption = calc_fuel_consumption(int(random_passenger))

    fuel_consumption_normal = 0
    fuel_consumption_saf = 0

    destination_airport = airports.get_airport_info_by_ident(selected_ident)

    des_latitude_deg = destination_airport["latitude_deg"]
    des_longitude_deg = destination_airport["longitude_deg"]

    distance = calc_distance(current_latitude_deg, current_longitude_deg, des_latitude_deg, des_longitude_deg)

    total_fuel_consumption = (distance * fuel_consumption) * -1

    earning = int(total_fuel_consumption * -1 * 2 * 3 * int(random_passenger) / max_passenger)

    if is_saf_fuel:
        fuel_consumption_saf = total_fuel_consumption
    else:
        fuel_consumption_normal = total_fuel_consumption

    remarks = (f"This trip collected {earning} euro revenue while traveling "
               f"{distance} km consuming"
               f" {int(total_fuel_consumption * -1)} liter fuel")

    trips.create_new_trip(profile_id, str(current_airport_id), str(destination_airport["id"]),
                          random_passenger, str(fuel_consumption_normal), str(fuel_consumption_saf),
                          str(distance),
                          str(earning), remarks)

    co2_emissions_total, co2_emissions_per_passenger = calculate_co2_emissions((total_fuel_consumption * -1),
                                                                               int(random_passenger))

    co2_emissions_total_saf = int(co2_emissions_total * .2)
    co2_emissions_per_passenger_saf = int(co2_emissions_per_passenger * .2)

    return_list = []

    if is_saf_fuel:
        return_list.append("Thank you! You have used SAF which reduces carbon emissions by 80%")
        return_list.append(f"Total CO2 emission               : {co2_emissions_total_saf} kg")
        return_list.append(f"Number of passenger on board     : {random_passenger}")
        return_list.append(f"Total CO2 emission per passenger : {co2_emissions_per_passenger_saf} kg")

    else:
        return_list.append("You have used normal fuel")
        return_list.append(f"Total CO2 emission               : {int(co2_emissions_total)} kg")
        return_list.append(f"Total CO2 emission per passenger : {int(co2_emissions_per_passenger)} kg")
        return_list.append(
            f"You could have reduced total carbon emissions to {co2_emissions_total_saf} kg if you would have used "
            f"SAF fuel which is better for the planet.")

    return_list.append(remarks)

    to_return = {"output": return_list}

    return to_return


@app.route('/api/make-a-trip', methods=['POST'])
def make_a_trip():
    data = request.get_json()

    try:
        to_return = make_a_trip_internal(data["airport_IATA"], data["use_saf"])
        return to_return, 200
    except:
        return make_response('', 400)


@app.route('/api/purchase', methods=['POST'])
def buy_fuel():
    data = request.get_json()
    print(data)
    # try:
    to_return = buy_fuel_internal(data["amount"], data["use_saf"])
    return to_return, 200
    # except:
    #     return make_response('', 400)


@app.route('/api/get-random-airports', methods=['GET'])
def change_current_profile():
    try:
        toStr = jsonify(get_random_destination_list())
        return toStr, 200
    except:
        return make_response('', 409)


@app.route('/api/statistics', methods=['GET'])
def get_current_statistics():
    try:
        toStr = jsonify(get_Statistics())
        return toStr, 200
    except:
        return make_response('', 409)


app.run(host="0.0.0.0", debug=True, port=80)
