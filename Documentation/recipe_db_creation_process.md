# How the database was created

* run _create_final_recipe_database_ with mode 'w+' and default query 'random'
* run _create_final_recipe_database_ with mode default mode 'a+' and default query 'random'
  * Does not add new recipes, only duplicates, which are removed  -> we need to search with queries instead of random
* Manually remove one non-vegan recipe (Mussels and clams in white wine sauce, ID 652750)
* run _create_final_recipe_database_ with mode default mode 'a+' and query 1, high(er) protein pasta recipes
* run _create_final_recipe_database_ with mode default mode 'a+' and query 2, high(er) protein rice recipes
* run _create_final_recipe_database_ with mode default mode 'a+' and query 3, high(er) protein tofu recipes
* run _create_final_recipe_database_ with mode default mode 'a+' and query 4, very high protein tofu recipes
* run _create_final_recipe_database_ with mode default mode 'a+' and query 5, high(er) protein salad recipes
