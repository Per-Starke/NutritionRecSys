"""
Create a similarity file for all recipes in the database.
The calculation of similarity takes into account: Ingredients, preparation and taste
"""

import pandas as pd
import numpy as np
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

parent_dir = os.path.dirname(os.getcwd())


def calc_text_sim(text1, text2):
    """
    Calculate the similarity between two texts, by getting a term frequency inverse document frequency matrix
    and then calculating the cosine-similarity
    :param text1: The first text, as string
    :param text2: The second text, as string
    :return: the similarity, between 0 and 1
    """

    tfidf = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf.fit_transform([text1, text2])
    tfidf_matrix = tfidf_matrix.astype(np.float32)
    tfidf_matrix.toarray()

    return cosine_similarity(tfidf_matrix, tfidf_matrix)[0][1]


def calc_taste_sim(taste1, taste2):
    """
    Calculate the similarity between two given taste dictionaries
    :param taste1: The first taste-dict
    :param taste2: The second taste-dict
    :return: the similarity, between 0 and 1
    """

    return cosine_similarity([taste1], [taste2])[0][0]


def calc_recipe_sim(recipe_id_1, recipe_id_2, recipe_info):
    """
    Calculate the similarity between two given recipes, using the text-similarity of their information-strings
    as well as the taste-similarity, adding them together and dividing by 2 for normalization
    :param recipe_id_1: the id of the first recipe
    :param recipe_id_2: the id of the second recipe
    :param recipe_info: The dataframe of the recipe database
    :return: the similarity, between 0 and 1
    """

    recipe_1 = recipe_info.loc[recipe_info["ID"] == recipe_id_1]
    recipe_2 = recipe_info.loc[recipe_info["ID"] == recipe_id_2]

    recipe_1_info = recipe_1[" Information-String"].iloc[0].split(" <<instructions>> ")
    recipe_2_info = recipe_2[" Information-String"].iloc[0].split(" <<instructions>> ")

    recipe_1_ingredients = recipe_1_info[0]
    recipe_2_ingredients = recipe_2_info[0]

    recipe_1_instructions = recipe_1_info[1]
    recipe_2_instructions = recipe_2_info[1]

    recipe_1_taste = [recipe_1[" Sweetness"].iloc[0], recipe_1[" Saltiness"].iloc[0], recipe_1[" Sourness"].iloc[0],
                      recipe_1[" Bitterness"].iloc[0], recipe_1[" Savoriness"].iloc[0], recipe_1[" Fattiness"].iloc[0],
                      recipe_1[" Spiciness "].iloc[0]]

    recipe_2_taste = [recipe_2[" Sweetness"].iloc[0], recipe_2[" Saltiness"].iloc[0], recipe_2[" Sourness"].iloc[0],
                      recipe_2[" Bitterness"].iloc[0], recipe_2[" Savoriness"].iloc[0], recipe_2[" Fattiness"].iloc[0],
                      recipe_2[" Spiciness "].iloc[0]]

    try:
        cos_ingredient_sim = calc_text_sim(recipe_1_ingredients, recipe_2_ingredients)
    except ValueError:
        cos_ingredient_sim = 0

    try:
        cos_instruction_sim = calc_text_sim(recipe_1_instructions, recipe_2_instructions)
    except ValueError:
        cos_instruction_sim = 0

    # Give higher weight to ingredients than instructions, divide by 3 for normalization
    cos_text_sim = (2 * cos_ingredient_sim + cos_instruction_sim) / 3

    cos_taste_sim = calc_taste_sim(recipe_1_taste, recipe_2_taste)

    return (cos_text_sim + cos_taste_sim) / 2


def calc_all_recipe_sims(recipe_info):
    """
    Calculate the similarity between all recipes in the database
    :param recipe_info: The dataframe of the recipe database
    :return: a list of lists with [ID_1, ID_2, Similarity, Title_1, Title_2]
    """

    all_sims = []
    all_ids = recipe_info["ID"]

    len_all_ids = len(all_ids)
    for current in range(0, len_all_ids):
        for to_compare in range(current + 1, len_all_ids):
            current_id = all_ids[current]
            id_to_compare = all_ids[to_compare]
            sim = calc_recipe_sim(current_id, id_to_compare, recipe_info)
            current_title = recipe_info[recipe_info["ID"] == current_id][" Title"].iloc[0][1:]
            to_compare_title = recipe_info[recipe_info["ID"] == id_to_compare][" Title"].iloc[0][1:]
            arr = [str(current_id), str(id_to_compare), str(sim), current_title, to_compare_title]
            all_sims.append(arr)

    return all_sims


def write_sims_in_file(sim_list):
    """
    Write a given similarity array into the similarities.csv file
    :param sim_list: the similarity list to write into the file
    """

    similarities_path_and_filename = parent_dir + "/Data/similarities.csv"
    with open(similarities_path_and_filename, "w+") as file:
        for line in sim_list:
            file.write((", ".join(line)))
            file.write("\n")


def calculate_similarities():
    """
    Calculate the similarities between all recipes in the database.
    Write into /Data/similarities.csv
    """

    recipe_database_path_and_filename = parent_dir + "/Data/recipe_database.csv"
    recipe_info = pd.read_csv(recipe_database_path_and_filename, index_col=False)

    write_sims_in_file(calc_all_recipe_sims(recipe_info))


if __name__ == "__main__":
    calculate_similarities()
