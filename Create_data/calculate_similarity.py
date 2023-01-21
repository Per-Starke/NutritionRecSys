import pandas as pd
import numpy as np
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

global recipe_info

parent_dir = os.path.dirname(os.getcwd())


def calc_text_sim(text1, text2):
    """
    Calculate the similarity between two texts, by getting a term frequency inverse document frequency matrix
    and then calculating the cosine-similarity
    :param text1:
    :param text2:
    :return: the similarity, between 0 and 1, as int
    """

    tfidf = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf.fit_transform([text1, text2])
    tfidf_matrix = tfidf_matrix.astype(np.float32)
    tfidf_matrix.toarray()

    return cosine_similarity(tfidf_matrix, tfidf_matrix)[0][1]


def calc_taste_sim(taste1, taste2):
    """
    Calculate the similarity between two given taste dictionaries
    :param taste1:
    :param taste2:
    :return: the similarity, between 0 and 1, as int
    """

    return cosine_similarity([taste1], [taste2])[0][0]


def calc_recipe_sim(recipe_id_1, recipe_id_2):
    """
    Calculate the similarity between two given recipes, using the text-similarity of their information-strings
    as well as the taste-similarity, adding them together and dividing by 2 for normalization
    :param recipe_id_1: the id of the first recipe
    :param recipe_id_2: the id of the second recipe
    :return: the similarity, between 0 and 1, as int
    """

    recipe_1 = recipe_info.loc[recipe_info["ID"] == recipe_id_1]
    recipe_2 = recipe_info.loc[recipe_info["ID"] == recipe_id_2]

    recipe_1_info_string = recipe_1[" Information-String"].iloc[0]
    recipe_2_info_string = recipe_2[" Information-String"].iloc[0]

    recipe_1_taste = [recipe_1[" Sweetness"].iloc[0], recipe_1[" Saltiness"].iloc[0], recipe_1[" Sourness"].iloc[0],
                      recipe_1[" Bitterness"].iloc[0], recipe_1[" Savoriness"].iloc[0], recipe_1[" Fattiness"].iloc[0],
                      recipe_1[" Spiciness "].iloc[0]]

    recipe_2_taste = [recipe_2[" Sweetness"].iloc[0], recipe_2[" Saltiness"].iloc[0], recipe_2[" Sourness"].iloc[0],
                      recipe_2[" Bitterness"].iloc[0], recipe_2[" Savoriness"].iloc[0], recipe_2[" Fattiness"].iloc[0],
                      recipe_2[" Spiciness "].iloc[0]]

    cos_text_sim = calc_text_sim(recipe_1_info_string, recipe_2_info_string)
    cos_taste_sim = calc_taste_sim(recipe_1_taste, recipe_2_taste)

    return (cos_text_sim + cos_taste_sim) / 2


def calc_all_recipe_sims():
    """
    Calculate the similarity between all recipes in the database
    :return: a list of lists with [ID_1, ID_2, Similarity, Title_1, Title_2]
    """

    all_sims = []
    all_ids = recipe_info["ID"]

    len_all_ids = len(all_ids)
    for current in range(0, len_all_ids):
        for to_compare in range(current + 1, len_all_ids):
            current_id = all_ids[current]
            id_to_compare = all_ids[to_compare]
            sim = calc_recipe_sim(current_id, id_to_compare)
            current_title = recipe_info[recipe_info["ID"] == current_id][" Title"].iloc[0][1:]
            to_compare_title = recipe_info[recipe_info["ID"] == id_to_compare][" Title"].iloc[0][1:]
            arr = [str(current_id), str(id_to_compare), str(sim), current_title, to_compare_title]
            all_sims.append(arr)

    return all_sims


def write_sims_in_file(sim_array):
    """
    Write a given similarity array into the similarities.csv file
    :param sim_array: the similarity array to write into the file
    """

    similarities_path_and_filename = parent_dir + "/Data/similarities.csv"
    with open(similarities_path_and_filename, "w+") as file:
        for line in sim_array:
            file.write("\n")
            file.write((", ".join(line)))


if __name__ == "__main__":

    recipe_database_path_and_filename = parent_dir + "/Data/recipe_database.csv"
    recipe_info = pd.read_csv(recipe_database_path_and_filename)
    write_sims_in_file(calc_all_recipe_sims())
