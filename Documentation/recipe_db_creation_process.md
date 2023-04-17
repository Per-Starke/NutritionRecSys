# How the database was created

* run ```create_final_recipe_database``` with mode 'w+' and default query 'random'
* run ```create_final_recipe_database``` with mode default mode 'a+' and default query 'random'
  * Does not add new recipes, only duplicates, which are removed  -> we need to search with queries instead of random
* Manually remove two non-vegan recipes 
  * *Mussels and clams in white wine sauce, ID 652750*
  * *Creamy Curry Chicken With Yellow Rice, ID 640634*
* run ```create_final_recipe_database``` with mode default mode 'a+' and query 1, high(er) protein pasta recipes
* run ```create_final_recipe_database``` with mode default mode 'a+' and query 2, high(er) protein rice recipes
* run ```create_final_recipe_database``` with mode default mode 'a+' and query 3, high(er) protein tofu recipes
* run ```create_final_recipe_database``` with mode default mode 'a+' and query 4, very high protein tofu recipes
* run ```create_final_recipe_database``` with mode default mode 'a+' and query 5, high(er) protein salad recipes
* run ```create_final_recipe_database``` with mode default mode 'a+' and query 6, low fat & high(er) protein salad recipes
* run ```create_final_recipe_database``` with mode default mode 'a+' and query 7, fruit recipes