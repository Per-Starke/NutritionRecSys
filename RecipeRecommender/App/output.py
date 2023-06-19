"""
Functions for outputting the recommendations, ratings and data
"""
import time

import pandas as pd
import os

import update_predictions

parent_dir = os.path.dirname(os.getcwd())
col_names = ["User", "Item", "Feedback"]

recipe_database_path_and_filename = parent_dir + "/NutritionRecSys/Data/recipe_database.csv"
recipe_info = pd.read_csv(recipe_database_path_and_filename, index_col=False)

ratings_path_and_filename = parent_dir + "/NutritionRecSys/Data/ratings.csv"


def write_recommendations():
    """
    Write the results of the recommendation algorithms in a list of dataframes
    :return: A list of two dataframes, with the predicted ratings of content-based and ItemKNN
    """

    recommend_contend_based_path_and_filename = \
        parent_dir + "/NutritionRecSys/Data/Predicted_ratings_data/recommendations_content_based.csv"
    recommendations_content_based = pd.read_csv(recommend_contend_based_path_and_filename, names=col_names)

    recommend_collaborative_itemknn_path_and_filename = \
        parent_dir + "/NutritionRecSys/Data/Predicted_ratings_data/recommendations_collaborative_itemknn.csv"
    recommendations_collaborative_itemknn = pd.read_csv(recommend_collaborative_itemknn_path_and_filename,
                                                        names=col_names)

    return [recommendations_content_based, recommendations_collaborative_itemknn]


def get_recipe_title_by_id(id_to_get):
    """
    Get the title of a recipe
    :param id_to_get: the ID of the recipe where we want to get the title from, as int
    :return: the title of the recipe, as string
    """

    return recipe_info[recipe_info["ID"] == id_to_get][" Title"].iloc[0][1:]


def get_macros_by_id(id_to_get):
    """
    Get the macronutrients of a recipe
    :param id_to_get: The ID of the reicpe where we want to get the macros from, as int
    :return: The macros, as dict
    """

    proteins = recipe_info[recipe_info["ID"] == id_to_get][" Proteins"].iloc[0][1:]
    carbs = recipe_info[recipe_info["ID"] == id_to_get][" Carbs"].iloc[0][1:]
    fats = recipe_info[recipe_info["ID"] == id_to_get][" Fats"].iloc[0][1:]

    kcal = str(float(proteins[:-1]) * 4.1 + float(carbs[:-1]) * 4.1 + float(fats[:-1]) * 9.3)

    return {"proteins": proteins, "carbs": carbs, "fats": fats, "kcal": kcal}


def get_mealtype_by_id(id_to_get):
    """
    Get the mealtypes of a recipe
    :param id_to_get: The ID of the reicpe where we want to get the mealtypes from, as int
    :return: the mealtypes, as list
    """

    mealtypes = recipe_info[recipe_info["ID"] == id_to_get][" Dish-Type"].iloc[0][1:].replace(" ", "")

    return mealtypes.split("|")


def get_ratings_for_user(user_id):
    """
    Get the ratings a user gave for all recipes
    :param user_id: the id of the user, as int
    :return: A dict of id:rating pairs, of all ratings a user gave
    """

    ratings = pd.read_csv(ratings_path_and_filename, names=col_names)

    single_user_ratings = ratings.loc[ratings["User"] == int(user_id)]
    single_user_ratings.sort_values(by="Item", inplace=True)

    return_dict = {}

    for line in single_user_ratings.iterrows():
        recipe_id = line[1][1]
        rating = str(line[1][2])

        return_dict[recipe_id] = rating

    print(len(return_dict.keys()))

    return return_dict


def get_amount_of_ratings_for_user(user_id):
    """
    Get the amount of ratings a user gave
    :param user_id: the id of the user, as int
    :return: the amount of ratings, as int
    """

    ratings_for_user = get_ratings_for_user(user_id)

    return len(ratings_for_user.keys())


def user_gave_enough_ratings(user_id):
    """
    Get if the user already rated enough (10+) recipes to use the software
    :param user_id: the id of the user, as int
    :return: True if the user rated 10 or more recipes, False otherwise
    """

    return get_amount_of_ratings_for_user(user_id) >= 10


