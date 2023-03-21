from flask import Flask, render_template, url_for
import pandas as pd
import os
import Run.output


app = Flask(__name__)


@app.route("/")
def home_page():
    """
    Create the home-page
    """

    return render_template("home.html")


@app.route("/get_rec")
def get_rec_page():
    """
    Create the get-recommendations-page
    """

    user_id = 6

    # Create data-structure for displaying given ratings
    given_ratings = Run.output.get_ratings_for_user(user_id)
    given_ratings_with_titles = {}
    for recipe_id, rating in given_ratings.items():
        given_ratings_with_titles[Run.output.get_recipe_title_by_id(recipe_id)] = rating

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

    return render_template("get_rec.html", user_id=user_id, given_ratings=given_ratings_with_titles,
                           recipes_and_ratings=recipes_and_ratings)


if __name__ == "__main__":
    app.run(debug=True)

