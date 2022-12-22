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

    print(nutrients)


def get_recipe():
    recipe_id = request.args['id']
    recipe_info_endpoint = "recipes/{0}/information".format(recipe_id)
    nutritionLabel = "recipes/{0}/nutritionLabel".format(recipe_id)

    recipe_info = requests.request("GET", url + recipe_info_endpoint, headers=headers).json()

    recipe_headers = {
        'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
        'x-rapidapi-key': "8ce59748eemshb5e01121999eb69p16d979jsn482d124d20a0",
        'accept': "text/html"
    }
    querystring = {"defaultCss": "true", "showBacklink": "false"}

    recipe_info['nutritionLabel'] = requests.request("GET", url + nutritionLabel, headers=recipe_headers,
                                                     params=querystring).text


if __name__ == '__main__':
    get_recipes()
