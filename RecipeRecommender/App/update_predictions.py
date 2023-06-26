"""
Functions to (set when to) update predicted ratings
"""

import pandas as pd
import os

parent_dir = os.path.dirname(os.getcwd())

new_ratings_counter_path_and_filename = parent_dir + "/NutritionRecSys/Data/Variables/new_ratings_counter.csv"
new_ratings_counter_df = pd.read_csv(new_ratings_counter_path_and_filename, index_col=False)
new_ratings_counter = new_ratings_counter_df["Value"][0]


def increment_new_ratings_counter():
    """
    Increment the global variable new_ratings_counter by 1, meaning there has been a new rating
    """

    global new_ratings_counter
    new_ratings_counter = new_ratings_counter + 1

    with open(new_ratings_counter_path_and_filename, "w+") as file:
        file.write("Value\n{}".format(new_ratings_counter))


def check_update_predicted_ratings():
    """
    Check if the predicted ratings shall be updated or not.
    If yes, set the new_ratings_counter back to 0
    :return: True if they shall be updated, False if not
    """

    global new_ratings_counter

    if new_ratings_counter >= 10:
        new_ratings_counter = 0
        with open(new_ratings_counter_path_and_filename, "w+") as file:
            file.write("Value\n{}".format(new_ratings_counter))
        return True

    return False
