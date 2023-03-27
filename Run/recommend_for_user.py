"""
Functions for getting ratings for recipes
"""

import os
import pandas as pd
import Run.output


current = 1
user_id = 0

parent_dir = os.path.dirname(os.getcwd())
ratings_path_and_filename = parent_dir + "/Data/ratings.csv"
recipe_database_path_and_filename = parent_dir + "/Data/recipe_database.csv"

recipe_info = pd.read_csv(recipe_database_path_and_filename, index_col=False)


def check_input(input_to_check):
    """
    Check if input is rating from 1-5
    :param input_to_check: The input to check, as str
    :return: True if input is valid, False otherwise
    """
    if input_to_check in ["1", "2", "3", "4", "5"]:
        return True

    return False


def write_rating_to_file(user_id, recipe_id, rating):
    """
    Writes the given rating into the ratings.csv file
    :param user_id: the id of the user who rated the recipe
    :param recipe_id: the id of the recipe that got rated
    :param rating: the rating
    """

    with open(ratings_path_and_filename, "a+") as file:
        str_to_write = str(user_id) + ", " + str(recipe_id) + ", " + str(rating) + "\n"
        file.write(str_to_write)



def get_recipe_to_rate(user_id):
    """
    Get a random recipe the user has not rated yet
    :param user_id: The id of the user
    :return: The id of a recipe the user has not rated yet
    """

    all_ids = recipe_info["ID"].sample(frac=1).reset_index(drop=True)

    rated_recipes = Run.output.get_ratings_for_user(user_id).keys()

    for recipe_id in all_ids:
        if recipe_id not in rated_recipes:
            return recipe_id

    return None



