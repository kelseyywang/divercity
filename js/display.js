var data = "Portland, OR+30.8+54148.0+58.1$Washington, DC+54.6+75628.0+51.9$Minneapolis, MN+33.7+63488.0+50.6$Seattle, WA+32.9+64129.0+50.0$Atlanta, GA+28.8+51244.0+46.2$Virginia Beach, VA+36.3+66262.0+46.2$Denver, CO+38.1+63909.0+42.1$Austin, TX+32.3+55653.0+39.7$Sacramento, CA+31.4+64500.0+30.0$New York, NY+34.2+60850.0+29.8$Oakland, CA+31.4+64500.0+29.3$Philadelphia, PA+28.6+55702.0+28.7$Albuquerque, NM+26.3+45382.0+28.1$San Diego, CA+31.4+64500.0+27.5$Baltimore, MD+37.9+75847.0+23.2$Long Beach, CA+31.4+64500.0+22.4$Fort Worth, TX+32.3+55653.0+21.5$Omaha, NE+29.3+54996.0+21.4$Nashville, TN+24.9+47275.0+21.1$Boston, MA+40.5+70628.0+21.1$San Francisco, CA+31.4+64500.0+18.8$Houston, TX+32.3+55653.0+18.4$Colorado Springs, CO+38.1+63909.0+17.6$Chicago, IL+27.6+59588.0+16.8$Jacksonville, FL+27.3+49426.0+16.2$Charlotte, NC+28.4+47830.0+15.8$Los Angeles, CA+31.4+64500.0+15.1$Phoenix, AZ+27.5+51492.0+14.2$Oklahoma City, OK+24.1+48568.0+13.2$Raleigh, NC+28.4+47830.0+13.0$Kansas City, MO+27.1+50238.0+12.8$Miami, FL+27.3+49426.0+12.8$Indianapolis, IN+24.1+50532.0+12.2$Columbus, OH+26.1+51075.0+12.2$Milwaukee, WI+27.8+55638.0+12.1$Mesa, AZ+27.5+51492.0+12.1$San Antonio, TX+32.3+55653.0+11.7$Fresno, CA+31.4+64500.0+11.4$Wichita, KS+31.0+53906.0+11.4$Louisville, KY+22.3+45215.0+10.6$Dallas, TX+32.3+55653.0+10.2$San Jose, CA+31.4+64500.0+10.0$Memphis, TN+24.9+47275.0+8.8$Tucson, AZ+27.5+51492.0+8.3$Tulsa, OK+24.1+48568.0+7.0$Cleveland, OH+26.1+51075.0+6.7$Detroit, MI+26.9+51084.0+2.8$Las Vegas, NV+23.0+52431.0+2.0$El Paso, TX+32.3+55653.0+0.0$Arlington, TX+32.3+55653.0+0.0$Palo Alto, CA+80+136519.0+71.2$East Palo Alto, CA+16.9+44006.0+20";
window.onload = function() {
  let thisUrl = window.location.href;
  let ind = thisUrl.indexOf('?location=');
  let parameter = thisUrl.slice(ind + 10);
  let locationName = parameter.split("+").join(" ");
  document.getElementById("display-button").onclick = (() => {contributeClicked(locationName)});
  fillComments(locationName);
  let cities = data.split("$");
  let found = false;
  for (let i = 0; i < cities.length; i++) {
    let city = cities[i];
    let newArr = city.split("+");
    if (newArr[0].toLowerCase().includes(locationName.toLowerCase())) {
      document.getElementById(`metric1`).innerHTML = `${newArr[3]}%`;
      document.getElementById(`metric2`).innerHTML = `${newArr[1]}%`;
      document.getElementById(`metric3`).innerHTML = `$${newArr[2]}0`;
      found = true;
      break;
    }
  }
  if (!found) {
    let randIncome = Math.floor(Math.random()*10000 + 50000);
    let randEducation = Math.floor(Math.random()*10 + 30);
    let randEducationDec = Math.floor(Math.random()*10);
    let randGentrification = Math.floor(Math.random()*20);
    let randGentrificationDec = Math.floor(Math.random()*10);
    document.getElementById(`metric1`).innerHTML = `${randGentrification}.${randGentrificationDec}%`;
    document.getElementById(`metric2`).innerHTML = `${randEducation}.${randEducationDec}%`;
    document.getElementById(`metric3`).innerHTML = `$${randIncome}.00`;
  }
};

function fillComments(location) {
  firebase.database().ref(`/${location}/`).once('value')
  .then(function(snapshot) {
    let obj = snapshot.val();
    if (obj) {
      let digits = obj.lastId.length;
      let keys = Object.keys(obj);
      for (let i = 0; i < keys.length; i++) {
        if (keys[i] !== "lastId") {
          document.getElementById(`p${i}`).innerHTML = keys[i].slice(digits);
          document.getElementById(`t${i}`).innerHTML = obj[keys[i]];
          document.getElementById(`c${i}`).style.display = "flex";
        }
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
