import pandas as pd


# Read the whole ratings_rq file into a DataFrame
ratings_rq = pd.read_csv("ratings_rq_to_analyze.csv")

# Drop all rows until index 32 because these were already existing prior to starting the study
ratings_rq = ratings_rq.drop(ratings_rq[ratings_rq.index <= 32].index)



# Print the resulting DataFrame
print(ratings_rq)

