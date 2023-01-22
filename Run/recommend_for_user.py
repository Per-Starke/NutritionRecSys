"""
Get ratings for recipes from active user, write them in the ratings-database, then recommend top n recipes for this user
"""

import os
import pandas as pd
from output import print_output

current = 1
user_id = 0

parent_dir = os.path.dirname(os.getcwd())

ratings_path_and_filename = parent_dir + "/Data/ratings.csv"

recipe_database_path_and_filename = parent_dir + "/Data/recipe_database.csv"
recipe_info = pd.read_csv(recipe_database_path_and_filename)
all_ids = recipe_info["ID"]


def get_and_write_input():
    """
    Ask user for rating about a recipe at the current position in the database.
    @todo: Ask again if input is invalid.
    :return: True when rating was written to file, False if "Stop" was entered
    """

    recipe_string = "Recipe " + str(current) + ": " + \
                    recipe_info[recipe_info["ID"] == all_ids[len(all_ids) - current]][" Title"].iloc[0][1:]
    print(recipe_string)

    current_rating = input("How good does that sound to you, on a scale from 1 to 5? ")

    if current_rating == "stop":
        return False

    elif current_rating.isnumeric():
        with open(ratings_path_and_filename, "a") as file:
            rating_string = str(user_id) + ", " + str(all_ids[len(all_ids) - current]) + ", " + str(current_rating) + "\n"
            file.write(rating_string)

    return True


def get_user_ratings():
    """
    Ask for ratings of recipes until "stop" is entered, then write them into ratings.csv
    """

    global current

    ask_for_next_rating = get_and_write_input()

    while ask_for_next_rating:
        current += 1
        ask_for_next_rating = get_and_write_input()


if __name__ == "__main__":
    get_user_ratings()
    print_output(user_id=user_id)
