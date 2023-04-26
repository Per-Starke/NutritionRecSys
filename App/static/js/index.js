/* Toggle between adding and removing the "responsive" class to the navigation when the user clicks on the icon */
function extendNav() {
    var x = document.getElementById("myTopnav");
        if (x.className === "nav main-nav") {
            x.className += " responsive";
        } else {
            x.className = "nav main-nav";
        }
    }