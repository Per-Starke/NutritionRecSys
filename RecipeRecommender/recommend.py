"""
Functions to run the CaseRec algorithms to predict ratings
"""

from caserec.recommenders.item_recommendation.itemknn import ItemKNN
from caserec.recommenders.item_recommendation.content_based import ContentBased
import os
import pandas as pd

import RecipeRecommender.output

parent_dir = os.path.dirname(os.getcwd())

ratings_path_and_filename = parent_dir + "/Data/ratings.csv"
col_names = ["User", "Item", "Feedback"]

parent_dir = os.path.dirname(os.getcwd())

ratings_path_and_filename = parent_dir + "/Data/ratings.csv"


def recommend_collaborative_itemknn(rank_length=3):
    """
    create or update the recommendations.csv file
    :param rank_length: The number of predictions to calculate, default 3
    """

    output_path_and_filename = parent_dir + "/Predicted_ratings_data/recommendations_collaborative_itemknn.csv"
    ItemKNN(train_file=ratings_path_and_filename, output_file=output_path_and_filename, sep=", ",
            rank_length=rank_length).compute()


def recommend_content_based(rank_length=3):
    """
    create or update the recommendations.csv file
    :param rank_length: The number of predictions to calculate, default 3
    """

    output_path_and_filename = parent_dir + "/Predicted_ratings_data/recommendations_content_based.csv"
    similarities_path_and_filename = parent_dir + "/Data/similarities.csv"
    ContentBased(train_file=ratings_path_and_filename, output_file=output_path_and_filename,
                 similarity_file=similarities_path_and_filename, sep=", ", similarity_sep=", ",
                 rank_length=rank_length).compute()


def run_recommendation_algos(rank_length=3):
    """
    Run the rating prediction algorithms
    :param rank_length: The number of predictions to calculate, default 3
    """

    recommend_content_based(rank_length=rank_length)
    recommend_collaborative_itemknn(rank_length=rank_length)


"""
Functions to get recommendations matching the required macronutrients
"""


def get_macros(recipe_ids):
    """
    Get the macronutrients of all recipes in the given list
    :param recipe_ids: A list of recipe ids to get the macros for
    :return: A dict, with pairs of recipe_id:dict_of_macros
    """

    return_dict = {}

    for recipe_id in recipe_ids:
        return_dict[recipe_id] = RecipeRecommender.output.get_macros_by_id(recipe_id)

    return return_dict


def get_recs_and_macros(user_id, algorithm):
    """
    For a give user, get all recommendations of the given algorithm and their respective macronutrients
    :param user_id: The ID of the user, as int
    :param algorithm: the name of the algorithm, as string, either contentbased or itemknn
    :return: A dict, with pairs of recipe_id:dict_of_macros
    """

    if algorithm == "contentbased":
        filename = "recommendations_content_based.csv"
    elif algorithm == "itemknn":
        filename = "recommendations_collaborative_itemknn.csv"
    else:
        raise ValueError("This is not a valid algorithm name, must be contentbased or itemknn")

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
    :param algorithm: The algorithm, either contentbased or itemknn
    :param proteins: the required amount of proteins, in grams
    :param carbs: the required amount of carbs, in grams
    :param fats: the required amount of fats, in grams
    :param allowed_range: The range of how much the real macros are allowed to differ from the required macros,
    default 0.2
    :return: The top 3 (or less, if less found) recommendations matchingthe given macros, as a list of recipe ids
    """

    min_protein = float(proteins) - float(proteins) * float(allowed_range)
    max_protein = float(proteins) + float(proteins) * float(allowed_range)
    protein_open = False
    if min_protein == 0 and max_protein == 0:
        protein_open = True

    min_carbs = float(carbs) - float(carbs) * float(allowed_range)
    max_carbs = float(carbs) + float(carbs) * float(allowed_range)
    carbs_open = False
    if min_carbs == 0 and max_carbs == 0:
        carbs_open = True

    min_fats = float(fats) - float(fats) * float(allowed_range)
    max_fats = float(fats) + float(fats) * float(allowed_range)
    fats_open = False
    if min_fats == 0 and max_fats == 0:
        fats_open = True

    recs_and_macros = get_recs_and_macros(int(user_id), algorithm)

    return_list = []

    for recipe_id, macro_dict in recs_and_macros.items():
        recipe_proteins = macro_dict["proteins"][:-1]
        recipe_carbs = macro_dict["carbs"][:-1]
        recipe_fats = macro_dict["fats"][:-1]

        # Case 1: All macros given
        if protein_open == False and carbs_open == False and fats_open == False:
            if (min_protein <= float(recipe_proteins) <= max_protein and min_carbs <= float(recipe_carbs)
                    <= max_carbs and min_fats <= float(recipe_fats) <= max_fats):
                return_list.append(recipe_id)
                if len(return_list) == 3:
                    return return_list

        # Case 2: Proteins open, rest given
        elif protein_open == True and carbs_open == False and fats_open == False:
            if min_carbs <= float(recipe_carbs) <= max_carbs and min_fats <= float(recipe_fats) <= max_fats:
                return_list.append(recipe_id)
                if len(return_list) == 3:
                    return return_list

        # Case 3: Carbs open, rest given
        elif protein_open == False and carbs_open == True and fats_open == False:
            if min_protein <= float(recipe_proteins) <= max_protein and min_fats <= float(recipe_fats) <= max_fats:
                return_list.append(recipe_id)
                if len(return_list) == 3:
                    return return_list

        # Case 4: Fats open, rest given
        elif protein_open == False and carbs_open == False and fats_open == True:
            if min_protein <= float(recipe_proteins) <= max_protein and min_carbs <= float(recipe_carbs) <= max_carbs:
                return_list.append(recipe_id)
                if len(return_list) == 3:
                    return return_list

        # Case 5: Proteins and carbs open, fats given
        elif protein_open == True and carbs_open == True and fats_open == False:
            if min_fats <= float(recipe_fats) <= max_fats:
                return_list.append(recipe_id)
                if len(return_list) == 3:
                    return return_list

        # Case 6: Carbs and fats open, proteins given
        elif protein_open == False and carbs_open == True and fats_open == True:
            if min_protein <= float(recipe_proteins) <= max_protein:
                return_list.append(recipe_id)
                if len(return_list) == 3:
                    return return_list

        # Case 7: Proteins and fats open, carbs given
        elif protein_open == True and carbs_open == False and fats_open == True:
            if min_carbs <= float(recipe_carbs) <= max_carbs:
                return_list.append(recipe_id)
                if len(return_list) == 3:
                    return return_list

        # Case 8: Nothing given (same as just getting recommendations)
        elif protein_open == True and carbs_open == True and fats_open == True:
            return_list.append(recipe_id)
            if len(return_list) == 3:
                return return_list

    return return_list
