import pandas as pd
import os
from Recommend import recommend

parent_dir = os.path.dirname(os.getcwd())

col_names = ["User", "Item", "Feedback"]

ratings_path_and_filename = parent_dir + "/Data/ratings.csv"

ratings = pd.read_csv(ratings_path_and_filename, names=col_names)

recommend.recommend_collaborative_itemknn()
recommend.recommend_collaborative_userknn()
recommend.recommend_content_based()

recommend_collaborative_itemknn_path_and_filename = parent_dir + \
                                                    "/Predicted_ratings_data/recommendations_collaborative_itemknn.csv"
recommendations_collaborative_itemknn = pd.read_csv(recommend_collaborative_itemknn_path_and_filename, names=col_names)

recommend_collaborative_userknn_path_and_filename = parent_dir + \
                                                    "/Predicted_ratings_data/recommendations_collaborative_userknn.csv"
recommendations_collaborative_userknn = pd.read_csv(recommend_collaborative_userknn_path_and_filename, names=col_names)

recommend_contend_based_path_and_filename = parent_dir + \
                                                    "/Predicted_ratings_data/recommendations_content_based.csv"
recommendations_content_based = pd.read_csv(recommend_contend_based_path_and_filename, names=col_names)

recipe_database_path_and_filename = parent_dir + "/Data/recipe_database.csv"
recipe_info = pd.read_csv(recipe_database_path_and_filename)


def get_recipe_title_by_id(id_to_get):
    """
    Get the title of a recipe
    :param id_to_get: the ID of the recipe where we want to get the title from, as int
    :return: the title of the recipe, as str
    """
    return recipe_info[recipe_info["ID"] == id_to_get][" Title"].iloc[0][1:]


def print_ratings_for_user(user_id):
    """
    Print the ratings a user gave for all recipes
    :param user_id: the id of the user, as int
    """

    ratings.sort_values(by="Item", inplace=True)

    for line in ratings.iterrows():
        user = str(line[1][0])
        recipe_id = line[1][1]
        rating = str(line[1][2])

        if user == str(user_id):
            print("User {} rated {} with {} out of 5".format(user, get_recipe_title_by_id(recipe_id), rating))


def print_calculated_ratings_for_user(user_id, algo):
    """
    Print the calculated ratings a user gave for recipes the user did not rate.
    If less than 10 unrated recipes, print all. Else, print the 10 recipes with the highest predicted rating.
    :param user_id: the id of the user, as int
    :param algo: the algorithm the predictions were made with. Can be: Content-Based, UserKNN, ItemKNN
    """

    if algo == "Content-Based":
        recommendations = recommendations_content_based
        title = "Content-based recommendations:"
    elif algo == "UserKNN":
        recommendations = recommendations_collaborative_userknn
        title = "Collaborative recommendations (UserKNN):"
    elif algo == "ItemKNN":
        recommendations = recommendations_collaborative_itemknn
        title = "Collaborative recommendations (ItemKNN):"
    else:
        return

    print(title)
    for line in recommendations.iterrows():
        user = str(int(line[1][0]))
        recipe_id = int(line[1][1])
        rating = str(line[1][2])

        if user == str(user_id):
            print(
                "User {} gets a predicted rating of {} for {}".format(user, rating, get_recipe_title_by_id(recipe_id)))


if __name__ == "__main__":
    user_to_print = 5

    print_ratings_for_user(user_to_print)
    print()
    print_calculated_ratings_for_user(user_to_print, "Content-Based")
    print()
    print_calculated_ratings_for_user(user_to_print, "UserKNN")
    print()
    print_calculated_ratings_for_user(user_to_print, "ItemKNN")
