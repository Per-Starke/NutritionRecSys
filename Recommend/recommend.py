from caserec.recommenders.item_recommendation.itemknn import ItemKNN
from caserec.recommenders.item_recommendation.userknn import UserKNN
from caserec.recommenders.item_recommendation.content_based import ContentBased
import os

parent_dir = os.path.dirname(os.getcwd())

ratings_path_and_filename = parent_dir + "/Data/ratings.csv"


def recommend_collaborative_itemknn():
    """
    create or update the recommendations.csv file
    """

    output_path_and_filename = parent_dir + "/Predicted_ratings_data/recommendations_collaborative_itemknn.csv"
    ItemKNN(train_file=ratings_path_and_filename, output_file=output_path_and_filename, sep=", ").compute()


def recommend_collaborative_userknn():
    """
    create or update the recommendations.csv file
    """

    output_path_and_filename = parent_dir + "/Predicted_ratings_data/recommendations_collaborative_userknn.csv"
    UserKNN(train_file=ratings_path_and_filename, output_file=output_path_and_filename, sep=", ").compute()


def recommend_content_based():
    """
    create or update the recommendations.csv file
    """

    output_path_and_filename = parent_dir + "/Predicted_ratings_data/recommendations_content_based.csv"
    similarities_path_and_filename = parent_dir + "/Data/similarities.csv"
    ContentBased(train_file=ratings_path_and_filename, output_file=output_path_and_filename,
                 similarity_file=similarities_path_and_filename, sep=", ", similarity_sep=", ").compute()
