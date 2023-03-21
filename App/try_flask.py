from flask import Flask, render_template, url_for
import pandas as pd
import os
import Run.output


app = Flask(__name__)


@app.route("/")
def home_page():

    return render_template("home.html")


@app.route("/get_rec")
def get_rec_page():

    user_id = 5
    recipes_and_ratings = Run.output.get_calculated_ratings_for_user(user_id, Run.output.write_recommendations())

    content_based = recipes_and_ratings["content-based"]
    cb_with_titles = {}

    for recipe_id, rating in content_based.items():
        cb_with_titles[Run.output.get_recipe_title_by_id(recipe_id)] = rating

    return render_template("get_rec.html", recipes_and_ratings=cb_with_titles)


if __name__ == "__main__":
    app.run(debug=True)

