# How the database was created

* run ```create_final_recipe_database``` with mode 'w+' and default query "random"
* run ```create_final_recipe_database``` with mode default mode 'a+' and default query "random"
  * Does not add new recipes, only duplicates, which are removed  -> we need to search with queries instead of random
* run ```create_final_recipe_database``` with default mode 'a+' and query 1, high(er) protein "pasta" recipes
* run ```create_final_recipe_database``` with default mode 'a+' and query 2, high(er) protein "rice" recipes
* run ```create_final_recipe_database``` with default mode 'a+' and query 3, high(er) protein "tofu" recipes
* run ```create_final_recipe_database``` with default mode 'a+' and query 4, very high protein "tofu" recipes
* run ```create_final_recipe_database``` with default mode 'a+' and query 5, high(er) protein "salad" recipes
* run ```create_final_recipe_database``` with default mode 'a+' and query 6, low fat & high(er) protein "salad" recipes
* run ```create_final_recipe_database``` with default mode 'a+' and query 7, "fruit" recipes
* run ```create_final_recipe_database``` with default mode 'a+' and query 8, low-carb "pasta" recipes
* run ```create_final_recipe_database``` with default mode 'a+' and query 9, high(er) protein "burger" recipes
* run ```create_final_recipe_database``` with default mode 'a+' and query 10, "burger" recipes
* run ```create_final_recipe_database``` with default mode 'a+' and query 11, "coffee" recipes
* run ```create_final_recipe_database``` with default mode 'a+' and query 12, "protein" recipes
* run ```create_final_recipe_database``` with default mode 'a+' and query 13, "healthy" recipes
* manually remove some none-vegan recipes, which are wrongly labelled vegan, namely the following ids:
  * 624873
  * 652750
  * 640634
  * 640238
  * 387781
  * 389758
  * 370623
  * 734758

## Result: 
***This leaves us with 1018 recipes in the final database***