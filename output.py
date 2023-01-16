import pandas as pd

ratings = pd.read_csv("ratings.csv")

recommendations = pd.read_csv("recommendations.csv")

recipe_info = pd.read_csv("recipe_database.csv")


def get_recipe_title_by_id(id_to_get):
    """
    Get the title of a recipe
    :param id_to_get: the ID of the recipe where we want to get the title from, as int
    :return: the title of the recipe, as str
    """
    return recipe_info[recipe_info["ID"] == id_to_get][" Title"].iloc[0][1:]


def print_ratings_for_user(user_id):
    """
    print the ratings a user gave for all recipes
    :param user_id: the id of the user, as int
    """

    for line in ratings.iterrows():
        user = str(line[1][0])
        recipe_id = line[1][1]
        rating = str(line[1][2])

        if user == str(user_id):
            print("User {} rated {} with {} out of 5".format(user, get_recipe_title_by_id(recipe_id), rating))


def print_calculated_ratings_for_user(user_id):
    """
    print the calculated ratings a user gave for all recipes the user did not rate
    :param user_id: the id of the user, as int
    """

    for line in recommendations.iterrows():
        user = str(int(line[1][0]))
        recipe_id = int(line[1][1])
        rating = str(line[1][2])

        if user == str(user_id):
            print(
                "User {} gets a predicted rating of {} for {}".format(user, rating, get_recipe_title_by_id(recipe_id)))


user_to_print = 3

print_ratings_for_user(user_to_print)
print()
print_calculated_ratings_for_user(user_to_print)
