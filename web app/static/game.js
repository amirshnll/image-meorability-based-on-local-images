var intervalTimer;
var locked;
var activeimage,
  appdata,
  lastimage,
  vigilanceerror,
  totalerror,
  irb,
  hitbtn,
  startbtn,
  count,
  vigilancecount,
  showtime,
  resttime;

function getflag() {
  "use strict";
  window.location.replace(
    "/getflag/" + document.getElementById("appdata").value
  );
}

function checkflag() {
  "use strict";
  vigilanceerror = document.getElementById("vigilanceerror");
  totalerror = document.getElementById("totalerror");
  lastimage = document.getElementById("lastimage");
  count = document.getElementById("count");
  vigilancecount = document.getElementById("vigilancecount");

  if (
    parseInt(lastimage.value) > 30 &&
    parseInt(totalerror.value) > Math.round((parseInt(lastimage.value) + 1) / 2)
  ) {
    getflag();
  } else if (parseInt(vigilanceerror.value) >= vigilancecount.value - 1) {
    getflag();
  }
}

function completeproccessing() {
  "use strict";
  window.location.replace(
    "/complete-form/" + document.getElementById("appdata").value
  );
}

function adddata(clicked) {
  "use strict";
  if (locked === 1) {
    return;
  }
  locked = 1;

  activeimage = document.getElementById("activeimage");
  appdata = document.getElementById("appdata");
  lastimage = document.getElementById("lastimage");
  if (parseInt(appdata.value) !== 0) {
    appdata.value = appdata.value + ",";
  } else {
    appdata.value = "";
  }
  if (clicked === 1) {
    if (document.getElementById(activeimage.value).classList.contains("hit")) {
      appdata.value = appdata.value + "1"; // hit
    } else {
      appdata.value = appdata.value + "2"; // false alarm
      if (
        document
          .getElementById(activeimage.value)
          .classList.contains("vigilance")
      ) {
        vigilanceerror = document.getElementById("vigilanceerror");
        vigilanceerror.value = (parseInt(vigilanceerror.value) + 1).toString();
      } else {
        totalerror = document.getElementById("totalerror");
        totalerror.value = (parseInt(totalerror.value) + 1).toString();
      }
      clicked = 1;
    }
    next();
  } else {
    if (
      document.getElementById("img" + lastimage.value).classList.contains("hit")
    ) {
      appdata.value = appdata.value + "3"; // miss
      if (
        document
          .getElementById("img" + lastimage.value)
          .classList.contains("vigilance")
      ) {
        vigilanceerror = document.getElementById("vigilanceerror");
        vigilanceerror.value = (parseInt(vigilanceerror.value) + 1).toString();
      } else {
        totalerror = document.getElementById("totalerror");
        totalerror.value = (parseInt(totalerror.value) + 1).toString();
      }
    } else {
      appdata.value = appdata.value + "4"; // correct rejection
    }
  }

  locked = 0;
}

function next() {
  "use strict";
  checkflag();
  count = parseInt(document.getElementById("count").value);
  if (lastimage.value > count) {
    clearInterval(intervalTimer);
    completeproccessing();
    return;
  }
  activeimage = document.getElementById("activeimage");
  document.getElementById(activeimage.value).classList.add("d-none");
  if (document.getElementById("activeimage").value == "fixation") {
    lastimage = document.getElementById("lastimage");
    lastimage.value = (parseInt(lastimage.value) + 1).toString();
    activeimage.value = "img" + lastimage.value;
    document.getElementById(activeimage.value).classList.remove("d-none");
    document.getElementById(activeimage.value).classList.add("d-block");
    clearInterval(intervalTimer);
    intervalTimer = setInterval(
      gameplay,
      parseInt(document.getElementById("showtime").value)
    );
  } else {
    lastimage = document.getElementById("lastimage");
    lastimage.classList.remove("d-block");
    lastimage.classList.add("d-none");
    activeimage.value = "fixation";
    document.getElementById(activeimage.value).classList.remove("d-none");
    document.getElementById(activeimage.value).classList.add("d-block");
    clearInterval(intervalTimer);
    intervalTimer = setInterval(
      gameplay,
      parseInt(document.getElementById("resttime").value)
    );

    adddata(0);
  }
}

function start() {
  "use strict";
  if (document.readyState !== "complete") {
    return 1;
  }
  irb = document.getElementById("irb");
  hitbtn = document.getElementById("hitbtn");
  startbtn = document.getElementById("startbtn");

  irb.innerHTML = "&nbsp;";
  startbtn.className += " d-none";
  hitbtn.className = "text-center d-block";

  activeimage = document.getElementById("activeimage");
  document.getElementById(activeimage.value).classList.add("d-none");
  lastimage = document.getElementById("lastimage");
  lastimage.value = (parseInt(lastimage.value) + 1).toString();
  activeimage.value = "img" + lastimage.value;
  document.getElementById(activeimage.value).classList.remove("d-none");
  document.getElementById(activeimage.value).classList.add("d-block");

  intervalTimer = setInterval(
    gameplay,
    parseInt(document.getElementById("showtime").value)
  );
}

function hit() {
  "use strict";
  if (document.readyState !== "complete") {
    return 1;
  }
  const startbtn = document.getElementById("startbtn");
  if (!startbtn.classList.contains("d-none")) {
    start();
  } else {
    if (document.getElementById("activeimage").value == "fixation") {
      return;
    }
    adddata(1);
  }
}

document.body.onkeyup = function (e) {
  if (e.key == " " || e.code == "Space" || e.keyCode == 32) {
    hit();
  }
};

document.addEventListener("contextmenu", (event) => event.preventDefault());

function gameplay() {
  "use strict";
  next();
  checkflag();
}

function hideimage() {
  "use strict";
  if (document.readyState !== "complete") {
    return 1;
  }
  count = parseInt(document.getElementById("count").value);
  showtime = parseInt(document.getElementById("showtime").value);
  resttime = parseInt(document.getElementById("resttime").value);

  for (let i = 1; i <= count; i++) {
    document.getElementById("img" + i.toString()).classList.add("d-none");
  }
}
