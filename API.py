from flask import Flask, request
from API_utils import *

app = Flask(__name__)

#argument names
SHOW_ID = 'showId'
USER_ID = 'userId'
LAT = 'lat'
LNG = 'lng'
VIEWS = 'views'



@app.route('/')
def func():
    return str(local_db), 200


@app.route('/purchase', methods=['POST'])
def purchase():

    show_id, user_id, lat, lng = parse_arguments([SHOW_ID, USER_ID, LAT, LNG])

    if not show_exists(show_id):
        return SHOW_NOT_FOUND_MSG, 404

    if has_purchased_show(show_id, user_id):
        return ALREADY_PURCHASED_MSG, 403

    if not is_location_for_purchase(lat, lng):
        return BLOCKED_LOCATION_MSG, 403

    purchase_show(show_id, user_id)

    return "", 201


@app.route('/restrictions', methods=['POST'])
def create_restriction():
    pass


@app.route('/restrictions', methods=['PUT'])
def add_restriction():
    pass


@app.route('/restrictions', methods=['GET'])
def get_restriction():
    pass


@app.route('/restrictions', methods=['DELETE'])
def delete_restriction():
    pass


@app.route('/view', methods=['GET'])
def view():
    show_id, user_id, lat, lng = parse_arguments([SHOW_ID, USER_ID, LAT, LNG])

    if not show_exists(show_id):
        return SHOW_NOT_FOUND_MSG, 404

    if not has_purchased_show(show_id, user_id):
        return NOT_PURCHASED_MSG, 403

    if not location_within_restrictions(show_id, lat, lng):
        return RESTRICTION_VIOLATION_MSG, 403

    view_show(show_id)

    return "", 200


@app.route('/most_popular', methods=['GET'])
def most_popular_show():
    if is_empty():
        return EMPTY_DB_MSG, 500

    show_id, views = get_most_popular_show_views()
    return {SHOW_ID: show_id,  VIEWS: views}, 200


def main():
    create_show('1', {'Israel'}, set())
    create_show('2', {'Egypt'}, set())
    app.run()


if __name__ == '__main__':
    main()

