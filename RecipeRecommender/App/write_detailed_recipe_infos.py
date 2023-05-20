import os
import json
import pandas as pd
import requests

parent_dir = os.path.dirname(os.getcwd())
detailed_recipe_infos_path_and_filename = parent_dir + "/NutritionRecSys/Data/detailed_recipe_info.json"
recipe_database_path_and_filename = parent_dir + "/NutritionRecSys/Data/recipe_database.csv"

rapid_api_key = os.getenv("RAPID_API_KEY")
url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/"
headers = {
    'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
    'x-rapidapi-key': rapid_api_key}

with open(detailed_recipe_infos_path_and_filename, "w+") as file:
    recipe_db = pd.read_csv(recipe_database_path_and_filename, index_col=False)
    recipe_ids = recipe_db["ID"]

    counter = 0
    for single_recipe_id in recipe_ids:

        counter = counter + 1
        if counter >= 20:
            break

        recipe_info_endpoint = "recipes/{0}/information".format(single_recipe_id)
        recipe_info = requests.request("GET", url + recipe_info_endpoint, headers=headers,
                                       params={'includeNutrition': 'true'}).json()

        json.dump(recipe_info, file)


