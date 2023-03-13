"""
Check the ratings file
"""

import os

import pandas as pd

parent_dir = os.path.dirname(os.getcwd())


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
    delete_double_ratings()
