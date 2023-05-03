"""
Functions for the coach-view of the web-app
"""

import pandas as pd
import os

parent_dir = os.path.dirname(os.path.dirname(os.getcwd()))

coach_user_db_path_and_filename = parent_dir + "/Data/User_data/coach_users.csv"
coach_user_requests_db_path_and_filename = parent_dir + "/Data/User_data/coach_users_requests.csv"


def get_users(coach_id):
    """
    Get all users that a coach manages
    :param coach_id: The id of the coach
    :return: a list of user_ids
    """

    coach_user_info = pd.read_csv(coach_user_db_path_and_filename, index_col=False)

    return coach_user_info.loc[coach_user_info['coach_id'] == int(coach_id)]["user_id"].values.tolist()


def remove_client_by_id(coach_id, client_id):
    """
    Remove a given client of a given coach
    :param coach_id: The id of the coach
    :param client_id: the id of the client
    """

    coach_user_info = pd.read_csv(coach_user_db_path_and_filename, index_col=False)

    coach_user_info_new = coach_user_info.drop(
        coach_user_info.loc[coach_user_info['coach_id'] == int(coach_id)].loc[coach_user_info['user_id']
                                                                              == int(client_id)].index)

    with open(coach_user_db_path_and_filename, "w+") as file:
        file.write("coach_id,user_id")
        for index, row in coach_user_info_new.iterrows():
            str_to_write = "\n" + str(row[0]) + "," + str(row[1])
            file.write(str_to_write)


def request_new_client(coach_id, client_id):
    """
    Writes the coach and client into the coach_users_requests.csv file ->
    "Sents a request to a client that a coach wants to add this client"
    :param coach_id: The id of the coach
    :param client_id: The id of the client
    """

    with open(coach_user_requests_db_path_and_filename, "a+") as file:
        str_to_write = "\n" + str(coach_id) + "," + str(client_id)
        file.write(str_to_write)


