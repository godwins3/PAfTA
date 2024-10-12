import requests

def get_location(ip: str):
    _ip = ip.strip()
    res = requests.get(f'https://ipapi.co/{_ip}/json/').json()

    return res


def distance(user_data, potential_user_data):
    distance = 0
    try:
        user_location = {"lon": user_data['personalInformation']['location'][0],
                         "lat": user_data['personalInformation']['location'][1]}

        potential_location = {"lon": potential_user_data['location'][0],
                              "lat": potential_user_data['location'][1]}

        distance = calculate_distance(user_location, potential_location)
    except Exception:
        pass

    return distance

from math import sin, cos, sqrt, atan2, radians


def calculate_distance(user: dict, potential: dict):
    # Approximate radius of earth in km
    R = 6373.0

    lat1 = radians(user['lat'])  # radians(-1.148030)
    lon1 = radians(user['lon'])  # radians(36.960590)
    lat2 = radians(potential['lat'])  # radians(-1.292066)
    lon2 = radians(potential['lon'])  # radians(36.821945)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    print("Result: ", distance)
    # print("Should be: ", 278.546, "km")
    return int(distance)

def get_country(ip: str):
    _ip = ip.strip()
    res = requests.get(f'http://ip-api.com/json/{_ip}').json()

    return res