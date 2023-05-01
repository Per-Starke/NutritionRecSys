/* Toggle between adding and removing the "responsive" class to the navigation when the user clicks on the icon */
function extendNav() {
    var x = document.getElementById("myTopnav");
        if (x.className === "nav main-nav") {
            x.className += " responsive";
        } else {
            x.className = "nav main-nav";
        }
    }

function extendNavCoach() {
    var x = document.getElementById("myTopnavCoach");
        if (x.className === "nav main-nav-coach") {
            x.className += " responsive";
        } else {
            x.className = "nav main-nav-coach";
        }
    }

function showMoreRecipes() {
    var button = document.getElementById("show-all-recipes");
    var recipes = document.getElementById("ratedRecipes").children;
    for(var i = 0; i < recipes.length; i++) {
        if (recipes[i].className === "body content more"){
            recipes[i].className = "body content more-shown";
            button.innerHTML = "show less";
        } else if (recipes[i].className === "body content more-shown"){
            recipes[i].className = "body content more";
            button.innerHTML = "show all";
        }
    }
}