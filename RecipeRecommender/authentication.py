"""
Functions to ensure security, check login data etc
"""

import pandas as pd
import os

from RecipeRecommender.coach_view import get_users

parent_dir = os.path.dirname(os.path.dirname(os.getcwd()))

users_path_and_filename = parent_dir + "/Data/User_data/users.csv"
coaches_path_and_filename = parent_dir + "/Data/User_data/coaches.csv"

users_and_pws = pd.read_csv(users_path_and_filename, index_col=False)
coaches_and_pws = pd.read_csv(coaches_path_and_filename, index_col=False)


def check_user_login(user_id, password):
    """
    Check if the entered user_id exists and if the password is correct
    :param user_id: the user-id
    :param password: the password
    :return: 1 if user-id is invalid, 2 if password is wrong, 3 if user-id exists and password is correct
    """

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
        print("inside")
        return True

    return False
