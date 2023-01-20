from caserec.recommenders.item_recommendation.itemknn import ItemKNN


def recommend():
    """
    create or update the recommendations.csv file
    """
    ItemKNN(train_file="ratings.csv", output_file="recommendations_collaborative.csv", sep=", ").compute()
