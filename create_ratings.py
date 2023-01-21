import pandas as pd
from random import randint

recipe_info = pd.read_csv("recipe_database.csv")
ids = recipe_info["ID"]

with open("ratings.csv", "w+") as file:
    for i in range(1, 100):
        j = 0
        while j < i:
            str_to_write = str(i) + ", " + str(ids[randint(0, 48)]) + ", " + str(randint(1, 5)) + "\n"
            file.write(str_to_write)
            j += 1

