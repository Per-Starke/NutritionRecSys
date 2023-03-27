from flask import Flask, render_template, url_for, request
import Run.output
import Run.recommend_for_user

app = Flask(__name__)

user_id = 0


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

    if request.method == 'POST':
        user_id = request.form['update_id']

    # Create data-structure for displaying given ratings
    given_ratings = Run.output.get_ratings_for_user(user_id)
    given_ratings_with_titles = {}
    for recipe_id, rating in given_ratings.items():
        given_ratings_with_titles[Run.output.get_recipe_title_by_id(recipe_id)] = rating
    sorted_given_ratings_with_titles = \
        {k: v for k, v in sorted(given_ratings_with_titles.items(), key=lambda item: item[1], reverse=True)}

    # Create data-structure for displaying predicted ratings
    recipes_and_ratings = Run.output.get_calculated_ratings_for_user(
        user_id, Run.output.write_recommendations(), ratings_to_get=3)

    content_based = recipes_and_ratings["content-based"]
    cb_with_titles = {}
    for recipe_id, rating in content_based.items():
        cb_with_titles[Run.output.get_recipe_title_by_id(recipe_id)] = rating

    itemknn = recipes_and_ratings["item-knn"]
    itemknn_with_titles = {}
    for recipe_id, rating in itemknn.items():
        itemknn_with_titles[Run.output.get_recipe_title_by_id(recipe_id)] = rating

    userknn = recipes_and_ratings["user-knn"]
    userknn_with_titles = {}
    for recipe_id, rating in userknn.items():
        userknn_with_titles[Run.output.get_recipe_title_by_id(recipe_id)] = rating

    recipes_and_ratings["content-based"] = cb_with_titles
    recipes_and_ratings["item-knn"] = itemknn_with_titles
    recipes_and_ratings["user-knn"] = userknn_with_titles

    return render_template("get_rec.html", user_id=user_id, given_ratings=sorted_given_ratings_with_titles,
                           recipes_and_ratings=recipes_and_ratings)


@app.route("/rate", methods=['POST', 'GET'])
def rate_page():
    """
    Create the get-recommendations-page
    """

    global user_id

    recipe_id = Run.recommend_for_user.get_recipe_to_rate(user_id)
    if recipe_id:
        recipe_title = Run.output.get_recipe_title_by_id(recipe_id)
    else:
        recipe_title = "No unrated recipe found!"

    if request.method == 'POST':
        try:
            user_id = request.form['update_id']
            recipe_id = Run.recommend_for_user.get_recipe_to_rate(user_id)
            if recipe_id:
                recipe_title = Run.output.get_recipe_title_by_id(recipe_id)
            else:
                recipe_title = "No unrated recipe found!"
        except KeyError:
            rating = request.form['get_rating']
            if Run.recommend_for_user.check_input(rating):
                Run.recommend_for_user.write_rating_to_file(user_id, recipe_id, rating)
            else:
                return "This is not a valid rating"

    return render_template("rate.html", user_id=user_id, recipe_title=recipe_title)


if __name__ == "__main__":
    app.run(port=8000, debug=True)
