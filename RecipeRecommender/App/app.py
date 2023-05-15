import datetime
import requests
import os
from flask import Flask, render_template, request, redirect, session
from werkzeug.exceptions import BadRequestKeyError

from update_predictions import check_update_predicted_ratings
from authentication import check_user_login, check_coach_login, check_coach_can_view_user, \
    write_new_user_to_file, write_new_coach_to_file, check_for_coaching_requests, \
    confirm_request_auth
from output import get_ratings_for_user, get_recipe_title_by_id, \
    get_calculated_ratings_for_user, write_recommendations, write_rating_to_file, get_recipe_to_rate
from ratings import delete_double_ratings
from recommend import find_top_3_matching_reqs, run_recommendation_algos
from coach_view import get_users, remove_client_by_id, request_new_client

app = Flask(__name__)
app.secret_key = os.urandom(12)
app.permanent_session_lifetime = datetime.timedelta(days=7)


@app.route("/login", methods=['POST', 'GET'])
def login():
    """
    Create login page
    """

    if 'user_id' in session:
        return redirect("/coach_logout")

    if request.method == 'POST':
        session.permanent = True
        session['user_id'] = request.form['set_id']
        password = request.form['set_pw']
        if not session['user_id'] or not session['user_id'].isdigit():
            session.pop('user_id', None)
            return render_template("error.html", error_text="this is no valid format for a user-id!")

        user_id_passsword_check = check_user_login(session['user_id'], password)

        if user_id_passsword_check == 1:
            session.pop('user_id', None)
            return render_template("error.html", error_text="This user-id does not exist")

        if user_id_passsword_check == 2:
            session.pop('user_id', None)
            return render_template("error.html", error_text="Wrong password")

        if user_id_passsword_check == 3:
            return redirect("/")

        return render_template("error.html", error_text="Unknown error")

    session["proteins"] = "0"
    session["carbs"] = "0"
    session["fats"] = "0"
    session["range"] = "0.2"
    session['mealtype'] = "Open"

    return render_template("login.html")


@app.route("/coach_login", methods=['POST', 'GET'])
def coach_login():
    """
    Create coach login page
    """

    if 'coach_id' in session:
        return redirect("/coach_logout")

    if 'user_id' in session:
        return redirect("/coach_logout")

    if request.method == 'POST':
        session.permanent = True
        session['coach_id'] = request.form['set_coach_id']
        password = request.form['set_coach_pw']
        if not session['coach_id'] or not session['coach_id'].isdigit():
            session.pop('coach_id', None)
            return render_template("error.html", error_text="this is no valid format for a coach-id!")

        coach_id_passsword_check = check_coach_login(session['coach_id'], password)

        if coach_id_passsword_check == 1:
            session.pop('coach_id', None)
            return render_template("error.html", error_text="This coach-id does not exist")

        if coach_id_passsword_check == 2:
            session.pop('coach_id', None)
            return render_template("error.html", error_text="Wrong password")

        if coach_id_passsword_check == 3:
            return redirect("/")

        return render_template("error.html", error_text="Unknown error")

    session["proteins"] = "0"
    session["carbs"] = "0"
    session["fats"] = "0"
    session["range"] = "0.2"
    session['mealtype'] = "Open"
    session['coach_views_user'] = False

    return render_template("coach_login.html")


@app.route("/logout")
def logout():
    """
    Not a shown page, redirect here to log out from user and return to login page, or home page if logged in as coach
    """

    coach_logged_in = False

    if 'coach_id' in session:
        coach_logged_in = True
        coach_id = session['coach_id']

    session.clear()

    if coach_logged_in:
        session['coach_id'] = coach_id
        session["proteins"] = "0"
        session["carbs"] = "0"
        session["fats"] = "0"
        session["range"] = "0.2"
        session['mealtype'] = "Open"
        session['coach_views_user'] = False
        return redirect("/")

    return redirect("/login")


@app.route("/coach_logout")
def coach_logout():
    """
    Not a shown page, redirect here to logout as coach and clear whole session
    """

    session.clear()
    return redirect("/coach_login")


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


@app.route("/decline_request")
def decline_request():
    """
    Not a shown page, redirect here with paramter coach_id added to the url to decline the coaching request from
    this coach for the currently logged-in user
    """

    if 'user_id' not in session:
        return redirect("/coach_logout")

    try:
        coach_id = request.args["coach_id"]
    except BadRequestKeyError:
        return render_template("error.html", error_text="Coach-id needs to be specified in the url")

    remove_client_by_id(coach_id, session['user_id'], request=True)

    return redirect("/")


@app.route("/confirm_request")
def confirm_request():
    """
    Not a shown page, redirect here with paramter coach_id added to the url to confirm the coaching request from
    this coach for the currently logged-in user
    """

    if 'user_id' not in session:
        return redirect("/coach_logout")

    try:
        coach_id = request.args["coach_id"]
    except BadRequestKeyError:
        return render_template("error.html", error_text="Coach-id needs to be specified in the url")

    confirm_request_auth(coach_id, session['user_id'])

    return redirect("/")


@app.route("/create_user", methods=['POST', 'GET'])
def create_user():
    """
    Create the page for creating a new user account
    """

    if 'coach_id' in session:
        return redirect("/coach_logout")

    if 'user_id' in session:
        return redirect("/logout")

    if request.method == 'POST':
        password_one = request.form['set_new_pw_first']
        password_two = request.form['set_new_pw_second']
        if password_one == "":
            return render_template("error.html", error_text="Password can't be empty")
        if password_one != password_two:
            return render_template("error.html", error_text="Passwords don't match")
        session["new_user_id"] = write_new_user_to_file(password_one)
        return redirect("/success")

    return render_template("create_user.html")


