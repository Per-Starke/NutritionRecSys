"""
Output the given and predicted ratings for users
"""

import pandas as pd
import os
from Recommend import recommend

parent_dir = os.path.dirname(os.getcwd())
col_names = ["User", "Item", "Feedback"]


def run_recommendation_algos():
    """
    Run the rating prediction algorithms
    """

    recommend.recommend_collaborative_itemknn()
    recommend.recommend_collaborative_userknn()
    recommend.recommend_content_based()


def write_recommendations():
    """
    Write the results of the recommendation algorithms in a list of dataframes
    :return: A list of three dataframes, with the predicted ratings of Content-based, ItemKNN and UserKNN
    """

    recommend_contend_based_path_and_filename = \
        parent_dir + "/Predicted_ratings_data/recommendations_content_based.csv"
    recommendations_content_based = pd.read_csv(recommend_contend_based_path_and_filename, names=col_names)

    recommend_collaborative_itemknn_path_and_filename = \
        parent_dir + "/Predicted_ratings_data/recommendations_collaborative_itemknn.csv"
    recommendations_collaborative_itemknn = pd.read_csv(recommend_collaborative_itemknn_path_and_filename,
                                                        names=col_names)

    recommend_collaborative_userknn_path_and_filename = \
        parent_dir + "/Predicted_ratings_data/recommendations_collaborative_userknn.csv"
    recommendations_collaborative_userknn = pd.read_csv(recommend_collaborative_userknn_path_and_filename,
                                                        names=col_names)

    return [recommendations_content_based, recommendations_collaborative_itemknn, recommendations_collaborative_userknn]


def get_recipe_title_by_id(id_to_get):
    """
    Get the title of a recipe
    :param id_to_get: the ID of the recipe where we want to get the title from, as int
    :return: the title of the recipe, as str
    """

    recipe_database_path_and_filename = parent_dir + "/Data/recipe_database.csv"
    recipe_info = pd.read_csv(recipe_database_path_and_filename)

    return recipe_info[recipe_info["ID"] == id_to_get][" Title"].iloc[0][1:]


def print_ratings_for_user(user_id):
    """
    Print the ratings a user gave for all recipes
    :param user_id: the id of the user, as int
    """

    ratings_path_and_filename = parent_dir + "/Data/ratings.csv"
    ratings = pd.read_csv(ratings_path_and_filename, names=col_names)

    ratings.sort_values(by="Item", inplace=True)

    for line in ratings.iterrows():
        user = str(line[1][0])
        recipe_id = line[1][1]
        rating = str(line[1][2])

        if user == str(user_id):
            print("User {} rated {} with {} out of 5".format(user, get_recipe_title_by_id(recipe_id), rating))


def print_single_algo_ratings(recommendations, user_id, title):
    """
    Prints the predicted ratings of a single algorithm
    :param recommendations: the dataframe of predicted ratings
    :param user_id: the id of the user the ratings shall be printed for
    :param title: The title to print before printing recommendations
    """

    print(title)

    for line in recommendations.iterrows():
        user = str(int(line[1][0]))
        recipe_id = int(line[1][1])
        rating = str(line[1][2])

        if user == str(user_id):
            print(
                "User {} gets a predicted rating of {} for {}".format(user, rating, get_recipe_title_by_id(recipe_id)))

    print()


def print_calculated_ratings_for_user(user_id, recommendations_list, cb=True, itemknn=True, userknn=True):
    """
    Print the calculated ratings a user gave for recipes the user did not rate.
    If less than 10 unrated recipes, print all. Else, print the 10 recipes with the highest predicted rating.
    :param user_id: the id of the user, as int
    :param recommendations_list: List of dataframes with the predicted ratings, ordererd: cb, itemknn, userknn
    :param cb: True (default) if Content-Based recommendations shall be printed
    :param itemknn: True (default) if Collaborative ItemKNN recommendations shall be printed
    :param userknn: True (default) if Collaborative UserKNN recommendations shall be printed
    """

    if cb:
        recommendations = recommendations_list[0]
        title = "Content-based recommendations:"
        print_single_algo_ratings(recommendations, user_id, title)
    if itemknn:
        recommendations = recommendations_list[1]
        title = "Collaborative recommendations (ItemKNN):"
        print_single_algo_ratings(recommendations, user_id, title)
    if userknn:
        recommendations = recommendations_list[2]
        title = "Collaborative recommendations (UserKNN):"
        print_single_algo_ratings(recommendations, user_id, title)


def print_output(user_id, run_rec_algos=True, cb=True, itemknn=True, userknn=True):
    """
    Print giv
    :param user_id: the id of the user to print the output for
    :param run_rec_algos: If True (default), run the recommendation algorithms,
    :param cb: True (default) if Content-Based recommendations shall be printed
    :param itemknn: True (default) if Collaborative ItemKNN recommendations shall be printed
    :param userknn: True (default) if Collaborative UserKNN recommendations shall be printed
    otherwise use existing predicted-rating files
    """

    if run_rec_algos:
        run_recommendation_algos()

    print_ratings_for_user(user_id)
    print()
    print_calculated_ratings_for_user(user_id, write_recommendations(), cb, itemknn, userknn)


if __name__ == "__main__":
    print_output(user_id=5, run_rec_algos=False)
