"""
Functions for outputting the recommendations and ratings
"""

import pandas as pd
import os
from Recommend import recommend


parent_dir = os.path.dirname(os.getcwd())
col_names = ["User", "Item", "Feedback"]

recipe_database_path_and_filename = parent_dir + "/Data/recipe_database.csv"
recipe_info = pd.read_csv(recipe_database_path_and_filename, index_col=False)


def run_recommendation_algos(rank_length=3):
    """
    Run the rating prediction algorithms
    :param rank_length: The number of predictions to calculate, default 3
    """

    recommend.recommend_content_based(rank_length=rank_length)
    recommend.recommend_collaborative_itemknn(rank_length=rank_length)
    # recommend.recommend_collaborative_userknn(rank_length=rank_length)


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

    # For User-KNN, out-commented because only Content-based and Item-KNN are used.
    # Remove triple quotation marks and add to returned list, if this shall be used!
    """
    recommend_collaborative_userknn_path_and_filename = \
        parent_dir + "/Predicted_ratings_data/recommendations_collaborative_userknn.csv"
    recommendations_collaborative_userknn = pd.read_csv(recommend_collaborative_userknn_path_and_filename,
                                                        names=col_names)
    """

    return [recommendations_content_based, recommendations_collaborative_itemknn]


def get_recipe_title_by_id(id_to_get):
    """
    Get the title of a recipe
    :param id_to_get: the ID of the recipe where we want to get the title from, as int
    :return: the title of the recipe, as str
    """

    return recipe_info[recipe_info["ID"] == id_to_get][" Title"].iloc[0][1:]


def get_macros_by_id(id_to_get):
    """
    Get the macronutrients of a recipe
    :param id_to_get: The ID of the reicpe where we want to get the macros from, as int
    :return: The macros, as dict
    """

    proteins = recipe_info[recipe_info["ID"] == id_to_get][" Proteins"].iloc[0][1:]
    carbs = recipe_info[recipe_info["ID"] == id_to_get][" Carbs"].iloc[0][1:]
    fats = recipe_info[recipe_info["ID"] == id_to_get][" Fats"].iloc[0][1:]

    return {"proteins": proteins, "carbs": carbs, "fats": fats}


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

    return_dict = {}

    if cb:
        recommendations = recommendations_list[0]
        return_dict["content-based"] = get_single_algo_ratings(recommendations, user_id, ratings_to_get)

    if itemknn:
        recommendations = recommendations_list[1]
        return_dict["item-knn"] = get_single_algo_ratings(recommendations, user_id, ratings_to_get)

    if userknn:
        recommendations = recommendations_list[2]
        return_dict["user-knn"] = get_single_algo_ratings(recommendations, user_id, ratings_to_get)

    return return_dict
