// uncollapse navbar
function open_sidebar() {
  document.getElementById("navbar_button").className = "fas fa-chevron-circle-left";
  document.getElementById("sidebar").style.width = "250px";
  document.getElementById("main").style.marginLeft = "250px";
  document.getElementById("navbar_button").onclick = function(){ close_sidebar() };
}
// collapse navbar
function close_sidebar() {
  document.getElementById("navbar_button").className = "fas fa-chevron-circle-right";
  document.getElementById("sidebar").style.width = "0";
  document.getElementById("main").style.marginLeft= "0";
  document.getElementById("navbar_button").onclick = function(){ open_sidebar() };
}