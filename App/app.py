from flask import Flask, render_template, url_for, request
import Run.output


app = Flask(__name__)


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

    user_id = 5

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


if __name__ == "__main__":
    app.run(port=8000, debug=True)

