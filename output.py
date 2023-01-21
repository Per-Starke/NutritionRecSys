import pandas as pd
import recommend


col_names = ["User", "Item", "Feedback"]

ratings = pd.read_csv("ratings.csv", names=col_names)

recommend.recommend_collaborative_itemknn()
recommend.recommend_collaborative_userknn()
recommend.recommend_content_based()

recommendations_collaborative_itemknn = pd.read_csv("recommendations_collaborative_itemknn.csv", names=col_names)
recommendations_collaborative_userknn = pd.read_csv("recommendations_collaborative_userknn.csv", names=col_names)
recommendations_content_based = pd.read_csv("recommendations_content_based.csv", names=col_names)

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

    print("Content-based recommendations:")
    for line in recommendations_content_based.iterrows():
        user = str(int(line[1][0]))
        recipe_id = int(line[1][1])
        rating = str(line[1][2])

        if user == str(user_id):
            print(
                "User {} gets a predicted rating of {} for {}".format(user, rating, get_recipe_title_by_id(recipe_id)))

    print("\nCollaborative recommendations (ItemKNN):")
    for line in recommendations_collaborative_itemknn.iterrows():
        user = str(int(line[1][0]))
        recipe_id = int(line[1][1])
        rating = str(line[1][2])

        if user == str(user_id):
            print(
                "User {} gets a predicted rating of {} for {}".format(user, rating, get_recipe_title_by_id(recipe_id)))

    print("\nCollaborative recommendations (UserKNN):")
    for line in recommendations_collaborative_userknn.iterrows():
        user = str(int(line[1][0]))
        recipe_id = int(line[1][1])
        rating = str(line[1][2])

        if user == str(user_id):
            print(
                "User {} gets a predicted rating of {} for {}".format(user, rating, get_recipe_title_by_id(recipe_id)))


user_to_print = 25

print_ratings_for_user(user_to_print)
print()
print_calculated_ratings_for_user(user_to_print)
