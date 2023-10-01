import pandas as pd


# Read the whole ratings_rq file into a DataFrame
ratings_rq = pd.read_csv("ratings_rq_to_analyze.csv")

# Drop all rows until index 32 because these were already existing prior to starting the study due to testing reasons
ratings_rq = ratings_rq.drop(ratings_rq[ratings_rq.index <= 32].index)

# Sort by user_id
# ratings_rq = ratings_rq.sort_values(by='user_id')

# Print the resulting DataFrame
print(ratings_rq)

# Count the number of user ids
unique_user_count = ratings_rq['user_id'].nunique()
print("\nUnique User IDs:", unique_user_count)

# Count how often each algo is used
algo_counts = ratings_rq['algo'].value_counts()
print("\n", algo_counts)

# Calculate the average ratings per algo
average_ratings_by_algo = ratings_rq.groupby('algo')['rating'].mean()
print("\n", average_ratings_by_algo)



