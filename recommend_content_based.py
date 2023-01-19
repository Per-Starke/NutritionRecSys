from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from create_recipe_database import get_recipe_information_string, get_taste
import numpy as np

recipe_id = 715769
recipe_information_string_1 = get_recipe_information_string(recipe_id)
recipe_id = 782600
recipe_information_string_2 = get_recipe_information_string(recipe_id)
tfidf = TfidfVectorizer(stop_words="english")
testlist = [recipe_information_string_1, recipe_information_string_2]
tfidf_matrix = tfidf.fit_transform(testlist)
tfidf_matrix = tfidf_matrix.astype(np.float32)
tfidf_matrix.toarray()
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)[0][1]

recipe_id = 715769
taste_1 = [get_taste(recipe_id)]
recipe_id = 782600
taste_2 = [get_taste(recipe_id)]

cosine_sim_2 = cosine_similarity(taste_1, taste_2)[0][0]

similarity = (cosine_sim + cosine_sim_2) / 2

print(similarity)
