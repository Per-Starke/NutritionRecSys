from flask import request

import requests

url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/"

headers = {
    'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
    'x-rapidapi-key': "8ce59748eemshb5e01121999eb69p16d979jsn482d124d20a0",
}

randomFind = "recipes/random"


def get_recipes():
    # Random recipes
    querystring = {"number": "5", "tags": "vegan"}
    response = requests.request("GET", url + randomFind, headers=headers, params=querystring).json()
    items = response.items()
    for keys, values in items:
        recipe_id = None
        for item in values[0].items():
            print(item)
            if item[0] == "id":
                recipe_id = item[1]
    print("\nid =", recipe_id, "\n")

    nutritionLabel = "recipes/{0}/nutritionLabel".format(recipe_id)

    nutrients = requests.request("GET", url + nutritionLabel, headers=headers).text

    protein_index = nutrients.find("Protein")
    protein_string = nutrients[protein_index+12:protein_index+20]
    protein_string_end = protein_string.find("g") + 1
    proteins = protein_string[:protein_string_end]
    print("Proteins:", proteins)

    fats_index = nutrients.find("Total Fat")
    fats_string = nutrients[fats_index + 14:fats_index + 20]
    fats_index_end = fats_string.find("g") + 1
    fats = fats_string[:fats_index_end]
    print("Fats:", fats)

    carbs_index = nutrients.find("Total Carbohydrate")
    carbs_string = nutrients[carbs_index + 23:carbs_index + 30]
    carbs_index_end = carbs_string.find("g") + 1
    carbs = carbs_string[:carbs_index_end]
    print("Carbs:", carbs)


if __name__ == '__main__':
    get_recipes()
