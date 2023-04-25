"""
This file creates a recipe database csv file using the Spoonacular API
"""

import requests
import os
from dotenv import load_dotenv, find_dotenv
import pandas as pd

parent_dir = os.path.dirname(os.getcwd())

load_dotenv(find_dotenv())
rapid_api_key = os.getenv("RAPID_API_KEY")

url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/"

headers = {
    'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
    'x-rapidapi-key': rapid_api_key,
}


def get_dishtype(recipe_id):
    """
    Get the dish-type of a certain recipe
    :param recipe_id: the id of the recipe
    :return: the dish-type, as an array
    """

    info_url = "recipes/{0}/information".format(recipe_id)
    info = requests.request("GET", url + info_url, headers=headers).json()

    dishtypes =  info["dishTypes"]
    if isinstance(dishtypes, list):
        return dishtypes
    else:
        return [dishtypes]


def get_recipe_information_string(recipe_id):
    """
    Get the ingredients and instructions for a certain recipe as a single string, without commas so that we can put it
    into a csv file. The ingredients are put in the string three times, so that they contribute more to the similarity
    :param recipe_id: the id of the recipe we want the information about
    :return: the information string
    """

    instructions_url = "recipes/{0}/analyzedInstructions".format(recipe_id)
    instructions = requests.request("GET", url + instructions_url, headers=headers).json()
    instructions_string_list = []
    if instructions:  # Make sure to not get an error if instructions are empty
        steps_list = instructions[0]["steps"]
        for step_dict in steps_list:
            instructions_string_list.append(step_dict["step"])
    instructions_string = " ".join(instructions_string_list)

    ingredients_string_list = []

    ingredients_url = "recipes/{0}/ingredientWidget.json".format(recipe_id)
    ingredients = requests.request("GET", url + ingredients_url, headers=headers).json()
    if ingredients:  # Make sure to not get an error if ingredients are empty
        ingredients_dict_list = ingredients["ingredients"]
        for ingredients_dict in ingredients_dict_list:
            ingredients_string_list.append(ingredients_dict["name"])
    ingredients_string = " ".join(ingredients_string_list)

    recipe_information_string = (ingredients_string + " <<instructions>> ") + instructions_string
    recipe_information_string = recipe_information_string.replace(",", " ").replace("\"", " ")

    return recipe_information_string


def get_taste(recipe_id):
    """
    Get the taste-scores of a certain recipe, divide spiciness by 10000, so it does not affect similarity too much
    :param recipe_id: the id of the recipe we want the taste from
    :return: the taste, as a dict
    """

    taste_url = "recipes/{0}/tasteWidget.json".format(recipe_id)
    taste = requests.request("GET", url + taste_url, headers=headers).json()
    taste["spiciness"] = taste["spiciness"] / 10000
    return taste


def get_nutrients(recipe_id):
    """
    Get the grams of proteins, carbs and fats for a given recipe
    :param recipe_id: the id of the recipe
    :return: a dict, of grams of proteins, carbs and fats of the recipe
    """

    nutrient_dict = {}

    nutrition_label = "recipes/{0}/nutritionLabel".format(recipe_id)

    nutrients = requests.request("GET", url + nutrition_label, headers=headers).text

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


def write_recipes_in_list(amount, query="random"):
    """
    write the id, title, dish-type, nutrients, information-string and taste of a given amount of vegan recipes
    following a given query in a list and return it
    :param amount: the amount of recipes we want
    :param query: the query to search for, default "random"
    :return: the list of recipes
    """

    remove_last = False

    recipe_list = []

    if query == "random":
        querystring = {"number": amount, "tags": "vegan"}
        response = requests.request("GET", url + "recipes/random", headers=headers, params=querystring).json()

    elif type(query) is dict:
        remove_last = True
        query["diet"] = "vegan"
        query["number"] = amount
        response = requests.request("GET", url + "recipes/complexSearch", headers=headers, params=query).json()

    else:
        raise ValueError("This is not a valid query!")

    # collect only the information we are interested in for each recipe, collect in list
    if remove_last:
        del response["offset"]
        del response["number"]
        del response["totalResults"]
    recipes = response.items()
    recipe_id = None
    recipe_title = None
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
                    recipe_title = recipe_title.replace("\"", " ")

            if not dish_type or dish_type == []:
                dish_type = ["None given"]

            recipe_list.append(list([recipe_id, recipe_title, dish_type, get_nutrients(recipe_id),
                                     get_recipe_information_string(recipe_id), get_taste(recipe_id)]))

    return recipe_list


