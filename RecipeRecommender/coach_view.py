"""
Functions for the coach-view of the web-app
"""

import pandas as pd
import os

parent_dir = os.path.dirname(os.path.dirname(os.getcwd()))

coach_user_db_path_and_filename = parent_dir + "/User_data/coach_users.csv"
coach_user_info = pd.read_csv(coach_user_db_path_and_filename, index_col=False)


def get_users(coach_id):
    """
    Get all users that a coach manages
    :param coach_id: The id of the coach
    :return: a list of user_ids
    """

    return coach_user_info.loc[coach_user_info['coach_id'] == int(coach_id)][" user_id"].values.tolist()
