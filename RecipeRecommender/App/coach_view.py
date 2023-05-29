"""
Functions for the coach-view of the web-app
"""

import os
import time
import pandas as pd

parent_dir = os.path.dirname(os.getcwd())

coach_user_db_path_and_filename = parent_dir + "/NutritionRecSys/Data/User_data/coach_users.csv"
coach_user_requests_db_path_and_filename = parent_dir + "/NutritionRecSys/Data/User_data/coach_users_requests.csv"


def get_users(coach_id):
    """
    Get all users that a coach manages
    :param coach_id: The id of the coach
    :return: a list of user_ids
    """

    coach_user_info = pd.read_csv(coach_user_db_path_and_filename, index_col=False)

    return_list = coach_user_info.loc[coach_user_info['coach_id'] == int(coach_id)]["user_id"].values.tolist()
    return_list.sort()

    return return_list


def remove_client_by_id(coach_id, client_id, request=False):
    """
    Remove a given client of a given coach, either from coach_users.csv or coach_users_requests.csv
    :param coach_id: The id of the coach
    :param client_id: the id of the client
    :param request: False (default) if client should be removed from coach_users.csv, True if from coach_users_requests.csv
    """

    filename = coach_user_db_path_and_filename
    if request:
        filename = coach_user_requests_db_path_and_filename

    coach_user_info = pd.read_csv(filename, index_col=False)

    coach_user_info_new = coach_user_info.drop(
        coach_user_info.loc[coach_user_info['coach_id'] == int(coach_id)].loc[coach_user_info['user_id']
                                                                              == int(client_id)].index)

    try:
        with open(filename, "w+") as file:
            file.write("coach_id,user_id")
            for index, row in coach_user_info_new.iterrows():
                string_to_write = "\n{},{}".format(str(row[0]), str(row[1]))
                file.write(string_to_write)
    except Exception:
        time.sleep(1)
        remove_client_by_id(coach_id, client_id, request)


def request_new_client(coach_id, client_id):
    """
    Writes the coach and client into the coach_users_requests.csv file ->
    "Sents a request to a client that a coach wants to add this client"
    :param coach_id: The id of the coach
    :param client_id: The id of the client
    """

    try:
        with open(coach_user_requests_db_path_and_filename, "a+") as file:
            string_to_write = "\n{},{}".format(coach_id, client_id)
            file.write(string_to_write)
    except Exception:
        time.sleep(1)
        request_new_client(coach_id, client_id)
