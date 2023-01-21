"""
Create all needed data to make recommendations: a recipe database, a similarity file, a ratings file
"""

from Create_data.calculate_similarity import calculate_similarities
from Create_data.create_ratings import create_ratings
from Create_data.create_recipe_database import create_recipe_database


def create_data(recipe_db="Create", recipe_amount=50, user_amount=50):
    """
    Create / get the data for recommending recipes
    :param recipe_db: "Use" if recipe database shall not be newly created, "Create" (default) if it should
    :param recipe_amount:
    :param user_amount:
    """

    if recipe_db == "Create":
        create_recipe_database(recipe_amount)
    elif recipe_db == "Use":
        pass
    else:
        raise ValueError("recipe_db must be 'Create' or 'Use'")

    calculate_similarities()
    create_ratings(user_amount)


if __name__ == "__main__":
    create_data("Use", 50, 100)
