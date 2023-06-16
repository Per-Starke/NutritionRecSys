"""
Provide functions regarding ratings
"""
import time

import pandas as pd
from random import randint
import os

parent_dir = os.path.dirname(os.getcwd())

current_recipe_position = 0  # global variable, over all sessions

recipe_database_path_and_filename = parent_dir + "/NutritionRecSys/Data/recipe_database.csv"
recipe_info = pd.read_csv(recipe_database_path_and_filename, index_col=False)
all_recipe_ids = recipe_info["ID"].tolist()


def create_ratings(amount_of_users):
    """
    Create random ratings from 1-5 for a given amount of users for recipes in the database.
    User 1 gives 1 rating, user 2 gives 2, and so on.
    Write into /Data/ratings.csv.
    *** This was used for test purposes, and not in real production ***
    :param amount_of_users: the amount of users, as int
    """

    ids = recipe_info["ID"]

    ratings_path_and_filename = parent_dir + "/NutritionRecSys/Data/ratings.csv"
    with open(ratings_path_and_filename, "w+") as file:
        for users_number in range(1, amount_of_users+1):
            ratings_number = 0
            while ratings_number < users_number:
                string_to_write = "{},{},{}\n".format(str(users_number), str(ids[randint(0, len(recipe_info)-1)]),
                                                      str(randint(1, 5)))
                file.write(string_to_write)
                ratings_number += 1


def delete_double_ratings():
    """
    Checks the ratings.csv file and if a user rated a single recipe more than once, only keep the latest rating.
    Write the corrected ratings in the file, if differences exist.
    """

    ratings_path_and_filename = parent_dir + "/NutritionRecSys/Data/ratings.csv"
    names = ["user", "item", "rating"]
    ratings = pd.read_csv(ratings_path_and_filename, index_col=False, names=names)

    ratings_without_duplicates = ratings.drop_duplicates(subset=["user", "item"], keep="last")

    if not ratings.equals(ratings_without_duplicates):
        try:
            with open(ratings_path_and_filename, "w+") as file:
                for index, row in ratings_without_duplicates.iterrows():
                    string_to_write = "{},{},{}\n".format(str(row[0]), str(row[1]), str(row[2]))
                    file.write(string_to_write)
        except Exception:
            time.sleep(1)
            delete_double_ratings()


##########
# Get initial ratings
##########

def get_next_recipe_to_rate():
    """
    Get the next recipe to rate, so that one by one all recipes can be rated,
    going through the ordered database one by one
    :return: The id of the next recipe
    """

    global current_recipe_position

    next_recipe_id = all_recipe_ids[current_recipe_position]

    return next_recipe_id


def increment_current_recipe_position():
    """
    Increment the global variable current_recipe_position by 1, or set back to 0 if we are at the end of the recipe-list
    """

    global current_recipe_position

    if current_recipe_position == 1017:  # Recipe database consists of 1018 recipes, list indexing starts at 0 -> 1017
        current_recipe_position = 0
    else:
        current_recipe_position = current_recipe_position + 1


if __name__ == "__main__":
    # create_ratings(1000)
    # delete_double_ratings()
    pass
