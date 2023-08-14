# Documentation / explanation video text

## Welcome & Introduction

Welcome to the Recipe Recommender. 
It's an online software tool that makes personalized recipe recommendations that match your taste.  
It does that by analyzing ratings you provide for recipes.  
You can furthermore specify meal types and macronutrients you are looking for, and you'll get recommendations suiting 
your requirements.  
Optionally, it allows working together with a nutrition coach.  
I developed this software in the scope of my Bachelor Thesis in order to find out which recommendation algorithm
performs best at matching your taste and recommend recipes that are to your liking.  
I hope you enjoy using the Recipe Recommender!

## Create account

To get started, please open any webbrowser and type in the URL _temporary-server.de_.  
You will see this login page, where you can log in as a coach or as a user.  

Let's create a new account, you can switch between coach and user account creation with this button, make sure you
are creating a user account.  
Enter your password, and optionally your name, and submit.  
On the next page, you'll see a short introduction text as well as your user-id, please note down this id, it's 
required for your login!  
Click "Login now", enter your id and password, submit, and then you are ready to go.  


## Get started

At the top, you see the navigation, your user-id and a logout-button.  
As the Recipe Recommender needs you to provide a few ratings to analyze your taste before being able to recommend
recipes for you, you need to rate 10 recipes before really getting started.  
That's why every button currently will redirect you to this page, showing you a random recipe.  
Click on the recipe title, which will open the recipe page in a new tab. You can now either really cook this recipe
if you want, or carefully look at the image, ingredients, preparation instructions and macronutrients.   
Then, please give a rating of 1-5 stars to this recipe, and submit.  
You can close the tab, reload this page, and you'll see a new recipe as well as the updated amount of recipes you 
still need to rate.  
Once you are done with rating 10 recipes, you are ready to get personalized recipe recommendations.  


## Explanation of the different pages
  
The first navigation button leads you to the home-page, that just includes some short information.  
If you work together with a coach, the coach can sent you a request for working with you.   
You will see that request here and can accept or decline it.   
If you accept, the coach can see your recommendations, enter required nutrients and can give ratings in your name.   

The second navigation button leads to the recommendations and ratings page.  
On this page, you see two things.  
At  the bottom, you see the recipes that you already rated, 
with the higher-rated recipes on top and the lower-rated recipes at the bottom.  
At the top of the page, you see your recommened recipes.  
Currently, recommendations are being calculated, so we wait a few seconds and then reload the page.  
We have 2 recommendation algorithms, and each of these algorithms presents you 3 recipes that should match your taste,
which you see here.  
You can click on each recipe to see more information and to give a rating after you have actually tried the recipe.  

The third navigation button leads you to the enter requirements page.  
Here, you can enter the macronutrients and meal-type that you want your recommended recipes to have.  
Here, you say what amount of kilocalories you want, here the grams of proteins, carbs and fats.  
In these fields, you can enter a value, but you can also leave it open.  
Allowed range means what percentage the macronutrients are allowed to differ from your entered value.  
Having a value in this field is obligatory, you can either leave the 0.2 that's in there by default, or replace it with
any other value, any value will work but only values between 0 and 1 really make sense. 
For example, if you enter 1000kcal and have an allowed range of 0.2, that means you will get recommendations that
have 1000 kilocalories plus/minus 20%, that means 800-1200 kilocalories, and similar with proteins, carbs and fats.  
0.2 is in most cases a good value for this, as it allows to get recommendations close to you required macronutrients,
while being flexible enough to actually find matching recipes.  
Once you have entered your requirements, click submit.  
If you want to reset your requirements, you can use the clear button.  

When you entered and submitted your requirements, click on the next navigation button,
which leads you to the matching recommendations page.  
On this page, you first of all see the requirements you just entered, and below that, the recommendations
matching these requirements. Again, each of the two algorithms presents you 3 matching recipes, which you can 
view in detail by clicking on the recipe title.  
It might happen that you enter too specific or strict requirements and no or not many matching recommendations 
can be found. In that case, you might want to be less strict with your requirements, to be able to get recommendations.  

The last navigation button just gives you a random recipe, you can reload the page to get a different one,
we've seen that page before when providing the 10 ratings neeeded for the software to get to know your taste.  

## Summary

To sum it up:  
On the home-page, you can accept or decline coaching requests.  
On the recommendations and ratings page, you see your personalized recipe recommendations, that 
just match your taste, not any nutrient requirements, as well as the recipes you have already rated.  
On the enter requirements page, you can enter nutrient and meal type requirements, and on the matching
recommendations page, you then find the recipe recommendations that match these requirements.  
So, recommendations that just match your taste, and recommendations that match both taste and your requirements.

That's it, feel free to contact me at this email adress if you have any questions!