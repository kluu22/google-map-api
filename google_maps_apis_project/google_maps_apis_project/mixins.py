from django.conf import settings
import requests
from humanfriendly import format_timespan
from math import radians, cos, asin, sqrt, pi, sin


def Directions(*args, **kwargs):
    '''
    Handles directions from Google
    '''
    address_a = kwargs.get("address_a")
    address_b = kwargs.get("address_b")

    # use Google Maps APIs - Geocoding to find lat/long of a given start address
    result = requests.get(
        'https://maps.googleapis.com/maps/api/geocode/json?',
        params={
            'address': address_a,
            "key": settings.GOOGLE_API_KEY
        })

    address_a_result = result.json()

    lat_a = address_a_result['results'][0]['geometry']['location']['lat']
    long_a = address_a_result['results'][0]['geometry']['location']['lng']

    # use Google Maps APIs - Geocoding to find lat/long of a given destination address
    result = requests.get(
        'https://maps.googleapis.com/maps/api/geocode/json?',
        params={
            'address': address_b,
            "key": settings.GOOGLE_API_KEY
        })

    address_a_result = result.json()

    lat_b = address_a_result['results'][0]['geometry']['location']['lat']
    long_b = address_a_result['results'][0]['geometry']['location']['lng']

    # format lat/long from start address and lat/long from destination address to strings
    origin = f'{lat_a},{long_a}'
    destination = f'{lat_b},{long_b}'

    # pass new formatted strings of origin and destination to Google Maps APIs - Direction
    # to get direction, duration, distance as bonus
    result = requests.get(
        'https://maps.googleapis.com/maps/api/directions/json?',
        params={
            'origin': origin,
            'destination': destination,
            "key": settings.GOOGLE_API_KEY
        })

    directions = result.json()

    if directions["status"] == "OK":

        routes = directions["routes"][0]["legs"]

        distance = 0
        duration = 0
        route_list = []

        for route in range(len(routes)):
            distance += int(routes[route]["distance"]["value"])
            duration += int(routes[route]["duration"]["value"])

            route_step = {
                'origin': routes[route]["start_address"],
                'destination': routes[route]["end_address"],
                'distance': routes[route]["distance"]["text"],
                'duration': routes[route]["duration"]["text"],

                'steps': [
                    [
                        s["distance"]["text"],
                        s["duration"]["text"],
                        s["html_instructions"],

                    ]
                    for s in routes[route]["steps"]]
            }

            route_list.append(route_step)


    def distance_by_formula(lat_a, long_a, lat_b, long_b):
        """
        Calculate the great circle distance in kilometers between two points on the earth
        using Haversine Formula and not API
        """
        # convert string of lat/lng to decimal lat/lng
        lat_a = float(lat_a)
        long_a = float(long_a)
        lat_b = float(lat_b)
        long_b = float(long_b)

        # convert decimal degrees to radians
        lat_a, long_a, lat_b, long_b = map(radians, [lat_a, long_a, lat_b, long_b])

        dlon = long_b - long_a
        dlat = lat_b - lat_a
        a = sin(dlat / 2) ** 2 + cos(lat_a) * cos(lat_b) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        r = 6371  # radius of earth in kilometers
        return c * r

    return {
        "origin_address": address_a,
        "origin": origin,
        "destination_address": address_b,
        "destination": destination,
        "distance": f"{round(distance / 1000, 2)} Km",
        "distance_formula": f"{round(distance_by_formula(lat_a=lat_a, long_a=long_a, lat_b=lat_b, long_b=long_b), 2)} Km",
        "duration": format_timespan(duration),
        "route": route_list
    }