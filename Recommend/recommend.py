"""
Includes functions to run the CaseRec algorithms to predict ratings
"""

from caserec.recommenders.item_recommendation.itemknn import ItemKNN
from caserec.recommenders.item_recommendation.userknn import UserKNN
from caserec.recommenders.item_recommendation.content_based import ContentBased
import os

parent_dir = os.path.dirname(os.getcwd())

ratings_path_and_filename = parent_dir + "/Data/ratings.csv"


def recommend_collaborative_itemknn(rank_length=4):
    """
    create or update the recommendations.csv file
    :param rank_length: The number of predictions to calculate, default 4
    """

    output_path_and_filename = parent_dir + "/Predicted_ratings_data/recommendations_collaborative_itemknn.csv"
    ItemKNN(train_file=ratings_path_and_filename, output_file=output_path_and_filename, sep=", ",
            rank_length=rank_length).compute()


def recommend_collaborative_userknn(rank_length=4):
    """
    create or update the recommendations.csv file
    :param rank_length: The number of predictions to calculate, default 4
    """

    output_path_and_filename = parent_dir + "/Predicted_ratings_data/recommendations_collaborative_userknn.csv"
    UserKNN(train_file=ratings_path_and_filename, output_file=output_path_and_filename, sep=", ",
            rank_length=rank_length).compute()


def recommend_content_based(rank_length=4):
    """
    create or update the recommendations.csv file
    :param rank_length: The number of predictions to calculate, default 4
    """

    output_path_and_filename = parent_dir + "/Predicted_ratings_data/recommendations_content_based.csv"
    similarities_path_and_filename = parent_dir + "/Data/similarities.csv"
    ContentBased(train_file=ratings_path_and_filename, output_file=output_path_and_filename,
                 similarity_file=similarities_path_and_filename, sep=", ", similarity_sep=", ",
                 rank_length=rank_length).compute()