@app.route("/create_coach", methods=['POST', 'GET'])
def create_coach():
    """
    Create the page for creating a new coach account
    """

    if 'coach_id' in session:
        return redirect("/coach_logout")

    if 'user_id' in session:
        return redirect("/logout")

    if request.method == 'POST':
        password_one = request.form['set_new_pw_first']
        password_two = request.form['set_new_pw_second']
        if password_one == "":
            return render_template("error.html", error_text="Password can't be empty")
        if password_one != password_two:
            return render_template("error.html", error_text="Passwords don't match")
        session["new_coach_id"] = write_new_coach_to_file(password_one)
        return redirect("/success")

    return render_template("create_coach.html")


@app.route("/success")
def success():
    """
    Create the page for showing that a new account has successfully been created
    """

    if 'coach_id' in session:
        return redirect("/coach_logout")

    if 'user_id' in session:
        return redirect("/logout")

    if "new_user_id" in session:
        return render_template("create_user_success.html", user_id=session["new_user_id"])

    if "new_coach_id" in session:
        return render_template("create_coach_success.html", coach_id=session["new_coach_id"])

    return redirect("/coach_logout")


@app.route("/remove_client", methods=['POST', 'GET'])
def remove_client():
    """
    Create the page for removing a client (coach-view)
    """

    if 'coach_id' not in session:
        return redirect("/coach_logout")

    if 'user_id' in session:
        return redirect("/logout")

    if request.method == 'POST':
        id_one = request.form['enter_id_one']
        id_two = request.form['enter_id_two']
        if not id_one.isdigit() or not id_two.isdigit():
            return render_template("error.html", error_text="That is not a valid id")
        if id_one == "":
            return render_template("error.html", error_text="Id can't be empty")
        if id_one != id_two:
            return render_template("error.html", error_text="Ids don't match")
        if int(id_one) not in get_users(session['coach_id']):
            return render_template("error.html", error_text="That is not one of your clients")

        remove_client_by_id(session['coach_id'], id_one)

        return redirect("/client_overview")

    return render_template("remove_client.html", coach_id=session['coach_id'])


@app.route("/add_client", methods=['POST', 'GET'])
def add_client():
    """
    Create the page for adding a client (coach-view)
    """

    if 'coach_id' not in session:
        return redirect("/coach_logout")

    if 'user_id' in session:
        return redirect("/logout")

    if request.method == 'POST':
        id_one = request.form['enter_id_one']
        id_two = request.form['enter_id_two']
        if not id_one.isdigit() or not id_two.isdigit():
            return render_template("error.html", error_text="That is not a valid id")
        if id_one == "":
            return render_template("error.html", error_text="Id can't be empty")
        if id_one != id_two:
            return render_template("error.html", error_text="Ids don't match")
        if int(id_one) in get_users(session['coach_id']):
            return render_template("error.html", error_text="That is already one of your clients")

        request_new_client(session['coach_id'], id_one)

        return redirect("client_overview")

    return render_template("add_client.html", coach_id=session['coach_id'])


@app.route("/", methods=['POST', 'GET'])
def home():
    """
    Create the home-page
    """

    try:
        session['user_id'] = request.args["user_id"]

        # Authenticate
        if 'coach_id' not in session:
            return redirect("coach_logout")
        else:
            coach_can_view_user = check_coach_can_view_user(session['coach_id'], session['user_id'])
            if not coach_can_view_user:
                return redirect("coach_logout")

        session['coach_views_user'] = True

    except BadRequestKeyError:

        # Logged in as coach, view coaches home page
        if 'coach_id' in session and not session['coach_views_user']:

            return render_template("home_coach.html", coach_id=session['coach_id'])

        # Logged in as user, view users home page
        if 'user_id' in session:

            # Logged in as user, a coach sent a request to this user
            coaching_requests = check_for_coaching_requests(session['user_id'])
            if coaching_requests:
                return render_template("home_with_requests.html", user_id=session['user_id'],
                                       coaching_requests=coaching_requests)

            return render_template("home.html", user_id=session['user_id'])

    # Logged in as coach, view user
    if 'coach_id' in session:

        return render_template("home.html", user_id=session['user_id'])

    return redirect("/coach_logout")


@app.route("/client_overview")
def client_overview():
    """
    Create the client overview page (coach-view)
    """

    if 'coach_id' not in session:
        return redirect("/coach_logout")

    users = get_users(session['coach_id'])

    return render_template("client_overview.html", users=users, coach_id=session['coach_id'])


@app.route("/recs_and_ratings")
def recs_and_ratings():
    """
    Create the recommendations & ratings page
    """

    if 'user_id' not in session:
        return redirect("/logout")

    if check_update_predicted_ratings():
        run_recommendation_algos(500)

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
        return redirect("/logout")

    if request.method == 'POST':
        session['rating'] = request.form['get_rating']
        write_rating_to_file(session['user_id'], session['recipe_id'], session['rating'])
        delete_double_ratings()
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
    Create the page to enter requirements (macros and meal-type)
    """

    if 'user_id' not in session:
        return redirect("/logout")

    if request.method == 'POST':
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
        return redirect("/logout")

    if check_update_predicted_ratings():
        run_recommendation_algos(300)

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
        return redirect("/logout")

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
        delete_double_ratings()

    return render_template('recipe.html', recipe=recipe_info, user_id=session['user_id'])


if __name__ == "__main__":
    app.run(port=8000, debug=True)
