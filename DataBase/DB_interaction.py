
local_db = dict()


def is_empty():
    """
    :return: True if the show DB is empty. False otherwise
    """
    return not bool(local_db)


def show_exists(show_id):
    """
    :param show_id:
    :return: True if show_id exists in the DB. False otherwise.
    """
    return show_id in local_db


def has_purchased_show(show_id, user_id):
    """
    checks if a user has purchased a show.
    :param show_id:
    :param user_id:
    :return: True if the user has purchased this show. False Otherwise
    """
    return user_id in local_db[show_id]['purchased']


def purchase_show(show_id, user_id):
    """
    makes a purchase - given user purchase given show.
    :param show_id:
    :param user_id:
    """
    local_db[show_id]['purchased'].add(user_id)

#
# def read_from_db(show_id, field=None):
#     if show_id in local_db:
#         if field == None:
#             return
#     return local_db[show_id][field]
#
# def write_to_db(show_id, field, value):
#     local_db[show_id][field] = value
#
# def increment_in_db(show_id, field):
#     local_db[show_id][field] += 1
#
# def add_to_db(show_id, field, value):
#     local_db[show_id][field].update(value)

    """
    checks if the given geolocation is in one of the specified locations
    :param geolocation:
    :param locations: iterable
    :return: True if geolocation in one of the locations. False otherwise.
    """


def get_restrictions(show_id):
    """
    :param show_id:
    :return: a set of restrictions (allowed locations) for viewing the show.
    """
    return local_db[show_id]['restrictions']


def view_show(show_id):
    """
    updates relevant data when a user views a show.
    :param show_id: id of the viewed show.
    """
    local_db[show_id]['views'] += 1


def get_most_popular_show():
    """
    :return: id of the most popular show (maximal view count)
    """
    return max(local_db,key= lambda x: local_db[x]['views'])


def get_most_popular_show_views():
    """
    finds the most popular show, and the number of views it has.
    :return: show_id, views
    """
    show_id = get_most_popular_show()
    views = local_db[show_id]['views']
    return show_id, views
