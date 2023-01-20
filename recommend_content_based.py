from caserec.recommenders.item_recommendation.content_based import ContentBased


def recommend():
    """
    create or update the recommendations.csv file
    """
    ContentBased(train_file="ratings.csv", output_file="recommendations_content_based.csv",
                 similarity_file='similarities.csv', sep=", ", similarity_sep=", ").compute()
