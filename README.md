# NutritionRecSys
The repo for the software for my bachelor-thesis about a recommender system for use by nutrition coaches, recommending recipes with fitting macronutrients and suitable for the taste of the customer

## How to use:

### Get predicted ratings output:
To output given and predicted ratings, run [output.py](/Run/output.py).
In the if-statement at the end, set the ID of the user plus what recommendation algorithm's result you want to print.
Supported algorithms are:
- Collaborative filtering:
  - ItemKNN
  - UserKNN
- Content-based

Making use of [CaseRecommender](https://github.com/caserec/CaseRecommender) for that.

### Create new data (recipes, ratings, similarities):
To create new data, run [create_data.py](/Run/create_data.py).
In the if-statement at the end, you can choose if you want to create a new recipe database or not, if yes then also the amount of recipes it should include (currently only <= 100 allowed), and you can specify the amount of users you want to create (random) ratings for the recipes for. A similarity file for the recipes will also be created.

#### If you choose to create a new recipe database:
You need a [Spoonacular API](https://spoonacular.com/) Key for that. Get one at their website or at [Rapidapi](https://rapidapi.com/spoonacular/api/recipe-food-nutrition). Put the key in the [template.env](/Envs/template.env) file (rename if you want to), and depending on your development environment, specify which file to use as env file for the files [create_recipe_database.py](/Create_data/create_recipe_database.py) and [create_data.py](/Run/create_data.py). You might need a plugin for your development environment for that. 

## License
This work is licensed under the [Creative Commons Attribution 4.0 International Public License](/LICENSE)