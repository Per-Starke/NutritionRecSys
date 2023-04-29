import datetime
import requests
import os
from flask import Flask, render_template, request, redirect, session

from RecipeRecommender.output import get_ratings_for_user, get_recipe_title_by_id, \
    get_calculated_ratings_for_user, write_recommendations, write_rating_to_file, get_recipe_to_rate
from RecipeRecommender.ratings import delete_double_ratings
from RecipeRecommender.recommend import find_top_3_matching_reqs, run_recommendation_algos

app = Flask(__name__)
app.secret_key = os.urandom(12)
app.permanent_session_lifetime = datetime.timedelta(days=7)


@app.route("/login", methods=['POST', 'GET'])
def login():
    """
    Create login page
    """

    if 'user_id' in session:
        return redirect("/")

    elif request.method == 'POST':
        session.permanent = True
        session['user_id'] = request.form['set_id']
        if not session['user_id'] or not session['user_id'].isdigit():
            session.pop('user_id', None)
            return render_template("error.html",
                                   error_text="this is no valid user id!")
        return redirect("/")

    session["proteins"] = "0"
    session["carbs"] = "0"
    session["fats"] = "0"
    session["range"] = "0.2"
    session['mealtype'] = "Open"

    return render_template("login.html")


@app.route("/logout")
def logout():
    """
    Not a shown page, redirect here to log out and return to login page
    """

    session.clear()

    return redirect("/login")


@app.route("/reset_requirements")
def reset_requirements():
    """
    Not a shown page, redirect here to reset given requirements and redirect to the enter_reqs page
    """

    session["proteins"] = "0"
    session["carbs"] = "0"
    session["fats"] = "0"
    session["range"] = "0.2"
    session["proteins"] = "0"
    session["mealtype"] = "Open"

    return redirect("/enter_reqs")


@app.route("/", methods=['POST', 'GET'])
def home():
    """
    Create the home-page
    """

    if 'user_id' not in session:
        return redirect("/login")

    session['prediction_needs_updating'] = False  # todo set to True
    session["large_rank"] = False

    return render_template("home.html", user_id=session['user_id'])


@app.route("/recs_and_ratings")
def recs_and_ratings():
    """
    Create the get-recommendations-page
    """

    if 'user_id' not in session:
        return redirect("/login")

    elif session['prediction_needs_updating']:
        run_recommendation_algos()
        session["large_rank"] = False
        session['prediction_needs_updating'] = False

    # Create data-structure for displaying given ratings
    given_ratings = get_ratings_for_user(session['user_id'])
    given_ratings_with_titles = {}
    for current_recipe_id, rating in given_ratings.items():
        given_ratings_with_titles[(current_recipe_id, get_recipe_title_by_id(current_recipe_id))] = rating
    sorted_given_ratings_with_titles = \
        {k: v for k, v in sorted(given_ratings_with_titles.items(), key=lambda item: item[1], reverse=True)}

    # Create data-structure for displaying predicted ratings
    recipes_and_ratings = get_calculated_ratings_for_user(
        session['user_id'], write_recommendations(), ratings_to_get=3)
    ids = {}

    try:
        content_based = recipes_and_ratings["content-based"]
        cb_with_titles = {}
        cb_ids = []
        for current_recipe_id, rating in content_based.items():
            current_title = get_recipe_title_by_id(current_recipe_id)
            if current_title in cb_with_titles:
                current_title = current_title + " "
            cb_with_titles[current_title] = rating
            cb_ids.append(current_recipe_id)
        recipes_and_ratings["content-based"] = cb_with_titles
        ids["content-based"] = cb_ids
    except KeyError:
        pass

    try:
        itemknn = recipes_and_ratings["item-knn"]
        itemknn_with_titles = {}
        itemknn_ids = []
        for current_recipe_id, rating in itemknn.items():
            itemknn_with_titles[get_recipe_title_by_id(current_recipe_id)] = rating
            itemknn_ids.append(current_recipe_id)
        recipes_and_ratings["item-knn"] = itemknn_with_titles
        ids["item-knn"] = itemknn_ids
    except KeyError:
        pass

    return render_template("recs_and_ratings.html", user_id=session['user_id'],
                           given_ratings=sorted_given_ratings_with_titles,
                           recipes_and_ratings=recipes_and_ratings, ids=ids)


