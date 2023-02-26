# How the database was created

* run _create_final_recipe_database_ with mode 'w+' and default query 'random'
* run _create_final_recipe_database_ with mode default mode 'a+' and default query 'random'
  * Does not add new recipes, only duplicates, which are removed  -> we need to search with queries instead of random
* run _create_final_recipe_database_ with mode default mode 'a+' and query 1, high protein pasta
