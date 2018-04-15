window.onload = function() {
  document.getElementById("el-button").onclick = (() => {submitClicked()});
};

function submitClicked() {
  let location = document.getElementById("location-field").value;
  location = location.split(" ").join("+");
  var queryString = "?location=" + location;
  window.location.href = "display.html" + queryString;
}