import pandas as pd


# Read the whole ratings_rq file into a DataFrame
ratings_rq = pd.read_csv("ratings_rq_to_analyze.csv")

# Print the DataFrame sorted by algorithm
print(ratings_rq.sort_values(by="algo"))

# Count the number of ratings
print("\nnumber of ratings:", len(ratings_rq.index))

# Count the number of user ids
unique_user_count = ratings_rq['user_id'].nunique()
print("\nUnique User IDs:", unique_user_count)

# Count how often each algo is used
algo_counts = ratings_rq['algo'].value_counts()
print("\n", algo_counts)

# Calculate the average ratings per algo
average_ratings_by_algo = ratings_rq.groupby('algo')['rating'].mean()
print("\n", average_ratings_by_algo)



