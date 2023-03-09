"""
Get ratings for recipes from active user, write them in the ratings-database, then recommend top n recipes for this user
"""

import os
import pandas as pd
import output

current = 1
user_id = 0

parent_dir = os.path.dirname(os.getcwd())

ratings_path_and_filename = parent_dir + "/Data/ratings.csv"

recipe_database_path_and_filename = parent_dir + "/Data/recipe_database.csv"
recipe_info = pd.read_csv(recipe_database_path_and_filename, index_col=False)
all_ids = recipe_info["ID"]

# Shuffle, so not always the same recipes are asked to be rated
all_ids = all_ids.sample(frac=1).reset_index(drop=True)


def check_input(input_to_check):
    """
    Check if input is rating from 1-5, or "stop"
    :param input_to_check: The input to check, as str
    :return: True if input is valid, False otherwise
    """
    if input_to_check in ["1", "2", "3", "4", "5", "stop"]:
        return True

    return False


def get_and_write_input():
    """
    Ask user for rating about a recipe at the current position in the database.
    Ask again if input is invalid.
    :return: True when rating was written to file, False if "Stop" was entered
    """

    recipe_string = "Recipe " + str(current) + ": " + \
                    recipe_info[recipe_info["ID"] == all_ids[current]][" Title"].iloc[0][1:]
    print(recipe_string)

    current_rating = input("How good does that sound to you, on a scale from 1 to 5? ")

    while not check_input(current_rating):
        current_rating = input("Enter a full number between 1 and 5 or 'stop'! Enter again: ")

    if current_rating == "stop":
        return False

    with open(ratings_path_and_filename, "a") as file:
        rating_string = str(user_id) + ", " + str(all_ids[current]) + ", " + str(current_rating) + \
                        "\n"
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
    output.print_output(user_id=user_id, ratings_to_print=3)
