/* Toggle between adding and removing the "responsive" class to the navigation when the user clicks on the icon */
function extendNav() {
  var x = document.getElementById("myTopnav");
  if (x.className === "main-nav") {
    x.className += " responsive";
  } else {
    x.className = "main-nav";
  }
}