from flask import Flask, render_template
import pandas as pd
import os


app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)


"""
@app.route("/home")
def home():
    parent_dir = os.path.dirname(os.getcwd())
    recipe_database_path_and_filename = parent_dir + "/NutritionRecSys/Data/recipe_database.csv"
    recipe_info = pd.read_csv(recipe_database_path_and_filename, index_col=False)

    return str(recipe_info.head())
"""
