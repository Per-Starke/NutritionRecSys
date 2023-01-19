"""
This file creates a recipe database csv file using the Spoonacular API
"""

import requests
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
rapid_api_key = os.getenv("RAPID_API_KEY")

url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/"

headers = {
    'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
    'x-rapidapi-key': rapid_api_key,
}

randomFind = "recipes/random"


def get_nutrients(recipe_id):
    """
    Get the grams of proteins, carbs and fats for a given recipe
    :param recipe_id: the id of the recipe
    :return: a dict, of grams of proteins, carbs and fats of the recipe
    """

    nutrient_dict = {}

    nutritionLabel = "recipes/{0}/nutritionLabel".format(recipe_id)

    nutrients = requests.request("GET", url + nutritionLabel, headers=headers).text

    # Find nutrient values and store p/c/f in seperate variables
    protein_index = nutrients.find("Protein")
    protein_string = nutrients[protein_index + 12:protein_index + 19]
    protein_string_end = protein_string.find("g") + 1
    proteins = protein_string[:protein_string_end]
    nutrient_dict["Proteins"] = proteins

    carbs_index = nutrients.find("Total Carbohydrate")
    carbs_string = nutrients[carbs_index + 23:carbs_index + 28]
    carbs_index_end = carbs_string.find("g") + 1
    carbs = carbs_string[:carbs_index_end]
    nutrient_dict["Carbs"] = carbs

    fats_index = nutrients.find("Total Fat")
    fats_string = nutrients[fats_index + 14:fats_index + 20]
    fats_index_end = fats_string.find("g") + 1
    fats = fats_string[:fats_index_end]
    nutrient_dict["Fats"] = fats

    return nutrient_dict


def write_recipes_in_list(amount):
    """
    write the id, title, dish-type and nutrients of a given amount of random vegan recipes in a list and return it
    :param amount: the amount of recipes we want
    :return: the list of recipes
    """

    recipe_list = []

    # Get random recipes
    querystring = {"number": amount, "tags": "vegan"}
    response = requests.request("GET", url + randomFind, headers=headers, params=querystring).json()

    # collect the information we are interested in for each recipe, collect in list
    recipes = response.items()
    dish_type = None
    for keys, values in recipes:
        for value in values:
            for recipe in value.items():
                if recipe[0] == "id":
                    recipe_id = recipe[1]
                elif recipe[0] == "dishTypes":
                    dish_type = recipe[1]
                elif recipe[0] == "title":
                    recipe_title = recipe[1]

            if not dish_type:
                dish_type = ["None given"]

            recipe_list.append(list([recipe_id, recipe_title, dish_type, get_nutrients(recipe_id)]))

    return recipe_list


def write_recipes_in_file(recipes):
    """
    write the id, title, dish-type and nutrients of given recipes in the recipe_database.csv file
    :param recipes: The list of recipes to write into the file
    """

    with open("recipe_database.csv", "w+") as file:
        file.write("ID, Title, Dish-Type, Proteins, Carbs, Fats \n")
        for recipe in recipes:

            dish_type_string = str(recipe[2][0])
            if len(recipe[2]) > 1:
                for dishtype in recipe[2][1:]:
                    dish_type_string += " | " + str(dishtype)

            string_to_append = "{0}, {1}, {2}, {3}, {4}, {5}\n".format(str(recipe[0]), str(recipe[1]).replace(",", "|"),
                                                                       dish_type_string, str(recipe[3]["Proteins"]),
                                                                       str(recipe[3]["Carbs"]), str(recipe[3]["Fats"]))

            file.write(string_to_append)


def get_recipe_information_string(recipe_id):
    """
    Get the ingredients and instructions for a certain recipe as a single string
    :param recipe_id: the id of the recipe we want the information about
    :return: the information string
    """
    instructions_url = "recipes/{0}/analyzedInstructions".format(recipe_id)
    instructions = requests.request("GET", url + instructions_url, headers=headers).json()

    instructions_string = ""
    steps_list = instructions[0]["steps"]
    for step_dict in steps_list:
        instructions_string += step_dict["step"] + " "

    ingredients_string = ""

    ingredients_url = "recipes/{0}/ingredientWidget.json".format(recipe_id)
    ingredients = requests.request("GET", url + ingredients_url, headers=headers).json()
    ingredients_dict_list = ingredients["ingredients"]
    for ingredients_dict in ingredients_dict_list:
        ingredients_string += ingredients_dict["name"] + " "

    recipe_information_string = ingredients_string + instructions_string

    return recipe_information_string


def get_taste(recipe_id):
    """
    Get the taste-scores of a certain recipe, divide spiciness by 10000 so it does not affect similarity too much
    :param recipe_id: the id of the recipe we want the taste from
    :return: the taste, as an array
    """
    taste_url = "recipes/{0}/tasteWidget.json".format(recipe_id)
    taste = requests.request("GET", url + taste_url, headers=headers).json()
    taste_array = []
    for key, value in taste.items():
        if key == "spiciness":
            value /= 10000
        taste_array.append(value)
    return taste_array


if __name__ == '__main__':
    pass
    # cleaned_recipes_list = write_recipes_in_list(10)
    # write_recipes_in_file(cleaned_recipes_list)
