// Credit: Mateusz Rybczonec

const FULL_DASH_ARRAY = 283;
const WARNING_THRESHOLD = 10;
const ALERT_THRESHOLD = 5;

const COLOR_CODES = {
  info: {
    color: "green"
  },
  warning: {
    color: "orange",
    threshold: WARNING_THRESHOLD
  },
  alert: {
    color: "red",
    threshold: ALERT_THRESHOLD
  }
};

let TIME_LIMIT = null;
let timePassed = 0;
let timeLeft = TIME_LIMIT;
let timerInterval = null;
let remainingPathColor = COLOR_CODES.info.color;

String.prototype.toProperCase = function () {
  return this.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
};

document.getElementById("timer").innerHTML = `
<div class="base-timer">
  <svg class="base-timer__svg" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
    <g class="base-timer__circle">
      <circle class="base-timer__path-elapsed" cx="50" cy="50" r="45"></circle>
      <path
        id="base-timer-path-remaining"
        stroke-dasharray="283"
        class="base-timer__path-remaining ${remainingPathColor}"
        d="
          M 50, 50
          m -45, 0
          a 45,45 0 1,0 90,0
          a 45,45 0 1,0 -90,0
        "
      ></path>
    </g>
  </svg>
  <span id="base-timer-label" class="base-timer__label">${"?"}
  </span>
  <p id="current_period">Second Period</p>
</div>
`;

fetch('http://192.168.1.212:8000/api')
  .then(response => response.json())
  .then(data => {
    document.getElementById("current_period").innerHTML = (
      data.current_period.replace("_", " ").replace("_", " ").replace("_", " ").toProperCase()
    );
    document.getElementById("current_day").innerHTML = (
      data.day_type.replace("_", " ").replace("_", " ").replace("_", " ").replace("_", " ").replace("_", " ").replace("_", " ").toProperCase()
    );
    document.getElementById("base-timer-label").innerHTML = formatTime(
      data.total_period_left_time_in_seconds
    );
    startTimer(data)
  });

function onTimesUp() {
  clearInterval(timerInterval);
  fetch('http://192.168.1.212:8000/api')
  .then(response => response.json())
  .then(data => {
    document.getElementById("current_period").innerHTML = (
      data.current_period.replace("_", " ").replace("_", " ").replace("_", " ").toProperCase()
    );
    document.getElementById("current_day").innerHTML = (
      data.day_type.replace("_", " ").replace("_", " ").replace("_", " ").replace("_", " ").replace("_", " ").replace("_", " ").toProperCase()
    );
    document.getElementById("base-timer-label").innerHTML = formatTime(
      data.total_period_time_in_seconds-data.total_period_time_in_seconds-data.total_period_left_time_in_seconds
    );
    startTimer(data)
  });
}

function startTimer(data) {
TIME_LIMIT  = data.total_period_time_in_seconds
timePassed = data.total_period_time_in_seconds-data.total_period_left_time_in_seconds
  timerInterval = setInterval(() => {
    timePassed = timePassed += 1;
    timeLeft = TIME_LIMIT - timePassed;
    if (timeLeft <= 0) {
      onTimesUp();
    }
    document.getElementById("base-timer-label").innerHTML = formatTime(
      timeLeft
    );
    setCircleDasharray();
    setRemainingPathColor(timeLeft);
  }, 1000);
}

function formatTime(time) {
  const minutes = Math.floor(time / 60);
  let seconds = time % 60;

  if (seconds < 10) {
    seconds = `0${seconds}`;
  }

  return `${minutes}:${seconds}`;
}

function setRemainingPathColor(timeLeft) {
  const { alert, warning, info } = COLOR_CODES;
  console.log("updating color!")
  if (timeLeft <= alert.threshold) {
    document
      .getElementById("base-timer-path-remaining")
      .classList.remove("green")
    document
      .getElementById("base-timer-path-remaining")
      .classList.remove("orange");
    document
      .getElementById("base-timer-path-remaining")
      .classList.add(alert.color);
      console.log("set to red")
  } else if (timeLeft <= warning.threshold) {
    document
      .getElementById("base-timer-path-remaining")
      .classList.remove("green")
    document
      .getElementById("base-timer-path-remaining")
      .classList.remove("red");
    document
      .getElementById("base-timer-path-remaining")
      .classList.add(warning.color);
      console.log("set to orange")
  } else {
    document
      .getElementById("base-timer-path-remaining")
      .classList.remove("red")
    document
      .getElementById("base-timer-path-remaining")
      .classList.remove("orange");
  document
    .getElementById("base-timer-path-remaining")
    .classList.add(info.color);
    console.log("set to green")
  }
}

function calculateTimeFraction() {
  const rawTimeFraction = timeLeft / TIME_LIMIT;
  return rawTimeFraction - (1 / TIME_LIMIT) * (1 - rawTimeFraction);
}

function setCircleDasharray() {
  const circleDasharray = `${(
    calculateTimeFraction() * FULL_DASH_ARRAY
  ).toFixed(0)} 283`;
  document
    .getElementById("base-timer-path-remaining")
    .setAttribute("stroke-dasharray", circleDasharray);
}
