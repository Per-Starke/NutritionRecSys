import pandas as pd
from random import randint
import os

parent_dir = os.path.dirname(os.getcwd())

recipe_database_path_and_filename = parent_dir + "/Data/recipe_database.csv"

recipe_info = pd.read_csv(recipe_database_path_and_filename)
ids = recipe_info["ID"]

ratings_path_and_filename = parent_dir + "/Data/ratings.csv"

with open(ratings_path_and_filename, "w+") as file:
    for i in range(1, 100):
        j = 0
        while j < i:
            str_to_write = str(i) + ", " + str(ids[randint(0, len(recipe_info)-1)]) + ", " + str(randint(1, 5)) + "\n"
            file.write(str_to_write)
            j += 1

