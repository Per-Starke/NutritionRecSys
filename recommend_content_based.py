import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


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

    recipe_info = pd.read_csv("recipe_database.csv")

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

    print(recipe_1_taste)
    print(recipe_2_taste)

    return (cos_text_sim + cos_taste_sim) / 2


print(calc_recipe_sim(635059, 647830))

