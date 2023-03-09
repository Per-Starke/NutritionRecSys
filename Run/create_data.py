"""
Create all needed data to make recommendations: a recipe database, a similarity file, a ratings file
"""

from Create_data.calculate_similarity import calculate_similarities
from Create_data.create_ratings import create_ratings
from Create_data.create_recipe_database import create_recipe_database, create_final_recipe_database


def create_data(create_recipe_db=False, calc_sims=True, recipe_amount=50, user_amount=10):
    """
    Create / get the data for recommending recipes
    :param create_recipe_db: False if recipe database shall not be newly created, True (default) if it should
    :param calc_sims: False if similarities shall not be newly calculated, True (default) if they should
    :param recipe_amount: the amount of recipes to get. Only relevant if create_recipe_db is True
    :param user_amount: the amount of users to create random ratings for
    """

    if create_recipe_db:
        create_recipe_database(recipe_amount)

    if calc_sims:
        calculate_similarities()

    create_ratings(user_amount)


if __name__ == "__main__":
    create_data(calc_sims=False)
