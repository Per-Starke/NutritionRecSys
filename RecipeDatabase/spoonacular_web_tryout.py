from flask import Flask, render_template, request

import requests

app = Flask(__name__)

url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/"

headers = {
    'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
    'x-rapidapi-key': "8ce59748eemshb5e01121999eb69p16d979jsn482d124d20a0",
}

randomFind = "recipes/random"


@app.route('/')
def search_page():
    return render_template('search.html')


@app.route('/recipes')
def get_recipes():
    # Random recipes
    querystring = {"number": "100", "tags": "vegan"}
    response = requests.request("GET", url + randomFind, headers=headers, params=querystring).json()
    print(response)
    return render_template('recipes.html', recipes=response['recipes'])


@app.route('/recipe')
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

    return render_template('recipe.html', recipe=recipe_info)


if __name__ == '__main__':
    app.run()
