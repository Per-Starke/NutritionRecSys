import requests
import os
from flask import Flask, render_template, url_for, request
import Run.output
import Run.recommend_for_user

app = Flask(__name__)

user_id = 0
prediction_needs_updating = True
recipe_id = None

rapid_api_key = os.getenv("RAPID_API_KEY")

url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/"
headers = {
  'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
  'x-rapidapi-key': rapid_api_key,
  }


@app.route("/", methods=['POST', 'GET'])
def home_page():
    """
    Create the home-page
    """

    return render_template("home.html")


@app.route("/get_rec", methods=['POST', 'GET'])
def get_rec_page():
    """
    Create the get-recommendations-page
    """

    global user_id
    global prediction_needs_updating
    global recipe_id

    if prediction_needs_updating:
        Run.output.run_recommendation_algos()
        prediction_needs_updating = False

    if request.method == 'POST':
        user_id = request.form['update_id']
        if not user_id or not user_id.isdigit():
            return render_template("error.html",
                                   error_text="this is no valid user id!", return_link="/get_rec")

    # Create data-structure for displaying given ratings
    given_ratings = Run.output.get_ratings_for_user(user_id)
    given_ratings_with_titles = {}
    for recipe_id, rating in given_ratings.items():
        given_ratings_with_titles[Run.output.get_recipe_title_by_id(recipe_id)] = rating
    sorted_given_ratings_with_titles = \
        {k: v for k, v in sorted(given_ratings_with_titles.items(), key=lambda item: item[1], reverse=True)}

    # Create data-structure for displaying predicted ratings
    recipes_and_ratings = Run.output.get_calculated_ratings_for_user(
        user_id, Run.output.write_recommendations(), ratings_to_get=3, userknn=False)

    try:
        content_based = recipes_and_ratings["content-based"]
        cb_with_titles = {}
        for recipe_id, rating in content_based.items():
            cb_with_titles[Run.output.get_recipe_title_by_id(recipe_id)] = rating
        recipes_and_ratings["content-based"] = cb_with_titles
    except KeyError:
        pass

    try:
        itemknn = recipes_and_ratings["item-knn"]
        itemknn_with_titles = {}
        for recipe_id, rating in itemknn.items():
            itemknn_with_titles[Run.output.get_recipe_title_by_id(recipe_id)] = rating
        recipes_and_ratings["item-knn"] = itemknn_with_titles
    except KeyError:
        pass

    try:
        userknn = recipes_and_ratings["user-knn"]
        userknn_with_titles = {}
        for recipe_id, rating in userknn.items():
            userknn_with_titles[Run.output.get_recipe_title_by_id(recipe_id)] = rating
        recipes_and_ratings["user-knn"] = userknn_with_titles
    except KeyError:
        pass

    return render_template("get_rec.html", user_id=user_id, given_ratings=sorted_given_ratings_with_titles,
                           recipes_and_ratings=recipes_and_ratings)


@app.route("/rate", methods=['POST', 'GET'])
def rate_page():
    """
    Create the get-recommendations-page
    """

    global user_id
    global prediction_needs_updating
    global recipe_id
    old_recipe_id = recipe_id

    recipe_id = Run.recommend_for_user.get_recipe_to_rate(user_id)

    if recipe_id:
        recipe_title = Run.output.get_recipe_title_by_id(recipe_id)
    else:
        recipe_title = "No unrated recipe found!"

    if request.method == 'POST':
        try:
            user_id = request.form['update_id']
            if not user_id or not user_id.isdigit():
                return render_template("error.html",
                                       error_text="this is no valid user id!", return_link="/rate")
            recipe_id = Run.recommend_for_user.get_recipe_to_rate(user_id)
            if recipe_id:
                recipe_title = Run.output.get_recipe_title_by_id(recipe_id)
            else:
                recipe_title = "No unrated recipe found!"
        except KeyError:
            rating = request.form['get_rating']
            if Run.recommend_for_user.check_input(rating):
                Run.recommend_for_user.write_rating_to_file(user_id, old_recipe_id, rating)
                prediction_needs_updating = True
            else:
                if not user_id or not user_id.isdigit():
                    return render_template("error.html",
                                           error_text="this is no valid rating!", return_link="/rate")

    return render_template("rate.html", user_id=user_id, recipe_title=recipe_title)


@app.route('/recipe')
def get_recipe():
    """
    Create the page where single recipes are displayed,
    mainly taken from "https://rapidapi.com/blog/build-food-website/"
    """

    single_recipe_id = request.args['id']
    recipe_info_endpoint = "recipes/{0}/information".format(single_recipe_id)
    ingedientsWidget = "recipes/{0}/ingredientWidget".format(single_recipe_id)
    equipmentWidget = "recipes/{0}/equipmentWidget".format(single_recipe_id)
    recipe_info = requests.request("GET", url + recipe_info_endpoint, headers=headers).json()

    recipe_headers = {
        'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
        'x-rapidapi-key': "<YOUR_RAPID_API_KEY>",
        'accept': "text/html"
    }
    querystring = {"defaultCss": "true", "showBacklink": "false"}
    recipe_info['ingredientsWidget'] = requests.request("GET", url + ingedientsWidget, headers=recipe_headers,
                                                        params=querystring).text
    recipe_info['equipmentWidget'] = requests.request("GET", url + equipmentWidget, headers=recipe_headers,
                                                      params=querystring).text

    return render_template('recipe.html', recipe=recipe_info)


if __name__ == "__main__":
    app.run(port=8000, debug=True)
