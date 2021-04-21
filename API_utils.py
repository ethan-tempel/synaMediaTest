import requests
from functools import lru_cache
from flask_restful import reqparse
from DataBase.DB_interaction import *

ALLOWED_PURCHASE_LOCATIONS = {'Israel'}

# error messages
SHOW_NOT_FOUND_MSG = "show not found"
ALREADY_PURCHASED_MSG = "user already purchased this show"
BLOCKED_LOCATION_MSG = "can't make purchases from this location"
NOT_PURCHASED_MSG = "user did not purchase this show"
RESTRICTION_VIOLATION_MSG = "location violates show's viewing restrictions"
EMPTY_DB_MSG = "no shows in the DB"


def parse_arguments(required_args=list(), optional_args=list()):
    """
    parses request arguments, returns a list of argument values in the same
    order they were given.
    :param required_args: specifies required arguments.
    :param optional_args: specifies optional arguments.
    :return: list of argument values.
    """
    parser = reqparse.RequestParser()
    for arg in required_args:
        parser.add_argument(arg, required=True)
    for arg in optional_args:
        parser.add_argument(arg, required=False)

    args = parser.parse_args()

    output_args = list()
    for arg in required_args:
        output_args.append(args[arg])
    for arg in optional_args:
        output_args.append(args[arg])

    return output_args


@lru_cache()
def get_location(lat, lng):
    """
    returns the location name (country name) of the given coordinates.
    uses a local cache. if the geolocation does not exist in the cache, gets
     the info from an external service.
    :param lat: latitude
    :param lng: longitude
    :return: location (country) name of the given geolocation
    """
    query = {'lat': lat, 'lng': lng, 'username': 'ethan.tempel','type': "JSON"}
    response = requests.get("http://api.geonames.org/countryCode?",params=query)
    return response.json()['countryName']


def is_location_for_purchase(lat, lng):
    """
    checks if the given location is allowed for making purchases.
    :param lat: latitude
    :param lng: longitude
    :return: True if the location is allowed for purchases. False otherwise.
    """
    location = get_location(lat, lng)
    return location in ALLOWED_PURCHASE_LOCATIONS


def location_within_restrictions(show_id, lat, lng):
    """
    checks if the location violates any restrictions of the show.
    :param show_id:
    :param lat: latitude
    :param lng: longitude
    :return: True if the location is within the restrictions. False otherwise.
    """
    location = get_location(lat, lng)
    return location in get_restrictions(show_id)


def create_show(show_id, restrictions, purchased, views=0):
    """
    initialize a show record in the DB
    :param show_id:
    :param restrictions:
    :param purchased:
    :param views:
    """
    local_db[show_id] = {'restrictions': restrictions, 'purchased': purchased, 'views': views}