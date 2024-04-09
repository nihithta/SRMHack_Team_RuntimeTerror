document.getElementById('toggle-mode').addEventListener('change', function() {
    
  console.log('Toggle button clicked')
  var bannerContainer = document.getElementById('banner');

  if (this.checked) {

    bannerContainer.classList.toggle("dark-mode");
  } else {      bannerContainer.classList.remove("dark-mode");
  }
});     

document.addEventListener("DOMContentLoaded", function() {
    var overlay = document.querySelector(".overlay");
    var indiaMap = document.getElementById("indiaMap");
  
    indiaMap.addEventListener("mousemove", function(event) {
      var x = event.offsetX;
      var y = event.offsetY;
      if (
        x >= 346 && x <= 453 &&
        y >= 574 && y <= 689
      ) {
        overlay.style.backgroundColor = "rgba(0, 0, 0, 0.5)";
      } else {
        overlay.style.backgroundColor = "rgba(0, 0, 0, 0)";
      }
    });
  });
  