"""
Create a User-Item-Rating file with random ratings
"""

import pandas as pd
from random import randint
import os

parent_dir = os.path.dirname(os.path.dirname(os.getcwd()))


def create_ratings(amount_of_users):
    """
    Create random ratings from 1-5 for a given amount of users for recipes in the database.
    User 1 gives 1 rating, user 2 gives 2, and so on.
    Write into /Data/ratings.csv
    :param amount_of_users:
    """

    recipe_database_path_and_filename = parent_dir + "/Data/recipe_database.csv"
    recipe_info = pd.read_csv(recipe_database_path_and_filename, index_col=False)

    ids = recipe_info["ID"]

    ratings_path_and_filename = parent_dir + "/Data/ratings.csv"
    with open(ratings_path_and_filename, "w+") as file:
        for users_number in range(1, amount_of_users+1):
            ratings_number = 0
            while ratings_number < users_number:
                str_to_write = str(users_number) + ", " + str(ids[randint(0, len(recipe_info)-1)]) + ", " + \
                               str(randint(1, 5)) + "\n"
                file.write(str_to_write)
                ratings_number += 1


def delete_double_ratings():
    """
    Checks the ratings.csv file and if a user rated a single recipe more than once, only keep the latest rating.
    Write the corrected ratings in the file.
    """

    ratings_path_and_filename = parent_dir + "/Data/ratings.csv"
    names = ["user", "item", "rating"]
    ratings = pd.read_csv(ratings_path_and_filename, index_col=False, names=names)
    ratings.drop_duplicates(subset=["user", "item"], keep="last", inplace=True)

    with open(ratings_path_and_filename, "w+") as file:
        for index, row in ratings.iterrows():
            str_to_write = str(row[0]) + ", " + str(row[1]) + ", " + str(row[2]) + "\n"
            file.write(str_to_write)


if __name__ == "__main__":
    create_ratings(1000)
    delete_double_ratings()
