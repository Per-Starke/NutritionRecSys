from caserec.recommenders.item_recommendation.itemknn import ItemKNN

ItemKNN(train_file="ratings.csv", output_file="recommendations.csv", sep=", ").compute()
