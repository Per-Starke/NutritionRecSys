"""
Output the given and predicted ratings for users
"""

import pandas as pd
import os
from Recommend import recommend


class Color:
    DARKCYAN = '\033[36m'
    YELLOW = '\033[93m'
    PURPLE = '\033[95m'
    BOLD = '\033[1m'
    END = '\033[0m'


parent_dir = os.path.dirname(os.getcwd())
col_names = ["User", "Item", "Feedback"]

recipe_database_path_and_filename = parent_dir + "/Data/recipe_database.csv"
recipe_info = pd.read_csv(recipe_database_path_and_filename)


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
            print("User {} rated {}{}{} with {} out of 5".format(user, Color.YELLOW, get_recipe_title_by_id(recipe_id),
                                                                 Color.END, rating))


def print_single_algo_ratings(recommendations, user_id, title, ratings_to_print=10):
    """
    Prints the predicted ratings of a single algorithm
    :param recommendations: the dataframe of predicted ratings
    :param user_id: the id of the user the ratings shall be printed for
    :param title: The title to print before printing recommendations
    :param ratings_to_print: The number of ratings to print, default 10
    """

    printed_counter = 0

    print(title)

    for line in recommendations.iterrows():
        user = str(int(line[1][0]))
        recipe_id = int(line[1][1])
        rating = str(line[1][2])

        if user == str(user_id):
            printed_counter += 1
            print("{}Recommendation {}: {}{}   |   predicted rating: {}".format(
                Color.PURPLE, printed_counter, get_recipe_title_by_id(recipe_id), Color.END, rating))

        if printed_counter >= ratings_to_print:
            break

    print()


def print_calculated_ratings_for_user(user_id, recommendations_list, cb=True, itemknn=True, userknn=True,
                                      ratings_to_print=10):
    """
    Print the calculated ratings a user gave for recipes the user did not rate.
    If less than 10 unrated recipes, print all. Else, print the 10 recipes with the highest predicted rating.
    :param user_id: the id of the user, as int
    :param recommendations_list: List of dataframes with the predicted ratings, ordererd: cb, itemknn, userknn
    :param cb: True (default) if Content-Based recommendations shall be printed
    :param itemknn: True (default) if Collaborative ItemKNN recommendations shall be printed
    :param userknn: True (default) if Collaborative UserKNN recommendations shall be printed
    :param ratings_to_print: The number of ratings to print, default 10
    """

    if cb:
        recommendations = recommendations_list[0]
        title = Color.BOLD + Color.DARKCYAN + "Here are your top " + str(
            ratings_to_print) + " recommendations, using a " \
                                "content-based " \
                                "recommendation algorithm:" \
                                + Color.END
        print_single_algo_ratings(recommendations, user_id, title, ratings_to_print)
    if itemknn:
        recommendations = recommendations_list[1]
        title = Color.BOLD + Color.DARKCYAN + "Here are your top " + str(
            ratings_to_print) + " recommendations, using the " \
                                "collaborative filtering " \
                                "ItemKNN recommendation " \
                                "algorithm:" + Color.END
        print_single_algo_ratings(recommendations, user_id, title, ratings_to_print)
    if userknn:
        recommendations = recommendations_list[2]
        title = Color.BOLD + Color.DARKCYAN + "Here are your top " + str(
            ratings_to_print) + " recommendations, using the " \
                                "collaborative filtering " \
                                "UserKNN recommendation " \
                                "algorithm:" + Color.END
        print_single_algo_ratings(recommendations, user_id, title, ratings_to_print)


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

    print_ratings_for_user(user_id)
    print()
    print_calculated_ratings_for_user(user_id, write_recommendations(), cb, itemknn, userknn, ratings_to_print)


if __name__ == "__main__":
    print_output(user_id=5, run_rec_algos=False)
