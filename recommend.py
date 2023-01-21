from caserec.recommenders.item_recommendation.itemknn import ItemKNN
from caserec.recommenders.item_recommendation.userknn import UserKNN
from caserec.recommenders.item_recommendation.content_based import ContentBased


def recommend_collaborative_itemknn():
    """
    create or update the recommendations.csv file
    """
    ItemKNN(train_file="ratings.csv", output_file="recommendations_collaborative_itemknn.csv", sep=", ").compute()


def recommend_collaborative_userknn():
    """
    create or update the recommendations.csv file
    """
    UserKNN(train_file="ratings.csv", output_file="recommendations_collaborative_userknn.csv", sep=", ").compute()


def recommend_content_based():
    """
    create or update the recommendations.csv file
    """
    ContentBased(train_file="ratings.csv", output_file="recommendations_content_based.csv",
                 similarity_file='similarities.csv', sep=", ", similarity_sep=", ").compute()