@app.route("/random", methods=['POST', 'GET'])
def random():
    """
    Create the random-recipes-page
    """

    if 'user_id' not in session:
        return redirect("/login")

    elif request.method == 'POST':
        session['rating'] = request.form['get_rating']
        write_rating_to_file(session['user_id'], session['recipe_id'], session['rating'])
        delete_double_ratings()
        # session['prediction_needs_updating'] = True todo
        return redirect("/random")

    session['recipe_id'] = get_recipe_to_rate(session['user_id'])

    if session['recipe_id']:
        session['recipe_title'] = get_recipe_title_by_id(session['recipe_id'])
    else:
        session['recipe_title'] = "No unrated recipe found!"

    return render_template("random.html", user_id=session['user_id'], recipe_title=session['recipe_title'],
                           recipe_id=session['recipe_id'])


@app.route('/enter_reqs', methods=['POST', 'GET'])
def enter_reqs():
    """
    Create the page to enter requirements
    """

    if 'user_id' not in session:
        return redirect("/login")

    elif request.method == 'POST':
        session['proteins'] = request.form['set_proteins']
        session['carbs'] = request.form['set_carbs']
        session['fats'] = request.form['set_fats']
        session['range'] = request.form['set_range']
        session['mealtype'] = request.form['get_mealtype']

        try:
            float(session['range'])
            range_is_number = True
        except ValueError:
            range_is_number = False

        if session["proteins"] == "":
            session["proteins"] = "0"
        if session["carbs"] == "":
            session["carbs"] = "0"
        if session["fats"] == "":
            session["fats"] = "0"

        if (not session['proteins'].isdigit() or not session['carbs'].isdigit() or not session['fats'].isdigit()
                or not range_is_number):
            session.pop('proteins', None)
            session.pop('carbs', None)
            session.pop('fats', None)
            session.pop('range', None)
            return render_template("error.html",
                                   error_text="Invalid input for required macronutrients!")
        return redirect("/enter_reqs")

    return render_template("enter_reqs.html", user_id=session['user_id'], proteins=session["proteins"],
                           carbs=session["carbs"], fats=session["fats"], range=session["range"],
                           mealtype=session["mealtype"])


@app.route('/get_recs_with_reqs')
def get_recs_with_reqs():
    """
    Create the page to show recommendations matching the given requirements
    """

    if 'user_id' not in session:
        return redirect("/login")

    if not session["large_rank"] or session['prediction_needs_updating']:
        pass  # todo remove
        # Run.output.run_recommendation_algos(rank_length=100) todo
    session["large_rank"] = True
    session['prediction_needs_updating'] = False

    content_based_recommendations = find_top_3_matching_reqs(
        user_id=session["user_id"], algorithm="contentbased", proteins=session["proteins"], carbs=session["carbs"],
        fats=session["fats"], allowed_range=session["range"], mealtype=session["mealtype"])

    itemknn_recommendations = find_top_3_matching_reqs(
        user_id=session["user_id"], algorithm="itemknn", proteins=session["proteins"], carbs=session["carbs"],
        fats=session["fats"], allowed_range=session["range"], mealtype=session["mealtype"])

    cb_rec_dict = {}
    itemknn_rec_dict = {}

    for recipe_id in content_based_recommendations:
        cb_rec_dict[recipe_id] = get_recipe_title_by_id(recipe_id)

    for recipe_id in itemknn_recommendations:
        itemknn_rec_dict[recipe_id] = get_recipe_title_by_id(recipe_id)

    return render_template("get_recs_with_reqs.html", user_id=session['user_id'], proteins=session["proteins"],
                           carbs=session["carbs"], fats=session["fats"], range_percent=float(session["range"])*100,
                           mealtype=session["mealtype"], cb_recs=cb_rec_dict, itemknn_recs=itemknn_rec_dict)


@app.route('/recipe', methods=['POST', 'GET'])
def recipe():
    """
    Create the page where single recipes are displayed
    """

    if 'user_id' not in session:
        return redirect("/login")

    rapid_api_key = os.getenv("RAPID_API_KEY")
    url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/"
    headers = {
        'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
        'x-rapidapi-key': rapid_api_key}
    single_recipe_id = request.args["id"]
    recipe_info_endpoint = "recipes/{0}/information".format(single_recipe_id)
    recipe_info = requests.request("GET", url + recipe_info_endpoint, headers=headers,
                                   params={'includeNutrition': 'true'}).json()

    user_id = session['user_id']

    if request.method == 'POST':
        session['rating'] = request.form['get_rating']
        write_rating_to_file(user_id, single_recipe_id, session['rating'])
        # session['prediction_needs_updating'] = True todo
        delete_double_ratings()

    return render_template('recipe.html', recipe=recipe_info, user_id=session['user_id'])


if __name__ == "__main__":
    app.run(port=8000, debug=True)
