"""
Includes functions to get recommendations matching the required macronutrients
"""

import os
import pandas as pd

import Run.output

parent_dir = os.path.dirname(os.getcwd())

ratings_path_and_filename = parent_dir + "/Data/ratings.csv"
col_names = ["User", "Item", "Feedback"]


def get_macros(recipe_ids):
    """
    Get the macronutrients of all recipes in the given list
    :param recipe_ids: A list of recipe ids to get the macros for
    :return: A dict, with pairs of recipe_id:dict_of_macros
    """

    return_dict = {}

    for recipe_id in recipe_ids:
        return_dict[recipe_id] = Run.output.get_macros_by_id(recipe_id)

    return return_dict


def get_recs_and_macros(user_id, algorithm):
    """
    For a give user, get all recommendations of the given algorithm and their respective macronutrients
    :param user_id: The ID of the user, as int
    :param algorithm: the name of the algorithm, as string, either contentbased, itemknn or userknn
    :return: A dict, with pairs of recipe_id:dict_of_macros
    """

    if algorithm == "contentbased":
        filename = "recommendations_content_based.csv"
    elif algorithm == "itemknn":
        filename = "recommendations_collaborative_itemknn.csv"
    elif algorithm == "userknn":
        filename = "recommendations_collaborative_userknn.csv"
    else:
        raise ValueError("This is not a valid algorithm name, must be contentbased, itemknn or userknn")

    path_and_filename = parent_dir + "/Predicted_ratings_data/" + filename

    recommendations = pd.read_csv(path_and_filename, names=col_names)
    recommendations = recommendations[recommendations["User"] == user_id]

    list_of_recommended_recipe_ids = []

    for recommendation in recommendations.itertuples():
        list_of_recommended_recipe_ids.append(recommendation[2])

    return get_macros(list_of_recommended_recipe_ids)


def find_top_3_recs_within_range_of_macros(user_id, algorithm, proteins, carbs, fats, allowed_range=0.2):
    """
    Find the top 3 recommendations withing a given range of the given macronutrients, for a given user and algorithm
    :param user_id: The ID of the user, as int
    :param algorithm: The algorithm, either contentbased, itemknn or userknn
    :param proteins: the required amount of proteins, in grams
    :param carbs: the required amount of carbs, in grams
    :param fats: the required amount of fats, in grams
    :param allowed_range: The range of how much the real macros are allowed to differ from the required macros,
    default 0.2
    :return: The top 3 (or less, if less found) recommendations matchingthe given macros, as a list of recipe ids
    """

    min_protein = float(proteins) - float(proteins) * allowed_range
    max_protein = float(proteins) + float(proteins) * allowed_range

    min_carbs = float(carbs) - float(carbs) * allowed_range
    max_carbs = float(carbs) + float(carbs) * allowed_range

    min_fats = float(fats) - float(fats) * allowed_range
    max_fats = float(fats) + float(fats) * allowed_range

    recs_and_macros = get_recs_and_macros(int(user_id), algorithm)

    return_list = []

    for recipe_id, macro_dict in recs_and_macros.items():
        recipe_proteins = macro_dict["proteins"][:-1]
        recipe_carbs = macro_dict["carbs"][:-1]
        recipe_fats = macro_dict["fats"][:-1]

        if (min_protein <= float(recipe_proteins) <= max_protein and min_carbs <= float(recipe_carbs) <= max_carbs and
                min_fats <= float(recipe_fats) <= max_fats):
            return_list.append(recipe_id)
            if len(return_list) == 3:
                return return_list

    return return_list
