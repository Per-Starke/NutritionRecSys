import datetime
import requests
import os
from flask import Flask, render_template, request, redirect, session
import Run.output
import Run.recommend_for_user
import Create_data.check_ratings
import Recommend.recommend_with_macros

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

    return render_template("login.html")


@app.route("/logout")
def logout():
    """
    Not a shown page, redirect here to log out and return to login page
    """

    session.clear()

    return redirect("/login")


@app.route("/", methods=['POST', 'GET'])
def home():
    """
    Create the home-page
    """

    if 'user_id' not in session:
        return redirect("/login")

    session['prediction_needs_updating'] = True
    session["large_range"] = False

    return render_template("home.html", user_id=session['user_id'])


@app.route("/get_rec")
def get_rec():
    """
    Create the get-recommendations-page
    """

    if 'user_id' not in session:
        return redirect("/login")

    elif session['prediction_needs_updating']:
        Run.output.run_recommendation_algos()
        session["large_range"] = False
        session['prediction_needs_updating'] = False

    # Create data-structure for displaying given ratings
    given_ratings = Run.output.get_ratings_for_user(session['user_id'])
    given_ratings_with_titles = {}
    for current_recipe_id, rating in given_ratings.items():
        given_ratings_with_titles[Run.output.get_recipe_title_by_id(current_recipe_id)] = rating
    sorted_given_ratings_with_titles = \
        {k: v for k, v in sorted(given_ratings_with_titles.items(), key=lambda item: item[1], reverse=True)}

    # Create data-structure for displaying predicted ratings
    recipes_and_ratings = Run.output.get_calculated_ratings_for_user(
        session['user_id'], Run.output.write_recommendations(), ratings_to_get=3, userknn=False)
    ids = {}

    try:
        content_based = recipes_and_ratings["content-based"]
        cb_with_titles = {}
        cb_ids = []
        for current_recipe_id, rating in content_based.items():
            current_title = Run.output.get_recipe_title_by_id(current_recipe_id)
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
            itemknn_with_titles[Run.output.get_recipe_title_by_id(current_recipe_id)] = rating
            itemknn_ids.append(current_recipe_id)
        recipes_and_ratings["item-knn"] = itemknn_with_titles
        ids["item-knn"] = itemknn_ids
    except KeyError:
        pass

    try:
        userknn = recipes_and_ratings["user-knn"]
        userknn_with_titles = {}
        userknn_ids = []
        for current_recipe_id, rating in userknn.items():
            userknn_with_titles[Run.output.get_recipe_title_by_id(current_recipe_id)] = rating
            userknn_ids.append(current_recipe_id)
        recipes_and_ratings["user-knn"] = userknn_with_titles
        ids["user-knn"] = userknn_ids
    except KeyError:
        pass

    return render_template("get_rec.html", user_id=session['user_id'], given_ratings=sorted_given_ratings_with_titles,
                           recipes_and_ratings=recipes_and_ratings, ids=ids)


@app.route("/rate", methods=['POST', 'GET'])
def rate():
    """
    Create the rate-recipes-page
    """

    if 'user_id' not in session:
        return redirect("/login")

    elif request.method == 'POST':
        session['rating'] = request.form['get_rating']
        Run.recommend_for_user.write_rating_to_file(session['user_id'], session['recipe_id'], session['rating'])
        Create_data.check_ratings.delete_double_ratings()
        session['prediction_needs_updating'] = True
        return redirect("/rate")

    session['recipe_id'] = Run.recommend_for_user.get_recipe_to_rate(session['user_id'])

    if session['recipe_id']:
        session['recipe_title'] = Run.output.get_recipe_title_by_id(session['recipe_id'])
    else:
        session['recipe_title'] = "No unrated recipe found!"

    return render_template("rate.html", user_id=session['user_id'], recipe_title=session['recipe_title'],
                           recipe_id=session['recipe_id'])


@app.route('/enter_macros', methods=['POST', 'GET'])
def enter_macros():
    """
    Create the page to enter required macronutrients
    """

    if 'user_id' not in session:
        return redirect("/login")

    elif request.method == 'POST':
        session['proteins'] = request.form['set_proteins']
        session['carbs'] = request.form['set_carbs']
        session['fats'] = request.form['set_fats']
        session['range'] = request.form['set_range']

        try:
            float(session['range'])
            range_is_number = True
        except ValueError:
            range_is_number = False

        if not session['proteins'].isdigit() or not session['carbs'].isdigit() or not session['fats'].isdigit()\
                or not range_is_number:
            session.pop('proteins', None)
            session.pop('carbs', None)
            session.pop('fats', None)
            session.pop('range', None)
            return render_template("error.html",
                                   error_text="Invalid input for required macronutrients!")
        return redirect("/get_rec_with_macros")

    return render_template("enter_macros.html", user_id=session['user_id'])


@app.route('/get_rec_with_macros')
def get_rec_with_macros():
    """
    Create the page to show recommendations matching the required macronutrients
    """

    if 'user_id' not in session:
        return redirect("/login")

    if not session["large_range"] or session['prediction_needs_updating']:
        Run.output.run_recommendation_algos(rank_length=100)
    session["large_range"] = True
    session['prediction_needs_updating'] = False

    content_based_recommendations = Recommend.recommend_with_macros.find_top_3_recs_within_range_of_macros(
        user_id=session["user_id"], algorithm="contentbased", proteins=session["proteins"], carbs=session["carbs"],
        fats=session["fats"], allowed_range=session["range"])

    itemknn_recommendations = Recommend.recommend_with_macros.find_top_3_recs_within_range_of_macros(
        user_id=session["user_id"], algorithm="itemknn", proteins=session["proteins"], carbs=session["carbs"],
        fats=session["fats"], allowed_range=session["range"])

    cb_rec_dict = {}
    itemknn_rec_dict = {}

    for recipe_id in content_based_recommendations:
        cb_rec_dict[recipe_id] = Run.output.get_recipe_title_by_id(recipe_id)

    for recipe_id in itemknn_recommendations:
        itemknn_rec_dict[recipe_id] = Run.output.get_recipe_title_by_id(recipe_id)

    return render_template("get_rec_with_macros.html", user_id=session['user_id'], proteins=session["proteins"],
                           carbs=session["carbs"], fats=session["fats"], range_percent=float(session["range"])*100,
                           cb_recs=cb_rec_dict, itemknn_recs=itemknn_rec_dict)


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
        Run.recommend_for_user.write_rating_to_file(user_id, single_recipe_id, session['rating'])
        session['prediction_needs_updating'] = True
        Create_data.check_ratings.delete_double_ratings()

    return render_template('recipe.html', recipe=recipe_info, user_id=session['user_id'])


if __name__ == "__main__":
    app.run(port=8000, debug=True)
