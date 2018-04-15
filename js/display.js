window.onload = function() {
  let thisUrl = window.location.href;
  let ind = thisUrl.indexOf('?location=');
  let parameter = thisUrl.slice(ind + 10);
  let words = parameter.split("+").join(" ");
  console.log(parameter);
};