def write_recipes_in_file(recipes, mode="w+"):
    """
    write the id, title, dish-type, nutrients, information-string and taste of given recipes in the
    recipe_database.csv file
    :param recipes: The list of recipes to write into the file
    :param mode: the write-mode for the file, default w+
    """

    database_path_and_filename = parent_dir + "/Data/recipe_database.csv"
    with open(database_path_and_filename, mode) as file:
        if mode == "w+":
            file.write("ID, Title, Dis"
                       "h-Type, Proteins, Carbs, Fats, Information-String, Sweetness, "
                       "Saltiness, Sourness, Bitterness, Savoriness, Fattiness, Spiciness\n")

        for recipe in recipes:
            if recipe[2] == ["None given"]:
                recipe[2] = get_dishtype(recipe[0])

            try:
                dish_type_string = str(recipe[2][0])
            except IndexError:
                dish_type_string = "None given"

            if len(recipe[2]) > 1:
                for dishtype in recipe[2][1:]:
                    dish_type_string += " | " + str(dishtype)

            string_to_append = "{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}\n".format(str(recipe[0]),
                                                                                                 str(recipe[1]).replace(
                                                                                                     ",", "|"),
                                                                                                 dish_type_string, str(
                    recipe[3]["Proteins"]),
                                                                                                 str(recipe[3][
                                                                                                         "Carbs"]),
                                                                                                 str(recipe[3]["Fats"]),
                                                                                                 str(recipe[4]),
                                                                                                 str(recipe[5][
                                                                                                         "sweetness"]),
                                                                                                 str(recipe[5][
                                                                                                         "saltiness"]),
                                                                                                 str(recipe[5][
                                                                                                         "sourness"]),
                                                                                                 str(recipe[5][
                                                                                                         "bitterness"]),
                                                                                                 str(recipe[5][
                                                                                                         "savoriness"]),
                                                                                                 str(recipe[5][
                                                                                                         "fattiness"]),
                                                                                                 str(recipe[5][
                                                                                                         "spiciness"]))

            file.write(string_to_append)


def write_recipes_in_file_from_df(recipe_df):
    """
    write the id, title, dish-type, nutrients, information-string and taste of given recipes in the
    recipe_database.csv file, append at the end of the file
    :param recipe_df: The pandas dataframe of recipes to write into the file
    """

    database_path_and_filename = parent_dir + "/Data/recipe_database.csv"
    with open(database_path_and_filename, "w+") as file:
        file.write("ID, Title, Dis"
                   "h-Type, Proteins, Carbs, Fats, Information-String, Sweetness, "
                   "Saltiness, Sourness, Bitterness, Savoriness, Fattiness, Spiciness \n")
        for index, recipe in recipe_df.iterrows():
            string_to_append = ""
            for i in range(0, 14):
                string_to_append = string_to_append + str(recipe[i]) + ","
            string_to_append = string_to_append + "\n"
            file.write(string_to_append)


def create_final_recipe_database(mode="a+", query="random"):
    """
    Creates the final recipe database, appending new recipes to the database and checking for duplicates.
    Needs to be done several times, spread over days, in order to not pay too much for spoonacular api due to
    too many requests / day.
    :param mode: the write-mode for the file, default a+
    :param query: the query to give to write_recipes_in_list
    """

    # add new recipes
    write_recipes_in_file(write_recipes_in_list(100, query), mode=mode)

    # read database, remove duplicates, write to file without duplicates
    recipe_database_path_and_filename = parent_dir + "/Data/recipe_database.csv"
    recipe_database = pd.read_csv(recipe_database_path_and_filename, index_col=False)
    recipe_database.drop_duplicates(inplace=True)
    write_recipes_in_file_from_df(recipe_database)


if __name__ == "__main__":
    # Initialize DB with search for 100 random recipes
    # create_final_recipe_database(mode="w+")

    # Search for more random recipes to append
    # create_final_recipe_database()

    # Query 1 to search for: High(er) protein pasta recipes
    query1 = {"query": "pasta", "minProtein": "20"}
    # create_final_recipe_database(query=query1)

    # Query 2 to search for: High(er) protein rice recipes
    query2 = {"query": "rice", "minProtein": "20"}
    # create_final_recipe_database(query=query2)

    # Query 3 to search for: High(er) protein tofu recipes
    query3 = {"query": "tofu", "minProtein": "20"}
    # create_final_recipe_database(query=query3)

    # Query 4 to search for: very high protein tofu recipes
    query4 = {"query": "tofu", "minProtein": "40"}
    # create_final_recipe_database(query=query4)

    # Query 5 to search for: high(er) protein salad recipes
    query5 = {"query": "salad", "minProtein": "20"}
    # create_final_recipe_database(query=query5)

    # Query 6 to search for: low fat & high(er) protein salad recipes
    query6 = {"query": "salad", "minProtein": "20", "maxFat": "15"}
    # create_final_recipe_database(query=query6)

    # Query 7 to search for: fruit recipes
    query7 = {"query": "fruit"}
    # create_final_recipe_database(query=query7)

    # Query 8 to search for: low-carb pasta recipes
    query8 = {"query": "pasta", "maxCarbs": "30"}
    # create_final_recipe_database(query=query8)

    # Query 9 to search for: High(er) protein burger recipes
    query9 = {"query": "burger", "minProtein": "20"}
    # create_final_recipe_database(query=query9)

    # Query 10 to search for: burger recipes
    query10 = {"query": "burger"}
    # create_final_recipe_database(query=query10)

    # Query 11 to search for: coffee recipes
    query11 = {"query": "coffee"}
    # create_final_recipe_database(query=query11)

    # Query 12 to search for: protein recipes
    query12 = {"query": "protein"}
    # create_final_recipe_database(query=query12)

    # Query 13 to search for: healthy recipes
    query13 = {"query": "healthy"}
    create_final_recipe_database(query=query13)
