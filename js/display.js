window.onload = function() {
  let thisUrl = window.location.href;
  let ind = thisUrl.indexOf('?location=');
  let parameter = thisUrl.slice(ind + 10);
  let locationName = parameter.split("+").join(" ");  
  document.getElementById("display-button").onclick = (() => {contributeClicked(locationName)});
  fillComments(locationName);
};

function fillComments(location) {
  firebase.database().ref(`/${location}/`).once('value')
  .then(function(snapshot) {
    // console.log(snapshot.val());
    let obj = snapshot.val();
    let digits = obj.lastId.length;
    let keys = Object.keys(obj);
    for (let i = 0; i < keys.length; i++) {
      if (keys[i] !== "lastId") {
        document.getElementById(`p${i}`).innerHTML = keys[i].slice(digits);
        document.getElementById(`t${i}`).innerHTML = obj[keys[i]];
        document.getElementById(`c${i}`).style.display = "flex";
      }
    }
  });
}

function contributeClicked(location) {
  let name = document.getElementById("name-field").value;
  let comment = document.getElementById("comment-field").value;
  let education = document.getElementById("education-field").value;
  let income = document.getElementById("income-field").value;
  firebase.database().ref(`/${location}/`).once('value')
  .then(function(snapshot) {
    let obj = snapshot.val();
    let lastId;
    if (obj) {
      lastId = parseInt(obj.lastId);
    }
    else {
      lastId = -1;
    }
    let newId = lastId+1;
    
    let updates = {};
    updates[`${location}/${newId}${name}`] = comment;
    updates[`${location}/lastId`] = `${newId}`;
    updates[`/education/${location}/${name}`] = education;
    updates[`/income/${location}/${name}`] = income;
    return firebase.database().ref().update(updates)
    .then(() => {
       window.location.reload(); 
    });
  });
}
