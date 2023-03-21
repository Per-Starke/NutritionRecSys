"""
Output the given and predicted ratings for users
"""

import pandas as pd
import os
from Recommend import recommend


parent_dir = os.path.dirname(os.getcwd())
col_names = ["User", "Item", "Feedback"]

recipe_database_path_and_filename = parent_dir + "/Data/recipe_database.csv"
recipe_info = pd.read_csv(recipe_database_path_and_filename, index_col=False)


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

    return recipe_info[recipe_info["ID"] == id_to_get][" Title"].iloc[0][1:]


def get_ratings_for_user(user_id):
    """
    Get the ratings a user gave for all recipes
    :param user_id: the id of the user, as int
    :return: A dict of id:rating pairs, of all ratings a user gave
    """

    ratings_path_and_filename = parent_dir + "/Data/ratings.csv"
    ratings = pd.read_csv(ratings_path_and_filename, names=col_names)

    ratings.sort_values(by="Item", inplace=True)

    return_dict = {}

    for line in ratings.iterrows():
        user = str(line[1][0])
        recipe_id = line[1][1]
        rating = str(line[1][2])

        if user == str(user_id):
            return_dict[recipe_id] = rating

    return return_dict


def get_single_algo_ratings(recommendations, user_id, ratings_to_get=10):
    """
    Get the predicted ratings of a single algorithm
    :param recommendations: the dataframe of predicted ratings
    :param user_id: the id of the user the ratings shall be returned for
    :param ratings_to_get: The number of ratings to print, default 10
    :return: A dict of the top-n recipes with the highest predicted ratings (with id:rating pairs) for a given user
    """

    ratings_counter = 0

    return_dict = {}

    for line in recommendations.iterrows():
        user = str(int(line[1][0]))
        recipe_id = int(line[1][1])
        rating = str(line[1][2])

        if user == str(user_id):
            ratings_counter += 1
            return_dict[recipe_id] = rating

        if ratings_counter >= ratings_to_get:
            break

    return return_dict


def get_calculated_ratings_for_user(user_id, recommendations_list, cb=True, itemknn=True, userknn=True,
                                    ratings_to_get=10):
    """
    Get the calculated ratings a user gave for recipes the user did not rate.
    If less than 10 unrated recipes, get all. Else, get the 10 (or given amount) recipes with the highest
    predicted rating.
    :param user_id: the id of the user, as int
    :param recommendations_list: List of dataframes with the predicted ratings, ordererd: cb, itemknn, userknn
    :param cb: True (default) if Content-Based recommendations shall be printed
    :param itemknn: True (default) if Collaborative ItemKNN recommendations shall be printed
    :param userknn: True (default) if Collaborative UserKNN recommendations shall be printed
    :param ratings_to_get: The number of ratings to get, default 10
    :return: a list of dicts of id:rating pairs with the calculated top-n ratings for the given user.
    """

    return_dict = {"content-based": [], "item-knn": [], "user-knn": []}

    if cb:
        recommendations = recommendations_list[0]
        return_dict["content-based"] = get_single_algo_ratings(recommendations, user_id, ratings_to_get)

    if itemknn:
        recommendations = recommendations_list[1]
        return_dict["item-knn"] = get_single_algo_ratings(recommendations, user_id, ratings_to_get)

    if userknn:
        recommendations = recommendations_list[0]
        return_dict["user-knn"] = get_single_algo_ratings(recommendations, user_id, ratings_to_get)

    return return_dict


def print_output(user_id, run_rec_algos=True, cb=True, itemknn=True, userknn=True, ratings_to_print=10):
    """
    Print given and predicted ratings (from given algorithms) for a single user
    :param user_id: the id of the user to print the output for
    :param run_rec_algos: If True (default), run the recommendation algorithms
    :param cb: True (default) if Content-Based recommendations shall be printed
    :param itemknn: True (default) if Collaborative ItemKNN recommendations shall be printed
    :param userknn: True (default) if Collaborative UserKNN recommendations shall be printed
    otherwise use existing predicted-rating files
    :param ratings_to_print: The number of ratings to print, default 10
    """

    if run_rec_algos:
        run_recommendation_algos()

    print(get_ratings_for_user(user_id))
    print()
    print(get_calculated_ratings_for_user(user_id, write_recommendations(), cb, itemknn, userknn, ratings_to_print))


if __name__ == "__main__":
    print_output(5)
