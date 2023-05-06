"""
Functions to ensure security, check login data, check user-visibilty for coaches and create new accounts
"""

import pandas as pd
import os

from coach_view import get_users, remove_client_by_id

parent_dir = os.path.dirname(os.getcwd())

users_path_and_filename = parent_dir + "/NutritionRecSys/Data/User_data/users.csv"
coaches_path_and_filename = parent_dir + "/NutritionRecSys/Data/User_data/coaches.csv"
coach_user_db_path_and_filename = parent_dir + "/NutritionRecSys/Data/User_data/coach_users.csv"
coach_user_requests_db_path_and_filename = parent_dir + "/NutritionRecSys/Data/User_data/coach_users_requests.csv"


def check_user_login(user_id, password):
    """
    Check if the entered user_id exists and if the password is correct
    :param user_id: the user-id
    :param password: the password
    :return: 1 if user-id is invalid, 2 if password is wrong, 3 if user-id exists and password is correct
    """

    users_and_pws = pd.read_csv(users_path_and_filename, index_col=False)

    all_valid_user_ids = users_and_pws["user_id"].values.tolist()
    all_valid_pws = users_and_pws["password"].values.tolist()

    if int(user_id) not in all_valid_user_ids:
        # Invalid user-id
        return 1

    for counter in range(len(all_valid_user_ids)):
        current_id = all_valid_user_ids[counter]
        if int(user_id) == int(current_id):
            current_pw = all_valid_pws[counter]
            if str(password) == str(current_pw):
                # Correct user-id and password combination
                return 3
            else:
                # Invalid password
                return 2


def check_coach_login(coach_id, password):
    """
    Check if the entered user_id exists and if the password is correct
    :param coach_id: the coach-id
    :param password: the password
    :return: 1 if coach-id is invalid, 2 if password is wrong, 3 if coach-id exists and password is correct
    """

    coaches_and_pws = pd.read_csv(coaches_path_and_filename, index_col=False)

    all_valid_coach_ids = coaches_and_pws["coach_id"].values.tolist()
    all_valid_pws = coaches_and_pws["password"].values.tolist()

    if int(coach_id) not in all_valid_coach_ids:
        # Invalid coach-id
        return 1

    for counter in range(len(all_valid_coach_ids)):
        current_id = all_valid_coach_ids[counter]
        if int(coach_id) == int(current_id):
            current_pw = all_valid_pws[counter]
            if str(password) == str(current_pw):
                # Correct coach-id and password combination
                return 3
            else:
                # Invalid password
                return 2


def check_coach_can_view_user(coach_id, user_id):
    """
    Check if the currently logged in coach is allowed to manage the user he/she is trying to view
    :param coach_id: the coach-id
    :param user_id: the user-id
    :return: True if allowed, False otherwise
    """

    current_coaches_users = get_users(coach_id)

    if int(user_id) in current_coaches_users:
        return True

    return False


def get_new_user_id():
    """
    Get a new, currently unused, user-id
    :return: A new user-id
    """

    users_and_pws = pd.read_csv(users_path_and_filename, index_col=False)

    user_id = 1
    all_used_user_ids = users_and_pws["user_id"].values.tolist()

    while user_id in all_used_user_ids:
        user_id = user_id + 1

    return user_id


def get_new_coach_id():
    """
    Get a new, currently unused, coach-id
    :return: A new coach-id
    """

    coaches_and_pws = pd.read_csv(coaches_path_and_filename, index_col=False)

    coach_id = 1
    all_used_coach_ids = coaches_and_pws["coach_id"].values.tolist()

    while coach_id in all_used_coach_ids:
        coach_id = coach_id + 1

    return coach_id


def write_new_coach_to_file(coach_id, password):
    """
    Write a newly created coach into the coaches.csv file
    :param coach_id: The id of the new coach
    :param password: the password the coach entered
    """

    with open(coaches_path_and_filename, "a+") as file:
        string_to_write = "\n" + str(coach_id) + "," + str(password)
        file.write(string_to_write)


def write_new_user_to_file(user_id, password):
    """
    Write a newly created user into the users.csv file
    :param user_id: The id of the new user
    :param password: the password the user entered
    """

    with open(users_path_and_filename, "a+") as file:
        string_to_write = "\n" + str(user_id) + "," + str(password)
        file.write(string_to_write)


def check_for_coaching_requests(user_id):
    """
    Check if the given user has an entry in the coach_users_requests.csv file, and return the coach ids of the
    coaches that requested to coach this user
    :param user_id: the id of the user
    :return: A list of coach ids, empty list if no request found
    """

    all_requests = pd.read_csv(coach_user_requests_db_path_and_filename, index_col=False)

    return all_requests.loc[all_requests['user_id'] == int(user_id)]["coach_id"].values.tolist()


def confirm_request_auth(coach_id, user_id):
    """
    Confirm a coaching request, delete the request from coach_users_requests.csv and add to coach_users.csv
    :param coach_id: The id of the coach
    :param user_id: The id of the client
    """

    remove_client_by_id(coach_id, user_id, True)

    with open(coach_user_db_path_and_filename, "a+") as file:
        string_to_write = "\n" + str(coach_id) + "," + str(user_id)
        file.write(string_to_write)