def get_single_algo_ratings(recommendations, user_id, ratings_to_get):
    """
    Get the predicted ratings of a single algorithm
    :param recommendations: the dataframe of predicted ratings
    :param user_id: the id of the user the ratings shall be returned for
    :param ratings_to_get: The number of ratings to print, as int
    :return: A dict of the top-n recipes with the highest predicted ratings (with id:rating pairs) for a given user
    """

    given_ratings = get_ratings_for_user(user_id)

    ratings_counter = 0

    return_dict = {}

    for line in recommendations.iterrows():
        user = str(int(line[1][0]))
        recipe_id = int(line[1][1])
        rating = str(line[1][2])

        if user == str(user_id) and recipe_id not in given_ratings:
            ratings_counter += 1
            return_dict[recipe_id] = rating

        if ratings_counter >= ratings_to_get:
            break

    return return_dict


def get_calculated_ratings_for_user(user_id, recommendations_list, ratings_to_get):
    """
    Get the calculated ratings a user gave for recipes the user did not rate.
    Get the ratings_to_get amount of recipes with the highest predicted rating.
    :param user_id: the id of the user, as int
    :param recommendations_list: List of dataframes with the predicted ratings, ordererd: cb, itemknn
    :param ratings_to_get: The number of ratings to get, as int
    :return: a list of dicts of id:rating pairs with the calculated top-n ratings for the given user.
    """

    return_dict = {}

    recommendations = recommendations_list[0]
    return_dict["content-based"] = get_single_algo_ratings(recommendations, user_id, ratings_to_get)

    recommendations = recommendations_list[1]
    return_dict["item-knn"] = get_single_algo_ratings(recommendations, user_id, ratings_to_get)

    return return_dict


def write_rating_to_file(user_id, recipe_id, rating):
    """
    Writes the given rating into the ratings.csv file and increment the new_ratings_counter
    :param user_id: the id of the user who rated the recipe
    :param recipe_id: the id of the recipe that got rated
    :param rating: the rating
    """

    try:
        with open(ratings_path_and_filename, "a+") as file:
            if recipe_id:
                str_to_write = "{},{},{}\n".format(str(user_id), str(recipe_id), str(rating))
                file.write(str_to_write)
        update_predictions.increment_new_ratings_counter()
    except Exception:
        time.sleep(1)
        write_rating_to_file(user_id, recipe_id, rating)


def write_rating_to_rq_file(user_id, recipe_id, rating, algo):
    """
    Writes the given ratings into the ratings_rq.csv file, with the additional info which algorithm
    recommended this recipe
    :param user_id: the id of the user who rated the recipe
    :param recipe_id: the id of the recipe that got rated
    :param rating: the rating
    :param algo: the algorithm that recommended this recipe
    """

    ratings_rq_path_and_filename = parent_dir + "/NutritionRecSys/Data/ratings_rq.csv"

    try:
        with open(ratings_rq_path_and_filename, "a+") as file:
            if recipe_id:
                str_to_write = "{},{},{},{}\n".format(str(user_id), str(recipe_id), str(rating), algo)
                file.write(str_to_write)
    except Exception:
        time.sleep(1)
        write_rating_to_file(user_id, recipe_id, rating)


def get_recipe_to_rate(user_id):
    """
    Get a random recipe the user has not rated yet
    :param user_id: The id of the user
    :return: The id of a recipe the user has not rated yet
    """

    all_ids = recipe_info["ID"].sample(frac=1).reset_index(drop=True)

    rated_recipes = get_ratings_for_user(user_id).keys()

    for recipe_id in all_ids:
        if recipe_id not in rated_recipes:
            return recipe_id

    return None


def get_data():
    """
    Get the user and ratings data to display for admin
    :return: a tuple of (coach_users, coach_users_requests, coaches, users, ratings) data, as iterrows
    """

    users_path_and_filename = parent_dir + "/NutritionRecSys/Data/User_data/users.csv"
    coaches_path_and_filename = parent_dir + "/NutritionRecSys/Data/User_data/coaches.csv"
    coach_users_path_and_filename = parent_dir + "/NutritionRecSys/Data/User_data/coach_users.csv"
    coach_user_requests_db_path_and_filename = parent_dir + "/NutritionRecSys/Data/User_data/coach_users_requests.csv"

    coach_users = pd.read_csv(coach_users_path_and_filename)
    coach_users_requests = pd.read_csv(coach_user_requests_db_path_and_filename)
    coaches = pd.read_csv(coaches_path_and_filename)
    users = pd.read_csv(users_path_and_filename)
    ratings = pd.read_csv(ratings_path_and_filename, names=col_names)

    coach_users = coach_users.itertuples()
    coach_users_requests = coach_users_requests.itertuples()
    coaches = coaches.itertuples()
    users = users.itertuples()
    ratings = ratings.itertuples()

    return coach_users, coach_users_requests, coaches, users, ratings
